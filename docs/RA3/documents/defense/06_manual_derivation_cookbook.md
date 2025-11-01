# Manual Derivation Cookbook
## Step-by-Step Recipes for Whiteboard Proofs

**Purpose**: Practice manual type derivations for oral defense
**Target**: 2-5 minute whiteboard demonstrations
**Method**: Follow the recipe, fill in blanks, practice until fluent

---

## How to Use This Cookbook

Each recipe is designed for **real-time whiteboard demonstration** during the defense.

### Recipe Structure
1. **Time Budget**: How long this should take
2. **Blank Template**: Fill-in-the-blank version for practice
3. **Worked Example**: Complete solution with explanations
4. **Common Mistakes**: What to avoid
5. **Practice Exercises**: Additional problems to try

### Practice Method
1. Read the recipe once
2. Try the blank template (no peeking!)
3. Check against worked example
4. Practice 3 more times
5. Time yourself - must finish within budget

---

## Recipe 1: Simple Binary Arithmetic
## Time Budget: 2 minutes

### What You'll Prove
Given a simple expression like `(5 3.5 +)`, prove its type step-by-step.

### The 5-Step Recipe

```
═════════════════════════════════════════════════════════════════
STEP 1: IDENTIFY COMPONENTS (15 seconds)
═════════════════════════════════════════════════════════════════
Parse: (operand₁ operand₂ operator)

Identify:
- Left operand: _____
- Right operand: _____
- Operator: _____

═════════════════════════════════════════════════════════════════
STEP 2: DERIVE LEFT OPERAND TYPE (30 seconds)
═════════════════════════════════════════════════════════════════
Ask: What is the operand?
- Literal integer (no decimal)? → type = int
- Literal real (has decimal)? → type = real
- Variable? → lookup in Γ

Apply rule:
─────────────────── (RULE-NAME)
  Γ ⊢ operand₁ : T₁

═════════════════════════════════════════════════════════════════
STEP 3: DERIVE RIGHT OPERAND TYPE (30 seconds)
═════════════════════════════════════════════════════════════════
(Same process as STEP 2)

Apply rule:
─────────────────── (RULE-NAME)
  Γ ⊢ operand₂ : T₂

═════════════════════════════════════════════════════════════════
STEP 4: CHECK COMPATIBILITY (30 seconds)
═════════════════════════════════════════════════════════════════
Ask: What operator category?
- {+, -, *, |} → PERMISSIVE (any numeric)
- {/, %} → STRICT (both must be int)
- ^ → SPECIAL (base any numeric, exp int only)
- comparison → any numeric
- logical → truthy-compatible

Check: tipos_compativeis_______(T₁, T₂) = _____

═════════════════════════════════════════════════════════════════
STEP 5: DETERMINE RESULT TYPE (30 seconds)
═════════════════════════════════════════════════════════════════
Apply type inference:
- If operator is | → result = real (ALWAYS)
- If operator is /, % → result = int
- If operator is ^ → result = typeof(base)
- If operator is comparison → result = boolean
- If operator is +, -, * → result = promover_tipo(T₁, T₂)

Final judgment:
Γ ⊢ (operand₁ operand₂ op) : T_result
```

---

### Blank Template (Practice This!)

```
Given: (_____ _____ _____)

═══════════════════════════════════════
STEP 1: IDENTIFY (15 sec)
═══════════════════════════════════════
  Left operand (e₁): _____
  Right operand (e₂): _____
  Operator (op): _____

═══════════════════════════════════════
STEP 2: LEFT TYPE (30 sec)
═══════════════════════════════════════
  Is e₁ a literal? _____ (yes/no)
  Has decimal point? _____ (yes/no)

  Type: Γ ⊢ e₁ : _____

  Rule applied: ___________

═══════════════════════════════════════
STEP 3: RIGHT TYPE (30 sec)
═══════════════════════════════════════
  Is e₂ a literal? _____ (yes/no)
  Has decimal point? _____ (yes/no)

  Type: Γ ⊢ e₂ : _____

  Rule applied: ___________

═══════════════════════════════════════
STEP 4: COMPATIBILITY (30 sec)
═══════════════════════════════════════
  Operator category: _____ (PERMISSIVE/STRICT/SPECIAL)

  Check function: tipos_compativeis_________

  Compatible? _____ (YES/NO)

═══════════════════════════════════════
STEP 5: RESULT TYPE (30 sec)
═══════════════════════════════════════
  Type inference rule: _____

  Result: Γ ⊢ (e₁ e₂ op) : _____

═══════════════════════════════════════
DERIVATION TREE
═══════════════════════════════════════

  _________ (_____)    _________ (_____)
    Γ ⊢ e₁:___           Γ ⊢ e₂:___
  ──────────────────────────────────────
      Γ ⊢ (e₁ e₂ op) : _____
```

