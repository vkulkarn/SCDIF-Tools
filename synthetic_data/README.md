<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

# SCDIF Synthetic Data & Validation Tools

Two standalone, **pure-standard-library** Python scripts (no `pip install` needed):

<table>
<thead>
<tr><th>Script</th><th>Purpose</th></tr>
</thead>
<tbody>
<tr><td><a href="generate.py"><code>generate.py</code></a></td><td>Generate a clean, referentially-valid synthetic SCDIF dataset at any scale.</td></tr>
<tr><td><a href="validate.py"><code>validate.py</code></a></td><td>Validate any SCDIF dataset, print a report, and (on issues) write a Claude-ready <code>validation_report.md</code>.</td></tr>
</tbody>
</table>


Both relate to the SCDIF data model documented in the skill at
`../scdif_documentation/scdif/` (start with `SKILL.md`).

---

## `generate.py` — synthetic data generator

Creates a complete SCDIF export: all record types, their satellite records, the
`8A` code table, and real document files — all referentially consistent.

### Usage

```bash
# Interactive: prompts for the number of people
python3 generate.py

# Non-interactive: pass the people count as an argument
python3 generate.py 2000
```

It asks (or takes as an argument) **how many people (`1A`) records** to create.
**Minimum is 100.** Everything else scales in the same proportion as the original
500-person specification:

<table>
<thead>
<tr><th>Quantity</th><th>Rule</th><th>At 500 people</th></tr>
</thead>
<tbody>
<tr><td>People (<code>1A</code>)</td><td>your input (min 100)</td><td>500</td></tr>
<tr><td>Communications (<code>2A</code>) per person</td><td>12–18</td><td>~7,500 total</td></tr>
<tr><td>Workflows (<code>3A</code>) per person</td><td>2–5</td><td>~1,750 total</td></tr>
<tr><td>Households (<code>5A</code>)</td><td>people ÷ 10</td><td>50</td></tr>
<tr><td>Doc-library items (<code>6A</code>)</td><td>people ÷ 10</td><td>50</td></tr>
<tr><td>Events (<code>7A</code>)</td><td>people ÷ 10</td><td>50</td></tr>
<tr><td>Recurring series (<code>7H</code>)</td><td>people ÷ 50</td><td>10</td></tr>
</tbody>
</table>


Rough size: **~96 records and ~8 document files per person** (e.g. 2,000 people →
~190k records, ~16k files), generated in a few seconds. The run is **seeded**, so
the same count always produces the same dataset.

### Output

Written beside the script (any previous output is cleared first, so changing scale
never leaves stale files):

```
synthetic_data/
├── data/                     # one TAB-delimited, CRLF file per record type
│   ├── out_1a.dat … out_7n.dat
│   └── out_8A.dat
└── documents/                # real files referenced by path in the data
    ├── formletters/          # 6A form-letter library (.docx)
    ├── objects/              # incoming docs & attachments (.pdf/.txt/.docx)
    ├── imail/                # incoming email (.txt)
    ├── indivletters/         # individual outgoing letters (.docx)
    └── fomletter_ima/        # form-letter images/attachments
```

### What it guarantees

- Every record padded to its **documented field count**; records end with **CRLF**.
- **Referential integrity:** every Person / Communication / Workflow / Household /
  Document / Event / Recurrence ID resolves; every staff `User ID` and every code
  resolves to an `8A` record; `3L` Workflow Type matches its `3A`.
- Document path references all point to files that exist on disk.
- Some people are intentionally **not** in any household (as requested).
- Document files are copies of one in-memory template per type, whose content is
  literally `Test document <ext>` — reused under many file names.

### Customizing

Distributions and pools live as constants near the top of `generate.py`
(name lists, code pools, workflow types, per-person ranges). Edit and re-run.

---

## `validate.py` — dataset validator & diagnostic reporter

Checks any SCDIF dataset against the documented format and reports problems —
including the real-world quirks catalogued during skill development.

### Usage

```bash
# Validate the generated synthetic data (default)
python3 validate.py

# Validate any other SCDIF export by pointing at its data folder
python3 validate.py ../sample_scdif_data/data
```

`DATA_DIR` defaults to the `data/` folder beside the script. The matching
`documents/` folder is expected as its sibling (for path-resolution checks).

### Output

1. **Console:** a per-record-type summary (counts, observed vs documented field
   widths) and a result line: `clean` or `N ERROR(s), M WARNING(s)`.
2. **`validation_report.md`** — written next to the data folder **only when issues
   are found** (a stale report is removed when the data is clean). It is structured
   for an AI assistant: each finding includes severity, what/why, the SCDIF rule,
   **file:line evidence**, a suggested fix, and a ready-to-paste prompt for Claude.

**Exit code:** `1` if any ERROR-level issues are found, otherwise `0` (useful in CI).

### What it checks

- **Structure:** stray/blank/non-record lines, wrong record type inside a file,
  non-CRLF line endings, records over the 32K limit.
- **Field counts:** records with more fields than documented (undocumented trailing
  fields) and varying widths (trailing-field trimming).
- **Uniqueness:** duplicate "unique" IDs (Person, Communication, Workflow,
  Household, Document, Event, Recurrence).
- **Referential integrity:** orphaned foreign keys, staff `User ID`s and codes
  missing from `8A`.
- **Field-order anomalies:** `6C` Code Type / Code columns swapped.
- **Code tables:** undocumented `8A` code types.
- **Document paths:** unresolved references, **with systematic-pattern detection**
  — e.g. *"removing the `BlobExport` path segment resolves 11 of 12,"* or a
  folder-name typo (`formletter_ima` vs on-disk `fomletter_ima`).

### Working through a report with Claude

```bash
python3 validate.py ../some_export/data        # writes ../some_export/validation_report.md
```

Then ask Claude:

> Read `some_export/validation_report.md`, then look at the data and help me fix these issues.

Each finding's **"Ask Claude"** line is a starting prompt for that specific issue.

---

## Typical workflow

```bash
# 1. Generate a dataset
python3 generate.py 1000

# 2. Validate it (synthetic data should be clean)
python3 validate.py

# 3. Validate a real export to surface its issues
python3 validate.py ../sample_scdif_data/data
#    -> writes ../sample_scdif_data/validation_report.md if problems are found
```

> Note: running `validate.py` against a dataset writes its report **next to that
> dataset's `data/` folder**. Avoid pointing it at a read-only/reference dataset you
> must not modify, or move the report afterward.
