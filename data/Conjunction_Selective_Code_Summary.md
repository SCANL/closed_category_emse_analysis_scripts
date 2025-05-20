# Selective Coding Summary by Axial Code (Conjunctions)

## Core Selective Coding Insight: Conjunctions in Identifier Names

Conjunction-based identifiers are rare but expressive. They signal **compound structures**, **guarded logic**, or **dual-purpose semantics** in a way that other closed-class terms do not.

These identifiers are particularly useful when modeling:
- **Duality** — representing more than one entity or mode simultaneously (`key_or_iv`, `input_and_output`)
- **Mutual exclusion** — expressing a singular selection between alternatives (`stream_or_cache`)
- **Precondition or guard semantics** — embedding logical gates directly into names (`load_if_needed`, `trigger_if_active`)

Their rarity suggests that developers typically resolve such complexity in code structure rather than naming. However, when used deliberately, conjunctions **make invisible relationships visible**—particularly in APIs, toggles, or test logic where multiple states or pathways must be understood at a glance.

While some usages may be incidental or stylistic, others clearly reflect a **desire to foreground the behavior**—making control flow or dual capability explicit at the naming level.

---

### Data Pair / Composite Value (7 items)
**Function:** Combines two values into a single name, representing a **composite or paired structure**  
**Conjunction Role:** Joins two related values or options (`key_or_iv`, `data_or_diff`)
**Use Cases:** Flexible APIs, compound returns, fallback formats  

### Guarded Action / Conditional Enablement (6 items)
**Function:** Indicates that a behavior or function is **only enabled or triggered under a specific condition**  
**Conjunction Role:** Signals a **precondition** or **logical gate** for execution  
**Use Cases:** Lazy loading, permission checks, guarded execution paths (`load_if_needed`, `activate_if_enabled`)

### Combined Action / Sequential Behavior (3 items)
**Function:** Represents a sequence of actions or behaviors that are combined in execution or intent  
**Conjunction Role:** Suggests a procedural or functional chain (`initialize_and_run`, `start_and_stop`)
**Use Cases:** Lifecycle methods, utility functions, test orchestration  

### Boolean Concept Name (1 item)
**Function:** Encodes a **boolean flag** or variable representing a compound logic concept  
**Conjunction Role:** Describes logical combination in flag semantics (`stream_or_cache`)
**Use Cases:** Mode toggles, configuration fields  

### Combined Configuration / UI Concept (1 item)
**Function:** Suggests that a configuration or interface setting represents a **joint behavior or multiple conceptual states**  
**Conjunction Role:** Declares combined semantics (`input_and_output_type`)
**Use Cases:** Mode switching, UI behavior settings  

### Boolean Multi-Condition Test (1 item)
**Function:** Signals that a boolean reflects the result of **multiple conditions tested together**  
**Conjunction Role:** Expresses a **logical combination** (`both_are_ready`)
**Use Cases:** Eligibility checks, boolean utilities  

### Shared Interface for Alternatives (1 item)
**Function:** Describes a variable or function that operates on **one of several interchangeable types or roles**  
**Conjunction Role:** Models mutually exclusive but related types (`generate_key_or_iv`)
**Use Cases:** Shared interfaces, type-switching logic, fallback behavior  
