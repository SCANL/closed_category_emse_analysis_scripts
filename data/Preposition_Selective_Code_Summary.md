# Selective Coding Summary by Axial Code (All Preposition Categories, Sorted by Frequency)

# Core Selective Coding Insight: Prepositions in Identifier Names

Prepositions in software identifiers are not merely syntactic residue—they serve critical, functional roles in expressing relationships across values, behaviors, and execution flows.

Across the dataset, prepositions consistently reflect **three dominant semantic functions**:

1. **Data Shaping (Movement and Transformation)**  
   Prepositions signal how data moves between formats, contexts, or positions.  
   Includes categories like Type Casting / Interpretation, Data Source / Origin, Data Movement / Transfer, and Deferred Processing.  
     
2. **Execution Control (Timing and Activation)**  
   Prepositions govern when or whether execution occurs, often by binding behavior to conditions, triggers, or configuration flags.  
   Includes Boolean Flow / Control Flag, Event Callback / Trigger, and Deferred Processing.  
     
3. **Contextual Association (Meaning and Scope)**  
   Prepositions encode how data relates to behaviors, roles, operations, or configuration scopes.  
   Includes Purpose / Role Annotation, Group Membership, Operation Basis, and Configuration / Grouping Context.

Additionally, the **relational nature** of prepositions is essential. Even when not expressing literal movement or containment, prepositions construct **semantic links**—between values and the conditions, transformations, or configurations that define their role in the system.

This highlights the **relational modeling power of prepositions in code**: they embed logic not just about *what something is*, but *how it participates* in a larger software structure.

## Type Casting / Interpretation (42 items)
**Function:** Reframe, reinterpret, or transform a value from one representation to another (e.g., `as_type`, `to_element`)  
**Prepositions:** `as`, `to`, `around`  
**Behavioral Role:** Declares conversion, reinterpretation, or semantic wrapping  
**Use Cases:** Casting helpers, type adapters, conversion utilities

## Position / Ordering in Time or Space (28 items)
**Function:** Specify relative position in time, data structure, or execution sequence (e.g., `at_index`, `before`, `after_processing`)  
**Prepositions:** `at`, `before`, `after`, `in`  
**Behavioral Role:** Positioning or boundary-setting  
**Use Cases:** Loop control, memory layout, step sequencing

## Boolean Flow / Control Flag (20 items)
**Function:** Signal whether a behavior is enabled, active, or suppressed based on a condition or context (e.g., `pass_through`, `for_backprop`, `in_best_path`)  
**Prepositions:** `for`, `in`, `by`, `over`, `through`  
**Behavioral Role:** Flag-based conditional behavior  
**Use Cases:** Config flags, toggles, runtime control

## Data Source / Origin (18 items)
**Function:** Indicate where a value was derived or extracted from (e.g., `from_header`, `from_iterator`, `version_bitmap_from_version`)  
**Prepositions:** `from` (dominant)  
**Behavioral Role:** Signals provenance or transformation input  
**Use Cases:** Mapping, I/O, derived fields, tracing origins

## Event Callback / Trigger (17 items)
**Function:** Attach behavior to a specific event or condition (e.g., `on_status`, `on_start`, `commit_on_success`)  
**Prepositions:** `on` (dominant)  
**Behavioral Role:** Event-triggered execution or registration  
**Use Cases:** UI callbacks, lifecycle hooks, network handlers

## Deferred Processing / Pending Action (12 items)
**Function:** Names items that have yet to be processed, serving as a placeholder for future transformation (e.g., `to_merge`, `to_clean`)  
**Prepositions:** `to`  
**Behavioral Role:** Scheduling or deferred intent  
**Use Cases:** Queues, pipelines, post-processing stages

## Purpose / Role Annotation (10 items)
**Function:** Explains the intended role or purpose of a value (e.g., `used_for_logging`, `reserved_for_system`)  
**Prepositions:** `for`  
**Behavioral Role:** Intent declaration  
**Use Cases:** Roles, access control, testing markers

## Data Movement / Transfer (8 items)
**Function:** Indicates that data or control flow is being directed or moved between components (e.g., `send_to_buffer`, `forward_to_queue`)  
**Prepositions:** `to`, `into`, `onto`  
**Behavioral Role:** Specifies the direction or endpoint of movement  
**Use Cases:** Buffering, data streaming, message passing, forwarding

## Configuration / Grouping Context (8 items)
**Function:** Define that a value or behavior is associated with a particular configuration, grouping, or context (e.g., `with_cache`, `with_operator`)  
**Prepositions:** `with`  
**Behavioral Role:** Composition and association  
**Use Cases:** Plugin systems, configuration flags, wrapper functions

## Operation Basis / Strategy (5 items)
**Function:** Communicates how an operation should be carried out, based on the strategy or parameter specified (e.g., `sort_by_key`, `filter_by_name`)  
**Prepositions:** `by`  
**Behavioral Role:** Strategy and method selection  
**Use Cases:** Sorting, routing, keying, delegation

## Unit-Based Decomposition / Measurement (2 items)
**Function:** Describes values expressed in terms of smaller units or rates (e.g., `per_user`, `per_frame`, `cost_per_unit`)  
**Prepositions:** `per`  
**Behavioral Role:** Quantifies, normalizes, or distributes across instances  
**Use Cases:** Rate-limited behaviors, resource allocation, aggregation logic

## Mathematical / Constraint Context (2 items)
**Function:** Use of preposition to express constraint or domain (e.g., `over_limit`, `over_range`)  
**Prepositions:** `over`  
**Behavioral Role:** Constraint framing or condition bounding  
**Use Cases:** Range checks, numeric domains, performance limits

## Other / Miscellaneous (1 items)
**Function:** Identifier does not clearly fit other categories or is too ambiguous for a confident assignment.  
**Prepositions:** Varies  
**Behavioral Role:** Unclear or inconsistent  
**Use Cases:** Outliers, unclear code intent

## Membership / Peer Grouping (1 items)
**Function:** Signals inclusion in a peer group or a set (e.g., `among_candidates`)  
**Prepositions:** `among`  
**Behavioral Role:** Collective referencing  
**Use Cases:** Voting sets, comparisons, related elements  
