#!/usr/bin/env python3
# SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
# SPDX-License-Identifier: MIT
# Licensed under the MIT License. See LICENSE.txt in the project root.
"""
SCDIF synthetic dataset generator (pure standard library).

Creates a clean, referentially-valid SCDIF dataset under this script's folder:
  synthetic_data/data/out_<code>.dat   (TAB-delimited, CRLF, padded to documented field count)
  synthetic_data/documents/<subfolder>/...  (real .docx/.pdf/.txt files)

Run:  python3 synthetic_data/generate.py
Deterministic (seeded). Re-running overwrites the previous output.
"""
import os, io, sys, shutil, random, zipfile, datetime

random.seed(20260619)
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
DOCS = os.path.join(BASE, "documents")

# ---------------------------------------------------------------- documented field counts
FIELDS = {
 '1A':16,'1B':22,'1C':4,'1D':7,'1E':6,'1F':8,'1G':24,'1H':4,
 '2A':20,'2B':5,'2C':8,'2D':8,'2E':5,
 '3A':11,'3B':4,'3D':8,'3E':5,'3F':9,'3G':5,'3L':6,
 '5A':4,'5B':4,'5C':8,'5D':7,
 '6A':17,'6B':4,'6C':4,'6D':8,'6E':7,'6F':3,
 '7A':27,'7B':3,'7C':4,'7D':8,'7E':7,'7F':3,'7H':6,'7I':27,'7J':3,'7K':4,'7L':8,'7M':7,'7N':3,
 '8A':6,
}
rows = {code: [] for code in FIELDS}

def add(code, *vals):
    n = FIELDS[code]
    out = []
    for v in vals:
        s = '' if v is None else str(v)
        s = s.replace('\t', ' ').replace('\r', '|').replace('\n', '|')
        out.append(s)
    if len(out) > n:
        raise ValueError("%s: %d fields > documented %d" % (code, len(out), n))
    out += [''] * (n - len(out))      # pad trailing fields per spec
    rows[code].append(out)

# ---------------------------------------------------------------- scale (interactive)
MIN_PEOPLE = 100
def ask_people():
    """Number of 1A (person) records to generate. Optional CLI arg; otherwise prompt. Minimum 100."""
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            sys.exit("Invalid people count: %r (must be a whole number >= %d)" % (sys.argv[1], MIN_PEOPLE))
        if n < MIN_PEOPLE:
            sys.exit("People count must be at least %d (got %d)." % (MIN_PEOPLE, n))
        return n
    while True:
        try:
            raw = input("How many people (1A) records should I create? (minimum %d): " % MIN_PEOPLE).strip()
        except EOFError:
            sys.exit("\nNo input provided. Re-run and enter a number, or pass it as an argument: "
                     "python3 generate.py 500")
        if not raw.lstrip('+').isdigit():
            print("  Please enter a whole number."); continue
        n = int(raw)
        if n < MIN_PEOPLE:
            print("  Minimum is %d. Please enter %d or more." % (MIN_PEOPLE, MIN_PEOPLE)); continue
        return n

PEOPLE     = ask_people()
# everything else scales in the same proportion as the original 500-person spec
HOUSEHOLDS = max(1, round(PEOPLE / 10))   # 50 households per 500 people
LIBRARY    = max(1, round(PEOPLE / 10))   # 50 doc-library items per 500
EVENTS     = max(1, round(PEOPLE / 10))   # 50 events per 500
SERIES     = max(1, round(PEOPLE / 50))   # 10 recurring series per 500
print("Generating SCDIF dataset for %d people  (households=%d, library=%d, events=%d, series=%d)..."
      % (PEOPLE, HOUSEHOLDS, LIBRARY, EVENTS, SERIES))
# start from a clean output tree so changing scale never leaves stale files
for d in (DATA, DOCS):
    if os.path.isdir(d):
        shutil.rmtree(d)