---

### Worked Example 1: (5 3.5 +)

```
Given: (5 3.5 +)

═══════════════════════════════════════
STEP 1: IDENTIFY (15 sec)
═══════════════════════════════════════
  Left operand: 5
  Right operand: 3.5
  Operator: +

═══════════════════════════════════════
STEP 2: LEFT TYPE (30 sec)
═══════════════════════════════════════
  Is 5 a literal? YES
  Has decimal point? NO

  Therefore: Γ ⊢ 5 : int

  Rule: INT-LITERAL

  Why? Literals without decimal points are integers.

═══════════════════════════════════════
STEP 3: RIGHT TYPE (30 sec)
═══════════════════════════════════════
  Is 3.5 a literal? YES
  Has decimal point? YES (.5)

  Therefore: Γ ⊢ 3.5 : real

  Rule: REAL-LITERAL

  Why? Literals with decimal points are real numbers.

═══════════════════════════════════════
STEP 4: COMPATIBILITY (30 sec)
═══════════════════════════════════════
  Operator + is PERMISSIVE (accepts any numeric)

  Check: tipos_compativeis_aritmetica(int, real) = TRUE

  Why? Addition + accepts int/int, int/real, real/int, real/real

═══════════════════════════════════════
STEP 5: RESULT TYPE (30 sec)
═══════════════════════════════════════
  Since + is in {+, -, *}, we use promover_tipo

  promover_tipo(int, real) = real

  Why? In the hierarchy int < real, so int promotes to real.

  Therefore: Γ ⊢ (5 3.5 +) : real

═══════════════════════════════════════
COMPLETE DERIVATION TREE
═══════════════════════════════════════

  ─────────── (INT)    ─────────── (REAL)
    Γ ⊢ 5:int            Γ ⊢ 3.5:real
  ────────────────────────────────────────── (ADD-PROMOTE)
          Γ ⊢ (5 3.5 +) : real

═══════════════════════════════════════
EXPLAIN IN WORDS
═══════════════════════════════════════
"First, 5 is an integer literal because it has no decimal point, giving us type int.
Second, 3.5 is a real literal because it has a decimal point (.5), giving us type real.
Third, addition is PERMISSIVE, so it accepts mixed int and real operands.
Finally, we apply type promotion: int promotes to real when mixed, so the result is real."
```

**Time Check**: Did you finish in 2 minutes? Practice until you can!

---

### Worked Example 2: (10 3 /)

```
Given: (10 3 /)

STEP 1: IDENTIFY
  e₁ = 10, e₂ = 3, op = /

STEP 2: LEFT TYPE
  10 is literal, no decimal → Γ ⊢ 10 : int

STEP 3: RIGHT TYPE
  3 is literal, no decimal → Γ ⊢ 3 : int

STEP 4: COMPATIBILITY
  Operator / is STRICT (int/int ONLY)
  tipos_compativeis_divisao_inteira(int, int) = TRUE

STEP 5: RESULT TYPE
  Division / always returns int
  Γ ⊢ (10 3 /) : int

DERIVATION TREE:
  ──────────── (INT)    ──────────── (INT)
    Γ ⊢ 10:int             Γ ⊢ 3:int
  ────────────────────────────────────────── (DIV-INT)
          Γ ⊢ (10 3 /) : int
```

---

### Common Mistakes in Recipe 1

❌ **Mistake 1**: "3.5 could be int if we round it"
✓ **Correction**: Types are determined lexically. Has decimal → real. No conversions.

❌ **Mistake 2**: "Division / accepts real because it's math"
✓ **Correction**: Division / is STRICT - only int/int. Use | for real division.

❌ **Mistake 3**: Forgetting to show derivation tree
✓ **Correction**: ALWAYS draw the tree! It shows formal proof.

