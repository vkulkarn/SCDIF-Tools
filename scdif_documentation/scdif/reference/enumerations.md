<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

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