# ---------------------------------------------------------------- name & value pools
FIRST = """James Mary Robert Patricia John Jennifer Michael Linda David Elizabeth William Barbara
Richard Susan Joseph Jessica Thomas Sarah Charles Karen Christopher Nancy Daniel Lisa Matthew Betty
Anthony Margaret Mark Sandra Donald Ashley Steven Kimberly Paul Emily Andrew Donna Joshua Michelle
Kenneth Carol Kevin Amanda Brian Dorothy George Melissa Timothy Deborah Ronald Stephanie Jason Rebecca
Edward Sharon Jeffrey Laura Ryan Cynthia Jacob Kathleen Gary Amy Nicholas Angela Eric Shirley
Jonathan Anna Stephen Brenda Larry Pamela Justin Emma Scott Nicole Brandon Helen Benjamin Samantha
Samuel Katherine Gregory Christine Frank Debra Raymond Rachel Alexander Carolyn Patrick Janet Jack Maria""".split()
LAST = """Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez Martinez Hernandez Lopez
Gonzalez Wilson Anderson Thomas Taylor Moore Jackson Martin Lee Perez Thompson White Harris Sanchez
Clark Ramirez Lewis Robinson Walker Young Allen King Wright Scott Torres Nguyen Hill Flores Green
Adams Nelson Baker Hall Rivera Campbell Mitchell Carter Roberts Gomez Phillips Evans Turner Diaz
Parker Cruz Edwards Collins Reyes Stewart Morris Morales Murphy Cook Rogers Gutierrez Ortiz Morgan
Cooper Peterson Bailey Reed Kelly Howard Ramos Kim Cox Ward Richardson Watson Brooks Chavez Wood""".split()
ORGS = ["American Medical Assn", "State Farm Bureau", "Veterans United", "Riverside Foundation",
        "Metro Chamber of Commerce", "Hartwell Industries", "Cumberland Energy Co", "Oak Ridge Labs",
        "Tennessee Hospital Assn", "Pioneer Manufacturing", "Greenfield Partners", "Summit Holdings"]
AGENCIES = ["Social Security Admin", "Dept of Veterans Affairs", "IRS", "USCIS",
            "Dept of Housing", "Medicare Services", "Passport Agency", "FEMA", "Small Business Admin"]
CITIES = [("Memphis","TN","38103","Shelby","TN09"),("Nashville","TN","37203","Davidson","TN05"),
          ("Knoxville","TN","37902","Knox","TN02"),("Chattanooga","TN","37402","Hamilton","TN03"),
          ("Jackson","TN","38301","Madison","TN08"),("Franklin","TN","37064","Williamson","TN07"),
          ("Clarksville","TN","37040","Montgomery","TN07"),("Johnson City","TN","37601","Washington","TN01")]
STREETS = ["Sample St","Test Dr","Maple Ave","Oak Blvd","Cedar Ln","Main St","Elm Way","Park Pl","River Rd","Hill Ct"]
REGIONS = ["DC","Memphis","Jackson","Nashville","Chattanooga","Knoxville","Tri-Cities"]
INTERESTS = ["Agriculture","Business - Small Business","Education - All","Energy - Alternative Energy",
             "Health - Hospitals","Immigration","Military - Veterans","Transportation - Safety","Seniors","Environment - Conservation"]

PERS_CODES = ["VIP","DOCTOR","MAYOR","POI","DONOR","VETERAN","OUTREACH DATABASE","NEWSLETTER"]
WORK_CODES = ["VET","SOCSEC","IMMIGRATION","MEDICARE","IRS","PASSPORT","MILITARY","HOUSING","EDUCATION"]
COM_CODES  = ["TAXES","GUNCTRL","HEALTHCARE","IMMIGRATION","BUDGET","VETERANS","ENVIRONMENT","EDUCATION","FOREIGN"]
EVENT_CODES= ["TOWNHALL","FUNDRAISER","RIBBON","MEETING","TOUR","AWARD"]
DOC_CODES  = ["FORMLTR","NEWSLTR","TEMPLATE","BROCHURE"]
WF_TYPES   = ["CASE","Outreach","Boy Scout","Flag Request","Tour Request","Academy Nomination","Grant Request"]
WF_STATUS  = ["OPEN","CLOSED","CL.FAV","CL.UNFAV","PG.OP","PG.CL","INCOMPLETE"]
COMM_TYPES = ["LETTER","EMAIL","PHONE","NEWSLETTER","VISIT","POST CARD","DMAIL"]
COMM_STAT  = ["P","RA","C","H"]

# ---------------------------------------------------------------- date helpers
def rdate(y0=2015, y1=2024):
    d = datetime.date(y0,1,1) + datetime.timedelta(days=random.randint(0,(datetime.date(y1,12,31)-datetime.date(y0,1,1)).days))
    return d.strftime("%Y%m%d")
