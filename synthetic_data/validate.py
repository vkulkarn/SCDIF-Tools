#!/usr/bin/env python3
# SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
# SPDX-License-Identifier: MIT
# Licensed under the MIT License. See LICENSE.txt in the project root.
"""
SCDIF dataset validator.

Reads a folder of SCDIF .dat files, prints a summary + checks to the console, and
-- if it finds problems -- writes `validation_report.md` (next to the data folder)
describing each issue with its location, the rule it breaks, evidence, and a
suggested fix, so you can hand it to Claude and work through the fixes.

Usage:
    python3 validate.py [DATA_DIR]

DATA_DIR defaults to the `data/` folder beside this script. Point it at another
SCDIF export to validate that instead, e.g.:
    python3 synthetic_data/validate.py sample_scdif_data/data

Exit code is 1 if any ERROR-level issues are found, else 0.
"""
import os, re, sys, glob, difflib, datetime, collections

# ----------------------------------------------------------- documented format facts (Attachment J-10)
FIELDS = {
 '1A':16,'1B':22,'1C':4,'1D':7,'1E':6,'1F':8,'1G':24,'1H':4,
 '2A':20,'2B':5,'2C':8,'2D':8,'2E':5,
 '3A':11,'3B':4,'3D':8,'3E':5,'3F':9,'3G':5,'3L':6,
 '5A':4,'5B':4,'5C':8,'5D':7,
 '6A':17,'6B':4,'6C':4,'6D':8,'6E':7,'6F':3,
 '7A':27,'7B':3,'7C':4,'7D':8,'7E':7,'7F':3,'7H':6,'7I':27,'7J':3,'7K':4,'7L':8,'7M':7,'7N':3,
 '8A':6,
}
PARENT_KEY = {'1A':1,'2A':2,'3A':2,'5A':1,'6A':1,'7A':1,'7H':1}      # unique-key field index per root record
UNIQUE_IDS = [('1A',1,'Person ID'),('2A',2,'Communication ID'),('3A',2,'Workflow ID'),
              ('5A',1,'Household ID'),('6A',1,'Document ID'),('7A',1,'Event ID'),('7H',1,'Recurrence ID')]
# (child code, child field index, parent code, key name)  -- empty values are treated as NULL and skipped
FK_RULES = [
 ('1B',1,'1A','Person ID'),('1C',1,'1A','Person ID'),('1D',1,'1A','Person ID'),('1E',1,'1A','Person ID'),
 ('1F',1,'1A','Person ID'),('1G',1,'1A','Constituent ID'),('1H',1,'1A','Constituent ID'),('2A',1,'1A','Person ID'),
 ('2B',2,'2A','Communication ID'),('2C',2,'2A','Communication ID'),('2D',2,'2A','Communication ID'),('2E',2,'2A','Communication ID'),
 ('3A',1,'1A','Person ID'),('3B',2,'3A','Workflow ID'),('3D',2,'3A','Workflow ID'),('3E',2,'3A','Workflow ID'),
 ('3F',2,'3A','Workflow ID'),('3L',2,'3A','Workflow ID'),('3E',3,'1A','Party ID'),
 ('3G',1,'1A','Constituent ID'),('3G',2,'3A','Casework ID'),('3G',3,'3A','Parent Casework ID'),
 ('5B',1,'5A','Household ID'),('5C',1,'5A','Household ID'),('5D',1,'5A','Household ID'),('5B',2,'1A','Person ID'),
 ('2A',17,'5A','Household ID'),
 ('6B',1,'6A','Document ID'),('6C',1,'6A','Document ID'),('6D',1,'6A','Document ID'),('6E',1,'6A','Document ID'),('6F',1,'6A','Document ID'),
 ('2C',5,'6A','Document ID'),('1F',3,'6A','Document ID'),('3F',4,'6A','Document ID'),
 ('7B',1,'7A','Event ID'),('7C',1,'7A','Event ID'),('7D',1,'7A','Event ID'),('7E',1,'7A','Event ID'),('7F',1,'7A','Event ID'),
 ('7A',4,'1A','Contact (Person ID)'),('7A',2,'7H','Recurrence ID'),('7F',2,'3A','Workflow ID'),
 ('7I',1,'7H','Recurrence ID'),('7J',1,'7H','Recurrence ID'),('7K',1,'7H','Recurrence ID'),('7L',1,'7H','Recurrence ID'),
 ('7M',1,'7H','Recurrence ID'),('7N',1,'7H','Recurrence ID'),('7N',2,'3A','Workflow ID'),('7D',3,'6A','Document ID'),('7L',3,'6A','Document ID'),
]
STAFF_FIELDS = {'1D':[6],'1F':[4],'2A':[6,7],'2D':[7],'3A':[4],'3D':[7],'3F':[5],'5C':[4],'5D':[6],
 '6A':[8,9,10],'6D':[3],'6E':[6],'6F':[2],'7A':[16,18],'7D':[4],'7E':[6],'7I':[16,18],'7L':[4],'7M':[6]}
