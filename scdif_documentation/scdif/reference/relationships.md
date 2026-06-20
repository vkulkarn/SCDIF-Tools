<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

# SCDIF Relationships — The Entity-Relationship Model

Understanding SCDIF is mostly understanding **which IDs connect which records**.
This file describes the linking keys, the referential-integrity rules, and the
central role of the `8A` code table.

## The linking keys

<table>
<thead>
<tr><th>Key</th><th>Defined in</th><th>Referenced by</th></tr>
</thead>
<tbody>
<tr><td><strong>Person ID</strong></td><td><code>1A</code> (one per person)</td><td><code>1B, 1C, 1D, 1E, 1F, 1G*, 1H*</code> (same person); <code>2A–2E</code> (communication's person); <code>3A, 3B, 3D, 3E, 3F, 3L</code> (workflow's person); <code>3G</code> (constituent); <code>5B</code> (household member); <code>3E</code> Party ID; <code>7A</code> Contact; <code>7C/7K</code> Participant ID when type=PERSON. (*1G/1H call it "Constituent ID".)</td></tr>
<tr><td><strong>Communication ID</strong></td><td><code>2A</code> (one per communication)</td><td><code>2B, 2C, 2D, 2E</code> (same communication).</td></tr>
<tr><td><strong>Workflow ID</strong></td><td><code>3A</code> (one per workflow)</td><td><code>3B, 3D, 3E, 3F, 3L</code> (same workflow); <code>2A</code> (communication's workflow); <code>3G</code> (Casework ID &amp; Parent Casework ID); <code>7F</code> (event→workflow); <code>7N</code> (series→workflow).</td></tr>
<tr><td><strong>Household ID</strong></td><td><code>5A</code> (one per household)</td><td><code>5B, 5C, 5D</code> (same household); <code>2A</code> (communication sent to household).</td></tr>
<tr><td><strong>Document ID</strong></td><td><code>6A</code> (one per library document version)</td><td><code>6B, 6C, 6D, 6E, 6F</code> (same document); and the Document ID field of every attachment record (<code>1F, 2C, 3F, 5C, 6D, 7D, 7L</code>) when the file is in the library.</td></tr>
<tr><td><strong>Event ID</strong></td><td><code>7A</code> (one per event)</td><td><code>7B, 7C, 7D, 7E, 7F</code> (same event).</td></tr>
<tr><td><strong>Recurrence ID</strong></td><td><code>7H</code> (one per series)</td><td><code>7I, 7J, 7K, 7L, 7M, 7N</code> (same series); <code>7A</code> (an event that belongs to the series).</td></tr>
<tr><td><strong>User ID (STAFF)</strong></td><td><code>8A</code> with Code Type = STAFF</td><td>every "User ID" / "Created By" / "Approved By" / "Scheduled by" / "Owned By" field across the format.</td></tr>
<tr><td><strong>Codes (WORK/PERS/COM/EVENT/DOC)</strong></td><td><code>8A</code> with the matching Code Type</td><td><code>1C, 2B, 3B, 6C, 7B, 7J</code> and the code fields they carry.</td></tr>
</tbody>
</table>


## Referential-integrity rules (stated in the format)

These "must match" / "must exist" obligations are explicit in Attachment J-10:

- A child record's foreign-key ID **must equal** the ID in its parent record
  (e.g. a `1B`'s Person ID must equal its `1A`'s Person ID; a `2B`'s
  Communication ID must equal its `2A`'s).
- **"There must be an 8A record containing this code / user ID."** Every code in
  `1C, 2B, 3B, 6C, 7B, 7J`, and every staff User ID anywhere, requires a defining
  `8A` row. This is the single most pervasive integrity rule in the format.
- An attachment that references a library file by **Document ID must match a 6A**
  Document ID; an attachment that instead gives a path-qualified **Document Name**
  is a non-library file (the two are mutually exclusive — one is NULL).
- `2A` Household ID requires a matching `5A`; if `2A` Household Flag = "Y" there
  must also be `5B` records defining members.
- `3E` Party ID and `7A` Contact and `7C/7K` PERSON participants must each have a
  matching `1A`.
- `7A` Recurrence ID (when present) must match a `7H`; `3G` Casework/Parent
  Casework IDs must match `3A` workflows.

## Common NULL conditions

- `2A` Workflow ID / Workflow Person ID are **NULL** when the communication is not
  tied to a workflow.
- `3A`/`3B`/`3D`/`3E`/`3F`/`3L` Person ID is **NULL** when no person is associated
  with the workflow.
- In Text records (`1D, 2D, 3D, 5D, 6E, 7E, 7M`), the **Sequence Number** is
  required only when Date and Time are NULL — i.e. ordering comes from either an
  explicit sequence or the date/time.
- "Approved By" fields are **NULL** when approval is not required or not yet given.
- `6A` Document ID vs. path Document Name; attachment Document ID vs. Document
  Name — exactly one side is populated.

## The 8A code table is the hub

`8A` is the lookup table for the entire export. Every coded value and every staff
identity resolves through it:

```
        ┌─────────────────────────── 8A (Code Table) ───────────────────────────┐
        │  STAFF 178  → "Claire McVay"      PERS  OUTREACH DATABASE → "Contacts…" │
        │  STAFF 298  → "Canon Woodward"    COM   OUTREACH          → "Outreach"  │
        │  WORK  VET  → "Veterans"          EVENT …    DOC …                      │
        └────────────────────────────────────────────────────────────────────────┘
            ▲              ▲                      ▲                 ▲
   User IDs everywhere   1C person codes    2B/6C comm codes   3B/6C work codes
   (1D,2A,3A,6A,7A,…)                       7B/7J event codes
```

When reading any record, resolve its codes and user IDs against `8A` to get human-
readable meanings.

## Category map (who owns what)

```
1 Person ──────┬── 1A name (root)            5 Household ── 5A name (root)
               ├── 1B addresses                          ├── 5B members → 1A
               ├── 1C codes → 8A                          ├── 5C attachments
               ├── 1D text → 8A(staff)                    └── 5D text → 8A(staff)
               ├── 1E phones/emails
               ├── 1F attachments → 6A?/8A     6 Doc Library ─ 6A document (root)
               ├── 1G demographics                        ├── 6B fill-ins
               └── 1H vote history                        ├── 6C codes → 8A
                                                          ├── 6D attachments
2 Communication ─ 2A comm (root) → 1A,3A,5A               ├── 6E text → 8A(staff)
               ├── 2B codes → 8A                          └── 6F owners → 8A(staff)
               ├── 2C documents → 6A?
               ├── 2D text → 8A(staff)         7 Schedule ── 7A event (root) → 1A,7H
               └── 2E fill-ins                            ├── 7B codes → 8A
                                                          ├── 7C participants → 8A/1A
3 Workflow ──── 3A workflow (root) → 1A                   ├── 7D attachments → 6A?
               ├── 3B codes → 8A                          ├── 7E text → 8A(staff)
               ├── 3D text/action history → 8A            ├── 7F → 3A workflows
               ├── 3E parties → 1A               7H series (root) ──┐
               ├── 3F attachments → 6A?/8A                ├── 7I source data
               ├── 3G casework links → 1A,3A             ├── 7J codes → 8A
               └── 3L additional fields                   ├── 7K participants → 8A/1A
                                                          ├── 7L attachments → 6A?
8 Code Tables ─ 8A (the hub for all codes & staff)        ├── 7M text → 8A(staff)
                                                          └── 7N → 3A workflows
```

`?` = via Document ID only when the file is in the library (else a path-qualified
Document Name is used instead).