def rtime():
    return "%02d:%02d:%02d" % (random.randint(7,19), random.randint(0,59), random.randint(0,59))

# ---------------------------------------------------------------- document templates
DOCX_CT = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
DOCX_RELS = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
def make_docx(text):
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('[Content_Types].xml', DOCX_CT)
    z.writestr('_rels/.rels', DOCX_RELS)
    z.writestr('word/document.xml',
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p><w:r><w:t>%s</w:t></w:r></w:p></w:body></w:document>' % text)
    z.close()
    return buf.getvalue()
def make_pdf(text):
    objs = ["<</Type/Catalog/Pages 2 0 R>>",
            "<</Type/Pages/Kids[3 0 R]/Count 1>>",
            "<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<</Font<</F1 5 0 R>>>>/Contents 4 0 R>>",
            None,
            "<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
    stream = "BT /F1 24 Tf 72 700 Td (%s) Tj ET" % text
    objs[3] = "<</Length %d>>\nstream\n%s\nendstream" % (len(stream), stream)
    out = "%PDF-1.4\n"; offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out.encode('latin-1')))
        out += "%d 0 obj\n%s\nendobj\n" % (i, o)
    xref = len(out.encode('latin-1'))
    out += "xref\n0 %d\n0000000000 65535 f \n" % (len(objs)+1)
    for off in offs: out += "%010d 00000 n \n" % off
    out += "trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF" % (len(objs)+1, xref)
    return out.encode('latin-1')

DOC_BYTES = {'txt': b"Test document txt", 'docx': make_docx("Test document docx"), 'pdf': make_pdf("Test document pdf")}
_doc_count = [0]
def write_doc(sub, name, ext):
    """Write a copy of the <ext> template at documents/<sub>/<name>.<ext>; return its relative path."""
    folder = os.path.join(DOCS, sub); os.makedirs(folder, exist_ok=True)
    fn = "%s.%s" % (name, ext)
    with open(os.path.join(folder, fn), 'wb') as f:
        f.write(DOC_BYTES[ext])
    _doc_count[0] += 1
    return "..\\documents\\%s\\%s" % (sub, fn)

# ---------------------------------------------------------------- ID allocators
class Seq:
    def __init__(s, start): s.n = start
    def __call__(s): s.n += 1; return s.n
pid_seq   = Seq(100000)
comm_seq  = Seq(5000000)
wf_seq    = Seq(10000)
hh_seq    = Seq(200000)
doc_seq   = Seq(300000)
event_seq = Seq(400000)
rec_seq   = Seq(500000)

# ---------------------------------------------------------------- 8A code table (staff + code pools)
STAFF = []
for i in range(25):
    uid = 101 + i
    nm = "%s %s" % (random.choice(FIRST), random.choice(LAST))
    STAFF.append(str(uid))
    add('8A', '8A', 'STAFF', uid, nm, '', '')
def emit_codes(ctype, codes):
    for c in codes:
        add('8A', '8A', ctype, c, c.title(), '', '')
emit_codes('PERS', PERS_CODES)
emit_codes('WORK', WORK_CODES)
emit_codes('COM',  COM_CODES)
emit_codes('EVENT',EVENT_CODES)
emit_codes('DOC',  DOC_CODES)
staff = lambda: random.choice(STAFF)

