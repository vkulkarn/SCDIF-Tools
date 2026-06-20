<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

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