CODE_FIELDS = [('1C',3,None),('2B',3,'COM'),('3B',3,'WORK'),('7B',2,'EVENT'),('7J',2,'EVENT')]  # (code, code idx, expected type)
PATH_FIELDS = {'6A':[7],'2C':[4],'1F':[2],'3F':[3],'5C':[2],'6D':[2],'7D':[2],'7L':[2]}
DOC_CODE_TYPES = {'WORK','PERS','COM','EVENT','DOC','STAFF'}

# ----------------------------------------------------------- findings
class Finding:
    def __init__(s, sev, fid, title, detail, rule, examples, count, fix, ask):
        s.sev=sev; s.fid=fid; s.title=title; s.detail=detail; s.rule=rule
        s.examples=examples; s.count=count; s.fix=fix; s.ask=ask
findings=[]
def report(sev, fid, title, detail, rule, examples, count, fix, ask):
    findings.append(Finding(sev,fid,title,detail,rule,examples,count,fix,ask))

# ----------------------------------------------------------- load
def code_from_file(fn):
    m=re.match(r'out_(.+)\.dat$', os.path.basename(fn))
    if not m: return None
    raw=m.group(1)
    return raw.upper() if len(raw)==2 else raw.upper()

def load(data_dir):
    recs=collections.defaultdict(list)         # code -> list of (lineno, [fields])
    widths=collections.defaultdict(collections.Counter)
    strays=collections.defaultdict(list)       # code -> [(lineno, text)]
    crlf_issue=[]; oversize=[]; unknown=[]
    files=sorted(glob.glob(os.path.join(data_dir,'out_*.dat')))
    for fp in files:
        code=code_from_file(fp)
        data=open(fp,'rb').read()
        if re.search(rb'(?<!\r)\n', data):
            crlf_issue.append(os.path.basename(fp))
        if code not in FIELDS:
            unknown.append(os.path.basename(fp)); continue
        parts=data.split(b'\r\n')
        for i,seg in enumerate(parts):
            if seg==b'' :
                if i!=len(parts)-1: strays[code].append((i+1,'(blank line)'))
                continue
            if len(seg)>32768: oversize.append((os.path.basename(fp),i+1,len(seg)))
            try: text=seg.decode('ascii')
            except UnicodeDecodeError: text=seg.decode('latin-1')
            fields=text.split('\t')
            tok=fields[0]
            if tok!=code:
                strays[code].append((i+1, text[:80] if tok not in FIELDS else '[%s row inside %s file] %s'%(tok,code,text[:60])))
                continue
            recs[code].append((i+1,fields))
            widths[code][len(fields)]+=1
    return recs,widths,strays,crlf_issue,oversize,unknown,files

# ----------------------------------------------------------- helpers
def col(recs, code, idx):
    return {f[idx] for (_,f) in recs.get(code,[]) if len(f)>idx and f[idx]!=''}
def looks_path(v): return v.startswith('..') or '\\' in v or '/' in v
def resolve(data_dir, p):
    return os.path.normpath(os.path.join(data_dir, p.replace('\\','/')))