# ---------------------------------------------------------------- 6A document library (build first; comms reference it)
library = []   # list of doc IDs
for i in range(LIBRARY):
    did = doc_seq()
    path = write_doc("formletters", str(did), "docx")
    disp = random.choice(["Veterans Benefits Reply","Tax Inquiry Response","Immigration Status Letter",
        "Thank You - Constituent","Newsletter - Monthly","Appropriations Request","Casework Follow-up",
        "Tour Confirmation","Flag Request Acknowledgment","Healthcare Policy Letter"]) + " v%d" % random.randint(1,3)
    add('6A','6A',did,1,did,'Form',disp,'Standard office form letter.',path,
        staff(), staff(), random.choice(['', staff()]), rdate(2014,2020), rdate(2020,2024), rdate(2022,2024),
        random.choice(['Approved','Approved','Draft']), random.choice(['','','Y']), "\\Form Letters\\"+random.choice(["Casework","Outreach","Appropriations"]))
    library.append(did)
    # 6B fill-ins
    for fn_ in random.sample(["Greeting","ConstituentName","Subject","ClosingDate"], random.randint(0,3)):
        add('6B','6B',did,fn_, fn_)
    # 6C codes (documented order: CodeType, then Code)
    for _ in range(random.randint(0,2)):
        ct = random.choice(['WORK','COM','DOC'])
        code = random.choice({'WORK':WORK_CODES,'COM':COM_CODES,'DOC':DOC_CODES}[ct])
        add('6C','6C',did,ct,code)
    # 6D attachment (real file)
    if random.random() < 0.3:
        ap = write_doc("fomletter_ima", "%d_a" % did, random.choice(['pdf','docx']))
        add('6D','6D',did,ap,staff(),rdate(),random.choice(['','Y']),os.path.basename(ap))
    # 6E note
    if random.random() < 0.3:
        add('6E','6E',did,'',('Reviewed and approved for current cycle.'),rdate(),rtime(),staff())
    # 6F owner
    add('6F','6F',did,staff())

# ---------------------------------------------------------------- people (1A + satellites)
people = []        # list of dicts {id,type,addr_ids,workflows:[],is_constituent}
agency_people = [] # person ids usable as 3E parties
for i in range(PEOPLE):
    pid = pid_seq()
    r = random.random()
    if   r < 0.86: ptype = 'CS'
    elif r < 0.92: ptype = 'OR'
    elif r < 0.96: ptype = 'AG'
    elif r < 0.98: ptype = 'PRESS'
    else:          ptype = 'USER'
    first = random.choice(FIRST); last = random.choice(LAST)
    org = ''
    if ptype in ('OR','AG'):
        org = random.choice(AGENCIES if ptype=='AG' else ORGS)
        agency_people.append(pid)
    prefix = random.choice(['Mr.','Ms.','Mrs.','Dr.','The Honorable',''])
    sal = ("%s %s" % (prefix, last)).strip() if prefix else first
    dob = rdate(1945,2000) if (ptype=='CS' and random.random()<0.5) else ''
    add('1A','1A',pid,ptype,prefix,first,
        random.choice(['', random.choice(FIRST)[0]+'.']), last,
        random.choice(['','','Jr.','Sr.','III']), random.choice(['','','MD','PhD']),
        org, sal, dob, random.choice(['','','','Y']), random.choice(['','','','','Y']),
        random.choice(['', "%s %s" % (random.choice(FIRST), last)]) if ptype=='CS' else '',
        random.choice(['','','Y']))
    # 1B addresses
    addr_ids = []
    for a in range(random.randint(1,2)):
        aid = pid * 10 + a
        addr_ids.append(aid)
        city,state,zipc,county,dist = random.choice(CITIES)
        atype = 'BU' if (ptype in ('OR','AG') and a==0) else random.choice(['HO','HO','BU'])
        add('1B','1B',pid,aid,atype,'Y' if a==0 else '','Y' if a==0 else '',
            'CEO' if atype=='BU' and random.random()<0.3 else '', org if atype=='BU' else '',
            "%d %s" % (random.randint(100,9999), random.choice(STREETS)),
            random.choice(['','Apt %d'%random.randint(1,400),'Suite %d'%random.randint(1,50)]),'','',
            city,state, zipc+('-%04d'%random.randint(0,9999) if random.random()<0.5 else ''),
            'R%03d'%random.randint(1,40), county, 'USA', dist, '', random.choice(['','Y']) if random.random()<0.05 else '',
            random.choice(['D','D','D','P','U','']))
    # 1C person codes
    for c in random.sample(PERS_CODES, random.randint(0,3)):
        add('1C','1C',pid,'PERS',c)
    # 1E phones/emails
    add('1E','1E',pid,'EMAIL', "%s.%s@testemail.com" % (first.lower(), last.lower()),'Y','')
    for t in random.sample(['HOME','CELL','WORK','FAX'], random.randint(1,3)):
        add('1E','1E',pid,t, "(%03d) %03d-%04d" % (random.randint(200,989),random.randint(200,999),random.randint(0,9999)),
            random.choice(['Y','']),'')
    # 1D notes
    for _ in range(random.randint(0,2)):
        add('1D','1D',pid,'', random.choice(["Confirmed contact info.","Prefers email.","Repeat constituent.","Updated address."]),
            rdate(), rtime(), staff())
    # 1F attachment (real file)
    if random.random() < 0.25:
        ap = write_doc("objects", "p%d_att" % pid, random.choice(['pdf','txt','docx']))
        add('1F','1F',pid,ap,'',staff(),rdate(),'Scanned correspondence',os.path.basename(ap))
    # 1G demographics + 1H vote history (constituents only)
    if ptype == 'CS' and random.random() < 0.6:
        add('1G','1G',pid,'VoterFile', "VF%07d"%random.randint(0,9999999), "%09d"%random.randint(0,10**9),
            rdate(2022,2024), rdate(2000,2018), random.choice(['','Y']),
            random.choice(['Single','Married','Non-Tradit']), random.choice(['Y','N']), random.choice(['Y','N']),
            random.choice(['Y','N']), random.choice(['White','Black','Asian','Hispanic','Other']),
            random.choice(['','Hispanic','Non-Hispanic']), 'English', str(random.randint(8,20)),
            'SD%02d'%random.randint(1,40), 'HD%02d'%random.randint(1,99), 'SS%02d'%random.randint(1,33),
            str(random.randint(1,12)), '', '', 'P%03d'%random.randint(1,200), str(random.randint(1945,2000)))
        for _ in range(random.randint(0,3)):
            add('1H','1H',pid,str(random.choice([2016,2018,2020,2022,2024])), random.choice(['P','G','PP']))
    people.append({'id':pid,'type':ptype,'addr':addr_ids,'wf':[],'cs':ptype=='CS'})