❌ **Mistake 4**: "(5 3.5 +) is int because 5 comes first"
✓ **Correction**: Order doesn't matter. promover_tipo chooses the "larger" type (real).

---

### Practice Exercises (Recipe 1)

Try these on your own, then check solutions:

**Exercise 1.1**: (2 8 +)
**Exercise 1.2**: (7.5 2.5 -)
**Exercise 1.3**: (4 2.0 *)
**Exercise 1.4**: (15 3 %)
**Exercise 1.5**: (10.0 2.5 |)

<details>
<summary>Solutions (click to reveal)</summary>

**1.1**: int (both int, + preserves when same type)
**1.2**: real (both real, - preserves when same type)
**1.3**: real (int * real → promover_tipo → real)
**1.4**: int (% is STRICT, both int, result int)
**1.5**: real (| ALWAYS returns real)
</details>

---

## Recipe 2: Nested Expressions
## Time Budget: 4 minutes

### What You'll Prove
Given nested expressions like `((5 3 +) 2 *)`, derive types inside-out.

### The 8-Step Recipe

```
═══════════════════════════════════════
RECIPE 2: NESTED EXPRESSIONS
═══════════════════════════════════════

Key Principle: Work INSIDE-OUT (deepest first)

STEP 1: Identify Nesting (20 sec)
   - Find innermost expression
   - Mark evaluation order

STEP 2-4: Derive Inner Expression (2 min)
   - Use Recipe 1 for inner part
   - Get type: Γ ⊢ inner : T_inner

STEP 5: Replace Inner with Type (10 sec)
   - Substitute: (inner) becomes T_inner

STEP 6-8: Derive Outer Expression (1.5 min)
   - Use Recipe 1 for outer part
   - Get final type

STEP 9: Build Complete Tree (30 sec)
   - Show nested structure
```

---

### Blank Template (Recipe 2)

```
Given: ((_____ _____ _____) _____ _____)

STEP 1: IDENTIFY NESTING
  Inner expression: (___ ___ ___)
  Outer structure: (INNER ___ ___)

STEP 2-4: DERIVE INNER (Recipe 1)
  [Use Recipe 1 steps here]

  Result: Γ ⊢ inner : _____

STEP 5: SUBSTITUTE
  Replace inner → type
  New expression: (_____ _____ _____)

STEP 6-8: DERIVE OUTER (Recipe 1)
  [Use Recipe 1 steps here]

  Result: Γ ⊢ outer : _____

STEP 9: COMPLETE TREE
  [Show full derivation]
```

---

### Worked Example: ((5 3 +) 2 *)

```
Given: ((5 3 +) 2 *)

═══════════════════════════════════════
STEP 1: IDENTIFY NESTING (20 sec)
═══════════════════════════════════════
Inner: (5 3 +)
Outer structure: (INNER 2 *)

Evaluation order: Inner first, then outer

═══════════════════════════════════════
STEPS 2-4: DERIVE INNER (2 min)
═══════════════════════════════════════
Applying Recipe 1 to (5 3 +):

  e₁ = 5 → Γ ⊢ 5 : int (no decimal)
  e₂ = 3 → Γ ⊢ 3 : int (no decimal)
  op = + → PERMISSIVE

  promover_tipo(int, int) = int

  Result: Γ ⊢ (5 3 +) : int

═══════════════════════════════════════
STEP 5: SUBSTITUTE (10 sec)
═══════════════════════════════════════
Replace (5 3 +) with its type: int

New expression: (int 2 *)

Actually: ([result_of_inner] 2 *)
where [result_of_inner] : int

═══════════════════════════════════════
STEPS 6-8: DERIVE OUTER (1.5 min)
═══════════════════════════════════════
Applying Recipe 1 to (inner 2 *):

  e₁ = (5 3 +) → type int (from STEP 4)
  e₂ = 2 → Γ ⊢ 2 : int (no decimal)
  op = * → PERMISSIVE

  promover_tipo(int, int) = int

  Result: Γ ⊢ ((5 3 +) 2 *) : int

═══════════════════════════════════════
STEP 9: COMPLETE DERIVATION TREE (30 sec)
═══════════════════════════════════════

          ────── (INT)  ────── (INT)
           Γ⊢5:int       Γ⊢3:int
          ─────────────────────────── (ADD)    ────── (INT)
            Γ ⊢ (5 3 +) : int                  Γ⊢2:int
          ─────────────────────────────────────────────────── (MULT)
                    Γ ⊢ ((5 3 +) 2 *) : int

═══════════════════════════════════════
EXPLAIN IN WORDS
═══════════════════════════════════════
"We evaluate inside-out. First, the inner expression (5 3 +): both are integers,
addition of int+int gives int. Now we have int * 2. The 2 is also int. Multiplication
is permissive, and int * int gives int. Therefore, the entire expression is int."
```

