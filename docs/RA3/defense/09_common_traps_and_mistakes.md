# Common Traps and Mistakes: Error Prevention Guide
## RA3 Defense Preparation

**Purpose**: Learn what NOT to do during defense by studying common mistakes
**How to Use**: Review before each practice session and before defense
**Target Audience**: Team members preparing for oral examination

---

## Overview

This guide catalogs the **8 most common mistake categories** students make during RA3 defense, with:
- Real examples from practice sessions
- Why the mistake happens
- How to recognize you're making it
- How to correct it in real-time
- Prevention strategies

---

## Table of Contents

1. [Operator Confusion](#trap-1-operator-confusion)
2. [Type Promotion Errors](#trap-2-type-promotion-errors)
3. [IFELSE Branch Compatibility](#trap-3-ifelse-branch-compatibility)
4. [Forgetting Initialization Checks](#trap-4-forgetting-initialization-checks)
5. [RES Reference Calculation](#trap-5-res-reference-calculation)
6. [Notation and Formalism](#trap-6-notation-and-formalism)
7. [Premature Conclusions](#trap-7-premature-conclusions)
8. [Boolean vs Numeric Confusion](#trap-8-boolean-vs-numeric-confusion)

---

# Trap 1: Operator Confusion

## The Mistake

**Confusing `/` (integer division) with `|` (real division)** or treating all operators as permissive.

### Example Error

**Question**: "What is the type of `(10 3.5 /)`?"

**Wrong Answer**:
```
Student: "This is division, so...
Γ ⊢ 10 : int
Γ ⊢ 3.5 : real
Division accepts mixed types, so promover_tipo(int, real) = real
Therefore (10 3.5 /) : real"
```

**Why Wrong**: Division `/` is STRICT (int/int only), not permissive.

### Correct Answer

```
Γ ⊢ 10 : int
Γ ⊢ 3.5 : real

Operator / is STRICT - only accepts (int, int)
Current operands: (int, real) ❌

tipos_compativeis_divisao_inteira(int, real) = FALSE

ERROR: "Operador '/' requer operandos inteiros (recebeu int e real)"
```

---

## Why This Happens

### Root Causes

1. **Mental Model**: Most operators (+, -, *, |) are permissive → brain defaults to "all operators accept mixed types"
2. **Math Familiarity**: In regular math, 10 ÷ 3.5 is valid → forget this language has special rules
3. **Symbol Similarity**: `/` and `|` look similar → easy to conflate

### Recognition Signs

**You're making this mistake if you**:
- Say "division accepts any numeric types" without specifying `/` vs `|`
- Apply `promover_tipo()` to `/` or `%` operations
- Forget to check operator compatibility before inferring result type

---

## How to Correct in Real-Time

### If You Catch Yourself

**Stop and say**:
> "Wait, let me check which division operator this is. Is it `/` or `|`?"

Then:
1. Identify the operator symbol clearly
2. State its compatibility rule: "Operator `/` is STRICT - int/int only"
3. Check operand types against requirement
4. Conclude validity

### If Professor Interrupts

**Professor**: "Are you sure about that?"

**Recovery**:
> "Let me reconsider. I need to check the operator compatibility rules.
> Operator `/` is STRICT and only accepts (int, int).
> Since we have (int, real), this is actually a type error."

---

## Prevention Strategies

### Mnemonic: "STRICT TWO"

**The only two STRICT operators**:
- `/` = **D**ivision **I**nteger
- `%` = **M**odulo

Remember: "**D**ivision **I**nteger and **M**odulo - only these two are strict!"

### Visual Cue

Draw this table in your notes:
```
┌─────────────────────────────────────┐
│ PERMISSIVE: +  -  *  |  ^          │
│ (accept mixed int/real)             │
├─────────────────────────────────────┤
│ STRICT:  /  %                       │
│ (int/int ONLY)                      │
└─────────────────────────────────────┘
```

### Checklist for Division/Modulo

Before answering division/modulo questions:
- [ ] Is operator `/` or `%`? → STRICT mode
- [ ] Check BOTH operands are int
- [ ] If not int → ERROR (not type promotion!)

---

## Practice Drill

**Fast Recognition Exercise** (30 seconds each):

1. `(10 5 /)` → STRICT, both int, valid ✓
2. `(10.0 5 /)` → STRICT, first is real, **ERROR** ❌
3. `(10 5 |)` → PERMISSIVE, always returns real ✓
4. `(10 5.0 %)` → STRICT, second is real, **ERROR** ❌
5. `(10.5 5.0 +)` → PERMISSIVE, valid, result real ✓

---

# Trap 2: Type Promotion Errors

## The Mistake

**Applying type promotion in wrong direction** or forgetting promotion rules entirely.

### Example Error 1: Wrong Direction

**Question**: "What is `promover_tipo(real, int)`?"

**Wrong Answer**:
```
Student: "We promote real to int, so... int"
```

**Why Wrong**: Type promotion goes UP the hierarchy (int → real), never DOWN (real → int).

### Correct Answer

```
promover_tipo(real, int) = real

Reason: In the hierarchy int < real, we always promote to the HIGHER type.
int promotes to real (upcast), not vice versa.
```

---

### Example Error 2: Forgetting to Promote

**Question**: "What is the type of `(5 3.5 +)`?"

**Wrong Answer**:
```
Student: "Left is int, right is real, so... wait, which one is the result?"
[Guesses] "int?"
```

**Why Wrong**: Didn't apply type promotion function.

### Correct Answer

```
Γ ⊢ 5 : int
Γ ⊢ 3.5 : real

Operator + is PERMISSIVE
promover_tipo(int, real) = real

Therefore: (5 3.5 +) : real
```

---

## Why This Happens

### Root Causes

1. **Intuition**: "5 is an integer, so result should be integer" (ignoring 3.5)
2. **Confusion**: Type hierarchies are abstract → hard to visualize which direction is "up"
3. **Skipping Steps**: Jump to conclusion without explicitly calling `promover_tipo()`

### Recognition Signs

**You're making this mistake if you**:
- Say result is int when real operand present (in permissive operators)
- Hesitate when asked which type is "higher"
- Skip writing `promover_tipo()` call in derivation

---

## How to Correct in Real-Time

### Mental Model

**Visualize the hierarchy**:
```
        real  ← HIGHER (more general, more precision)
         ↑
       promote
         ↑
        int   ← LOWER (more specific, less precision)
```

**Rule**: Always promote UP, never DOWN.

### Correction Phrase

**If you make mistake**:
> "Let me correct that. In the type hierarchy int < real,
> we always promote to the higher type to preserve precision.
> So promover_tipo(int, real) = real."

---

## Prevention Strategies

### Mnemonic: "UP for Precision"

- **U**pcast = **P**reserve precision
- int → real (adds decimal capability)
- real → int (LOSES precision - NOT ALLOWED)

### Quick Check

Before stating result type:
1. List operand types: "int, real"
2. Identify higher type: "real is higher"
3. State promotion: "promover_tipo(int, real) = real"
4. Conclude: "Result is real"

### Promotion Table (Memorize)

```
promover_tipo(T₁, T₂)
┌─────┬─────┬──────┐
│     │ int │ real │
├─────┼─────┼──────┤
│ int │ int │ real │
├─────┼─────┼──────┤
│real │ real│ real │
└─────┴─────┴──────┘

Rule: If ANY operand is real → result is real
```

---

## Practice Drill

**Quick Promotion Quiz** (15 seconds each):

1. `promover_tipo(int, int)` = ?
   - Answer: **int**

2. `promover_tipo(int, real)` = ?
   - Answer: **real**

3. `promover_tipo(real, int)` = ?
   - Answer: **real**

4. `promover_tipo(real, real)` = ?
   - Answer: **real**

5. `promover_tipo(int, boolean)` = ?
   - Answer: **None** (incompatible!)

---

# Trap 3: IFELSE Branch Compatibility

## The Mistake

**Assuming IFELSE can have any branch types** or forgetting to check compatibility.

### Example Error

**Question**: "Is `((X 5 >) (100) ((Y 3 <)) IFELSE)` valid?"

**Wrong Answer**:
```
Student: "Yes, IFELSE just picks one branch.
True branch is int, false branch is boolean.
So the type is... whichever branch executes?"
```

**Why Wrong**: IFELSE requires **compatible branch types**. int and boolean are incompatible.

### Correct Answer

```
True branch: Γ ⊢ 100 : int
False branch: Γ ⊢ (Y 3 <) : boolean

Check compatibility:
promover_tipo(int, boolean) = None ❌

Branches are INCOMPATIBLE.

ERROR: "Branches de IFELSE incompatíveis: int e boolean"
```

---

## Why This Happens

### Root Causes

1. **Runtime Thinking**: "Only one branch executes, so type is determined at runtime"
   - **Wrong**: Type must be known at compile-time (semantic analysis)
2. **Forgetting Rule**: Don't memorize "branches must be compatible"
3. **Assuming Flexibility**: Think IFELSE is "flexible" like logical operators

### Recognition Signs

**You're making this mistake if you**:
- Say "IFELSE type depends on which branch runs"
- Don't check `promover_tipo()` for branches
- Think int and boolean can be in IFELSE together

---

## How to Correct in Real-Time

### Recovery Statement

**If professor questions you**:
> "Actually, I need to check branch compatibility.
> IFELSE requires promover_tipo(then, else) ≠ None.
> Since promover_tipo(int, boolean) = None, these branches are incompatible.
> This is a semantic error."

---

## Prevention Strategies

### Mnemonic: "BBC - Both Branches Compatible"

**B**oth **B**ranches must be **C**ompatible!

### IFELSE Checklist

Before concluding IFELSE type:
- [ ] Derive true branch type: T_then
- [ ] Derive false branch type: T_else
- [ ] Check: `promover_tipo(T_then, T_else)` ≠ None
- [ ] If None → ERROR
- [ ] If type T → IFELSE : T

### Compatible vs Incompatible

**Compatible Pairs** ✓:
- int + int → int
- int + real → real
- real + real → real
- boolean + boolean → boolean

**Incompatible Pairs** ❌:
- int + boolean → None
- real + boolean → None

**Key**: No promotion between numeric and boolean!

---

## Practice Drill

**IFELSE Compatibility Check** (30 seconds each):

1. `((X > 5) (10) (20) IFELSE)` → int + int → **valid** ✓
2. `((X > 5) (10.5) (20) IFELSE)` → real + int → **valid** ✓ (promotes to real)
3. `((X > 5) (true) (false) IFELSE)` → boolean + boolean → **valid** ✓
4. `((X > 5) (10) (true) IFELSE)` → int + boolean → **ERROR** ❌
5. `((X > 5) (10.5) ((Y < 3)) IFELSE)` → real + boolean → **ERROR** ❌

---

# Trap 4: Forgetting Initialization Checks

## The Mistake

**Using variables without checking if they're initialized** in symbol table derivations.

### Example Error

**Question**: "Derive type for `(X Y +)` with Γ = {}"

**Wrong Answer**:
```
Student: "Γ ⊢ X : int
Γ ⊢ Y : int
promover_tipo(int, int) = int
Therefore (X Y +) : int"
```

**Why Wrong**: X and Y don't exist in symbol table Γ = {}!

### Correct Answer

```
Given: Γ = {} (empty symbol table)

Attempt to evaluate (X Y +):
  Check X: Γ.buscar("X") = None ❌

ERROR: "Variável 'X' não declarada ou não inicializada"

Cannot proceed with type derivation.
```

---

## Why This Happens

### Root Causes

1. **Assumption**: "Variables just have types" → forget they must be declared
2. **Skipping Validation**: Jump straight to type derivation without symbol table lookup
3. **Focus on Happy Path**: Practice only valid expressions, not errors

### Recognition Signs

**You're making this mistake if you**:
- Never mention symbol table when variables appear
- Assign types to variables without checking Γ
- Don't validate initialization before use

---

## How to Correct in Real-Time

### Mandatory Variable Check

**When you see a variable identifier**:

**Step 1**: State you're checking symbol table
> "I need to look up X in the symbol table Γ."

**Step 2**: Perform lookup
> "Γ.buscar('X') = ..."

**Step 3**: Validate result
- If found: "X exists with type int, initialized = true"
- If not found: "X not found → ERROR"

---

## Prevention Strategies

### Variable Derivation Template

**Always follow this structure**:

```
For variable VAR:
1. State: "VAR is a variable, must check symbol table"
2. Lookup: "Γ.buscar('VAR') = ..."
3. Validate:
   a. Exists? If no → ERROR
   b. Initialized? If no → ERROR
   c. Type? Extract from result
4. Conclude: "Γ ⊢ VAR : <type>"
```

### Symbol Table Awareness

**Before starting any derivation with variables**:
- Look at given Γ
- List what's in symbol table
- State "I'll need to validate any variables against this table"

---

## Practice Drill

**Variable Validation Exercise** (45 seconds each):

Given: `Γ = {X: (int, true), Y: (real, false)}`

1. Derive type of `(X)`:
   - Γ.buscar("X") = (int, true) ✓
   - Initialized: true ✓
   - **Answer**: int ✓

2. Derive type of `(Y)`:
   - Γ.buscar("Y") = (real, false) ✓
   - Initialized: false ❌
   - **Answer**: ERROR "Y não inicializada" ❌

3. Derive type of `(Z)`:
   - Γ.buscar("Z") = None ❌
   - **Answer**: ERROR "Z não declarada" ❌

4. Derive type of `(X Y +)`:
   - X: int, initialized ✓
   - Y: not initialized ❌
   - **Answer**: ERROR (can't use Y) ❌

---

# Trap 5: RES Reference Calculation

## The Mistake

**Calculating RES referenced line incorrectly** or forgetting to validate bounds.

### Example Error

**Question**: "What line does `(3 RES)` on Line 5 reference?"

**Wrong Answer**:
```
Student: "RES 3 means... Line 3"
```

**Why Wrong**: RES argument is **offset**, not absolute line number!

### Correct Answer

```
Current line: 5
RES argument: 3
Referenced line = Current - Argument = 5 - 3 = 2

Therefore: (3 RES) on Line 5 references Line 2

Validation:
  1 ≤ 2 < 5 ✓ (valid range)
```

---

## Why This Happens

### Root Causes

1. **Naming Confusion**: "RES" sounds like "result" → think it's a line number
2. **Skipping Calculation**: See "3 RES" → assume "Line 3"
3. **Forgetting Context**: Don't track current line number

### Recognition Signs

**You're making this mistake if you**:
- Say "RES N" references "Line N"
- Don't subtract current line from RES argument
- Don't validate referenced line bounds

---

## How to Correct in Real-Time

### RES Calculation Template

**Always follow these steps**:

```
For (N RES) on Line L:

STEP 1: State current line
  "Current line: L"

STEP 2: State RES argument
  "RES argument: N"

STEP 3: Calculate referenced line
  "Referenced line = L - N = [result]"

STEP 4: Validate bounds
  "Check: 1 ≤ [result] < L"
  If valid: ✓ proceed
  If invalid: ❌ ERROR

STEP 5: Look up referenced line type
  "Line [result] has type: ..."

STEP 6: Conclude
  "Therefore: (N RES) : <type>"
```

---

## Prevention Strategies

### Mnemonic: "RES = Rewind by N"

Think of RES as "rewind" (go backwards):
- Current line 10, RES 3 → rewind 3 steps → Line 7
- Current line 5, RES 1 → rewind 1 step → Line 4

### Visual Aid

```
Line 1:  ●
Line 2:  ●
Line 3:  ●  ← Referenced line
Line 4:  ●
Line 5:  ●  ← Current: (2 RES)
         ↑
      rewind 2
```

### Validation Formula

**Valid RES range on line L**:
```
1 ≤ argument ≤ L - 1
```

Examples:
- Line 1: No valid RES (can't reference previous lines)
- Line 2: RES 1 only
- Line 10: RES 1, 2, 3, ..., 9

---

## Practice Drill

**RES Calculation Quiz** (30 seconds each):

1. Line 5, `(2 RES)` → references Line **3** (5-2)
2. Line 10, `(1 RES)` → references Line **9** (10-1)
3. Line 3, `(5 RES)` → references Line **-2** → **ERROR** ❌
4. Line 8, `(8 RES)` → references Line **0** → **ERROR** ❌
5. Line 7, `(6 RES)` → references Line **1** (7-6) ✓

---

# Trap 6: Notation and Formalism

## The Mistake

**Using informal or incorrect notation** instead of formal type judgments.

### Example Error

**Question**: "Prove `(5 3 +)` has type int"

**Wrong Answer** (Informal):
```
Student: "Well, 5 is an int, and 3 is an int,
so when you add them you get an int."
```

**Why Wrong**: Missing formal notation `Γ ⊢ e : T`, no rule names, no structure.

### Correct Answer (Formal)

```
Γ ⊢ 5 : int     (INT-LITERAL)
Γ ⊢ 3 : int     (INT-LITERAL)

Operator + is PERMISSIVE
tipos_compativeis_aritmetica(int, int) = TRUE
promover_tipo(int, int) = int

Derivation:
────────────── (INT)    ────────────── (INT)
 Γ ⊢ 5 : int             Γ ⊢ 3 : int
──────────────────────────────────────────────── (ADD)
          Γ ⊢ (5 3 +) : int
```

---

## Why This Happens

### Root Causes

1. **Comfort**: Informal language feels more natural
2. **Forgetting Audience**: Professor expects formal compiler theory
3. **Skipping Practice**: Don't practice writing formal derivations

### Recognition Signs

**You're making this mistake if you**:
- Never write `Γ ⊢ e : T`
- Don't draw horizontal lines in derivations
- Don't name rules (INT-LITERAL, ADD, etc.)

---

## How to Correct in Real-Time

### Switch to Formal Mode

**If professor says "be more formal"**:
> "Let me restate that formally using type judgments:
> [Write Γ ⊢ 5 : int]
> This uses the INT-LITERAL rule..."

---

## Prevention Strategies

### Notation Checklist

**Every type derivation must include**:
- [ ] Type judgment: `Γ ⊢ e : T`
- [ ] Rule names: (INT-LITERAL), (ADD), etc.
- [ ] Horizontal lines for inference rules
- [ ] Premises above line, conclusion below

### Standard Format

```
[Premise 1]    [Premise 2]    [Conditions]
────────────────────────────────────────────── (RULE-NAME)
              [Conclusion]
```

### Rule Names to Memorize

**Common Rules**:
- INT-LITERAL, REAL-LITERAL
- ADD, SUB, MULT, DIV-INT, DIV-REAL, MOD, POWER
- COMP-GT, COMP-LT, COMP-EQ, etc.
- AND, OR, NOT
- IFELSE, WHILE, FOR
- MEM-STORE, MEM-LOAD, RES

---

## Practice Drill

**Formalize These Statements** (60 seconds each):

1. Informal: "X is an int"
   - Formal: **Γ ⊢ X : int** (from symbol table lookup)

2. Informal: "5 plus 3 is 8"
   - Formal:
     ```
     Γ ⊢ 5:int  Γ ⊢ 3:int  promover_tipo(int,int)=int
     ───────────────────────────────────────────────── (ADD)
                  Γ ⊢ (5 3 +) : int
     ```

3. Informal: "This IFELSE returns int"
   - Formal:
     ```
     Γ ⊢ cond:bool  Γ ⊢ then:int  Γ ⊢ else:int  promover_tipo(int,int)=int
     ─────────────────────────────────────────────────────────────────────── (IFELSE)
                      Γ ⊢ (cond then else IFELSE) : int
     ```

---

# Trap 7: Premature Conclusions

## The Mistake

**Jumping to final answer without showing intermediate steps**.

### Example Error

**Question**: "Derive type of `((5 3 +) 2 *)`"

**Wrong Answer**:
```
Student: "This is nested, so... the result is int."
```

**Why Wrong**: Didn't show:
- Inner expression evaluation
- Outer expression evaluation
- Type inference steps

### Correct Answer (Step-by-Step)

```
STEP 1: Evaluate inner (5 3 +)
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  promover_tipo(int, int) = int
  Γ ⊢ (5 3 +) : int

STEP 2: Evaluate outer (<inner> 2 *)
  Γ ⊢ <inner> : int (from Step 1)
  Γ ⊢ 2 : int
  promover_tipo(int, int) = int
  Γ ⊢ ((5 3 +) 2 *) : int

CONCLUSION: Type is int
```

---

## Why This Happens

### Root Causes

1. **Mental Shortcuts**: See pattern, know answer → skip to end
2. **Time Pressure**: Think showing steps wastes time
3. **Nervousness**: Rush to show you know the answer

### Recognition Signs

**You're making this mistake if you**:
- State result without showing derivation
- Skip intermediate expressions in nested code
- Don't verbalize your reasoning

---

## How to Correct in Real-Time

### Slow Down Deliberately

**Professor asks**: "How did you get that?"

**Response**:
> "Let me show the steps:
> First, I evaluate the inner expression...
> [Show Step 1]
> Then, using that result...
> [Show Step 2]
> Therefore, the final type is..."

---

## Prevention Strategies

### Numbered Step Format

**Always use**:
```
STEP 1: [First subexpression]
STEP 2: [Second subexpression]
...
CONCLUSION: [Final answer]
```

### Think-Aloud Protocol

**Verbalize everything**:
- "First, I need to..."
- "Now I can see that..."
- "This tells me..."
- "Therefore..."

### Write While Talking

**Physical slowing**:
- Write each step on board as you explain it
- Don't erase intermediate work
- Point to previous steps when referencing them

---

## Practice Drill

**Expand These Answers** (2 minutes each):

1. Question: "Type of `(5 3.5 +)`?"
   - Wrong: "real"
   - Right: [Show full derivation with literals, operator check, promotion]

2. Question: "Why does `(10 3.0 /)` fail?"
   - Wrong: "Wrong types"
   - Right: [Show operand types, operator requirement, compatibility check, error message]

---

# Trap 8: Boolean vs Numeric Confusion

## The Mistake

**Confusing boolean operations with numeric** or forgetting truthiness conversion.

### Example Error 1: Comparison in Arithmetic

**Question**: "What is type of `((5 3 >) 10 +)`?"

**Wrong Answer**:
```
Student: "5 > 3 is boolean, then... boolean + int?
I think that's... hmm... int?"
```

**Why Wrong**: Comparison returns boolean, but `+` doesn't accept boolean operands!

### Correct Answer

```
Inner: (5 3 >)
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  Γ ⊢ (5 3 >) : boolean (comparison)

Outer: (<inner> 10 +)
  Left: boolean
  Right: int

Operator + requires numeric operands (int/real)
tipos_compativeis_aritmetica(boolean, int) = FALSE

ERROR: "Operador '+' requer operandos numéricos"
```

---

### Example Error 2: Logical Operators

**Question**: "Can `(5 0 &&)` work?"

**Wrong Answer**:
```
Student: "No, && requires boolean, but 5 and 0 are integers."
```

**Why Wrong**: Logical operators use PERMISSIVE mode with truthiness!

### Correct Answer

```
Γ ⊢ 5 : int
Γ ⊢ 0 : int

Operator && uses PERMISSIVE mode
Accepts: int, real, boolean via truthiness conversion

para_booleano(5, int) = true (non-zero)
para_booleano(0, int) = false (zero)

Γ ⊢ (5 0 &&) : boolean ✓

Result: boolean (evaluates to false)
```

---

## Why This Happens

### Root Causes

1. **Operator Categories**: Forget which operators accept boolean
2. **Truthiness**: Don't know about permissive mode for logical operators
3. **Type Boundaries**: Unclear where numeric ends and boolean begins

### Recognition Signs

**You're making this mistake if you**:
- Try to use boolean in arithmetic (`+`, `-`, `*`, `/`)
- Say logical operators only accept boolean (forgetting permissive mode)
- Don't mention `para_booleano()` for logical operators

---

## How to Correct in Real-Time

### Operator Category Check

**Before answering, identify operator category**:

| Category | Operators | Accept Boolean? | Use Truthiness? |
|----------|-----------|-----------------|-----------------|
| Arithmetic | +, -, *, /, %, \|, ^ | NO ❌ | NO |
| Comparison | >, <, ==, !=, >=, <= | NO ❌ | NO |
| Logical | &&, \|\|, ! | YES ✓ | YES (permissive) |
| Control | IFELSE, WHILE, FOR | Depends | WHILE/IFELSE: yes |
| Memory | MEM, VAR, RES | NO ❌ | NO |

---

## Prevention Strategies

### Truthiness Table (Memorize)

```
para_booleano(value, type):
┌────────┬──────────┬────────────┐
│ Value  │   Type   │  Truthiness│
├────────┼──────────┼────────────┤
│   0    │   int    │   false    │
│  ≠ 0   │   int    │   true     │
│  0.0   │  real    │   false    │
│ ≠ 0.0  │  real    │   true     │
│  true  │ boolean  │   true     │
│  false │ boolean  │   false    │
└────────┴──────────┴────────────┘
```

### Quick Decision Tree

**When you see a boolean type**:

```
Is operator arithmetic/comparison?
  YES → ERROR (boolean not accepted)
  NO → Continue

Is operator logical?
  YES → OK (permissive mode)
  NO → Check specific operator rules
```

---

## Practice Drill

**Boolean Compatibility Check** (30 seconds each):

1. `((5 > 3) 10 +)` → boolean + int in arithmetic → **ERROR** ❌
2. `((5 > 3) (10 < 20) &&)` → boolean + boolean in logical → **OK** ✓
3. `(5 0 &&)` → int + int in logical (truthiness) → **OK** ✓
4. `((5 > 3) X)` → MEM store boolean → **ERROR** ❌
5. `((X > 0) (10) (20) IFELSE)` → boolean condition in IFELSE → **OK** ✓

---

# Summary: Quick Mistake Prevention Checklist

## Before Starting Any Derivation

- [ ] Identify all operators and their compatibility modes (STRICT/PERMISSIVE)
- [ ] Check symbol table for any variables
- [ ] Note current line number (for RES references)
- [ ] Plan to show all intermediate steps

## During Derivation

- [ ] Use formal notation: `Γ ⊢ e : T`
- [ ] Name rules: (INT-LITERAL), (ADD), etc.
- [ ] Apply `promover_tipo()` explicitly for mixed types
- [ ] Validate variables: exist? initialized?
- [ ] Calculate RES: current_line - argument
- [ ] Check IFELSE branches: `promover_tipo(then, else)` ≠ None

## Common Gotchas

- [ ] `/` and `%` are STRICT (int/int only), NOT permissive
- [ ] Type promotion goes UP (int → real), never DOWN
- [ ] Boolean CANNOT be in arithmetic, but CAN be in logical (permissive)
- [ ] IFELSE branches MUST be compatible
- [ ] Power exponent MUST be int AND positive
- [ ] MEM CANNOT store boolean

---

# Error Recovery Phrases

## If You Make a Mistake

**Catching yourself**:
> "Wait, let me reconsider that..."
> "Actually, I need to check..."
> "Let me correct my reasoning..."

**Professor hints at error**:
> "You're right, let me think about that again..."
> "I should be more careful about..."
> "Let me verify that step..."

## Stay Calm

**Mistakes are OK!**:
- Catching and correcting shows understanding
- Professor wants to see reasoning, not perfection
- Self-correction demonstrates critical thinking

---

# Final Advice

## The Three Cs

1. **Careful**: Check each step, don't rush
2. **Clear**: Use formal notation, show all work
3. **Correct**: Validate as you go, catch mistakes early

## Practice Makes Perfect

- Review this guide before each practice session
- Practice intentionally making mistakes, then correcting them
- Time yourself recovering from errors

## You've Got This!

**Remember**: Everyone makes mistakes during defense. What matters is:
- ✓ Showing systematic reasoning
- ✓ Catching errors when they occur
- ✓ Correcting mistakes confidently
- ✓ Learning from the process

---

**Good luck! Trust your preparation and stay calm.** 🎓

---

*Last updated: 2025-01-19*
*RA3_1 Defense Preparation Team*