# ---------------------------------------------------------------- workflows (3A + satellites)
for p in people:
    nwf = random.randint(2,5)
    case_wfs = []
    for _ in range(nwf):
        wid = wf_seq(); wtype = random.choice(WF_TYPES)
        sd = rdate(); ed = '' if random.random()<0.4 else rdate()
        status = random.choice(WF_STATUS)
        add('3A','3A',p['id'],wid,wtype,staff(),sd,ed,'' if random.random()<0.7 else rdate(),
            rdate(), random.choice(["Veteran benefits inquiry","Immigration problem","Tax assistance",
            "Tour request for DC","Academy nomination","Grant application support","Flag request"]), status)
        p['wf'].append(wid)
        if wtype == 'CASE': case_wfs.append(wid)
        # 3B codes
        for c in random.sample(WORK_CODES, random.randint(0,2)):
            add('3B','3B',p['id'],wid,c)
        # 3D action history
        for _ in range(random.randint(1,3)):
            add('3D','3D',p['id'],wid,'', random.choice(["Opened workflow.","Contacted agency.",
                "Awaiting response.","Closed with resolution.","Constituent updated."]), rdate(), rtime(), staff())
        # 3E parties (agencies)
        if agency_people and random.random() < 0.5:
            add('3E','3E',p['id'],wid,random.choice(agency_people), random.choice(['Agency','Co-signer','Referral','Advocate']))
        # 3F attachment
        if random.random() < 0.3:
            if random.random() < 0.5 and library:
                add('3F','3F',p['id'],wid,'',random.choice(library),staff(),rdate(),'Form letter attached','')
            else:
                ap = write_doc("objects","wf%d"%wid, random.choice(['pdf','txt']))
                add('3F','3F',p['id'],wid,ap,'',staff(),rdate(),'Supporting document',os.path.basename(ap))
        # 3L type-specific fields
        if wtype == 'CASE':
            for fn_, val in [('govern',random.choice(['Yes','No'])),('OpenStatus',random.choice(['Active','Pending'])),
                             ('Region',random.choice(REGIONS)),('SS #',''),('ID #',str(random.randint(10000,99999)))]:
                add('3L','3L',p['id'],wid,wtype,fn_,val)
        elif wtype == 'Outreach':
            for fn_, val in [('interest1',random.choice(INTERESTS)),('interest2',random.choice(INTERESTS)),
                             ('Region',random.choice(REGIONS)),('offcont',staff())]:
                add('3L','3L',p['id'],wid,wtype,fn_,val)
        elif wtype == 'Boy Scout':
            for fn_, val in [('OpenStatus',random.choice(['Active','Pending'])),('Region',random.choice(REGIONS)),
                             ('trplead',"%s %s"%(random.choice(FIRST),random.choice(LAST))),('trpnum',str(random.randint(1,500)))]:
                add('3L','3L',p['id'],wid,wtype,fn_,val)
    # 3G casework relationships (parent/child among this person's CASE workflows)
    if len(case_wfs) >= 2:
        parent = case_wfs[0]
        for child in case_wfs[1:]:
            if random.random() < 0.6:
                add('3G','3G',p['id'],child,parent,rdate())

