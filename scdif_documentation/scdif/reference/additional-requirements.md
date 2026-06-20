<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

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