# ----------------------------------------------------------- main
def main():
    data_dir = sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')
    data_dir = os.path.abspath(data_dir)
    if not os.path.isdir(data_dir):
        sys.exit("Data folder not found: %s" % data_dir)
    root = os.path.dirname(data_dir)
    recs,widths,strays,crlf_issue,oversize,unknown,files = load(data_dir)
    total = sum(len(v) for v in recs.values())

    # ---- console: dataset summary ----
    print("="*64)
    print("SCDIF VALIDATION  ·  %s" % data_dir)
    print("="*64)
    print("files: %d   records: %d" % (len(files), total))
    print("\n %-4s %8s  %-9s %s" % ("type","count","fields","(documented)"))
    for code in sorted(recs):
        ws=widths[code]; lo,hi=min(ws),max(ws); rng="%d"%lo if lo==hi else "%d-%d"%(lo,hi)
        print(" %-4s %8d  %-9s %d" % (code, len(recs[code]), rng, FIELDS[code]))

    # ---- structural checks ----
    if unknown:
        report('WARNING','unknown-files','Unrecognized record-type files',
            'These files do not map to a documented SCDIF record type.', 'Record Type is a 2-byte code; file names are out_<code>.dat.',
            [(f,0,f) for f in unknown], len(unknown),
            'Confirm whether these are valid records the format doc is missing, or stray files.','Are these expected record types?')
    if crlf_issue:
        report('WARNING','crlf','Lines not terminated with CRLF',
            'One or more files contain LF line endings without a preceding CR.',
            'Each record must end with carriage-return line-feed (CRLF).',
            [(f,0,f) for f in crlf_issue], len(crlf_issue),
            'Normalize line endings to CRLF (\\r\\n).','Which files have wrong line endings and is it safe to normalize them?')
    if oversize:
        report('ERROR','oversize','Records exceed the 32K limit',
            'Records longer than 32768 bytes were found.', 'No record may be longer than 32K.',
            [(f,ln,'%d bytes'%b) for f,ln,b in oversize[:6]], len(oversize),
            'Investigate the oversized records; likely an unescaped delimiter merged rows.','Why are these records oversized?')
    stray_ex=[]; stray_n=0
    for code,lst in strays.items():
        stray_n+=len(lst)
        for ln,t in lst[:3]: stray_ex.append(("out_%s.dat"%(code if code=='8A' else code.lower()),ln,t))
    if stray_n:
        report('ERROR','stray-lines','Stray / non-record lines',
            'Lines that are blank or whose first field is not the file\'s record type. A reader expecting one record per line will misparse these.',
            'Every line is one record terminated by CRLF; the first field is the 2-byte Record Type.',
            stray_ex[:8], stray_n,
            'Remove blank/separator lines; investigate any rows of the wrong record type.','Which lines are stray and can they be removed?')

    # ---- field-count anomalies ----
    for code in sorted(recs):
        ws=widths[code]; lo,hi=min(ws),max(ws); doc=FIELDS[code]
        if hi>doc:
            ex=[("out_%s.dat"%(code if code=='8A' else code.lower()),ln,"%d fields (documented %d) | tail: %r"%(len(f),doc,f[doc:]))
                for ln,f in recs[code] if len(f)>doc][:5]
            report('WARNING','extra-fields-%s'%code,'%s has more fields than documented'%code,
                '%s records carry %d fields but the format documents %d. The extra trailing field(s) are undocumented.'%(code,hi,doc),
                'Each record type has a fixed documented field list.',
                ex, sum(1 for _,f in recs[code] if len(f)>doc),
                'Identify what the extra trailing field holds and document it (or drop it).',
                'What does the extra trailing field in %s contain?'%code)
        elif lo!=hi:
            report('WARNING','varwidth-%s'%code,'%s records vary in field count'%code,
                '%s records range from %d to %d fields (documented %d) — trailing empty fields appear to be trimmed rather than padded.'%(code,lo,hi,doc),
                'Records should be padded with trailing TABs to a uniform field count.',
                [("out_%s.dat"%(code if code=='8A' else code.lower()),ln,"%d fields"%len(f)) for ln,f in recs[code] if len(f)!=doc][:5],
                sum(1 for _,f in recs[code] if len(f)!=doc),
                'Read fields by position and treat missing trailing fields as NULL; pad if a uniform width is required.',
                'Is the trailing-field trimming in %s a problem for your importer?'%code)

    # ---- duplicate unique IDs ----
    for code,idx,name in UNIQUE_IDS:
        seen=collections.Counter(f[idx] for _,f in recs.get(code,[]) if len(f)>idx and f[idx]!='')
        dups={k:v for k,v in seen.items() if v>1}
        if dups:
            ex=[]
            for ln,f in recs[code]:
                if len(f)>idx and f[idx] in dups: ex.append(("out_%s.dat"%(code if code=='8A' else code.lower()),ln,"%s = %s"%(name,f[idx])))
            report('ERROR','dup-%s'%code,'Duplicate %s in %s'%(name,code),
                '%d %s value(s) appear on more than one %s record, but %s must be unique.'%(len(dups),name,code,name),
                '%s is a unique identifier.'%name,
                ex[:8], sum(dups.values()),
                'De-duplicate or re-key the affected records; check which row is authoritative.',
                'Which %s row is correct for the duplicated %s?'%(code,name))

    # ---- referential integrity ----
    parentset={p:col(recs,p,PARENT_KEY[p]) for p in PARENT_KEY}
    staffset=col(recs,'8A',2) if False else {f[2] for _,f in recs.get('8A',[]) if len(f)>2 and f[1]=='STAFF'}
    a8types=collections.defaultdict(set)
    for _,f in recs.get('8A',[]):
        if len(f)>2: a8types[f[1]].add(f[2])
    for child,cidx,parent,name in FK_RULES:
        if not recs.get(child): continue
        pset=parentset.get(parent,set())
        if not pset and not recs.get(parent):
            continue
        orphans=[(ln,f[cidx]) for ln,f in recs[child] if len(f)>cidx and f[cidx]!='' and f[cidx] not in pset]
        if orphans:
            ex=[("out_%s.dat"%(child if child=='8A' else child.lower()),ln,"%s = %s  (no %s record)"%(name,v,parent)) for ln,v in orphans[:6]]
            report('ERROR','fk-%s-%d-%s'%(child,cidx,parent),'%s.%s references a missing %s'%(child,name,parent),
                '%d %s record(s) reference a %s (%s) that does not exist in %s.'%(len(orphans),child,parent,name,parent),
                'A child record\'s %s must match an existing %s record.'%(name,parent),
                ex,len(orphans),
                'Either the referenced %s rows are missing from the export, or the IDs use a different key space than %s.'%(parent,parent),
                'Why do these %s references not resolve to a %s record?'%(name,parent))
    # staff user IDs
    staff_orphans=[]
    for code,idxs in STAFF_FIELDS.items():
        for ln,f in recs.get(code,[]):
            for i in idxs:
                if len(f)>i and f[i]!='' and f[i] not in staffset:
                    staff_orphans.append(("out_%s.dat"%(code if code=='8A' else code.lower()),ln,"%s field %d = %s"%(code,i+1,f[i])))
    if staff_orphans:
        report('ERROR','fk-staff','Staff User IDs missing from 8A',
            '%d User ID reference(s) have no matching 8A STAFF record.'%len(staff_orphans),
            'Every staff User ID must have an 8A record (Code Type = STAFF).',
            staff_orphans[:8], len(staff_orphans),
            'Add the missing 8A STAFF rows, or correct the User IDs.','Which staff are referenced but undefined in 8A?')
    # codes -> 8A
    code_orphans=[]
    for code,cidx,ctype in CODE_FIELDS:
        for ln,f in recs.get(code,[]):
            if len(f)<=cidx or f[cidx]=='': continue
            if code=='1C':
                t=f[2] if len(f)>2 else ''
                pool=a8types.get(t,set()) or (a8types.get('PERS',set())|a8types.get('WORK',set()))
            else:
                pool=a8types.get(ctype,set())
            if f[cidx] not in pool:
                code_orphans.append(("out_%s.dat"%code.lower(),ln,"%s code = %s"%(code,f[cidx])))
    if code_orphans:
        report('ERROR','fk-codes','Codes missing from 8A',
            '%d code reference(s) are not defined in the 8A code table.'%len(code_orphans),
            'Every code must have a matching 8A record of the appropriate Code Type.',
            code_orphans[:8], len(code_orphans),
            'Add the missing 8A code rows, or correct the codes.','Which codes are used but undefined in 8A?')

    # ---- 6C column order (Code Type vs Code) ----
    if recs.get('6C'):
        known=set(a8types.keys()) | DOC_CODE_TYPES
        swapped=[(ln,f) for ln,f in recs['6C'] if len(f)>3 and f[2] not in known and f[3] in known]
        if swapped:
            report('WARNING','6c-swap','6C Code Type and Code columns look swapped',
                '%d 6C record(s) have a value in field 3 that is not a Code Type, while field 4 *is* a known Code Type — the columns appear reversed vs the documented order (field 3 = Code Type, field 4 = Code).'%len(swapped),
                '6C documented order: field 3 = Code Type, field 4 = Code.',
                [("out_6c.dat",ln,"field3=%s  field4=%s"%(f[2],f[3])) for ln,f in swapped[:6]], len(swapped),
                'Read 6C by detecting which column holds a known Code Type, not by position; or swap the columns on import.',
                'Are 6C\'s Code Type / Code columns reversed, and should I swap them?')

    # ---- undocumented 8A code types ----
    undoc=sorted(set(a8types)-DOC_CODE_TYPES)
    if undoc:
        report('WARNING','code-types','Undocumented 8A code types',
            'The 8A code table uses code type(s) not in the documented set (WORK/PERS/COM/EVENT/DOC/STAFF): %s.'%', '.join(undoc),
            'Code Type values are a documented set; additions are not in the freely-extensible list.',
            [("out_8A.dat",ln,"Code Type = %s"%f[1]) for ln,f in recs['8A'] if len(f)>1 and f[1] in undoc][:6],
            sum(1 for _,f in recs['8A'] if len(f)>1 and f[1] in undoc),
            'Treat the export\'s 8A as authoritative for code types; document the extra type(s).',
            'What does the %s code type mean and how should I handle it?'%undoc[0])

    # ---- document path resolution + systematic patterns ----
    unresolved=[]; checked=0
    for code,idxs in PATH_FIELDS.items():
        for ln,f in recs.get(code,[]):
            for i in idxs:
                if len(f)>i and f[i]!='' and looks_path(f[i]):
                    checked+=1
                    if not os.path.exists(resolve(data_dir,f[i])):
                        unresolved.append(("out_%s.dat"%(code if code=='8A' else code.lower()),ln,f[i]))
    if unresolved:
        seg_fix=collections.Counter(); seg_example={}
        rename_sugg=collections.Counter()
        docs_dir=os.path.join(root,'documents')
        actual_subs=[d for d in os.listdir(docs_dir)] if os.path.isdir(docs_dir) else []
        for _,_,p in unresolved:
            segs=[s for s in p.replace('\\','/').split('/')]
            for j,s in enumerate(segs):
                if s in ('..','documents') or s=='' : continue
                cand='/'.join(segs[:j]+segs[j+1:])
                if os.path.exists(resolve(data_dir,cand)):
                    seg_fix[s]+=1; seg_example.setdefault(s,(p,cand))
            # folder typo near 'documents'
            if 'documents' in segs:
                k=segs.index('documents')
                if k+1<len(segs):
                    cm=difflib.get_close_matches(segs[k+1], actual_subs, n=1, cutoff=0.7)
                    if cm and cm[0]!=segs[k+1]: rename_sugg[(segs[k+1],cm[0])]+=1
        detail=('%d of %d document path reference(s) do not resolve to a file on disk.'%(len(unresolved),checked))
        fix_lines=[]
        for seg,cnt in seg_fix.most_common(3):
            ex=seg_example[seg]
            fix_lines.append('Removing the `%s` path segment resolves %d of them (e.g. `%s` → `%s`).'%(seg,cnt,ex[0],ex[1]))
        for (bad,good),cnt in rename_sugg.most_common(3):
            fix_lines.append('Folder name `%s` in paths likely should be `%s` (on-disk folder); affects %d.'%(bad,good,cnt))
        report('ERROR','paths','Document paths do not resolve',
            detail + ('  These look systematic (a repeated, fixable pattern):\n  - '+'\n  - '.join(fix_lines) if fix_lines else ''),
            'Document/attachment path fields must point to a file delivered alongside the data.',
            unresolved[:8], len(unresolved),
            (fix_lines[0] if fix_lines else 'Locate the files or correct the path roots.'),
            'These document paths are broken in a repeatable way — can you confirm the fix and apply it across all of them?')

    # ---- console: findings ----
    errs=[f for f in findings if f.sev=='ERROR']; warns=[f for f in findings if f.sev=='WARNING']
    print("\n"+"-"*64)
    if not findings:
        print("RESULT: clean — no issues found.")
        rp=os.path.join(root,'validation_report.md')
        if os.path.exists(rp): os.remove(rp)
        return 0
    print("RESULT: %d ERROR(s), %d WARNING(s)" % (len(errs),len(warns)))
    for f in findings:
        print("  [%-7s] %s  (x%d)" % (f.sev,f.title,f.count))
    md=write_md(root,data_dir,recs,total,findings)
    print("\nWrote report: %s" % md)
    print("Hand it to Claude:  'Read %s, then look at the data and help me fix these issues.'" % os.path.relpath(md))
    return 1 if errs else 0