# ---------------------------------------------------------------- communications (2A + satellites)
for p in people:
    for _ in range(random.randint(12,18)):
        cid = comm_seq()
        linked = p['wf'] and random.random() < 0.3
        wid = random.choice(p['wf']) if linked else ''
        ctype = random.choice(COMM_TYPES)
        status = random.choice(COMM_STAT)
        din = rdate(); dout = din if status=='C' else ('' if random.random()<0.4 else rdate())
        aid = random.choice(p['addr']) if p['addr'] else ''
        add('2A','2A',p['id'],cid,wid, p['id'] if linked else '', ctype, staff(),
            random.choice(['', staff()]), status, din, dout, '' if random.random()<0.7 else rdate(), rdate(),
            random.choice(['imail','usmail','email','letter']), aid,
            "%d@testemail.com"%p['id'] if ctype=='EMAIL' else '', '', '', random.choice(['','Batch-A','Newsletter-Q1']),
            'Constituent')
        # 2B codes
        for c in random.sample(COM_CODES, random.randint(1,2)):
            add('2B','2B',p['id'],cid,c, random.choice(['PRO','CON','NEUTRAL','NONE']))
        # 2C documents: outgoing -> library by Document ID; incoming -> real file
        if random.random() < 0.5 and library:
            add('2C','2C',p['id'],cid,'OUTGOING','',random.choice(library),'','')
        else:
            sub = random.choice(['objects','imail','indivletters'])
            ext = {'objects':'pdf','imail':'txt','indivletters':'docx'}[sub]
            dp = write_doc(sub, "%d_in"%cid, ext)
            add('2C','2C',p['id'],cid,'INCOMING',dp,'','',os.path.basename(dp))
        # 2D note
        if random.random() < 0.3:
            add('2D','2D',p['id'],cid,'', random.choice(["Logged incoming.","Drafted response.","Sent reply."]), rdate(), rtime(), staff())
        # 2E fill-ins (for outgoing form letters)
        if random.random() < 0.2:
            for fn_ in random.sample(["ConstituentName","Subject","ClosingDate"], random.randint(1,2)):
                add('2E','2E',p['id'],cid,fn_, random.choice(["Dear Constituent","Your inquiry","October 2024"]))

# ---------------------------------------------------------------- households (5A + satellites)
cs_people = [p['id'] for p in people if p['cs']]
random.shuffle(cs_people)
assigned = set()
idx = 0
for _ in range(HOUSEHOLDS):
    hid = hh_seq()
    fam = random.choice(LAST)
    add('5A','5A',hid,"The %s Family"%fam, "%s Family"%fam)
    members = []
    for m in range(random.randint(1,5)):
        if idx >= len(cs_people): break
        members.append(cs_people[idx]); assigned.add(cs_people[idx]); idx += 1
    for j, mid in enumerate(members):
        add('5B','5B',hid,mid, 'Y' if j==0 else '')
    if random.random() < 0.3:
        ap = write_doc("objects","hh%d"%hid, random.choice(['pdf','docx']))
        add('5C','5C',hid,ap,'',staff(),rdate(),'Household document',os.path.basename(ap))
    if random.random() < 0.3:
        add('5D','5D',hid,'', "Household prefers consolidated mailings.", rdate(), rtime(), staff())
# (people not in `assigned` remain unaffiliated -- intentionally many)

