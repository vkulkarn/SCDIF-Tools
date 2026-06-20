<!--
SCDIF Toolkit — Copyright (c) 2026 Vikram Kulkarni
SPDX-License-Identifier: MIT
Licensed under the MIT License. See LICENSE.txt in the project root.
-->

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
