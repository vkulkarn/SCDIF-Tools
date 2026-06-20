<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

# SCDIF — Senate CSS Data Interchange Format (Single-File Knowledge Bundle)

_This is a portable, self-contained version of the `scdif-data-model` skill: the SKILL.md orientation followed by all reference files concatenated. Drop it into any AI system as context/knowledge. The structured folder version (SKILL.md + reference/*.md) is the source of truth._


---

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



---


# SCDIF Record Types — Field Reference

Every record begins with field 1, the **Record Type** (e.g. `1A`). Fields are
numbered in order. "Mult." notes how many of this record may exist per parent
entity. Unless stated, an empty field means NULL / not provided. Dates are
`YYYYMMDD`; times are `HH:MM:SS`. For the fixed value sets referenced below, see
`enumerations.md`; for how the IDs link, see `relationships.md`.

---

## Category 1 — Person Data

A person (or organization) is a `1A` record plus any number of related 1x
records, all sharing the same **Person ID**.

### 1A — Name Data  *(one per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1A</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Unique ID identifying the person. The key referenced by all other person records.</td></tr>
<tr><td>3</td><td>Person Type</td><td>Code for the kind of person — see <strong>Person Type Values</strong>.</td></tr>
<tr><td>4</td><td>Prefix</td><td>e.g. "Mr.", "Mrs.", "The Honorable".</td></tr>
<tr><td>5</td><td>First Name</td><td></td></tr>
<tr><td>6</td><td>Middle Name</td><td>Middle name or initial.</td></tr>
<tr><td>7</td><td>Last Name</td><td></td></tr>
<tr><td>8</td><td>Suffix</td><td>e.g. "Jr."</td></tr>
<tr><td>9</td><td>Appellation</td><td>e.g. "MD".</td></tr>
<tr><td>10</td><td>Organization Name</td><td>Used if the record is for an organization, not an individual.</td></tr>
<tr><td>11</td><td>Salutation</td><td>Preferred salutation, e.g. "Bob" or "Senator Jones".</td></tr>
<tr><td>12</td><td>Date of Birth</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>13</td><td>No Mail Flag</td><td>"Y" if the person has requested no mail to any of their addresses.</td></tr>
<tr><td>14</td><td>Deceased Flag</td><td>"Y" if the person is deceased.</td></tr>
<tr><td>15</td><td>Spouse's Name</td><td></td></tr>
<tr><td>16</td><td>Email Flag</td><td>"Y" if the person's preferred communication method is email.</td></tr>
</tbody>
</table>


### 1B — Address Data  *(multiple per person, one per address)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1B</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the Person ID of the associated 1A.</td></tr>
<tr><td>3</td><td>Address ID</td><td>Numeric ID/sequence identifying this address.</td></tr>
<tr><td>4</td><td>Address Type</td><td>Code for the address kind — see <strong>Address Type Values</strong>.</td></tr>
<tr><td>5</td><td>Primary Flag</td><td>"Y" if this is the primary address <em>of this type</em>.</td></tr>
<tr><td>6</td><td>Default Address Flag</td><td>"Y" if this is the person's default mailing address.</td></tr>
<tr><td>7</td><td>Title</td><td>Title tied to an org/business address, e.g. "CEO".</td></tr>
<tr><td>8</td><td>Organization Name</td><td>Org/business name when a person's business address.</td></tr>
<tr><td>9–12</td><td>Address line 1–4</td><td>Street address lines.</td></tr>
<tr><td>13</td><td>City</td><td></td></tr>
<tr><td>14</td><td>State Code</td><td>2-letter, e.g. "VA", "DC", "MD".</td></tr>
<tr><td>15</td><td>Zip Code</td><td><code>XXXXX-XXXX</code> (9-digit) or <code>XXXXX</code> (5-digit); for international, the country's zip.</td></tr>
<tr><td>16</td><td>Carrier Route</td><td></td></tr>
<tr><td>17</td><td>County</td><td></td></tr>
<tr><td>18</td><td>Country</td><td>For international addresses.</td></tr>
<tr><td>19</td><td>District</td><td>Congressional district.</td></tr>
<tr><td>20</td><td>Precinct</td><td></td></tr>
<tr><td>21</td><td>No Mail Flag</td><td>"Y" if no mail should go to this address.</td></tr>
<tr><td>22</td><td>Deliverability</td><td>"U" undeliverable, "D" deliverable, "P" possibly deliverable, NULL = not verified.</td></tr>
</tbody>
</table>


### 1C — Person Codes  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1C</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Should match the associated 1A.</td></tr>
<tr><td>3</td><td>Person Code Type</td><td>Type of code in field 4 — see <strong>Person Code Type Values</strong> (PERS, WORK). The same type may repeat.</td></tr>
<tr><td>4</td><td>Code</td><td>A code describing the person/agency. <strong>Must have a matching 8A</strong> record for this person/workflow code.</td></tr>
</tbody>
</table>


### 1D — Person Text (Comments or Notes)  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1D</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>1D Sequence Number</td><td>Orders the 1D records for a person. Required if Date (5) and Time (6) are NULL.</td></tr>
<tr><td>4</td><td>Text</td><td>Freeform comments/notes about the person.</td></tr>
<tr><td>5</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who entered the text. <strong>Must have a matching 8A</strong> staff record.</td></tr>
</tbody>
</table>


### 1E — Person Phone/Email  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1E</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Person Phone or Email Type</td><td>Type code — see <strong>Person Phone/Email Type Values</strong>. May repeat.</td></tr>
<tr><td>4</td><td>Phone Number, Email, or URL</td><td>The value.</td></tr>
<tr><td>5</td><td>Primary Flag</td><td>"Y" if primary for this type.</td></tr>
<tr><td>6</td><td>Invalid Flag</td><td>"Y" if marked invalid/undeliverable.</td></tr>
</tbody>
</table>


### 1F — Person Attachments  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1F</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Document Name</td><td>For files <strong>not</strong> in the document library: the path-qualified file location.</td></tr>
<tr><td>4</td><td>Document ID</td><td>For files <strong>in</strong> the library: must match a 6A Document ID.</td></tr>
<tr><td>5</td><td>User ID</td><td>Staffer who attached it. <strong>Must have a matching 8A</strong> staff record.</td></tr>
<tr><td>6</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Text</td><td>Comments/notes about the attachment.</td></tr>
<tr><td>8</td><td>File name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 1G — People Demographics  *(per constituent)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1G</code></td></tr>
<tr><td>2</td><td>Constituent ID</td><td>Should match the associated 1A's Person ID.</td></tr>
<tr><td>3</td><td>Provider</td><td>The data provider.</td></tr>
<tr><td>4</td><td>Provider ID</td><td>Unique ID from the data provider.</td></tr>
<tr><td>5</td><td>Voter ID</td><td>State Voter ID.</td></tr>
<tr><td>6</td><td>Last Updated</td><td>Date record last updated.</td></tr>
<tr><td>7</td><td>Regis Date</td><td>Voter registration date.</td></tr>
<tr><td>8</td><td>Absentee Voter</td><td>"Y" if absentee voter.</td></tr>
<tr><td>9</td><td>Marital Status</td><td>Single / Non-Tradit / Married.</td></tr>
<tr><td>10</td><td>Have Child</td><td>Y/N.</td></tr>
<tr><td>11</td><td>Home Owner</td><td>Y/N.</td></tr>
<tr><td>12</td><td>Business Owner</td><td>Y/N.</td></tr>
<tr><td>13</td><td>Race</td><td></td></tr>
<tr><td>14</td><td>Ethnicity</td><td></td></tr>
<tr><td>15</td><td>Language</td><td>Primary language spoken.</td></tr>
<tr><td>16</td><td>Education</td><td>Number of years of education.</td></tr>
<tr><td>17</td><td>School Dist</td><td></td></tr>
<tr><td>18</td><td>State House Dist</td><td></td></tr>
<tr><td>19</td><td>State Senate Dist</td><td></td></tr>
<tr><td>20</td><td>Ward</td><td></td></tr>
<tr><td>21</td><td>Township</td><td></td></tr>
<tr><td>22</td><td>Borough</td><td></td></tr>
<tr><td>23</td><td>Precinct</td><td></td></tr>
<tr><td>24</td><td>Birthyear</td><td></td></tr>
</tbody>
</table>


### 1H — People Vote History  *(multiple per constituent)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>1H</code></td></tr>
<tr><td>2</td><td>Constituent ID</td><td>Should match the associated 1A.</td></tr>
<tr><td>3</td><td>Election Year</td><td>Year the constituent voted.</td></tr>
<tr><td>4</td><td>Election Type</td><td>P, G, or PP.</td></tr>
</tbody>
</table>


---

## Category 2 — Communication Data

A communication is any contact between a person and the office (a constituent's
phone call, an outgoing mailing, etc.). Workflow "action history" is **not** here
— that lives in `3D`.

### 2A — Communication Data  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>2A</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Communication ID</td><td>Unique ID for the communication.</td></tr>
<tr><td>4</td><td>Workflow ID</td><td>Matches a 3A Workflow ID; NULL if not tied to a workflow.</td></tr>
<tr><td>5</td><td>Workflow Person ID</td><td>Matches the 3A's Person ID; NULL if not tied to a workflow.</td></tr>
<tr><td>6</td><td>Communication Type</td><td>Type/method, e.g. "LETTER", "EMAIL", "PHONE", "NEWSLETTER", "POST CARD", "VISIT", "DMAIL", "NONE". <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who handled it. <strong>Must have a matching 8A</strong> staff record.</td></tr>
<tr><td>8</td><td>Approved By</td><td>Approving staffer's User ID; NULL if no approval required/granted. <strong>8A</strong> staff record.</td></tr>
<tr><td>9</td><td>Status</td><td>Communication status — all possible values documented; see <strong>Communication Status Values</strong>.</td></tr>
<tr><td>10</td><td>Date In</td><td>Received date <code>YYYYMMDD</code>.</td></tr>
<tr><td>11</td><td>Date Out</td><td>Completed date <code>YYYYMMDD</code>.</td></tr>
<tr><td>12</td><td>Reminder date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>13</td><td>Update Date</td><td>Last-updated date <code>YYYYMMDD</code>.</td></tr>
<tr><td>14</td><td>Response Type</td><td>Reply method, e.g. "LETTER", "EMAIL". <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
<tr><td>15</td><td>Address ID</td><td>Matches the 1B Address ID the communication was sent to.</td></tr>
<tr><td>16</td><td>Email Address</td><td>Email it was sent to.</td></tr>
<tr><td>17</td><td>Household Flag</td><td>"Y" if sent to a household (then a 5B must define members).</td></tr>
<tr><td>18</td><td>Household ID</td><td>The 5A household; <strong>must have a matching 5A</strong>.</td></tr>
<tr><td>19</td><td>Group Name</td><td>The group/batch this communication is part of.</td></tr>
<tr><td>20</td><td>Salutation</td><td>Salutation used.</td></tr>
<tr><td>21</td><td>Subject - Undocumented</td><td>Subject/description of the communication.</td></tr>
</tbody>
</table>


### 2B — Communication Codes  *(multiple per communication)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>2B</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Communication ID</td><td>Must match the associated 2A.</td></tr>
<tr><td>4</td><td>Communication Code</td><td>Subject/interest code (e.g. "TAXES", "GUNCTRL"). <strong>Must have a matching 8A</strong>.</td></tr>
<tr><td>5</td><td>Position</td><td>Constituent's position on the subject, e.g. "PRO", "CON", "NEUTRAL", "NONE". <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
</tbody>
</table>


### 2C — Communication Documents  *(multiple per communication)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>2C</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Communication ID</td><td>Must match the associated 2A.</td></tr>
<tr><td>4</td><td>Document Type</td><td>INCOMING / OUTGOING / AT_INn / AT_OUTn — see <strong>Document Type Values</strong>.</td></tr>
<tr><td>5</td><td>Communication Document Name</td><td>Path-qualified file name; NULL if the doc is in the library (then use field 6).</td></tr>
<tr><td>6</td><td>Communication Document ID</td><td>Matches a 6A Document ID; NULL if not in the library (then use field 5).</td></tr>
<tr><td>7</td><td>File Location</td><td>Physical hardcopy location (e.g. file-cabinet location of the original).</td></tr>
<tr><td>8</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


> **Observed deviation:** in some exports, an *incoming* document's file name
> appears in field 7 (File Location) with field 8 (File Name) omitted/trimmed,
> rather than in field 8 as documented. When reading `2C`, allow for the file
> name to surface in either field 7 or field 8.

### 2D — Communication Text (Comments or Notes)  *(multiple per communication)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>2D</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Communication ID</td><td>Must match the associated 2A.</td></tr>
<tr><td>4</td><td>2D Sequence Number</td><td>Orders 2D records; required if Date (6) and Time (7) are NULL.</td></tr>
<tr><td>5</td><td>Text</td><td>Freeform comments/notes about the communication.</td></tr>
<tr><td>6</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>8</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


### 2E — Communication Fill-in Data  *(multiple per communication, one per fill-in field)*

User-defined fill-in (variable text insert) values used in a letter sent to a
person. May be stored in the letter itself or here.

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>2E</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Must match the associated 1A.</td></tr>
<tr><td>3</td><td>Communication ID</td><td>Must match the associated 2A.</td></tr>
<tr><td>4</td><td>Fill-in Field Name</td><td>Name of the fill-in field as it appears in the document.</td></tr>
<tr><td>5</td><td>Fill-in Data</td><td>Text inserted in place of the fill-in field.</td></tr>
</tbody>
</table>


---

## Category 3 — Workflow Data

Office business processes not defined elsewhere: casework (constituent requests
for help with a federal agency), flag requests, tour requests, etc. (There is no
`3C`.)

### 3A — Workflow Data  *(multiple per person)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3A</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>The person the workflow is about; matches 1A. NULL if no person is associated.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Unique ID for the workflow.</td></tr>
<tr><td>4</td><td>Workflow Type</td><td>Code for the process — see <strong>Workflow Type Values</strong>.</td></tr>
<tr><td>5</td><td>User ID</td><td>Staffer who handled it. <strong>8A</strong> staff record.</td></tr>
<tr><td>6</td><td>Start Date</td><td>Initiated <code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>End Date</td><td>Completed <code>YYYYMMDD</code>.</td></tr>
<tr><td>8</td><td>Reminder date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>9</td><td>Update Date</td><td>Last-updated <code>YYYYMMDD</code>.</td></tr>
<tr><td>10</td><td>Workflow Description</td><td>Freeform, e.g. "Veteran benefits inquiry".</td></tr>
<tr><td>11</td><td>Status</td><td>Workflow status — all possible values documented; see <strong>Workflow Status Values</strong> (carries Closed-Flag meaning).</td></tr>
</tbody>
</table>


### 3B — Workflow Codes  *(multiple per workflow)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3B</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Matches 3A's Person ID; NULL if none.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches the associated 3A.</td></tr>
<tr><td>4</td><td>Workflow Code</td><td>e.g. "VET", "SOCSEC", "RAILROAD RETIREMENT", "IMMIGRATION". <strong>Must have a matching 8A</strong>.</td></tr>
</tbody>
</table>


### 3D — Workflow Text (Comments/Notes) / Action Histories  *(multiple per workflow)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3D</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Matches 3A's Person ID; NULL if none.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches the associated 3A.</td></tr>
<tr><td>4</td><td>3D Sequence Number</td><td>Orders 3D records; required if Date (6) and Time (7) are NULL.</td></tr>
<tr><td>5</td><td>Text</td><td>Freeform comments/notes, or action-history detail about the workflow.</td></tr>
<tr><td>6</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>8</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


### 3E — Workflow Parties  *(multiple per workflow)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3E</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>The person the workflow is about; matches 3A. NULL if none.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches the associated 3A.</td></tr>
<tr><td>4</td><td>Party ID</td><td>Person ID of a party (incl. agencies) interested in the workflow. <strong>Must have a matching 1A</strong>.</td></tr>
<tr><td>5</td><td>Role</td><td>Function/role the party/person serves in the workflow.</td></tr>
</tbody>
</table>


### 3F — Workflow Attachments  *(multiple per workflow)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3F</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Matches 3A's Person ID; NULL if none.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches the associated 3A.</td></tr>
<tr><td>4</td><td>Document Name</td><td>For files <strong>not</strong> in the library: path-qualified location.</td></tr>
<tr><td>5</td><td>Document ID</td><td>For files <strong>in</strong> the library: matches a 6A Document ID.</td></tr>
<tr><td>6</td><td>User ID</td><td>Staffer who attached it. <strong>8A</strong> staff record.</td></tr>
<tr><td>7</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>8</td><td>Text</td><td>Comments/notes about the attachment.</td></tr>
<tr><td>9</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 3G — Casework Relationship  *(multiple per case)*

Links one casework record to another (parent/child cases).

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3G</code></td></tr>
<tr><td>2</td><td>Constituent ID</td><td>The constituent the case was opened for; matches 1A.</td></tr>
<tr><td>3</td><td>Casework ID</td><td>Matches the associated 3A's (casework) Workflow ID.</td></tr>
<tr><td>4</td><td>Parent Casework ID</td><td>The parent case's 3A Workflow ID.</td></tr>
<tr><td>5</td><td>Create Date</td><td><code>YYYYMMDD</code>.</td></tr>
</tbody>
</table>


### 3L — Additional Workflow Data  *(multiple per workflow)*

A continuation of 3A used to transmit **workflow-type-specific** fields (both
out-of-the-box and custom/user-defined). One 3L per extra field. See
`additional-requirements.md` for the documented field sets per workflow type.

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>3L</code></td></tr>
<tr><td>2</td><td>Person ID</td><td>Matches 3A's Person ID; NULL if none.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches the associated 3A.</td></tr>
<tr><td>4</td><td>Workflow Type</td><td>Must match the 3A's Workflow Type for this workflow.</td></tr>
<tr><td>5</td><td>Field Name</td><td>Name of the additional field.</td></tr>
<tr><td>6</td><td>Field Value</td><td>Value of the additional field.</td></tr>
</tbody>
</table>


---

## Category 5 — Household Data

### 5A — Household Name Data  *(one per household)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>5A</code></td></tr>
<tr><td>2</td><td>Household ID</td><td>Unique ID for the household.</td></tr>
<tr><td>3</td><td>Household Name</td><td>e.g. "The Smith Family".</td></tr>
<tr><td>4</td><td>Household Salutation</td><td>e.g. "Smith Family".</td></tr>
</tbody>
</table>


### 5B — Household Member Data  *(multiple per household, one per member)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>5B</code></td></tr>
<tr><td>2</td><td>Household ID</td><td>Matches the associated 5A.</td></tr>
<tr><td>3</td><td>Person ID</td><td>A member; <strong>must have a matching 1A</strong>.</td></tr>
<tr><td>4</td><td>Primary Contact Flag</td><td>"Y" if head of household / primary contact.</td></tr>
</tbody>
</table>


### 5C — Household Attachments  *(multiple per household)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>5C</code></td></tr>
<tr><td>2</td><td>Household ID</td><td>Matches the associated 5A.</td></tr>
<tr><td>3</td><td>Document Name</td><td>For files <strong>not</strong> in the library: path-qualified location.</td></tr>
<tr><td>4</td><td>Document ID</td><td>For files <strong>in</strong> the library: matches a 6A Document ID.</td></tr>
<tr><td>5</td><td>User ID</td><td>Staffer who attached it. <strong>8A</strong> staff record.</td></tr>
<tr><td>6</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Text</td><td>Comments/notes.</td></tr>
<tr><td>8</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 5D — Household Text (Comments or Notes)  *(multiple per household)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>5D</code></td></tr>
<tr><td>2</td><td>Household ID</td><td>Matches the associated 5A.</td></tr>
<tr><td>3</td><td>5D Sequence Number</td><td>Orders 5D records; required if Date (5) and Time (6) are NULL.</td></tr>
<tr><td>4</td><td>Text</td><td>Freeform comments/notes.</td></tr>
<tr><td>5</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


---

## Category 6 — Form Letter / Document Library Data

The office's library of reusable form letters and documents (typically with
metadata). Incoming email, incoming correspondence images, and ad-hoc outgoing
mail are **not** part of the library.

### 6A — Form Letter / Document Library Data  *(one per document version)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6A</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Unique ID for this form letter/document. The key referenced by all other 6x records and by attachment fields elsewhere.</td></tr>
<tr><td>3</td><td>Version</td><td>Version of the document (e.g. 1, 2, 3).</td></tr>
<tr><td>4</td><td>Document Grouping ID</td><td>Links multiple versions of the same document.</td></tr>
<tr><td>5</td><td>Document Type</td><td>The type of document/file.</td></tr>
<tr><td>6</td><td>Document Display Name</td><td>Name the user sees. Required for all 6A.</td></tr>
<tr><td>7</td><td>Document Description</td><td>Freeform description.</td></tr>
<tr><td>8</td><td>Document Name</td><td>Path-qualified file name of this version, e.g. <code>/docs/newsltrs/oct99nl.doc</code>.</td></tr>
<tr><td>9</td><td>Created By</td><td>Staffer who created this version. <strong>8A</strong> staff record.</td></tr>
<tr><td>10</td><td>Revised By</td><td>Staffer who last revised it. <strong>8A</strong> staff record.</td></tr>
<tr><td>11</td><td>Approved By</td><td>Approving staffer; NULL if no approval required/granted. <strong>8A</strong> staff record.</td></tr>
<tr><td>12</td><td>Creation Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>13</td><td>Revision Date</td><td>Last revision <code>YYYYMMDD</code>.</td></tr>
<tr><td>14</td><td>Last Used Date</td><td>Last used/assigned <code>YYYYMMDD</code>.</td></tr>
<tr><td>15</td><td>Status</td><td>e.g. Draft, Approved. <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
<tr><td>16</td><td>Inactive Flag</td><td>"Y" if this version is inactive (used before, but content now out of date).</td></tr>
<tr><td>17</td><td>Virtual Directory</td><td>The directory path the user sees, e.g. <code>\FY16 Appropriation Requests\Education\</code>.</td></tr>
</tbody>
</table>


### 6B — Form Letter / Document Library Fill-in Data  *(multiple per document, one per fill-in)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6B</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Matches the associated 6A.</td></tr>
<tr><td>3</td><td>Fill-in Field Name</td><td>Name of the fill-in field as it appears in the document.</td></tr>
<tr><td>—</td><td>Field Label</td><td>Name of the fill-in field as shown in software, if different from the field name.</td></tr>
</tbody>
</table>


### 6C — Form Letter / Document Library Code Data  *(multiple per document)*

Associates a document with workflow, communication, or document codes.

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6C</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Matches the associated 6A.</td></tr>
<tr><td>3</td><td>Code Type</td><td>WORK / COM / DOC — see <strong>Code Type Values</strong>.</td></tr>
<tr><td>4</td><td>Code</td><td>The code. <strong>Must have a matching 8A</strong>.</td></tr>
</tbody>
</table>


> **Observed deviation:** some exports populate these two columns in the reverse
> order — the **Code** in field 3 and the **Code Type** in field 4 (e.g.
> `OUTREACH | COM` instead of `COM | OUTREACH`). When reading `6C`, determine
> which column is which by checking which value is a known Code Type rather than
> trusting position.

### 6D — Form Letter / Document Library Attachments  *(multiple per document)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6D</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Matches the associated 6A.</td></tr>
<tr><td>3</td><td>Document Name</td><td>Path-qualified file name of the attached file.</td></tr>
<tr><td>4</td><td>User ID</td><td>Staffer who attached it. <strong>8A</strong> staff record.</td></tr>
<tr><td>5</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Text</td><td>Comments/notes.</td></tr>
<tr><td>7</td><td>Form Letter Attachment Flag</td><td>"Y" if the file is attached to a form letter <strong>and</strong> should be sent as part of the form-letter response.</td></tr>
<tr><td>8</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 6E — Form Letter / Document Library Text (Comments/Notes)  *(multiple per document)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6E</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Matches the associated 6A.</td></tr>
<tr><td>3</td><td>6E Sequence Number</td><td>Orders 6E records; required if Date (5) and Time (6) are NULL.</td></tr>
<tr><td>4</td><td>Text</td><td>Freeform comments/notes.</td></tr>
<tr><td>5</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


### 6F — Form Letter / Document Library Owner Data  *(multiple per document)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>6F</code></td></tr>
<tr><td>2</td><td>Document ID</td><td>Matches the associated 6A.</td></tr>
<tr><td>3</td><td>Owned By</td><td>Owner/responsible staffer's User ID. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


---

## Category 7 — Schedule Data

Events (`7A`–`7F`) and recurring series (`7H`–`7N`). (There is no `7G`.) The
`7I`–`7N` records are adjuncts to the `7H` recurring-series definition.

### 7A — Schedule/Event Data  *(one per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7A</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Unique ID for the event.</td></tr>
<tr><td>3</td><td>Recurrence ID</td><td>If part of a recurring series, matches a 7H Recurrence ID; NULL otherwise. (Each event in a series is also provided individually as 7A–7F.)</td></tr>
<tr><td>4</td><td>Event Description</td><td>Freeform.</td></tr>
<tr><td>5</td><td>Contact</td><td>Contact info for the requester/organizer (name, phone, etc.). <strong>Must have a matching 1A</strong>.</td></tr>
<tr><td>6</td><td>County</td><td>County the event takes place in.</td></tr>
<tr><td>7</td><td>Organization</td><td>Hosting organization.</td></tr>
<tr><td>8</td><td>Start Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>9</td><td>Start Time</td><td><code>HH:MM:SS</code>, in the event's time zone.</td></tr>
<tr><td>10</td><td>End Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>11</td><td>End Time</td><td><code>HH:MM:SS</code>, in the event's time zone.</td></tr>
<tr><td>12</td><td>Time Zone</td><td>EST, CST, MST, PST, etc. Default EST.</td></tr>
<tr><td>13</td><td>Location</td><td>e.g. the DC or state office.</td></tr>
<tr><td>14</td><td>Status</td><td>e.g. Pending, Approved, Tentative, Declined. <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
<tr><td>15</td><td>Private Flag</td><td>"Y" if marked private.</td></tr>
<tr><td>16</td><td>Scheduled Date</td><td>When entered into the schedule <code>YYYYMMDD</code>.</td></tr>
<tr><td>17</td><td>Scheduled by</td><td>Entering staffer's User ID. <strong>8A</strong> staff record.</td></tr>
<tr><td>18</td><td>Revision Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>19</td><td>Revised By</td><td>Last-reviser's User ID. <strong>8A</strong> staff record.</td></tr>
<tr><td>20–23</td><td>Address line 1–4</td><td>Event address lines.</td></tr>
<tr><td>24</td><td>City</td><td></td></tr>
<tr><td>25</td><td>State Code</td><td>2-letter.</td></tr>
<tr><td>26</td><td>Zip Code</td><td><code>XXXXX-XXXX</code> / <code>XXXXX</code> / country zip.</td></tr>
<tr><td>27</td><td>Country</td><td>If international.</td></tr>
</tbody>
</table>


### 7B — Event Code Data  *(multiple per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7B</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Matches the associated 7A.</td></tr>
<tr><td>3</td><td>Event Code</td><td>Subject/interest code. <strong>Must have a matching 8A</strong>.</td></tr>
</tbody>
</table>


### 7C — Event Participant Data  *(multiple per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7C</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Matches the associated 7A.</td></tr>
<tr><td>3</td><td>Participant Type</td><td>STAFF or PERSON — see <strong>Participant Type Values</strong>.</td></tr>
<tr><td>4</td><td>Participant ID</td><td>If STAFF: a User ID with a matching <strong>8A</strong> staff record. If PERSON: a Person ID with a matching <strong>1A</strong>.</td></tr>
</tbody>
</table>


### 7D — Event Attachments  *(multiple per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7D</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Matches the associated 7A.</td></tr>
<tr><td>3</td><td>Document Name</td><td>For files <strong>not</strong> in the library: path-qualified location.</td></tr>
<tr><td>4</td><td>Document ID</td><td>For files <strong>in</strong> the library: matches a 6A Document ID.</td></tr>
<tr><td>5</td><td>User ID</td><td>Staffer who attached it. <strong>8A</strong> staff record.</td></tr>
<tr><td>6</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Text</td><td>Comments/notes.</td></tr>
<tr><td>8</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 7E — Event Text (Comments or Notes)  *(multiple per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7E</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Matches the associated 7A.</td></tr>
<tr><td>3</td><td>7E Sequence Number</td><td>Orders 7E records; required if Date (5) and Time (6) are NULL.</td></tr>
<tr><td>4</td><td>Text</td><td>Freeform comments/notes.</td></tr>
<tr><td>5</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


### 7F — Event Associated Workflows  *(multiple per event)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7F</code></td></tr>
<tr><td>2</td><td>Event ID</td><td>Matches the associated 7A.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches a 3A Workflow ID.</td></tr>
</tbody>
</table>


### 7H — Recurring Series Definition Data  *(one per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7H</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Unique ID for the recurring series.</td></tr>
<tr><td>3</td><td>Start Series Date</td><td>First event date <code>YYYYMMDD</code>.</td></tr>
<tr><td>4</td><td>End Series Date</td><td>Last event date <code>YYYYMMDD</code> (NULL if no end date).</td></tr>
<tr><td>5</td><td>Recurrence Type</td><td>DAILY, WEEKLY, MONTHLY, or YEARLY.</td></tr>
<tr><td>6</td><td>Recurrence Interval</td><td>Per the <strong>Recurrence Interval Schema</strong> (see enumerations).</td></tr>
</tbody>
</table>


### 7I — Recurring Series Source Data  *(adjunct to 7H)*

Mirrors 7A's descriptive fields for a series. Fields 3, 8, 10 are **Not used**.

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7I</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td><em>(Not used)</em></td><td></td></tr>
<tr><td>4</td><td>Event Description</td><td>Freeform description of the series.</td></tr>
<tr><td>5</td><td>Contact</td><td>Requester/organizer contact info.</td></tr>
<tr><td>6</td><td>County</td><td></td></tr>
<tr><td>7</td><td>Organization</td><td></td></tr>
<tr><td>8</td><td><em>(Not used)</em></td><td></td></tr>
<tr><td>9</td><td>Start Time</td><td><code>HH:MM:SS</code>, series time zone.</td></tr>
<tr><td>10</td><td><em>(Not used)</em></td><td></td></tr>
<tr><td>11</td><td>End Time</td><td><code>HH:MM:SS</code>, series time zone.</td></tr>
<tr><td>12</td><td>Time Zone</td><td>EST, CST, MST, PST, etc. Default EST.</td></tr>
<tr><td>13</td><td>Location</td><td></td></tr>
<tr><td>14</td><td>Status</td><td>Pending, Approved, Tentative, Declined. <strong>Non-exhaustive — examples only, no closed list.</strong></td></tr>
<tr><td>15</td><td>Private Flag</td><td>"Y" if private.</td></tr>
<tr><td>16</td><td>Scheduled Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>17</td><td>Scheduled by</td><td>User ID. <strong>8A</strong> staff record.</td></tr>
<tr><td>18</td><td>Revision Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>19</td><td>Revised By</td><td>User ID. <strong>8A</strong> staff record.</td></tr>
<tr><td>20–23</td><td>Address line 1–4</td><td></td></tr>
<tr><td>24</td><td>City</td><td></td></tr>
<tr><td>25</td><td>State Code</td><td></td></tr>
<tr><td>26</td><td>Zip Code</td><td></td></tr>
<tr><td>27</td><td>Country</td><td></td></tr>
</tbody>
</table>


### 7J — Recurring Series Code Data  *(multiple per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7J</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td>Event Code</td><td>Subject/interest code. <strong>Must have a matching 8A</strong>.</td></tr>
</tbody>
</table>


### 7K — Recurring Series Participant Data  *(multiple per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7K</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td>Participant Type</td><td>STAFF or PERSON — see <strong>Participant Type Values</strong>.</td></tr>
<tr><td>4</td><td>Participant ID</td><td>If STAFF: User ID with a matching <strong>8A</strong> staff record. If PERSON: Person ID with a matching <strong>1A</strong>.</td></tr>
</tbody>
</table>


### 7L — Recurring Series Attachments  *(multiple per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7L</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td>Document Name</td><td>For files <strong>not</strong> in the library: path-qualified location.</td></tr>
<tr><td>4</td><td>Document ID</td><td>For files <strong>in</strong> the library: matches a 6A Document ID.</td></tr>
<tr><td>5</td><td>User ID</td><td>Staffer who attached it. <strong>8A</strong> staff record.</td></tr>
<tr><td>6</td><td>Attached Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>7</td><td>Text</td><td>Comments/notes.</td></tr>
<tr><td>8</td><td>File Name</td><td>User-readable file name.</td></tr>
</tbody>
</table>


### 7M — Recurring Series Text (Comments or Notes)  *(multiple per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7M</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td>7M Sequence Number</td><td>Orders 7M records; required if Date (5) and Time (6) are NULL.</td></tr>
<tr><td>4</td><td>Text</td><td>Freeform comments/notes.</td></tr>
<tr><td>5</td><td>Date</td><td><code>YYYYMMDD</code>.</td></tr>
<tr><td>6</td><td>Time</td><td><code>HH:MM:SS</code>.</td></tr>
<tr><td>7</td><td>User ID</td><td>Staffer who entered it. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>


### 7N — Recurring Series Associated Workflows  *(multiple per series)*

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>7N</code></td></tr>
<tr><td>2</td><td>Recurrence ID</td><td>Matches the associated 7H.</td></tr>
<tr><td>3</td><td>Workflow ID</td><td>Matches a 3A Workflow ID.</td></tr>
</tbody>
</table>


---

## Category 8 — Code Table Data

### 8A — Code Table Data  *(one per code/value)*

Defines every code (and staff User ID) referenced anywhere else in the format.
**This is the lookup hub.**

<table>
<thead>
<tr><th>#</th><th>Field</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Record Type</td><td><code>8A</code></td></tr>
<tr><td>2</td><td>Code Type</td><td>The kind of code — see <strong>Code Type Values</strong> (WORK, PERS, COM, EVENT, DOC, STAFF).</td></tr>
<tr><td>3</td><td>Code</td><td>The standard code used throughout the format (for STAFF, the staff User ID).</td></tr>
<tr><td>4</td><td>Code Description</td><td>Description/value of the code (for STAFF, the staffer's name). If absent in source data, the code itself is repeated here.</td></tr>
<tr><td>5</td><td>Inactive Flag</td><td>"Y" if the code is inactive (used before, not currently assignable).</td></tr>
<tr><td>6</td><td>User ID</td><td>Where applicable, the staffer associated with this code. <strong>8A</strong> staff record.</td></tr>
</tbody>
</table>



---


# SCDIF Enumerations — Fixed Value Sets

The value sets below are the documented codes for specific fields. Some sets are
**extensible** (the vendor may add values but must document them); these are
noted. See `additional-requirements.md` for the rules governing extensibility.

---

## Which value sets are closed vs. open

Not every "Values" list is a closed set. Treat fields in these three tiers
accordingly:

**Closed sets** — the documented values are the complete allowed set:
Person Type (1A.3), Document Type (2C.4), Code Type (8A.2 / 1C.3 / 6C.3),
Participant Type (7C.3 / 7K.3), Recurrence Type (7H.5).

**Open via an authoritative table** — the field draws from a "Values" table, but
the producing vendor may add values and **must document all of them** (so the
table for a given export is authoritative, but the format-level list is not
exhaustive): Address Type (1B.4), Phone/Email Type (1E.3), Workflow Type (3A.4,
3L.4), Communication Status (2A.9), Workflow Status (3A.11).

**Open with no table** — the definition only gives illustrative examples ("for
example … etc." / "e.g. …"); there is no governing list, so values may extend
beyond those shown. **Do not treat the examples as a closed set:**

<table>
<thead>
<tr><th>Record.Field</th><th>Field</th><th>Example values shown</th></tr>
</thead>
<tbody>
<tr><td>2A.6</td><td>Communication Type</td><td>LETTER, EMAIL, PHONE, NEWSLETTER, POST CARD, VISIT, DMAIL, NONE</td></tr>
<tr><td>2A.14</td><td>Response Type</td><td>LETTER, EMAIL</td></tr>
<tr><td>2B.5</td><td>Position</td><td>PRO, CON, NEUTRAL, NONE</td></tr>
<tr><td>6A.15</td><td>Status (Document Library)</td><td>Draft, Approved</td></tr>
<tr><td>7A.14</td><td>Status (Event)</td><td>Pending, Approved, Tentative, Declined</td></tr>
<tr><td>7I.14</td><td>Status (Recurring Series)</td><td>Pending, Approved, Tentative, Declined</td></tr>
</tbody>
</table>


Separately, the **code** fields (1C.4, 2B.4 Communication Code, 3B.4 Workflow
Code, 6C.4, 7B.3 / 7J.3 Event Code) hold office-defined codes whose full domain
lives in the `8A` code table — inherently open, resolved per export via `8A`.

---

## Person Type Values  *(1A field 3)*

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>AG</td><td>Agency</td></tr>
<tr><td>CS</td><td>Constituent</td></tr>
<tr><td>MC</td><td>Member of Congress</td></tr>
<tr><td>OR</td><td>Organization</td></tr>
<tr><td>PRESS</td><td>Press</td></tr>
<tr><td>USER</td><td>Internal Staff</td></tr>
</tbody>
</table>


## Address Type Values  *(1B field 4)* — *extensible*

Additional address types may be added as needed, but the vendor must document all
non-standard types.

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>BU</td><td>Business</td></tr>
<tr><td>HO</td><td>Home</td></tr>
<tr><td>IN</td><td>International/Foreign</td></tr>
</tbody>
</table>


## Person Code Type Values  *(1C field 3)*

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>PERS</td><td>Code describing the person (e.g. DOCTOR, MAYOR, VIP, POI).</td></tr>
<tr><td>WORK</td><td>For agency records, code describing the agency/workflow (e.g. SSA).</td></tr>
</tbody>
</table>


## Person Phone or Email Type Values  *(1E field 3)* — *extensible*

Additional types may be added as needed, but the vendor must document all
non-standard types used.

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>CELL</td><td>Cell phone</td></tr>
<tr><td>EMAIL</td><td>Email address</td></tr>
<tr><td>FAX</td><td>Fax number</td></tr>
<tr><td>HOME</td><td>Home phone number</td></tr>
<tr><td>PAGER</td><td>Pager number</td></tr>
<tr><td>PHONE</td><td>Phone number, type undetermined</td></tr>
<tr><td>URL</td><td>Web page address</td></tr>
<tr><td>WORK</td><td>Work/business phone number</td></tr>
</tbody>
</table>


---

## Document Type Values  *(2C field 4)*

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>INCOMING</td><td>Incoming document (incoming communication from the person).</td></tr>
<tr><td>OUTGOING</td><td>Outgoing document (outgoing communication to the person).</td></tr>
<tr><td>AT_INn</td><td>Numbered attachment to the <strong>incoming</strong> communication; <em>n</em> = sequence order (AT_IN1, AT_IN2, …).</td></tr>
<tr><td>AT_OUTn</td><td>Numbered attachment to the <strong>outgoing</strong> communication; <em>n</em> = sequence order (AT_OUT1, AT_OUT2, …).</td></tr>
</tbody>
</table>


---

## Workflow Type Values  *(3A field 4)* — *extensible*

Additional workflow types should be added as needed; all additions must be
documented by the vendor. Documented examples include:

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>CASE</td><td>Casework</td></tr>
<tr><td>Outreach</td><td>Outreach</td></tr>
<tr><td>Academy Nomination</td><td>Academy nomination</td></tr>
<tr><td>Flag Request</td><td>Flag request</td></tr>
<tr><td>Tour Request</td><td>Tour request</td></tr>
<tr><td>Approps General</td><td>General appropriations</td></tr>
<tr><td>State Assistance</td><td>State assistance</td></tr>
</tbody>
</table>


(Workflow types are office-defined and carry type-specific extra fields via `3L`
— see `additional-requirements.md`.)

---

## Code Type Values  *(8A field 2; also used by 1C, 6C)*

The "Record Location" column shows which record types a code of that type appears
in. Every such code must be defined by an `8A` record of the matching type.

<table>
<thead>
<tr><th>Value</th><th>Record Location(s)</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>WORK</td><td>1C, 3B, 6C</td><td>Workflow codes</td></tr>
<tr><td>PERS</td><td>1C</td><td>Person codes</td></tr>
<tr><td>COM</td><td>2B, 6C</td><td>Communication subject codes</td></tr>
<tr><td>EVENT</td><td>7B</td><td>Event codes</td></tr>
<tr><td>DOC</td><td>6C</td><td>Document codes</td></tr>
<tr><td>STAFF</td><td>1D, 1F, 2A, 2D, 3A, 3D, 3F, 5C, 5D, 6A, 6D, 6E, 7A, 7C, 7D, 7E</td><td>Staff user IDs</td></tr>
</tbody>
</table>


> **Key consequence:** every "User ID" field anywhere in the format is a **STAFF**
> code that must have a matching `8A` record (field 3 = the user ID, field 4 = the
> staffer's name).

> **Note:** real exports may include additional code types beyond this documented
> set (the `8A` Code Type column and the code-type fields in `1C`/`6C` are not
> guaranteed to be limited to the six values above). Treat the producer's `8A`
> table as the authoritative list of code types for a given export.

---

## Participant Type Values  *(7C field 3; 7K field 3)*

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>STAFF</td><td>A Member or staffer participating (Participant ID is a User ID → 8A).</td></tr>
<tr><td>PERSON</td><td>A person participating (Participant ID is a Person ID → 1A).</td></tr>
</tbody>
</table>


---

## Communication Status Values  *(2A field 9)*

The **value stored must be the value displayed** to the user. The **Closed Flag**
indicates whether this status means the office has finished/completed work on the
communication ("Y" = work complete; NULL = work not complete). All possible
status values must be documented by the producing vendor. Sample set:

<table>
<thead>
<tr><th>Status Value</th><th>Translation</th><th>Closed Flag</th></tr>
</thead>
<tbody>
<tr><td>P</td><td>Pending</td><td></td></tr>
<tr><td>RA</td><td>Request Approval</td><td></td></tr>
<tr><td>C</td><td>Closed</td><td>Y</td></tr>
<tr><td>H</td><td>Hold</td><td></td></tr>
</tbody>
</table>


## Workflow Status Values  *(3A field 11)*

Same conventions as above (stored = displayed; Closed Flag = work complete).
Status values are office/workflow-specific; all must be documented. Sample set:

<table>
<thead>
<tr><th>Status Value</th><th>Translation</th><th>Closed Flag</th></tr>
</thead>
<tbody>
<tr><td>INCOMPLETE</td><td>Incomplete</td><td>Y</td></tr>
<tr><td>NO NOM</td><td>No Nomination</td><td>Y</td></tr>
<tr><td>NOM BY ANOTHER</td><td>Nominated by Another Source</td><td>Y</td></tr>
<tr><td>BC NOM</td><td>BC Nomination</td><td>Y</td></tr>
<tr><td>WITHDREW</td><td>Withdrew</td><td>Y</td></tr>
<tr><td>CLOSED</td><td>Closed</td><td></td></tr>
<tr><td>OPEN</td><td>Open</td><td>Y</td></tr>
<tr><td>CL.UNFAV</td><td>Closed Unfavorably</td><td>Y</td></tr>
<tr><td>CL.FAV</td><td>Closed Favorably</td><td>Y</td></tr>
<tr><td>PG.CL</td><td>Closed</td><td>Y</td></tr>
<tr><td>PG.AB</td><td>Abandoned</td><td>Y</td></tr>
<tr><td>PG.OP</td><td>Open</td><td></td></tr>
<tr><td>PG.PR</td><td>Proposed</td><td></td></tr>
<tr><td>CL.REJECT</td><td>Rejected – do not process</td><td>Y</td></tr>
<tr><td>CL.APPROVED</td><td>Approved – Entered into ROSS</td><td>Y</td></tr>
</tbody>
</table>


> Note: the Closed Flag is independent of whether the label sounds "closed." It
> reflects the office's documented intent for that status. Treat the producer's
> documented table as authoritative.

---

## Recurrence Interval Schema  *(7H field 6, interpreted with 7H field 5 Recurrence Type)*

The Recurrence Interval is a dash-delimited string whose grammar depends on the
Recurrence Type:

<table>
<thead>
<tr><th>Recurrence Type</th><th>Parts</th><th>Definition</th></tr>
</thead>
<tbody>
<tr><td><strong>DAILY</strong></td><td>one value</td><td>Daily frequency interval. Valid: <code>1</code>, <code>2</code>, … , <code>weekdays</code>, <code>weekenddays</code>.</td></tr>
<tr><td><strong>WEEKLY</strong></td><td>two values, dash-separated</td><td>Part 1 = weekly frequency (<code>1</code>, <code>2</code>, …). Part 2 = day of week (<code>sunday</code>…<code>saturday</code>).</td></tr>
<tr><td><strong>MONTHLY</strong></td><td>three values, dash-separated</td><td>Part 1 = monthly frequency. Part 2 = day descriptor (<code>1</code>…<code>31</code>, <code>last</code>). Part 3 = type of day (<code>sunday</code>…<code>saturday</code>, <code>day</code>, <code>weekday</code>, <code>weekendday</code>).</td></tr>
<tr><td><strong>YEARLY</strong></td><td>four values, dash-separated</td><td>Parts 1–3 as MONTHLY. Part 4 = month (<code>january</code>…<code>december</code>).</td></tr>
</tbody>
</table>


### Sample recurrence interval values

<table>
<thead>
<tr><th>Value</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td><code>1</code></td><td>Every day (DAILY).</td></tr>
<tr><td><code>4</code></td><td>Every 4th day (DAILY).</td></tr>
<tr><td><code>weekdays</code></td><td>Every weekday (DAILY).</td></tr>
<tr><td><code>weekenddays</code></td><td>Every weekend day (DAILY).</td></tr>
<tr><td><code>1-sunday</code></td><td>Every week on Sunday (WEEKLY).</td></tr>
<tr><td><code>2-monday</code></td><td>Every 2nd week on Monday (WEEKLY).</td></tr>
<tr><td><code>1-1-day</code></td><td>Every month on the 1st day (MONTHLY).</td></tr>
<tr><td><code>3-15-day</code></td><td>Every 3rd month on the 15th (MONTHLY).</td></tr>
<tr><td><code>2-last-day</code></td><td>Every 2nd month on the last day (MONTHLY).</td></tr>
<tr><td><code>4-1-weekday</code></td><td>Every 4th month on the first weekday (MONTHLY).</td></tr>
<tr><td><code>3-1-weekendday</code></td><td>Every 3rd month on the first weekend day (MONTHLY).</td></tr>
<tr><td><code>1-1-tuesday</code></td><td>Every month on the 1st Tuesday (MONTHLY).</td></tr>
<tr><td><code>4-3-sunday</code></td><td>Every 4th month on the 3rd Sunday (MONTHLY).</td></tr>
<tr><td><code>1-9-day-may</code></td><td>Every year on the 9th of May (YEARLY).</td></tr>
<tr><td><code>1-5-weekday-june</code></td><td>Every year on the 5th weekday of June (YEARLY).</td></tr>
<tr><td><code>1-last-day-january</code></td><td>Every year on the last day of January (YEARLY).</td></tr>
<tr><td><code>2-1-tuesday-november</code></td><td>Every 2nd year on the 1st Tuesday of November (YEARLY).</td></tr>
<tr><td><code>1-2-weekendday-april</code></td><td>Every year on the 2nd weekend day of April (YEARLY).</td></tr>
</tbody>
</table>


---

## A note on the large "interest" value lists

Some office-defined workflow fields (e.g. the `Outreach` workflow's
`interest1`…`interest6` fields, transmitted via `3L`) draw from a long pipe-
delimited list of interest categories (African American, Agriculture, Asian,
Automotive, Business – *many subcategories*, Chamber of Commerce, Conservative,
Crime, Education, Energy, Environment, Financial Services, Foreign Affairs,
Health – *many subcategories*, Housing, Humanitarian, Immigration, Military,
Minority Leaders, Religious, Seniors, Sportsman, Technology, Tourism,
Transportation, Young Professional, and so on). These lists are **office-specific
and documented per office** in the additional-workflow-data tables, not part of
the universal format. See `additional-requirements.md`.



---


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



---


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



---


# SCDIF Additional Requirements (Cross-Cutting Rules)

These are the universal rules from the closing section of Attachment J-10. They
govern how fields are formatted, how the format may be extended, and how
workflow-type-specific data is carried.

## Date and Time formats

- **All dates** are `YYYYMMDD` (e.g. 2016-11-01 → `20161101`).
- **All times** are `HH:MM:SS`, 24-hour (e.g. 2:07:23 PM → `14:07:23`;
  2:20 PM → `14:20:00`).

## Documents / Attachments

- All documents/files associated with the CSS are copied and provided alongside
  the data. **All directory structures (including virtual directories) are
  maintained.** Files include correct extensions that accurately reflect format.
- Word-processing documents (responses, form letters, library docs) are provided
  so all formatting is preserved when opened in Word.
- Incoming email message files are provided in native format (e.g. `.txt`,
  `.eml`); other files in their native format (e.g. `.xls`, `.tif`, `.pdf`),
  provided they are native to Windows-based standard supported software.
- Document/attachment fields hold **relative file paths** (e.g.
  `..\documents\formletters\175959.doc`). A file is either in the **document
  library** (referenced by a `6A` Document ID) or a standalone file (referenced
  by a path-qualified Document Name) — not both.

### Attachment paths are often wrong in consistent, repeatable ways

In practice the path strings stored in attachment fields frequently do **not**
match the delivered folder layout exactly. The errors tend to be **systematic**
rather than random — the same defect repeats across many records. Common patterns:

- a spurious or missing intermediate directory segment (e.g. every form-letter
  path contains an extra `\BlobExport\` that does not exist on disk — removing
  that one segment makes all of the paths resolve);
- a folder-name typo or mismatch between the path string and the actual directory
  (e.g. `formletter_ima` in the data vs. `fomletter_ima` on disk);
- the same logical file referenced via different paths in different record types
  (e.g. a library document written one way in `6A`/`6D` and another in `2C`);
- mixed path conventions (forward vs. back slashes, absolute vs. relative roots).

Because these defects are consistent and repeatable, they are usually fixable with
a single rule (a find/replace, a path-prefix rewrite, a folder remap). **An import
tool should not trust attachment paths literally.** It should validate each path
against the delivered files, **surface the unresolved paths to the user grouped by
their common pattern**, and offer a way to apply a bulk correction (e.g. preview
the affected records, accept a suggested rewrite, then re-validate) so the whole
class of errors can be fixed in one step during import rather than file by file.

## Type Codes / Values — extensibility

New type codes/values may be added **without prior approval only** in the
specifically marked extensible areas:

- `1B` Address Type Values,
- `1E` Person Phone/Email Type Values,
- `3A` Workflow Type Values.

All additions must be **fully documented** and must be **consistent with the
field's definition** — e.g. it's fine to add address type `SU` (summer home), but
not to smuggle a constituent's gender through an address-type field.

## "Text" (Comments or Notes) fields

Text fields (`1D, 2D, 3D, 5D, 6E, 7E, 7M`, etc.) are for **freeform comments/notes
only** and must not be repurposed to transmit other structured data. (Exception:
if a legacy system had previously stored other data in a text field, that data may
remain there.)

## Custom / User-defined Fields

Custom/user-defined fields are fields unique to a particular office's CSS install,
not part of the standard configuration. They are added to the format, documented,
and submitted for approval ahead of a conversion.

**Important rule:** if a field is "custom" from the application's perspective but
an equivalent field **already exists** in SCDIF, the data is transmitted through
the existing standard field rather than as a custom field. (Example: if "spouse's
name" is a custom field in the application, it is still provided in `1A` field 15,
not as a custom field.)

## 3L — Additional Workflow Data

`3L` carries CSS field data tied to **particular workflow types** (not all). Two
sources:

1. **Out-of-the-box workflow types** — fields that are part of the CSS's standard
   templates. Documented and provided for approval after contract award.
2. **Custom/user-defined workflow types** — templates and/or fields that are
   themselves office-defined. Documented and provided ahead of the conversion.

Fields applicable to **all** workflow types are provided in the standard 3-series
records (`3A`–`3F`). The `3L` documentation provides, per field: field name,
description, **data type**, possible values (if any), and the **workflow type code**
the field belongs to.

### Documented 3L field sets (examples)

These illustrate how `3L` field sets look; the exact sets are office-specific.

**Workflow type = `Boy Scout`** (all String unless noted):

<table>
<thead>
<tr><th>Field Name</th><th>Description</th><th>Possible Values</th></tr>
</thead>
<tbody>
<tr><td>ceraddr</td><td>Ceremony Address</td><td></td></tr>
<tr><td>ID #</td><td>ID #</td><td></td></tr>
<tr><td>OpenStatus</td><td>Active / Pending?</td><td>Active | Pending</td></tr>
<tr><td>Region</td><td>Region</td><td>DC | Memphis | Jackson - West Tennessee | Nashville - Middle Tennessee | Chattanooga - Southeast Tennessee | Knoxville - East Tennessee | Tri-Cities - Upper East Tennessee</td></tr>
<tr><td>SS #</td><td>SS #</td><td></td></tr>
<tr><td>trplead</td><td>Troop Leader</td><td></td></tr>
<tr><td>trpnum</td><td>Troop #</td><td></td></tr>
</tbody>
</table>


**Workflow type = `Case`** (all String):

<table>
<thead>
<tr><th>Field Name</th><th>Description</th><th>Possible Values</th></tr>
</thead>
<tbody>
<tr><td>govern</td><td>From Governor's Office?</td><td>Yes | No</td></tr>
<tr><td>ID #</td><td>ID #</td><td></td></tr>
<tr><td>OpenStatus</td><td>Active / Pending?</td><td>Active | Pending</td></tr>
<tr><td>Region</td><td>Region</td><td>DC | Memphis | Jackson - West Tennessee | Nashville - Middle Tennessee | Chattanooga - Southeast Tennessee | Knoxville - East Tennessee | Tri-Cities - Upper East Tennessee</td></tr>
<tr><td>SS #</td><td>SS #</td><td></td></tr>
</tbody>
</table>


**Workflow type = `Outreach`** (selected; all String unless noted):

<table>
<thead>
<tr><th>Field Name</th><th>Description</th><th>Notes</th></tr>
</thead>
<tbody>
<tr><td>allmeet</td><td>All Meeting Dates</td><td></td></tr>
<tr><td>asstemail</td><td>Assistant's Email Address</td><td></td></tr>
<tr><td>asstname</td><td>Assistant's Name</td><td></td></tr>
<tr><td>asstphone</td><td>Assistant's Phone Number</td><td></td></tr>
<tr><td>interest1 … interest6</td><td>Contact's Interest 1–6</td><td>Each drawn from a long pipe-delimited interest-category list (see <code>enumerations.md</code>).</td></tr>
<tr><td>lastmeet</td><td>Last Meeting Date</td><td>Date</td></tr>
<tr><td>notes</td><td>Notes</td><td></td></tr>
<tr><td>offcont</td><td>Office Contact</td><td></td></tr>
<tr><td>Region</td><td>Region</td><td>Chattanooga | Jackson | Knoxville | Memphis | Middle Tennessee | Nashville | Tri-Cities | DC</td></tr>
</tbody>
</table>


> The full `interest` value list (~100+ categories such as Agriculture,
> Business – *subcategories*, Conservative – *subcategories*, Education –
> *subcategories*, Health – *subcategories*, Military – *subcategories*,
> Transportation – *subcategories*, etc.) is documented per office. It is provided
> as a single pipe-delimited enumeration shared by interest1–interest6.

## 8A — Code Table Data handling

- For **exit conversions** (CSS-to-CSS), the vendor provides an advance copy of
  the `8A` data to the receiving vendor ~2 weeks before the conversion so code
  data can be reconciled. (Not required for SCDIF archiving conversions.)
- The outgoing vendor provides **all** `8A` data as part of the standard
  conversion data.

## SCDIF Archiving Conversion customizations

Archiving conversions are customizable: Member offices may **include or exclude**
some or all **category 3 (workflow)** data and **all of category 7 (schedule)**
data. For offices including only some workflow data, the office specifies which
**workflow types** to include or exclude (e.g. include all except `CASE` and
`INTERN`).

## Changes to the Format

Revisions may be necessary as CSS functionality changes. New/updated fields are
documented within the format, submitted for approval, and provided to the
receiving vendor ahead of the conversion. Documentation for each added field
includes: field number (n/a for `3L`), field name, a description expanding on the
name, a custom/user-defined notation (as applicable), data type (date, time,
number, text), all predefined values (as applicable), and — for workflow data —
the workflow type code the field is used with.



---


# SCDIF Serialization (Conceptual Note)

This is a **logical-level** description of how SCDIF records are laid out as text,
so you can correctly interpret a raw line if you ever see one. It is **not** a
parsing tutorial and does **not** describe any particular export's file set.

## How records are laid out

- **One record = one line.** Each record is a variable-length ASCII line
  terminated by **CRLF** (carriage return + line feed). One record per line.
- **Fields are TAB-separated.** Within a record, fields are delimited by **TAB**
  characters, in the order documented in `record-types.md` (field 1, 2, 3, …).
- **The first field is always the 2-byte Record Type** (`1A`, `3L`, `7H`, …),
  which tells you which record layout applies to the rest of the line.
- **Skip stray lines.** Real exports may contain blank lines or other non-record
  lines (e.g. separator lines) between records. A reader should **skip any line
  whose first field is not a valid 2-byte record type** rather than treating it as
  data.
- **Field count via trailing TABs (with a caveat).** The spec requires records to
  be padded with extra trailing TABs so that every record of a type has the same
  number of fields. **In practice, real exports often trim trailing empty fields**,
  so records of the same type may vary in width. Therefore: do **not** rely on a
  fixed field count — read fields by position, and treat any missing trailing
  fields as NULL / not provided.

## Reserved characters and how data is escaped

- A field value never contains a raw **TAB** or **CRLF** (the producer guarantees
  this).
- Any CRLF (line break) that was part of the original field data — e.g. inside a
  freeform note — is replaced with a **PIPE (`|`)**. So in Text fields
  (`1D, 2D, 3D, 5D, 6E, 7E, 7M`), a `|` represents an original newline.

## Empty vs. NULL

- An **empty field** (nothing between two TABs) represents **NULL / "not
  provided"**. This is how all the "NULL if…" conditions in the field tables and
  in `relationships.md` are expressed on the wire.

## Size limit

- Fields may be any length, but **no record may exceed 32K**.

## Attachments are external

- Document/attachment fields hold a **relative file path** (e.g.
  `..\documents\formletters\175959.doc`); the actual files travel alongside the
  data with their directory structure (including virtual directories) and correct
  file extensions preserved. See `additional-requirements.md`.

## What this note deliberately omits

- The names of the `.dat` (or other) files in any specific export, and which
  record types appear in which file.
- How records of different types are grouped or ordered across files.
- Any step-by-step "how to split/parse a line" procedure or code.