---

### Practice Exercises (Recipe 2)

**Exercise 2.1**: ((2.5 1.5 +) 2 /)
**Exercise 2.2**: ((10 2 /) 3.0 +)
**Exercise 2.3**: (((5 3 +) 2 *) 4 -)

Time yourself! Each should take ~4 minutes.

---

## Recipe 3: IFELSE Derivation
## Time Budget: 5 minutes

### What You'll Prove
Given `(condition then_branch else_branch IFELSE)`, prove the result type.

### The 6-Step Recipe

```
═══════════════════════════════════════
RECIPE 3: IFELSE STRUCTURE
═══════════════════════════════════════

STEP 1: Parse Structure (20 sec)
  (cond then else IFELSE)

STEP 2: Derive Condition Type (1 min)
  Must be boolean-compatible (boolean or truthy-convertible)

STEP 3: Derive Then Branch (1.5 min)
  Use Recipe 1 or 2 as needed

STEP 4: Derive Else Branch (1.5 min)
  Use Recipe 1 or 2 as needed

STEP 5: Check Branch Compatibility (30 sec)
  promover_tipo(tipo_then, tipo_else) ≠ None?

STEP 6: Determine Result (30 sec)
  Result = promover_tipo(tipo_then, tipo_else)
```

---

### Worked Example: ((5 > 3) (10) (20.5) IFELSE)

```
Given: ((5 > 3) (10) (20.5) IFELSE)

═══════════════════════════════════════
STEP 1: PARSE (20 sec)
═══════════════════════════════════════
  condition: (5 > 3)
  then_branch: (10)
  else_branch: (20.5)
  structure: IFELSE

═══════════════════════════════════════
STEP 2: DERIVE CONDITION (1 min)
═══════════════════════════════════════
For (5 > 3):
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  > is comparison → result is boolean

  Γ ⊢ (5 > 3) : boolean ✓

Condition is boolean-compatible ✓

═══════════════════════════════════════
STEP 3: DERIVE THEN BRANCH (1 min)
═══════════════════════════════════════
For (10):
  10 is literal, no decimal

  Γ ⊢ (10) : int

═══════════════════════════════════════
STEP 4: DERIVE ELSE BRANCH (1 min)
═══════════════════════════════════════
For (20.5):
  20.5 is literal, has decimal (.5)

  Γ ⊢ (20.5) : real

═══════════════════════════════════════
STEP 5: CHECK COMPATIBILITY (30 sec)
═══════════════════════════════════════
  tipo_then = int
  tipo_else = real

  promover_tipo(int, real) = real ≠ None

  Branches are COMPATIBLE ✓

═══════════════════════════════════════
STEP 6: RESULT TYPE (30 sec)
═══════════════════════════════════════
  Result type = promover_tipo(int, real) = real

  Γ ⊢ ((5>3) (10) (20.5) IFELSE) : real

═══════════════════════════════════════
DERIVATION TREE
═══════════════════════════════════════

  ──────(INT) ──────(INT)       ────────(INT)  ──────────(REAL)
   Γ⊢5:int    Γ⊢3:int            Γ⊢(10):int    Γ⊢(20.5):real
  ──────────────────────(CMP)
    Γ⊢(5>3):boolean            promover_tipo(int,real)=real
  ───────────────────────────────────────────────────────────── (IFELSE)
          Γ ⊢ ((5>3) (10) (20.5) IFELSE) : real
```

---

### Common Mistakes (Recipe 3)

❌ **Mistake**: "IFELSE returns type of then branch"
✓ **Correction**: Returns promover_tipo(then, else) - BOTH branches matter!

❌ **Mistake**: "int and boolean branches are OK"
✓ **Correction**: promover_tipo(int, boolean) = None → ERROR!

---