def write_md(root, data_dir, recs, total, findings):
    path=os.path.join(root,'validation_report.md')
    errs=[f for f in findings if f.sev=='ERROR']; warns=[f for f in findings if f.sev=='WARNING']
    L=[]
    L.append("# SCDIF Data Validation Report\n")
    L.append("> Generated %s by `validate.py`. This report is written for an AI assistant "
             "(e.g. Claude) to read alongside the data so it can help diagnose and fix the issues below.\n"
             % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    L.append("**Dataset:** `%s`  \n**Records:** %d across %d record types  \n**Result:** %d error(s), %d warning(s)\n"
             % (data_dir, total, len(recs), len(errs), len(warns)))
    L.append("## How to use this report\n")
    L.append("Each finding lists **where** it occurs (file and line numbers), the **SCDIF rule** it relates to, "
             "**evidence** (sample offending rows), and a **suggested fix**. To work through them: open the cited "
             "`.dat` files at the given lines, confirm the issue, and apply the suggested correction — many are "
             "systematic and fixable in one pass. Field layouts are defined in the SCDIF skill "
             "(`scdif_documentation/scdif/reference/record-types.md`).\n")
    def esc(x): return str(x).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    L.append("## Findings summary\n")
    L.append("<table>")
    L.append("<thead><tr><th>#</th><th>Severity</th><th>Issue</th><th>Count</th></tr></thead>")
    L.append("<tbody>")
    for i,f in enumerate(findings,1):
        L.append("<tr><td>%d</td><td>%s</td><td>%s</td><td>%d</td></tr>" % (i,f.sev,esc(f.title),f.count))
    L.append("</tbody>")
    L.append("</table>\n")
    for i,f in enumerate(findings,1):
        L.append("## %d. [%s] %s\n" % (i,f.sev,f.title))
        L.append("**What:** %s\n" % f.detail)
        L.append("**Rule:** %s\n" % f.rule)
        L.append("**Occurrences:** %d\n" % f.count)
        if f.examples:
            L.append("**Evidence:**\n")
            L.append("```")
            for fn,ln,txt in f.examples:
                L.append(("%s:%d  %s" % (fn,ln,txt)) if ln else ("%s  %s" % (fn,txt)))
            L.append("```\n")
        L.append("**Suggested fix:** %s\n" % f.fix)
        L.append("**Ask Claude:** \"%s\"\n" % f.ask)
        L.append("---\n")
    open(path,'w',encoding='utf-8').write("\n".join(L))
    return path

if __name__=='__main__':
    sys.exit(main())
