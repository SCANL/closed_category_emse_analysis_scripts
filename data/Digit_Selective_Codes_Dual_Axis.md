# Selective Coding Summary for Digits (Dual-Axis)

## Core Selective Coding Insight: Digits in Identifier Names

- Digit-based identifiers often serve as compact signals for indexing, versioning, and alternative roles. They encode both semantic roles (e.g., distinguishing elements, encoding versions, or substituting for words) and sources of meaning (e.g., human conventions, auto-generation, or domain standards). The dual-axis structure reflects this interplay:

- Semantic Role (what the digit does in context)

- Source of Meaning (how or why the digit was chosen)

Together, these dimensions explain how digits communicate structure, position, or purpose—even in the smallest syntactic units. By combining these two axes, we can surface patterns like system-specific layout markers, manual disambiguation via suffixes, and semantically significant version indicators.
---

### Distinguisher x Human-Named Convention (122 items)
**Function:** Differentiate entities with manually assigned numeric suffixes.  
**Digits:** `1`, `2`, `3` (manually indexed)
**Example:** `arg1`, `col2`, `tile3`  
**Behavioral Role:** Developer-assigned structure for disambiguating similar items.  
**Use Cases:** Function parameters, field disambiguation, ordered grouping (`APPLICATION_INFO2`, `GenerateProlog1`, `SET_GROUP_NAME_1`)

### Distinguisher x Locally Specific Concept (45 items)
**Function:** Encode positions or roles tied to system-specific logic.  
**Digits:** `3`, `4`, `0` (meaning varies by system)
**Example:** `tile3`, `m34` (row 3, col 4 of a matrix)
**Behavioral Role:** Reference internal concepts like layout rows or node positions.  
**Use Cases:** Matrix traversal, AST node identification, paired roles (`BLOCK_CONTACT_16x16`, `BypassComparison_8192x8192`, `CMatrix33`)

### Distinguisher x Technology Term / Standard (17 items)
**Function:** Embed numeric components of standardized names or terms.  
**Digits:** `2`, `437`, `64` (fixed values from standards)
**Example:** `cp437`, `http2`  
**Behavioral Role:** Define precise domain-specific behavior or formatting.  
**Use Cases:** Protocol names, encoding formats, technology identifiers (`B1110`, `BaseLevel1`, `BaseLevel3`)

### Distinguisher x Auto-Generated (8 items)
**Function:** Automatically increment digits to avoid naming collisions.  
**Digits:** `1`, `2`, `3` (auto-generated)
**Example:** `jButton3`, `FOLLOW_1_2`  
**Behavioral Role:** Ensure uniqueness in code generation or tooling output.  
**Use Cases:** UI components, compiler-generated labels, testing artifacts (`_field37`, `_field4`, `_field63`)

### Version Identifier x Technology Term / Standard (9 items)
**Function:** Specify version as part of a structured identifier.  
**Digits:** `1`, `2`, `3` (indicating version)
**Example:** `http2`, `v1`  
**Behavioral Role:** Convey backward compatibility or semantic versioning.  
**Use Cases:** API versions, file formats, compatibility flags (`MurmurHash3`, `YOLO2`, `gw6`)