# ---------------------------------------------------------------- schedule: recurring series (7H + adjuncts) then events (7A + satellites)
all_wf = [w for p in people for w in p['wf']]
series = []
for _ in range(SERIES):
    rid = rec_seq()
    rtype = random.choice(['DAILY','WEEKLY','MONTHLY','YEARLY'])
    interval = {'DAILY':random.choice(['1','weekdays']),
                'WEEKLY':random.choice(['1-monday','2-friday']),
                'MONTHLY':random.choice(['1-1-day','3-15-day','1-1-tuesday']),
                'YEARLY':random.choice(['1-9-day-may','1-last-day-january'])}[rtype]
    add('7H','7H',rid, rdate(2022,2023), rdate(2024,2025), rtype, interval)
    contact = random.choice(cs_people)
    city,state,zipc,county,dist = random.choice(CITIES)
    add('7I','7I',rid,'', "Recurring %s meeting"%rtype.lower(), "%s %s"%(random.choice(FIRST),random.choice(LAST)),
        county,'','', rtime(),'', rtime(), random.choice(['EST','CST']), random.choice(['DC office','State office']),
        random.choice(['Approved','Pending']), random.choice(['','Y']), rdate(), staff(), rdate(), staff(),
        "%d %s"%(random.randint(100,9999),random.choice(STREETS)),'','','', city, state, zipc, '')
    for c in random.sample(EVENT_CODES, random.randint(0,2)):
        add('7J','7J',rid,c)
    for _ in range(random.randint(1,3)):
        if random.random()<0.5: add('7K','7K',rid,'STAFF',staff())
        else: add('7K','7K',rid,'PERSON',random.choice(cs_people))
    if random.random()<0.3:
        ap = write_doc("objects","rec%d"%rid,'pdf'); add('7L','7L',rid,ap,'',staff(),rdate(),'Series agenda',os.path.basename(ap))
    if random.random()<0.3:
        add('7M','7M',rid,'', "Recurring series notes.", rdate(), rtime(), staff())
    if all_wf and random.random()<0.3:
        add('7N','7N',rid,random.choice(all_wf))
    series.append(rid)

for i in range(EVENTS):
    eid = event_seq()
    rid = random.choice(series) if (series and random.random()<0.3) else ''
    contact = random.choice(cs_people)
    city,state,zipc,county,dist = random.choice(CITIES)
    sd = rdate(2023,2025)
    add('7A','7A',eid,rid, random.choice(["Town hall","Ribbon cutting","Constituent meeting",
        "Veterans event","Award ceremony","Office tour"]), contact,
        county, random.choice(ORGS), sd, rtime(), sd, rtime(), random.choice(['EST','CST','EST']),
        random.choice(['DC office','State office','Community Center']), random.choice(['Pending','Approved','Tentative','Declined']),
        random.choice(['','Y']), rdate(), staff(), rdate(), staff(),
        "%d %s"%(random.randint(100,9999),random.choice(STREETS)),'','','', city, state, zipc, '')
    for c in random.sample(EVENT_CODES, random.randint(0,2)):
        add('7B','7B',eid,c)
    for _ in range(random.randint(0,3)):
        if random.random()<0.5: add('7C','7C',eid,'STAFF',staff())
        else: add('7C','7C',eid,'PERSON',random.choice(cs_people))
    if random.random()<0.3:
        if random.random()<0.5 and library:
            add('7D','7D',eid,'',random.choice(library),staff(),rdate(),'Event handout','')
        else:
            ap = write_doc("objects","ev%d"%eid,random.choice(['pdf','docx']))
            add('7D','7D',eid,ap,'',staff(),rdate(),'Event document',os.path.basename(ap))
    if random.random()<0.3:
        add('7E','7E',eid,'', "Event logistics confirmed.", rdate(), rtime(), staff())
    if all_wf and random.random()<0.3:
        add('7F','7F',eid,random.choice(all_wf))

# ---------------------------------------------------------------- write .dat files
os.makedirs(DATA, exist_ok=True)
total = 0
for code in sorted(rows):
    fn = "out_%s.dat" % (code if code == '8A' else code.lower())
    with open(os.path.join(DATA, fn), 'w', newline='', encoding='ascii', errors='replace') as f:
        for rec in rows[code]:
            f.write('\t'.join(rec) + '\r\n')
    total += len(rows[code])

print("=== SCDIF synthetic dataset generated ===")
print("people: %d | households: %d | 6A library: %d | events: %d | series: %d"
      % (len(people), HOUSEHOLDS, LIBRARY, EVENTS, SERIES))
print("records by type:")
for code in sorted(rows):
    if rows[code]:
        print("  %-3s %6d" % (code, len(rows[code])))
print("TOTAL records: %d" % total)
print("document files written: %d" % _doc_count[0])
print("output: %s" % BASE)
