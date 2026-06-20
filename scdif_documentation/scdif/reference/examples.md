<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

# SCDIF Worked Examples

These walkthroughs trace how records interconnect. The IDs and values are drawn
from real SCDIF sample data so the relationships are concrete. (Field values are
shown logically; this is not a guide to the physical file layout.)

---

## Example 1 — A constituent and their records: Robert Anderson (Person ID 100002)

**`1A` (Name)** establishes the person:

> Person ID **100002**, Person Type `CS` (Constituent), Mr. Robert Anderson,
> salutation "Mr. Anderson".

Everything else about him hangs off Person ID `100002`:

- **`1B` (Address):** Person 100002, Address 100002, type `HO` (Home), Primary `Y`,
  Default `Y`, "1001 Sample St., Unit 202", Chattanooga, TN 37402-1801, Hamilton
  county, district TN03.
- **`1C` (Person Code):** Person 100002, code type `PERS`, code
  `OUTREACH DATABASE`. → resolves in **`8A`**: `PERS / OUTREACH DATABASE /
  "Contacts from the Outreach Database"`.
- **`1E` (Phone/Email):** three records for Person 100002 —
  `PHONE (423) 668-0000` (primary), `EMAIL robert.anderson.test@testemail.com`
  (primary), `FAX (423) 668-1111` (primary).
- **`5A`/`5B` (Household):** Household 100002 "The Anderson Family" (salutation
  "Mr. Anderson and Family"); `5B` lists Person 100002 as a member with Primary
  Contact `Y`.

**A communication he received — `2A` (Communication ID 7769507):**

> Person 100002, Communication 7769507, status `C` (Closed → Closed Flag Y),
> Date In/Out 2013-07-30, response type "imail", sent to
> robert.anderson.test@testemail.com.

Its satellite records:

- **`2B` (Comm Code):** Comm 7769507, code `OUTREACH`, Position "Neutral". →
  resolves in **`8A`**: `COM / OUTREACH / "Outreach"`.
- **`2C` (Comm Document):** Comm 7769507, Document Type `OUTGOING`, Document Name
  `..\documents\formletters\175959.doc`, Document ID **175959**. The Document ID
  ties this outgoing letter to a **`6A`** library item.

**Reading it as a story:** Constituent Robert Anderson (a contact from the
Outreach Database) was sent an outgoing "Outreach" letter (form-letter 175959) on
2013-07-30; the communication is closed; he is the primary contact of the Anderson
household.

---

## Example 2 — A casework/Boy Scout workflow: Person ID 100025, Workflow ID 562726

**`3A` (Workflow)** is the root:

> Person **100025**, Workflow **562726**, Workflow Type `Boy Scout`, User ID
> `298`, Start 2018-11-08, Update 2018-11-08, description "Eagle Scout request",
> Status `CL.FAV` (Closed Favorably → Closed Flag Y).

- The handling staffer resolves in **`8A`**: `STAFF / 298 / "Canon Woodward"`.

**`3L` (Additional Workflow Data)** carries the Boy-Scout-specific fields for this
workflow (Workflow Type must match the `3A`):

> Workflow 562726 / type `Boy Scout`: `OpenStatus = Active`, `Region`, `trpnum`
> (Troop #), `trplead` (Troop Leader), `ceraddr` (Ceremony Address), `SS #`,
> `ID #`.

These field names/meanings come from the office's documented 3L field set for the
`Boy Scout` workflow type (see `additional-requirements.md`).

**`1F` (Person Attachment)** — the Eagle Scout letter attached to the person:

> Person 100025, Document Name `..\documents\BlobExport\objects\test1.tif`, User
> ID `129`, Attached 2007-12-05, File name "EagleScoutLetter.tif".

Because a path-qualified Document Name is given (and Document ID is empty), this is
a **non-library** file traveling with the export, not a `6A` item.

**Reading it as a story:** An Eagle Scout request (workflow 562726) for person
100025 was handled by Canon Woodward and closed favorably; Boy-Scout-specific
details (troop, leader, ceremony address) ride along in `3L`; a scanned Eagle
Scout letter is attached to the person.

---

## Example 3 — Resolving codes through 8A

Every coded value and staff identity is defined once in `8A` and referenced
everywhere:

<table>
<thead>
<tr><th>Seen in a record</th><th>Code Type</th><th>8A definition</th></tr>
</thead>
<tbody>
<tr><td><code>1C</code> code <code>OUTREACH DATABASE</code></td><td>PERS</td><td>"Contacts from the Outreach Database"</td></tr>
<tr><td><code>2B</code> code <code>OUTREACH</code></td><td>COM</td><td>"Outreach"</td></tr>
<tr><td><code>3A</code>/<code>2A</code> User ID <code>178</code></td><td>STAFF</td><td>"Claire McVay"</td></tr>
<tr><td><code>3A</code> User ID <code>298</code></td><td>STAFF</td><td>"Canon Woodward"</td></tr>
<tr><td><code>1F</code> User ID <code>129</code></td><td>STAFF</td><td><em>(staffer name in 8A STAFF 129)</em></td></tr>
</tbody>
</table>


So whenever you encounter a bare code or a numeric "User ID", look it up in `8A`
(matching the appropriate Code Type) to get its human-readable meaning.

---

## Example 4 — A form-letter library item (6A) referenced by a communication

**`6A` (Document Library)** defines a reusable letter:

> Document ID **129330**, Version 1, Grouping 129330, type "Form", display name
> "Interchange Fee Amendment - oppose", file
> `..\documents\BlobExport\formletters\129330.doc`, Created By `151`, Revised By
> `211`, Created 2009-06-09, Status "Inactive", Inactive Flag `Y`, virtual
> directory "Form Letters".

A communication that sent this letter points back to it by **Document ID 129330**
in its `2C` record (Document Type `OUTGOING`). That is the link between a sent
communication and the library version it used — and the `6A`'s `6B` fill-in
definitions plus the communication's `2E` fill-in values together describe how the
template was personalized.