## Recipe 4: Symbol Table Evolution
## Time Budget: 3 minutes

### What You'll Prove
Track how symbol table Γ evolves through a multi-line program.

### Worked Example

```
Given program:
  Line 1: (5 X)       # Store 5 in X
  Line 2: (10.5 Y)    # Store 10.5 in Y
  Line 3: (X Y +)     # Add X and Y

Prove: Show Γ₀ → Γ₁ → Γ₂ → Γ₃

═══════════════════════════════════════
INITIAL STATE
═══════════════════════════════════════
Γ₀ = {} (empty)

═══════════════════════════════════════
LINE 1: (5 X)
═══════════════════════════════════════
Operation: MEM_STORE (store 5 in X)

Type of 5: int

Action: Add X to symbol table
  X ↦ (type: int, inicializada: true, linha: 1)

Γ₁ = {X: int (initialized)}

═══════════════════════════════════════
LINE 2: (10.5 Y)
═══════════════════════════════════════
Operation: MEM_STORE (store 10.5 in Y)

Type of 10.5: real

Action: Add Y to symbol table
  Y ↦ (type: real, inicializada: true, linha: 2)

Γ₂ = {X: int (initialized), Y: real (initialized)}

═══════════════════════════════════════
LINE 3: (X Y +)
═══════════════════════════════════════
Operation: Arithmetic (add X and Y)

Check X: X ∈ dom(Γ₂)? YES, initialized? YES, type? int ✓
Check Y: Y ∈ dom(Γ₂)? YES, initialized? YES, type? real ✓

Types: int + real → promover_tipo → real

Result type: real

Γ₃ = Γ₂ (no new variables)

═══════════════════════════════════════
EVOLUTION SUMMARY
═══════════════════════════════════════
Γ₀ = {}
  ↓ (line 1: 5→X)
Γ₁ = {X: int}
  ↓ (line 2: 10.5→Y)
Γ₂ = {X: int, Y: real}
  ↓ (line 3: use X, Y)
Γ₃ = {X: int, Y: real}
```

---

## Recipe 5: RES Resolution
## Time Budget: 2 minutes

### Worked Example

```
Given program:
  Line 1: (5 3 +)     # Returns 8 : int
  Line 2: (2.5 2 *)   # Returns 5.0 : real
  Line 3: (2 RES)     # Reference line 3-2=1

Prove: What is the type of (2 RES) on line 3?

═══════════════════════════════════════
STEP 1: IDENTIFY RES OPERAND
═══════════════════════════════════════
RES with operand N = 2

═══════════════════════════════════════
STEP 2: CALCULATE REFERENCE LINE
═══════════════════════════════════════
Current line: 3
Offset: 2
Reference line = linha_atual - N = 3 - 2 = 1

═══════════════════════════════════════
STEP 3: CHECK BOUNDS
═══════════════════════════════════════
Is linha_ref >= 1? Is 1 >= 1? YES ✓
Is N <= linha_atual - 1? Is 2 <= 2? YES ✓

Reference is VALID

═══════════════════════════════════════
STEP 4: LOOKUP TYPE
═══════════════════════════════════════
What was the type of line 1?

Line 1: (5 3 +)
  Both int → int + int → int

tipo(Line 1) = int

═══════════════════════════════════════
STEP 5: APPLY RES RULE
═══════════════════════════════════════
RES inherits the type from referenced line

Γ ⊢ (2 RES) : int

(on line 3, RES references line 1 which had type int)
```

---

## Practice Schedule

### Week Before Defense

**Monday**: Practice Recipe 1 (10 times)
**Tuesday**: Practice Recipe 2 (5 times)
**Wednesday**: Practice Recipe 3 (5 times)
**Thursday**: Practice Recipes 4 & 5 (3 times each)
**Friday**: Mixed practice (all recipes)
**Weekend**: Timed practice with team

### Day Before Defense

Practice each recipe 2-3 times. Focus on:
- Clear handwriting
- Step numbering
- Speaking while writing
- Time management

---

**YOU'RE READY!**

These recipes cover 90% of likely defense questions. Practice them until you can do each one smoothly on a whiteboard while explaining your reasoning.

Remember: **Slow and correct beats fast and wrong.**

---

*RA3_1 Defense Cookbook*
*Last updated: 2025-01-19*
