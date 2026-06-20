---
name: scdif-data-model
description: >-
  Understand the Senate CSS Data Interchange Format (SCDIF), the standard data
  model used to transfer constituent-services data between Senate offices' CSS
  systems and to archival repositories. Use this whenever you must read,
  interpret, explain, map, validate, or answer questions about SCDIF / "Senate
  CSS Interchange Format" / "Attachment J-10" data: its record types (1A, 2A,
  3L, 6A, 7H, 8A, etc.), field meanings, fixed value sets, the IDs that link
  records together, and the cross-cutting rules. Covers the logical data model.
---

<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->


# SCDIF — Senate CSS Data Interchange Format

## What this is

A **Constituent Services System (CSS)** is the database a U.S. Senator's official
office uses to track constituents, the casework and requests it handles for them,
the mail and other communications exchanged, form letters, schedules, and
households.

**SCDIF** (Senate CSS Data Interchange Format, defined in **Attachment J-10**) is
the **standard format for exchanging that data**. It is used to:

- transfer data from one CSS vendor's system to another (e.g. when an office
  changes vendors), and
- transfer data from an outgoing Senator's CSS to a designated **archival
  repository** ("SCDIF archiving conversion").

This skill describes the **logical data model**: the record types, what every
field means, the fixed (enumerated) value sets, how records relate to each other,
and the universal rules. It is the authoritative mental model an AI needs to
correctly read and reason about SCDIF data.

## The 8 data categories

SCDIF data is organized into numbered categories. **There is no category 4.**

<table>
<thead>
<tr><th>#</th><th>Category</th><th>Purpose</th></tr>
</thead>
<tbody>
<tr><td>1</td><td><strong>Person data</strong></td><td>People and organizations: names, addresses, codes, notes, phones/emails, attachments, demographics, vote history</td></tr>
<tr><td>2</td><td><strong>Communication data</strong></td><td>Any contact between a person and the office (incoming/outgoing letters, email, phone, newsletters, etc.)</td></tr>
<tr><td>3</td><td><strong>Workflow data</strong></td><td>The office's business processes — casework, flag requests, tour requests, academy nominations, outreach, etc.</td></tr>
<tr><td>5</td><td><strong>Household data</strong></td><td>Groupings of people into households</td></tr>
<tr><td>6</td><td><strong>Form Letter / Document Library data</strong></td><td>The office's library of reusable form letters and documents (with versions, fill-ins, owners)</td></tr>
<tr><td>7</td><td><strong>Schedule data</strong></td><td>Events and recurring event series, their participants, codes, and linked workflows</td></tr>
<tr><td>8</td><td><strong>Code tables</strong></td><td>The lookup tables that define every code (and staff user ID) referenced elsewhere</td></tr>
</tbody>
</table>


## How records are named (the 2-byte Record Type)

Every record's **first field is a 2-byte Record Type**:

- **1st character = the category digit** (1, 2, 3, 5, 6, 7, or 8).
- **2nd character = a letter** identifying the specific record within that
  category (A, B, C, …).

So `1A` = Person Name, `1B` = Person Address, `2A` = Communication, `3A` =
Workflow, `3L` = Additional Workflow Data, `6A` = Form Letter/Document Library
item, `7H` = Recurring Series Definition, `8A` = Code Table entry.

A single real-world entity is assembled from **many records**: e.g. one person is
a `1A` plus its `1B`/`1C`/`1D`/`1E`/`1F`/`1G`/`1H` records, all tied together by a
shared **Person ID**. Understanding SCDIF is mostly understanding **which IDs link
which records** — see `reference/relationships.md`.

## The 4 things you must keep in mind

1. **IDs link everything.** Person ID, Communication ID, Workflow ID, Household
   ID, Document ID, Event ID, and Recurrence ID are foreign keys that stitch
   records together. Many fields are explicitly *required to match* an ID in
   another record, or are NULL under stated conditions.
2. **The 8A code table is the hub.** Almost every code or staff "User ID" used
   anywhere must have a corresponding `8A` record that defines it.
3. **Fixed value sets matter.** Type and status fields draw from documented value
   lists; status values in particular carry a "Closed Flag" meaning (whether the
   office considers the work done).
4. **Universal formats.** Dates are `YYYYMMDD`; times are `HH:MM:SS`; empty
   fields mean NULL/"not provided".

## Reference files (read these for detail)

<table>
<thead>
<tr><th>File</th><th>Contents</th></tr>
</thead>
<tbody>
<tr><td><code>reference/record-types.md</code></td><td>Every record type, field by field (number, name, meaning, type, multiplicity, NULL rules). The core reference.</td></tr>
<tr><td><code>reference/enumerations.md</code></td><td>All fixed value sets: person/address/phone/document types, the code-type→record matrix, communication &amp; workflow <strong>status values with Closed-Flag semantics</strong>, the recurrence-interval grammar, participant types.</td></tr>
<tr><td><code>reference/relationships.md</code></td><td>The entity-relationship model: which IDs link which records, referential-integrity rules, NULL conditions, the 8A hub, and a category-by-category map.</td></tr>
<tr><td><code>reference/examples.md</code></td><td>Worked walkthroughs (grounded in real sample data) tracing how a constituent's records interconnect.</td></tr>
<tr><td><code>reference/additional-requirements.md</code></td><td>The cross-cutting rules: date/time formats, type-code extensibility, Text-field constraints, custom/user-defined fields, <strong>3L Additional Workflow Data</strong> (with Boy Scout / Case / Outreach examples), archiving customizations.</td></tr>
<tr><td><code>reference/serialization.md</code></td><td>A conceptual note on how records are laid out as text (TAB-delimited lines, pipe-substituted newlines, empty=NULL). Logical-level only — not a parsing guide.</td></tr>
</tbody>
</table>


## Scope note

This skill teaches **the data** — the logical model defined in Attachment J-10.
It is *not* a guide to a specific physical file set: it does not enumerate the
`.dat` files of any particular export or explain how to parse them beyond the
conceptual note in `reference/serialization.md`.
