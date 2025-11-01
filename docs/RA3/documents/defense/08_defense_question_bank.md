# Defense Question Bank: 40 Timed Questions
## RA3 Semantic Analyzer Oral Examination Practice

**Purpose**: Simulate real defense scenarios with timed questions and complete answers
**How to Use**:
1. Set a timer for the specified time budget
2. Answer the question on whiteboard/paper
3. Compare your answer with the provided solution
4. Track your performance over multiple attempts

**Difficulty Levels**:
- ⭐ Basic (2 minutes) - Single concept, straightforward
- ⭐⭐ Intermediate (3-4 minutes) - Multiple steps, type promotion
- ⭐⭐⭐ Advanced (4-5 minutes) - Complex nesting, multiple rules

---

## Question Distribution

Based on likely defense patterns:

| Category | Count | Probability | Questions |
|----------|-------|-------------|-----------|
| **Type Inference** | 16 | 40% | Q1-Q16 |
| **Error Detection** | 12 | 30% | Q17-Q28 |
| **Control Structures** | 8 | 20% | Q29-Q36 |
| **Symbol Table** | 4 | 10% | Q37-Q40 |
| **TOTAL** | **40** | 100% | All |

---

# Category A: Type Inference (Q1-Q16)

## Q1: Simple Integer Arithmetic ⭐

**Time Budget**: 2 minutes

**Question**: Prove that the expression `(8 4 -)` has type `int`.

**Answer**:

### Step 1: Identify Components
- Left operand: 8
- Right operand: 4
- Operator: -

### Step 2: Derive Operand Types
```
Γ ⊢ 8 : int     (INT-LITERAL - no decimal point)
Γ ⊢ 4 : int     (INT-LITERAL - no decimal point)
```

### Step 3: Check Operator Compatibility
- Operator `-` is PERMISSIVE (accepts any numeric types)
- `tipos_compativeis_aritmetica(int, int) = TRUE`

### Step 4: Infer Result Type
- `promover_tipo(int, int) = int`
- Both operands same type → no promotion needed

### Step 5: Conclusion
```
────────────── (INT)    ────────────── (INT)
 Γ ⊢ 8 : int             Γ ⊢ 4 : int
──────────────────────────────────────────────── (SUB)
          Γ ⊢ (8 4 -) : int
```

**Therefore**: `(8 4 -)` has type `int`.

---

## Q2: Type Promotion in Multiplication ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(5 2.0 *)` has type `real` and explain the type promotion.

**Answer**:

### Step 1: Derive Left Operand
- Literal: 5
- Has decimal? NO
- `Γ ⊢ 5 : int` (INT-LITERAL)

### Step 2: Derive Right Operand
- Literal: 2.0
- Has decimal? YES (.0)
- `Γ ⊢ 2.0 : real` (REAL-LITERAL)

### Step 3: Check Compatibility
- Operator `*` is PERMISSIVE
- Accepts: int/int, int/real, real/int, real/real
- Combination (int, real) is valid

### Step 4: Type Promotion
- `promover_tipo(int, real) = real`
- **Explanation**: In the type hierarchy `int < real`, when mixing types, the lower type (int) is promoted to the higher type (real) to maintain precision

### Step 5: Formal Derivation
```
────────────── (INT)    ────────────── (REAL)    promover_tipo(int, real) = real
 Γ ⊢ 5 : int             Γ ⊢ 2.0 : real
──────────────────────────────────────────────────────────────────────────────────── (MULT-PROMOTE)
                    Γ ⊢ (5 2.0 *) : real
```

**Therefore**: `(5 2.0 *)` has type `real` due to type promotion.

---

## Q3: Real Division Always Returns Real ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(10 5 |)` has type `real` and explain why the result is always real even with integer operands.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 10 : int    (INT-LITERAL)
Γ ⊢ 5 : int     (INT-LITERAL)
```

### Step 2: Check Operator Semantics
- Operator `|` is real division (PERMISSIVE)
- Accepts: any numeric types
- `tipos_compativeis_aritmetica(int, int) = TRUE`

### Step 3: Result Type Rule
- **Critical**: Operator `|` ALWAYS returns `real`
- This is independent of operand types
- Reason: Division may produce fractional results (10 ÷ 5 = 2.0, not 2)

### Step 4: Type Inference
- Even though both operands are int
- Result type = `real` (by operator semantics)

### Step 5: Formal Derivation
```
────────────── (INT)    ────────────── (INT)
 Γ ⊢ 10 : int            Γ ⊢ 5 : int
──────────────────────────────────────────────── (DIV-REAL)
          Γ ⊢ (10 5 |) : real
```

**Key Point**: Unlike `/` (int division), the `|` operator always produces real results to handle fractional quotients correctly.

**Therefore**: `(10 5 |)` has type `real`.

---

## Q4: Comparison Operators Return Boolean ⭐

**Time Budget**: 2 minutes

**Question**: What is the type of `(7 3.5 >)` and why?

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 7 : int       (INT-LITERAL)
Γ ⊢ 3.5 : real    (REAL-LITERAL - has .5)
```

### Step 2: Check Operator Category
- Operator `>` is a comparison operator
- Comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`

### Step 3: Result Type Rule
- **All comparison operators return `boolean`**
- This is independent of operand types
- Operands must be numeric, but result is always boolean

### Step 4: Formal Derivation
```
────────────── (INT)    ────────────── (REAL)
 Γ ⊢ 7 : int             Γ ⊢ 3.5 : real
──────────────────────────────────────────────── (COMP-GT)
          Γ ⊢ (7 3.5 >) : boolean
```

**Therefore**: `(7 3.5 >)` has type `boolean`.

---

## Q5: Power Operator with Integer Exponent ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(3.5 2 ^)` has type `real` and explain the exponent restriction.

**Answer**:

### Step 1: Identify Operand Roles
- Base: 3.5 → Type: real
- Exponent: 2 → Type: int

### Step 2: Derive Types
```
Γ ⊢ 3.5 : real    (REAL-LITERAL - has .5)
Γ ⊢ 2 : int       (INT-LITERAL)
```

### Step 3: Check Power Operator Requirements
- Base can be: `int` or `real`
- Exponent MUST be: `int` (strict requirement)
- Exponent MUST be: `> 0` (positive)

### Step 4: Validate Exponent
- Is 2 an int? YES
- Is 2 > 0? YES
- Compatibility: `tipos_compativeis_potencia(real, int) = TRUE`

### Step 5: Result Type Rule
- For power operator: `typeof(base^exp) = typeof(base)`
- Base type = real
- Therefore: result type = real

### Step 6: Formal Derivation
```
Γ ⊢ 3.5 : real    Γ ⊢ 2 : int    2 > 0
──────────────────────────────────────────────── (POWER)
          Γ ⊢ (3.5 2 ^) : real
```

**Exponent Restriction Explanation**: The exponent must be a positive integer to ensure:
1. Termination of power calculation
2. Deterministic result (no complex numbers from negative/fractional exponents)
3. Efficient computation (integer multiplication loop)

**Therefore**: `(3.5 2 ^)` has type `real`.

---

## Q6: Nested Expression Inside-Out ⭐⭐

**Time Budget**: 4 minutes

**Question**: Derive the type of `((3 2 +) 5.0 *)` step-by-step.

**Answer**:

### Step 1: Identify Structure
- Inner expression: `(3 2 +)`
- Outer expression: `(<inner> 5.0 *)`

### Step 2: Evaluate Inner Expression
```
Γ ⊢ 3 : int     (INT-LITERAL)
Γ ⊢ 2 : int     (INT-LITERAL)

promover_tipo(int, int) = int

Γ ⊢ (3 2 +) : int    (ADD)
```

### Step 3: Substitute Inner Result
- Now we have: `(int 5.0 *)`
- Left operand: result of inner = `int`
- Right operand: 5.0 = `real`

### Step 4: Evaluate Outer Expression
```
Γ ⊢ <inner> : int     (from Step 2)
Γ ⊢ 5.0 : real        (REAL-LITERAL)

Operator * is PERMISSIVE
tipos_compativeis_aritmetica(int, real) = TRUE

promover_tipo(int, real) = real
```

### Step 5: Complete Derivation Tree
```
────────── (INT)    ────────── (INT)
Γ ⊢ 3 : int          Γ ⊢ 2 : int
──────────────────────────────────────── (ADD)         ────────────── (REAL)
      Γ ⊢ (3 2 +) : int                                Γ ⊢ 5.0 : real
──────────────────────────────────────────────────────────────────────────────── (MULT-PROMOTE)
                    Γ ⊢ ((3 2 +) 5.0 *) : real
```

**Key Principle**: Always evaluate inside-out in RPN nested expressions.

**Therefore**: `((3 2 +) 5.0 *)` has type `real`.

---

## Q7: Logical AND with Permissive Mode ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(5 0 &&)` has type `boolean` and explain truthiness conversion.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 5 : int     (INT-LITERAL)
Γ ⊢ 0 : int     (INT-LITERAL)
```

### Step 2: Check Operator Requirements
- Operator `&&` is a logical operator
- Logical operators use PERMISSIVE mode
- Accept: int, real, boolean (via truthiness conversion)

### Step 3: Truthiness Conversion
- `para_booleano(5, int) = true` (non-zero)
- `para_booleano(0, int) = false` (zero)

**Truthiness Rule**:
- For int: 0 = false, ≠0 = true
- For real: 0.0 = false, ≠0.0 = true
- For boolean: true = true, false = false

### Step 4: Logical AND Evaluation
- Left (as boolean): `true`
- Right (as boolean): `false`
- `true && false = false`

### Step 5: Result Type
- All logical operators return: `boolean`
- `tipos_compativeis_logico(int, int) = TRUE` (both convertible)

### Step 6: Formal Derivation
```
Γ ⊢ 5 : int    Γ ⊢ 0 : int    para_booleano(5, int) = true    para_booleano(0, int) = false
─────────────────────────────────────────────────────────────────────────────────────────────── (AND)
                            Γ ⊢ (5 0 &&) : boolean
```

**Therefore**: `(5 0 &&)` has type `boolean` (evaluates to `false`).

---

## Q8: Three-Level Nested Expression ⭐⭐⭐

**Time Budget**: 5 minutes

**Question**: Derive the type of `(((10 2 /) (3 1 -) ^) 5.5 +)` showing all intermediate steps.

**Answer**:

### Step 1: Identify Nesting Levels
- Level 1 (innermost left): `(10 2 /)`
- Level 1 (innermost right): `(3 1 -)`
- Level 2 (middle): `((10 2 /) (3 1 -) ^)`
- Level 3 (outermost): `(<level2> 5.5 +)`

### Step 2: Evaluate Level 1 Left - `(10 2 /)`
```
Γ ⊢ 10 : int    (INT-LITERAL)
Γ ⊢ 2 : int     (INT-LITERAL)

Operator / is STRICT (int/int only)
tipos_compativeis_divisao_inteira(int, int) = TRUE

Result type: int (integer division)

Γ ⊢ (10 2 /) : int
```

### Step 3: Evaluate Level 1 Right - `(3 1 -)`
```
Γ ⊢ 3 : int     (INT-LITERAL)
Γ ⊢ 1 : int     (INT-LITERAL)

promover_tipo(int, int) = int

Γ ⊢ (3 1 -) : int
```

### Step 4: Evaluate Level 2 - `((10 2 /) (3 1 -) ^)`
```
Base: int (from Step 2)
Exponent: int (from Step 3)

Check exponent value: (3 - 1) = 2 > 0 ✓

Operator ^ requirements:
- Base: int/real ✓
- Exponent: int ✓
- Exponent > 0 ✓

Result type: typeof(base) = int

Γ ⊢ ((10 2 /) (3 1 -) ^) : int
```

### Step 5: Evaluate Level 3 - `(<level2> 5.5 +)`
```
Γ ⊢ <level2> : int     (from Step 4)
Γ ⊢ 5.5 : real         (REAL-LITERAL)

Operator + is PERMISSIVE
tipos_compativeis_aritmetica(int, real) = TRUE

promover_tipo(int, real) = real

Γ ⊢ (((10 2 /) (3 1 -) ^) 5.5 +) : real
```

### Step 6: Complete Derivation Tree
```
[Level 1 Left]                [Level 1 Right]
Γ ⊢ 10:int  Γ ⊢ 2:int        Γ ⊢ 3:int  Γ ⊢ 1:int
──────────────────────        ──────────────────────
Γ ⊢ (10 2 /):int              Γ ⊢ (3 1 -):int
─────────────────────────────────────────────────────── [Level 2]
        Γ ⊢ ((10 2 /) (3 1 -) ^) : int
                                              Γ ⊢ 5.5:real
──────────────────────────────────────────────────────────────────── [Level 3]
            Γ ⊢ (((10 2 /) (3 1 -) ^) 5.5 +) : real
```

**Therefore**: `(((10 2 /) (3 1 -) ^) 5.5 +)` has type `real`.

---

## Q9: Modulo Operator Strict Typing ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(23 6 %)` has type `int` and explain why modulo requires integers.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 23 : int    (INT-LITERAL)
Γ ⊢ 6 : int     (INT-LITERAL)
```

### Step 2: Check Operator Requirements
- Operator `%` (modulo) is STRICT
- ONLY accepts: int/int
- `tipos_compativeis_divisao_inteira(int, int) = TRUE`

### Step 3: Result Type
- Modulo always returns: `int`
- Result is the remainder of integer division

### Step 4: Why Integers Only?
**Reason**: Modulo is defined as the remainder after integer division:
- `a % b = a - (a / b) * b` where `/` is integer division
- Example: `23 % 6 = 23 - (23 / 6) * 6 = 23 - 3 * 6 = 23 - 18 = 5`
- For real numbers, the concept of "remainder" is ambiguous
- Integer constraint ensures deterministic, well-defined result

### Step 5: Formal Derivation
```
────────────── (INT)    ────────────── (INT)
 Γ ⊢ 23 : int            Γ ⊢ 6 : int
──────────────────────────────────────────────── (MOD)
          Γ ⊢ (23 6 %) : int
```

**Therefore**: `(23 6 %)` has type `int`.

---

## Q10: Equality Comparison with Mixed Types ⭐⭐

**Time Budget**: 3 minutes

**Question**: What is the type of `(10 10.0 ==)` and does type mixing matter for comparison?

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 10 : int      (INT-LITERAL - no decimal)
Γ ⊢ 10.0 : real   (REAL-LITERAL - has .0)
```

### Step 2: Check Operator Compatibility
- Operator `==` is a comparison operator
- Comparison operators accept: any numeric types
- `tipos_compativeis_comparacao(int, real) = TRUE`

### Step 3: Result Type
- All comparison operators return: `boolean`
- Independent of operand types

### Step 4: Does Type Mixing Matter?
**Answer**: NO for result type, but YES for semantic evaluation:
- Result type: Always `boolean`
- Semantic value: Types are promoted for comparison
  - `10 (int)` promoted to `10.0 (real)`
  - Then compared: `10.0 == 10.0` → `true`

### Step 5: Formal Derivation
```
────────────── (INT)    ────────────── (REAL)
 Γ ⊢ 10 : int            Γ ⊢ 10.0 : real
──────────────────────────────────────────────── (COMP-EQ)
          Γ ⊢ (10 10.0 ==) : boolean
```

**Key Points**:
- Comparison operators are permissive (accept mixed numeric types)
- Types are promoted before comparison
- Result is always boolean

**Therefore**: `(10 10.0 ==)` has type `boolean`.

---

## Q11: Logical OR with Zero ⭐⭐

**Time Budget**: 3 minutes

**Question**: Derive the type of `(0.0 5 ||)` and explain the truthiness evaluation.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 0.0 : real    (REAL-LITERAL - has .0)
Γ ⊢ 5 : int       (INT-LITERAL)
```

### Step 2: Check Operator Requirements
- Operator `||` is a logical operator (OR)
- Uses PERMISSIVE mode
- Accepts: int, real, boolean (via truthiness)

### Step 3: Truthiness Conversion
- `para_booleano(0.0, real) = false` (zero is false)
- `para_booleano(5, int) = true` (non-zero is true)

**Truthiness Table**:
| Value | Type | Truthiness |
|-------|------|------------|
| 0.0 | real | false |
| 5 | int | true |

### Step 4: Logical Evaluation
- Left (as boolean): `false`
- Right (as boolean): `true`
- `false || true = true`

### Step 5: Result Type
- All logical operators return: `boolean`
- `tipos_compativeis_logico(real, int) = TRUE`

### Step 6: Formal Derivation
```
Γ ⊢ 0.0 : real    Γ ⊢ 5 : int    para_booleano(0.0, real) = false    para_booleano(5, int) = true
────────────────────────────────────────────────────────────────────────────────────────────────── (OR)
                            Γ ⊢ (0.0 5 ||) : boolean
```

**Therefore**: `(0.0 5 ||)` has type `boolean` (evaluates to `true`).

---

## Q12: Unary NOT Operator ⭐

**Time Budget**: 2 minutes

**Question**: What is the type of `(0 !)` in postfix notation?

**Answer**:

### Step 1: Identify Operator
- Operator: `!` (NOT)
- Aridade: Unary (1 operand)
- Notation: Postfix `(operand !)`

### Step 2: Derive Operand Type
```
Γ ⊢ 0 : int    (INT-LITERAL)
```

### Step 3: Check Operator Requirements
- Operator `!` uses PERMISSIVE mode
- Accepts: int, real, boolean (via truthiness)

### Step 4: Truthiness Conversion
- `para_booleano(0, int) = false`
- NOT inverts: `!false = true`

### Step 5: Result Type
- Logical operators return: `boolean`

### Step 6: Formal Derivation
```
Γ ⊢ 0 : int    para_booleano(0, int) = false
──────────────────────────────────────────────── (NOT)
          Γ ⊢ (0 !) : boolean
```

**Therefore**: `(0 !)` has type `boolean` (evaluates to `true`).

---

## Q13: Chain of Additions ⭐⭐

**Time Budget**: 3 minutes

**Question**: Derive the type of `(((5 2 +) 3.0 +) 1 +)` explaining type promotion at each level.

**Answer**:

### Step 1: Evaluate Innermost - `(5 2 +)`
```
Γ ⊢ 5 : int
Γ ⊢ 2 : int
promover_tipo(int, int) = int

Γ ⊢ (5 2 +) : int
```
**Promotion**: None (both int)

### Step 2: Evaluate Middle - `((5 2 +) 3.0 +)`
```
Γ ⊢ <inner> : int    (from Step 1)
Γ ⊢ 3.0 : real       (REAL-LITERAL)

promover_tipo(int, real) = real

Γ ⊢ ((5 2 +) 3.0 +) : real
```
**Promotion**: int → real (due to 3.0)

### Step 3: Evaluate Outermost - `(((5 2 +) 3.0 +) 1 +)`
```
Γ ⊢ <middle> : real    (from Step 2)
Γ ⊢ 1 : int            (INT-LITERAL)

promover_tipo(real, int) = real

Γ ⊢ (((5 2 +) 3.0 +) 1 +) : real
```
**Promotion**: int → real (1 promoted to match real)

### Step 4: Type Promotion Summary

| Expression | Left Type | Right Type | Result Type | Promotion |
|------------|-----------|------------|-------------|-----------|
| `(5 2 +)` | int | int | int | None |
| `(<L1> 3.0 +)` | int | real | real | int → real |
| `(<L2> 1 +)` | real | int | real | int → real |

### Step 5: Derivation Tree
```
        Γ ⊢ 5:int  Γ ⊢ 2:int
        ──────────────────────
        Γ ⊢ (5 2 +):int         Γ ⊢ 3.0:real
        ──────────────────────────────────────
        Γ ⊢ ((5 2 +) 3.0 +):real              Γ ⊢ 1:int
        ──────────────────────────────────────────────────
              Γ ⊢ (((5 2 +) 3.0 +) 1 +) : real
```

**Key Principle**: Once a real appears, all subsequent results are real.

**Therefore**: `(((5 2 +) 3.0 +) 1 +)` has type `real`.

---

## Q14: Subtraction with Type Mixing ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(100.5 50 -)` has type `real`.

**Answer**:

### Step 1: Derive Left Operand
- Literal: 100.5
- Has decimal? YES (.5)
- `Γ ⊢ 100.5 : real` (REAL-LITERAL)

### Step 2: Derive Right Operand
- Literal: 50
- Has decimal? NO
- `Γ ⊢ 50 : int` (INT-LITERAL)

### Step 3: Check Operator Compatibility
- Operator `-` is PERMISSIVE
- Accepts: int/int, int/real, real/int, real/real
- Combination (real, int) is valid

### Step 4: Type Promotion
- `promover_tipo(real, int) = real`
- int is promoted to real to match left operand

### Step 5: Result Type Reasoning
- When mixing real and int, result is real
- Reason: Preserve precision (100.5 - 50 = 50.5, not 50)

### Step 6: Formal Derivation
```
────────────── (REAL)    ────────────── (INT)    promover_tipo(real, int) = real
 Γ ⊢ 100.5:real          Γ ⊢ 50 : int
──────────────────────────────────────────────────────────────────────────────────── (SUB-PROMOTE)
                    Γ ⊢ (100.5 50 -) : real
```

**Therefore**: `(100.5 50 -)` has type `real`.

---

## Q15: Integer Division Result ⭐⭐

**Time Budget**: 3 minutes

**Question**: Prove that `(15 7 /)` has type `int` and explain the division semantics.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 15 : int    (INT-LITERAL)
Γ ⊢ 7 : int     (INT-LITERAL)
```

### Step 2: Check Operator Requirements
- Operator `/` is STRICT
- ONLY accepts: int/int
- `tipos_compativeis_divisao_inteira(int, int) = TRUE`

### Step 3: Result Type
- Integer division always returns: `int`
- Result is the quotient, discarding remainder

### Step 4: Division Semantics
- `/` performs integer division (floor division)
- `15 / 7 = 2` (not 2.142857...)
- Remainder is discarded: `15 % 7 = 1`
- Mathematical: `15 = 7 * 2 + 1`

### Step 5: Comparison with Real Division
| Operator | Operands | Result Type | Example |
|----------|----------|-------------|---------|
| `/` | int/int ONLY | int | 15 / 7 = 2 |
| `\|` | any numeric | real | 15 \| 7 = 2.142857 |

### Step 6: Formal Derivation
```
────────────── (INT)    ────────────── (INT)
 Γ ⊢ 15 : int            Γ ⊢ 7 : int
──────────────────────────────────────────────── (DIV-INT)
          Γ ⊢ (15 7 /) : int
```

**Therefore**: `(15 7 /)` has type `int` (evaluates to 2).

---

## Q16: Power with Real Base ⭐⭐

**Time Budget**: 3 minutes

**Question**: Derive the type of `(2.0 5 ^)` and explain the exponent type requirement.

**Answer**:

### Step 1: Identify Operand Roles
- Base: 2.0
- Exponent: 5

### Step 2: Derive Types
```
Γ ⊢ 2.0 : real    (REAL-LITERAL - has .0)
Γ ⊢ 5 : int       (INT-LITERAL)
```

### Step 3: Check Power Operator Requirements

**Base Requirements**:
- Can be: `int` or `real`
- Current: `real` ✓

**Exponent Requirements**:
- MUST be: `int` (strict)
- MUST be: `> 0` (positive)
- Current: `5` (int, positive) ✓

### Step 4: Why Exponent Must Be Int?
**Reasons**:
1. **Termination**: Integer exponent ensures finite computation
2. **Determinism**: No complex/irrational results (unlike fractional exponents)
3. **Efficiency**: Simple multiplication loop (base * base * ... n times)
4. **No ambiguity**: 2^0.5 = √2 (irrational), 2^-1 = 1/2 (fractional)

### Step 5: Result Type Rule
- For power: `typeof(base^exp) = typeof(base)`
- Base is real → result is real
- `2.0^5 = 32.0` (not 32)

### Step 6: Formal Derivation
```
Γ ⊢ 2.0 : real    Γ ⊢ 5 : int    5 > 0
──────────────────────────────────────────────── (POWER)
          Γ ⊢ (2.0 5 ^) : real
```

**Therefore**: `(2.0 5 ^)` has type `real`.

---

# Category B: Error Detection (Q17-Q28)

## Q17: Division with Real Operand ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does `(10 3.5 /)` cause a semantic error? Provide the exact error message and explain the fix.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 10 : int     (INT-LITERAL)
Γ ⊢ 3.5 : real   (REAL-LITERAL - has .5)
```

### Step 2: Check Operator Requirements
- Operator `/` is STRICT
- ONLY accepts: `(int, int)`
- Current operands: `(int, real)` ❌

### Step 3: Compatibility Check
```
tipos_compativeis_divisao_inteira(int, real) = FALSE
```
**Reason**: Second operand is real, but `/` requires both to be int

### Step 4: Error Details
- **Error Type**: `tipo` (type error)
- **Error Message**: `"Operador '/' requer operandos inteiros (recebeu int e real)"`
- **Line**: Where `(10 3.5 /)` appears
- **Context**: Shows types of both operands

### Step 5: How to Fix

**Option 1**: Use real division operator `|`
```
(10 3.5 |)    → type: real
```
✓ Accepts any numeric types

**Option 2**: Convert operand to int
```
(10 3 /)      → type: int
```
✓ Both operands now int

**Which is better?**
- If you want fractional result: Use Option 1 (`|`)
- If you want integer quotient: Use Option 2 (change 3.5 to 3)

### Step 6: Implementation Location
- **File**: `src/RA3/functions/python/tipos.py`
- **Function**: `tipos_compativeis_divisao_inteira()`
- **Check**: Returns `False` if either operand is not int

**Therefore**: `(10 3.5 /)` fails because `/` requires both operands to be integers.

---

## Q18: Power with Real Exponent ⭐⭐

**Time Budget**: 3 minutes

**Question**: Explain why `(2 3.0 ^)` is a semantic error.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 2 : int       (INT-LITERAL)
Γ ⊢ 3.0 : real    (REAL-LITERAL - has .0)
```

### Step 2: Identify Operand Roles
- Base: 2 (type: int) ✓
- Exponent: 3.0 (type: real) ❌

### Step 3: Check Power Operator Requirements
- Base: Can be int or real ✓
- Exponent: MUST be int (strict) ❌
- Exponent: MUST be > 0 ✓

**Violation**: Exponent is real, not int

### Step 4: Compatibility Check
```
tipos_compativeis_potencia(int, real) = FALSE
```
**Reason**: Second operand (exponent) must be int, but received real

### Step 5: Error Details
- **Error Message**: `"Operador '^' requer expoente inteiro (recebeu real)"`
- **Error Type**: `tipo`
- **Violated Rule**: POWER operator exponent type restriction

### Step 6: Why This Restriction?
**Reasons**:
1. **Complexity**: `2^3.0 = 2^(3.0)` could yield complex numbers if generalized
2. **Ambiguity**: Real exponents can have multiple interpretations
3. **Efficiency**: Integer exponents allow simple multiplication loop
4. **Specification**: Language design choice to avoid floating-point exponentiation

### Step 7: How to Fix
```
(2 3 ^)    → type: int  (change 3.0 to 3)
```
✓ Exponent is now int

**Therefore**: `(2 3.0 ^)` fails because the exponent must be an integer.

---

## Q19: Negative Exponent ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does `(5 -2 ^)` cause an error even though the exponent is an integer?

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 5 : int      (INT-LITERAL)
Γ ⊢ -2 : int     (INT-LITERAL - negative)
```

### Step 2: Check Power Operator Requirements

**Base**: int or real ✓
**Exponent Type**: int ✓
**Exponent Sign**: MUST be > 0 ❌

### Step 3: Error Details
- **Violated Requirement**: Exponent must be POSITIVE
- **Current Exponent**: -2 (negative)
- **Error Message**: `"Operador '^' requer expoente positivo (recebeu -2)"`

### Step 4: Why Positive Only?
**Reasons**:
1. **Type Consistency**: Negative exponents produce fractions
   - `5^-2 = 1/(5^2) = 1/25 = 0.04`
   - Result would need to be real, but base is int
2. **Avoid Division**: Negative exponents require division, which may not preserve type
3. **Specification**: Simplifies type inference (result type = base type)

### Step 5: Type Inconsistency Example
```
If allowed: (5 -2 ^)
  5 is int
  typeof(base) = int
  But 5^-2 = 0.04 (real)
  Type mismatch!
```

### Step 6: How to Fix

**Option 1**: Use positive exponent
```
(5 2 ^)    → type: int  (5^2 = 25)
```

**Option 2**: Compute reciprocal separately
```
(1 (5 2 ^) |)    → type: real  (1 / 25 = 0.04)
```

**Therefore**: `(5 -2 ^)` fails because the exponent must be positive (> 0).

---

## Q20: MEM with Boolean Value ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why is `((5 3 >) X)` a semantic error?

**Answer**:

### Step 1: Evaluate Value to Store
```
Expression: (5 3 >)

Γ ⊢ 5 : int
Γ ⊢ 3 : int
Γ ⊢ (5 3 >) : boolean    (comparison returns boolean)
```

### Step 2: Identify MEM Operation
- Pattern: `(value VAR)`
- Operation: `MEM_STORE`
- Value: `(5 3 >)` → Type: `boolean`
- Variable: `X`

### Step 3: Check MEM Restrictions
**MEM can store**:
- int ✓
- real ✓
- boolean ❌

**Current value type**: `boolean` (NOT ALLOWED)

### Step 4: Error Details
- **Error Message**: `"MEM não aceita valor do tipo boolean (apenas int ou real)"`
- **Error Type**: `memoria`
- **Violated Rule**: MEM_STORE type restriction

### Step 5: Why Boolean Not Allowed?
**Reasons**:
1. **Memory Model**: Variables represent numeric computations
2. **Type Safety**: Boolean operations should not persist in memory
3. **Specification**: Explicit restriction in language design (Section 18.7.3)

### Step 6: Common Mistake
**Incorrect Fix**: Try to convert boolean to int
```
(para_booleano((5 3 >)) X)    ❌ Invalid
```
**Reason**: `para_booleano()` converts TO boolean, not FROM boolean

### Step 7: Correct Fixes

**Option 1**: Store the comparison operands
```
(5 X)    → stores 5 (int)
```

**Option 2**: Store a numeric value instead
```
(100 X)    → stores 100 (int)
```

**Option 3**: Use IFELSE to convert boolean to numeric
```
(((5 3 >) (1) (0) IFELSE) X)    → stores 1 or 0 (int)
```

**Therefore**: `((5 3 >) X)` fails because MEM cannot store boolean values.

---

## Q21: Uninitialized Variable Usage ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does the program below cause an error on Line 2?
```
Line 1: ( 10 X )
Line 2: ( Y )
```

**Answer**:

### Step 1: Analyze Line 1
```
Expression: ( 10 X )
Operation: MEM_STORE
Value: 10 (int)
Variable: X

Symbol Table Update:
Γ₁ = {
  X: {tipo: int, inicializada: true, linha_declaracao: 1}
}
```

### Step 2: Analyze Line 2
```
Expression: ( Y )
Operation: MEM_LOAD (retrieve variable value)
Variable: Y
```

### Step 3: Validation Checks

**Check 1**: Does Y exist in symbol table?
```
Γ₁.buscar("Y") = None    ❌
```

**Check 2**: Is Y initialized?
```
Γ₁.verificar_inicializacao("Y")    → raises error
```

### Step 4: Error Details
- **Error Type**: `memoria`
- **Error Message**: `"Variável 'Y' não declarada ou não inicializada"`
- **Location**: Line 2
- **Context**: `( Y )`

### Step 5: Why This Is an Error
**Reason**: Using uninitialized variables leads to undefined behavior
- Variable Y has never been assigned a value
- Cannot determine Y's type
- Cannot retrieve Y's value

### Step 6: Symbol Table State
```
Γ₁ = {X: (int, inicializada=true)}

Lookup for Y:
  Y ∉ Γ₁    (Y not in symbol table)
  Error!
```

### Step 7: How to Fix

**Add declaration before Line 2**:
```
Line 1: ( 10 X )
Line 1.5: ( <value> Y )    ← Add this line
Line 2: ( Y )
```

Example:
```
Line 1: ( 10 X )
Line 2: ( 20 Y )    ← Initialize Y
Line 3: ( Y )       ← Now valid
```

**Implementation**:
- **File**: `src/RA3/functions/python/tabela_simbolos.py`
- **Function**: `verificar_inicializacao()`
- **Raises**: `ErroSemantico` when variable not found or not initialized

**Therefore**: Line 2 fails because variable Y is used before being declared/initialized.

---

## Q22: Invalid RES Reference ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does `(10 RES)` on Line 1 cause an error?

**Answer**:

### Step 1: Identify Operation
```
Expression: ( 10 RES )
Operation: RES (reference previous line result)
RES Argument: 10
Current Line: 1
```

### Step 2: Calculate Referenced Line
```
Referenced Line = Current Line - RES Argument
Referenced Line = 1 - 10 = -9
```

### Step 3: Validate RES Reference

**Requirement**: Referenced line must satisfy:
```
1 ≤ referenced_line < current_line
```

**Current Situation**:
```
referenced_line = -9
-9 < 1    ❌ Violates lower bound
```

### Step 4: Error Details
- **Error Type**: `memoria`
- **Error Message**: `"Referência RES aponta para linha inexistente (-9)"`
- **Violated Rule**: RES reference must be within valid range

### Step 5: Valid RES Range

For a given line N, valid RES arguments are:
```
1 ≤ (N - argument) < N
⟹ 1 ≤ argument ≤ N - 1
```

**Line 1**: No valid RES arguments (no previous lines)
**Line 2**: Valid RES arguments: {1}
**Line 3**: Valid RES arguments: {1, 2}
**Line 10**: Valid RES arguments: {1, 2, 3, ..., 9}

### Step 6: Why This Restriction?
**Reasons**:
1. **Causality**: Can't reference future lines (not yet computed)
2. **Existence**: Can't reference non-existent lines (before Line 1)
3. **Type Safety**: Referenced line must have been type-checked

### Step 7: Example Valid RES Usage
```
Line 1: ( 5 3 + )        → type: int
Line 2: ( 1 RES 2 * )    → references Line 1 (1-1=0... wait, that's wrong)
```

**Correction**:
```
Line 1: ( 5 3 + )        → type: int
Line 2: ( 1 RES 2 * )    → references Line (2-1) = 1 ✓
```

**Therefore**: `(10 RES)` on Line 1 fails because it references Line -9, which doesn't exist.

---

## Q23: IFELSE with Incompatible Branches ⭐⭐

**Time Budget**: 4 minutes

**Question**: Why does `((X 0 >) (100) ((Y 5 <)) IFELSE)` cause an error?

**Answer**:

### Assume:
```
Γ = {X: (int, inicializada), Y: (int, inicializada)}
```

### Step 1: Evaluate Condition
```
Expression: (X 0 >)

Γ ⊢ X : int       (from symbol table)
Γ ⊢ 0 : int       (INT-LITERAL)
Γ ⊢ (X 0 >) : boolean    (comparison)
```

### Step 2: Evaluate True Branch
```
Expression: (100)

Γ ⊢ 100 : int    (INT-LITERAL)
```

### Step 3: Evaluate False Branch
```
Expression: ((Y 5 <))

Γ ⊢ Y : int       (from symbol table)
Γ ⊢ 5 : int       (INT-LITERAL)
Γ ⊢ (Y 5 <) : boolean    (comparison)
```

### Step 4: Check Branch Compatibility
```
True branch type: int
False branch type: boolean

promover_tipo(int, boolean) = None    ❌
```

**Reason**: int and boolean are incompatible types - no type promotion exists

### Step 5: Error Details
- **Error Type**: `controle`
- **Error Message**: `"Branches de IFELSE incompatíveis: int e boolean"`
- **Violated Rule**: IFELSE-COMPATIBLE

### Step 6: IFELSE Branch Compatibility Rule
**Requirement**: `promover_tipo(tipo_then, tipo_else) ≠ None`

**Compatible Pairs**:
- int + int → int ✓
- int + real → real ✓
- real + real → real ✓

**Incompatible Pairs**:
- int + boolean → None ❌
- real + boolean → None ❌

### Step 7: Why This Restriction?
**Reason**: IFELSE must have deterministic type
- If branches have different incompatible types, what is IFELSE's type?
- Can't promote int to boolean or vice versa
- Type system would be unsound

### Step 8: How to Fix

**Option 1**: Make both branches int
```
((X 0 >) (100) (50) IFELSE)    → type: int
```

**Option 2**: Make both branches boolean
```
((X 0 >) ((X 10 >)) ((Y 5 <)) IFELSE)    → type: boolean
```

**Option 3**: Convert boolean to int via nested IFELSE
```
((X 0 >) (100) ((((Y 5 <)) (1) (0) IFELSE)) IFELSE)    → type: int
```

**Therefore**: The expression fails because IFELSE branches must be compatible types (int and boolean are not).

---

## Q24: FOR with Real Parameters ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does `(1.0 10.0 1.0 (X 2 *) FOR)` cause an error?

**Answer**:

### Step 1: Identify FOR Parameters
```
Init: 1.0
End: 10.0
Step: 1.0
Body: (X 2 *)
```

### Step 2: Derive Parameter Types
```
Γ ⊢ 1.0 : real     (REAL-LITERAL - has .0)
Γ ⊢ 10.0 : real    (REAL-LITERAL - has .0)
Γ ⊢ 1.0 : real     (REAL-LITERAL - has .0)
```

### Step 3: Check FOR Requirements
**FOR Requires**:
- Init: int ❌ (received real)
- End: int ❌ (received real)
- Step: int ❌ (received real)

**Current**: (real, real, real) - ALL WRONG

### Step 4: Error Details
- **Error Type**: `controle`
- **Error Message**: `"FOR requer início, fim e passo inteiros (recebeu real, real, real)"`
- **Violated Rule**: FOR-INT-PARAMS

### Step 5: Why Integers Only?
**Reasons**:
1. **Loop Counter**: FOR uses integer-based iteration
2. **Termination**: Integer steps ensure predictable termination
3. **Precision**: Avoid floating-point precision issues in loop counter
   - Example: `1.0, 1.1, 1.2, ..., 2.0` vs `1.0, 1.0+ε, 1.0+2ε, ...` (rounding errors)
4. **Simplicity**: Integer loops are deterministic

### Step 6: Floating-Point Loop Problem
```
Example:
for i = 0.0; i < 1.0; i += 0.1:
  Iterations: 0.0, 0.1, 0.2, ..., 0.9, 1.0 (11 iterations?)
  But 0.1 + 0.1 + ... (10 times) ≠ 1.0 exactly (floating-point error)
  Loop may execute 10 or 11 times depending on rounding!
```

### Step 7: How to Fix
```
(1 10 1 (X 2 *) FOR)    → type: int
```
Change all parameters to integers:
- Init: `1.0` → `1`
- End: `10.0` → `10`
- Step: `1.0` → `1`

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_memoria_controle.py`
- **Function**: `analisarSemanticaControle()`
- **Check**: Validates init, end, step are all int

**Therefore**: FOR fails because all three parameters (init, end, step) must be integers.

---

## Q25: Modulo with Real Operand ⭐⭐

**Time Budget**: 3 minutes

**Question**: Explain why `(10.5 3 %)` is invalid.

**Answer**:

### Step 1: Derive Operand Types
```
Γ ⊢ 10.5 : real    (REAL-LITERAL - has .5)
Γ ⊢ 3 : int        (INT-LITERAL)
```

### Step 2: Check Operator Requirements
- Operator `%` (modulo) is STRICT
- ONLY accepts: `(int, int)`
- Current: `(real, int)` ❌

### Step 3: Compatibility Check
```
tipos_compativeis_divisao_inteira(real, int) = FALSE
```

**Violation**: First operand is real, but `%` requires both to be int

### Step 4: Error Details
- **Error Message**: `"Operador '%' requer operandos inteiros (recebeu real e int)"`
- **Error Type**: `tipo`

### Step 5: Why Modulo Requires Integers
**Mathematical Definition**:
```
a % b = a - (a / b) * b
```
where `/` is integer division

**Example**:
```
10 % 3 = 10 - (10 / 3) * 3
       = 10 - 3 * 3
       = 10 - 9
       = 1
```

**For Real Numbers**:
```
10.5 % 3 = 10.5 - (10.5 / 3) * 3
         = 10.5 - ??? * 3
```
What is `10.5 / 3`?
- If integer division: `3` (incorrect - loses fractional part)
- If real division: `3.5` → `10.5 - 3.5 * 3 = 10.5 - 10.5 = 0` (not the expected remainder)

**Real Modulo is Ambiguous**:
- Different interpretations (truncated, floored, Euclidean)
- No standard definition for real operands in this language

### Step 6: How to Fix
```
(10 3 %)    → type: int  (change 10.5 to 10)
```

**Note**: If you need "remainder" for reals, use:
```
(10.5 (10.5 3 | 3 *) -)    → real division-based "remainder"
```
But this is NOT standard modulo.

**Therefore**: `(10.5 3 %)` fails because modulo requires both operands to be integers.

---

## Q26: Division by Zero (Semantic vs Runtime) ⭐⭐

**Time Budget**: 3 minutes

**Question**: Is `(10 0 /)` a semantic error or a runtime error? Explain.

**Answer**:

### Step 1: Perform Semantic Analysis

**Derive Operand Types**:
```
Γ ⊢ 10 : int    (INT-LITERAL)
Γ ⊢ 0 : int     (INT-LITERAL)
```

**Check Operator Compatibility**:
```
Operator / is STRICT
Requires: (int, int)
Current: (int, int) ✓

tipos_compativeis_divisao_inteira(int, int) = TRUE
```

**Result Type**:
```
Γ ⊢ (10 0 /) : int
```

### Step 2: Semantic Validation Result
**Semantic Analysis**: PASSES ✓
- Both operands are int
- Type compatibility satisfied
- Type inference successful: `int`

### Step 3: Error Classification

**Semantic Error**: Violations of type/scope/initialization rules
- Examples: type mismatch, uninitialized variables, incompatible branches

**Runtime Error**: Violations of execution constraints
- Examples: division by zero, arithmetic overflow, null pointer

### Step 4: Why Division by Zero is NOT a Semantic Error

**Reason**: The divisor's VALUE (0) is a runtime property, not a type property
- Semantic analysis checks TYPES, not VALUES
- 0 is a valid `int` literal
- Type system cannot predict divisor will be zero at runtime

**Analogy**:
```
(X 0 /)    ← X is int (valid type), but might be 0 at runtime
```

### Step 5: Detection Timing

| Phase | Checks | Can Detect Division by Zero? |
|-------|--------|------------------------------|
| Lexical | Tokens | No |
| Syntactic | Grammar | No |
| **Semantic** | **Types** | **No (only types, not values)** |
| Code Generation | Emit code | No |
| **Runtime** | **Execute code** | **Yes (when divisor is 0)** |

### Step 6: Conclusion

**Answer**: `(10 0 /)` is a **RUNTIME ERROR**, NOT a semantic error.

**Semantic Analysis Result**:
- Type: `int` ✓
- Compatibility: Valid ✓
- No semantic errors detected

**Runtime Execution**:
- Attempts to compute `10 / 0`
- Division by zero exception raised
- Program terminates with runtime error

**Implementation Note**:
- RA3 semantic analyzer does NOT check for division by zero
- This is expected behavior (semantic analysis is about types, not values)
- A more advanced compiler might add constant folding to detect this at compile-time, but it's not required for RA3

**Therefore**: `(10 0 /)` passes semantic analysis but fails at runtime.

---

## Q27: Comparison with Boolean (Type Error) ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why doesn't `((5 3 >) 10 >)` type-check correctly?

**Answer**:

### Step 1: Evaluate Inner Expression
```
Expression: (5 3 >)

Γ ⊢ 5 : int
Γ ⊢ 3 : int
Γ ⊢ (5 3 >) : boolean    (comparison returns boolean)
```

### Step 2: Evaluate Outer Expression
```
Expression: (<inner> 10 >)

Γ ⊢ <inner> : boolean    (from Step 1)
Γ ⊢ 10 : int             (INT-LITERAL)
```

### Step 3: Check Operator Compatibility
```
Operator: >
Left operand: boolean
Right operand: int

Requirement: Both operands must be numeric (int or real)
```

**Compatibility Check**:
```
tipos_compativeis_comparacao(boolean, int) = FALSE
```

### Step 4: Error Details
- **Error Type**: `tipo`
- **Error Message**: `"Operador '>' requer operandos numéricos (recebeu boolean e int)"`
- **Violated Rule**: Comparison operators only accept numeric types

### Step 5: Why Boolean Not Allowed?
**Reason**: Comparison operators are for numeric ordering
- `>` means "greater than" (numeric comparison)
- Boolean values (true/false) have no inherent ordering
- What does `true > 10` mean? Undefined!

**Note**: Some languages allow boolean comparison (true > false), but this language restricts comparison to numeric types only.

### Step 6: Logical vs Comparison Operators

| Operator Type | Accepts | Returns |
|---------------|---------|---------|
| Comparison (`>`, `<`, ...) | int, real | boolean |
| Logical (`&&`, `\|\|`, `!`) | int, real, boolean (via truthiness) | boolean |

**Key Difference**: Logical operators use permissive mode (accept boolean), comparison operators do NOT.

### Step 7: How to Fix

**Option 1**: Remove inner comparison (compare numbers directly)
```
(5 10 >)    → type: boolean
```

**Option 2**: Use logical operator if combining boolean expressions
```
((5 3 >) (X 10 >) &&)    → type: boolean
```

**Therefore**: `((5 3 >) 10 >)` fails because comparison operators require numeric operands, not boolean.

---

## Q28: WHILE with Non-Boolean Condition (Permissive Mode) ⭐⭐

**Time Budget**: 3 minutes

**Question**: Is `(5 (X 1 +) WHILE)` valid? Explain the condition type requirement.

**Answer**:

### Step 1: Identify WHILE Components
```
Condition: 5
Body: (X 1 +)
```

### Step 2: Evaluate Condition
```
Γ ⊢ 5 : int    (INT-LITERAL)
```

### Step 3: Check WHILE Requirements
**WHILE Condition**:
- Must be "boolean-compatible"
- Uses PERMISSIVE mode
- Accepts: int, real, boolean (via truthiness)

### Step 4: Truthiness Conversion
```
Condition type: int
para_booleano(5, int) = true    (non-zero is true)
```

**Truthiness Table**:
| Value | Type | Truthiness |
|-------|------|------------|
| 0 | int | false |
| 5 | int | **true** |
| 0.0 | real | false |
| 3.5 | real | true |
| true | boolean | true |
| false | boolean | false |

### Step 5: Validation Result
**Answer**: YES, `(5 (X 1 +) WHILE)` is VALID ✓

**Reason**: WHILE uses permissive mode for condition
- Condition type: `int`
- Converted to boolean: `true`
- Loop will execute (infinite loop, since condition is always true!)

### Step 6: Formal Derivation
```
Γ ⊢ 5 : int    para_booleano(5, int) = true    Γ ⊢ (X 1 +) : int
──────────────────────────────────────────────────────────────────── (WHILE)
              Γ ⊢ (5 (X 1 +) WHILE) : int
```

**Result Type**: WHILE returns type of body = `int`

### Step 7: Practical Consideration
**Warning**: This creates an infinite loop!
- Condition is literal `5` (always true)
- Loop will never terminate
- This is semantically valid but logically problematic

**Better Example**:
```
((X 10 <) (((X 1 +) X)) WHILE)    ← Condition depends on X, can terminate
```

### Step 8: Comparison with IFELSE and FOR

| Control Structure | Condition Type | Permissive? |
|-------------------|----------------|-------------|
| IFELSE | boolean-compatible | YES (int/real/boolean) |
| WHILE | boolean-compatible | YES (int/real/boolean) |
| FOR | int (init, end, step) | NO (strict int) |

**Therefore**: `(5 (X 1 +) WHILE)` is semantically valid - WHILE accepts numeric conditions via truthiness conversion.

---

# Category C: Control Structures (Q29-Q36)

## Q29: IFELSE Type Inference ⭐⭐

**Time Budget**: 4 minutes

**Question**: Derive the type of `((X 5 >) (10.5) (20) IFELSE)` given `Γ = {X: (int, inicializada)}`.

**Answer**:

### Step 1: Evaluate Condition
```
Expression: (X 5 >)

Γ ⊢ X : int       (from symbol table)
Γ ⊢ 5 : int       (INT-LITERAL)
Γ ⊢ (X 5 >) : boolean    (comparison)
```

### Step 2: Evaluate True Branch
```
Expression: (10.5)

Γ ⊢ 10.5 : real    (REAL-LITERAL - has .5)
```

### Step 3: Evaluate False Branch
```
Expression: (20)

Γ ⊢ 20 : int    (INT-LITERAL)
```

### Step 4: Check Branch Compatibility
```
True branch type: real
False branch type: int

promover_tipo(real, int) = real    ✓
```

**Compatibility**: YES
- int is promoted to real
- Compatible pair: real + int → real

### Step 5: Infer IFELSE Type
```
IFELSE type = promover_tipo(tipo_then, tipo_else)
IFELSE type = promover_tipo(real, int)
IFELSE type = real
```

### Step 6: Formal Derivation
```
Γ ⊢ X : int    Γ ⊢ 5 : int
────────────────────────────────────── (COMP-GT)
     Γ ⊢ (X 5 >) : boolean

Γ ⊢ 10.5 : real    Γ ⊢ 20 : int    promover_tipo(real, int) = real
─────────────────────────────────────────────────────────────────── (IFELSE)
        Γ ⊢ ((X 5 >) (10.5) (20) IFELSE) : real
```

### Step 7: Complete Derivation Tree
```
Γ ⊢ X:int  Γ ⊢ 5:int
──────────────────────
Γ ⊢ (X 5 >):boolean      Γ ⊢ 10.5:real  Γ ⊢ 20:int  promover_tipo(real,int)=real
────────────────────────────────────────────────────────────────────────────────────
                 Γ ⊢ ((X 5 >) (10.5) (20) IFELSE) : real
```

**Therefore**: `((X 5 >) (10.5) (20) IFELSE)` has type `real`.

---

## Q30: WHILE Type Inference ⭐⭐

**Time Budget**: 3 minutes

**Question**: What is the type of `((COUNTER 5 <) (((COUNTER 1 +) COUNTER)) WHILE)` given `Γ = {COUNTER: (int, inicializada)}`?

**Answer**:

### Step 1: Evaluate Condition
```
Expression: (COUNTER 5 <)

Γ ⊢ COUNTER : int    (from symbol table)
Γ ⊢ 5 : int          (INT-LITERAL)
Γ ⊢ (COUNTER 5 <) : boolean    (comparison)
```

### Step 2: Evaluate Body (Outer Level)
```
Expression: (((COUNTER 1 +) COUNTER))

This is a MEM_STORE operation nested in extra parentheses
Inner: ((COUNTER 1 +) COUNTER)
```

### Step 3: Evaluate Body Inner Expression
```
Expression: (COUNTER 1 +)

Γ ⊢ COUNTER : int
Γ ⊢ 1 : int
promover_tipo(int, int) = int

Γ ⊢ (COUNTER 1 +) : int
```

### Step 4: Evaluate MEM_STORE
```
Expression: ((COUNTER 1 +) COUNTER)
Pattern: (value VAR)

Value: (COUNTER 1 +) → type: int
Variable: COUNTER

MEM_STORE type: int (type of value being stored)
```

### Step 5: WHILE Type Rule
```
WHILE type = typeof(body)
Body type = int (from Step 4)
WHILE type = int
```

### Step 6: Formal Derivation
```
Γ ⊢ (COUNTER 5 <) : boolean    Γ ⊢ ((COUNTER 1 +) COUNTER) : int
─────────────────────────────────────────────────────────────────── (WHILE)
      Γ ⊢ ((COUNTER 5 <) (((COUNTER 1 +) COUNTER)) WHILE) : int
```

**Key Point**: WHILE returns the type of its body (not the condition type).

**Therefore**: The WHILE expression has type `int`.

---

## Q31: FOR Type Inference ⭐⭐

**Time Budget**: 4 minutes

**Question**: Derive the type of `(1 10 1 ((I 2 *)) FOR)` given `Γ = {I: (int, inicializada)}`.

**Answer**:

### Step 1: Identify FOR Parameters
```
Init: 1
End: 10
Step: 1
Body: ((I 2 *))
```

### Step 2: Validate Parameters
```
Γ ⊢ 1 : int     (INT-LITERAL)
Γ ⊢ 10 : int    (INT-LITERAL)
Γ ⊢ 1 : int     (INT-LITERAL)

FOR requirements: All parameters must be int ✓
```

### Step 3: Evaluate Body
```
Expression: ((I 2 *))

Γ ⊢ I : int      (from symbol table)
Γ ⊢ 2 : int      (INT-LITERAL)

promover_tipo(int, int) = int

Γ ⊢ (I 2 *) : int
```

### Step 4: FOR Type Rule
```
FOR type = typeof(body)
Body type = int
FOR type = int
```

### Step 5: Formal Derivation
```
Γ ⊢ 1:int  Γ ⊢ 10:int  Γ ⊢ 1:int  Γ ⊢ ((I 2 *)):int
──────────────────────────────────────────────────────── (FOR)
        Γ ⊢ (1 10 1 ((I 2 *)) FOR) : int
```

### Step 6: FOR Semantics Explanation
- **Init**: Loop variable starts at 1
- **End**: Loop runs while variable ≤ 10
- **Step**: Variable increments by 1 each iteration
- **Body**: Executes `(I 2 *)` for I = 1, 2, 3, ..., 10
- **Result**: Type is type of body (int)

**Therefore**: `(1 10 1 ((I 2 *)) FOR)` has type `int`.

---

## Q32: Nested IFELSE ⭐⭐⭐

**Time Budget**: 5 minutes

**Question**: Derive the type of `((X 0 >) (((Y 5 <) (10) (20) IFELSE)) (30) IFELSE)` given `Γ = {X: (int, inicializada), Y: (int, inicializada)}`.

**Answer**:

### Step 1: Identify Structure
```
Outer IFELSE:
  Condition: (X 0 >)
  True branch: ((Y 5 <) (10) (20) IFELSE)    ← Inner IFELSE
  False branch: (30)
```

### Step 2: Evaluate Outer Condition
```
Expression: (X 0 >)

Γ ⊢ X : int
Γ ⊢ 0 : int
Γ ⊢ (X 0 >) : boolean
```

### Step 3: Evaluate True Branch (Inner IFELSE)

**Inner IFELSE Structure**:
```
Condition: (Y 5 <)
True branch: (10)
False branch: (20)
```

**Inner Condition**:
```
Γ ⊢ Y : int
Γ ⊢ 5 : int
Γ ⊢ (Y 5 <) : boolean
```

**Inner Branches**:
```
Γ ⊢ 10 : int
Γ ⊢ 20 : int
promover_tipo(int, int) = int
```

**Inner IFELSE Type**:
```
Γ ⊢ ((Y 5 <) (10) (20) IFELSE) : int
```

### Step 4: Evaluate Outer False Branch
```
Γ ⊢ 30 : int
```

### Step 5: Check Outer Branch Compatibility
```
Outer true branch: int (from Step 3)
Outer false branch: int (from Step 4)

promover_tipo(int, int) = int    ✓
```

### Step 6: Infer Outer IFELSE Type
```
Outer IFELSE type = promover_tipo(int, int) = int
```

### Step 7: Complete Derivation Tree
```
              [Inner IFELSE]
Γ ⊢ Y:int  Γ ⊢ 5:int           Γ ⊢ 10:int  Γ ⊢ 20:int
──────────────────────          ────────────────────────
Γ ⊢ (Y 5 <):boolean             promover_tipo(int, int)=int
────────────────────────────────────────────────────────────────
        Γ ⊢ ((Y 5 <) (10) (20) IFELSE) : int

                            [Outer IFELSE]
Γ ⊢ X:int  Γ ⊢ 0:int       Γ ⊢ <inner>:int  Γ ⊢ 30:int
──────────────────────     ──────────────────────────────
Γ ⊢ (X 0 >):boolean        promover_tipo(int, int)=int
────────────────────────────────────────────────────────────────────
  Γ ⊢ ((X 0 >) ((Y 5 <) (10) (20) IFELSE) (30) IFELSE) : int
```

**Therefore**: The nested IFELSE has type `int`.

---

## Q33: WHILE with RES Reference ⭐⭐⭐

**Time Budget**: 5 minutes

**Question**: Derive the type of the following program:
```
Line 1: ( 10 X )
Line 2: ( (X 0 >) (((X 1 -) X) (1 RES)) WHILE )
```

**Answer**:

### Step 1: Analyze Line 1
```
Expression: ( 10 X )
Operation: MEM_STORE

Γ ⊢ 10 : int
Store in X

Γ₁ = {X: (int, inicializada, linha_declaracao=1)}
```

### Step 2: Analyze Line 2 - Condition
```
Expression: (X 0 >)

Γ₁ ⊢ X : int      (from symbol table)
Γ₁ ⊢ 0 : int
Γ₁ ⊢ (X 0 >) : boolean
```

### Step 3: Analyze Line 2 - Body Structure
```
Body: (((X 1 -) X) (1 RES))

This is a sequence with two subexpressions:
1. ((X 1 -) X)      ← MEM_STORE
2. (1 RES)          ← RES reference
```

### Step 4: Evaluate Body Part 1 - MEM_STORE
```
Expression: ((X 1 -) X)

Inner expression: (X 1 -)
  Γ₁ ⊢ X : int
  Γ₁ ⊢ 1 : int
  promover_tipo(int, int) = int
  Γ₁ ⊢ (X 1 -) : int

MEM_STORE:
  Value: (X 1 -) → type: int
  Variable: X
  Type: int
```

### Step 5: Evaluate Body Part 2 - RES Reference
```
Expression: (1 RES)
Current line: 2
Referenced line: 2 - 1 = 1

Line 1 type: int (from Step 1, value stored was 10)

Γ₁ ⊢ (1 RES) : int
```

### Step 6: Determine Body Type
```
Body consists of sequence: MEM_STORE then RES
Body type = type of last expression = int
```

### Step 7: Infer WHILE Type
```
WHILE type = typeof(body) = int
```

### Step 8: Complete Derivation for Line 2
```
Γ₁ ⊢ (X 0 >) : boolean    Γ₁ ⊢ (((X 1 -) X) (1 RES)) : int
─────────────────────────────────────────────────────────────── (WHILE)
    Γ₁ ⊢ ((X 0 >) (((X 1 -) X) (1 RES)) WHILE) : int
```

### Step 9: Symbol Table Evolution
```
Γ₀ = {}
Γ₁ = {X: (int, inicializada, linha_declaracao=1)}    (after Line 1)
Γ₂ = {X: (int, inicializada, linha_ultimo_uso=2)}    (after Line 2)
```

**Therefore**: Line 2 has type `int`.

---

## Q34: FOR Loop Variable Scope ⭐⭐

**Time Budget**: 4 minutes

**Question**: Explain the type and symbol table behavior of:
```
Line 1: ( (1) (10) (1) ( (I 2 *) ) FOR )
Line 2: ( I )
```

**Answer**:

### Step 1: Analyze Line 1 - FOR Parameters
```
Init: (1) → Γ ⊢ 1 : int
End: (10) → Γ ⊢ 10 : int
Step: (1) → Γ ⊢ 1 : int

All parameters are int ✓
```

### Step 2: Analyze Line 1 - FOR Body
```
Expression: ( (I 2 *) )

Γ ⊢ I : int      (I is the loop variable)
Γ ⊢ 2 : int
promover_tipo(int, int) = int

Γ ⊢ (I 2 *) : int
```

### Step 3: FOR Type
```
FOR type = typeof(body) = int

Γ ⊢ ((1) (10) (1) ((I 2 *)) FOR) : int
```

### Step 4: Symbol Table After Line 1

**Question**: Is I added to symbol table?

**Answer**: Depends on implementation:
- **Option A**: I is implicitly declared within FOR scope (loop variable)
  - `Γ₁ = {I: (int, inicializada, escopo_FOR)}`
  - I only visible within FOR body
- **Option B**: I must be declared before FOR
  - FOR does NOT declare I
  - I must exist in Γ₀

**Specification Clarification**:
Looking at the test files and specification, FOR does NOT automatically declare I. The loop variable I must already exist in the symbol table (or be implicitly available).

**Assuming Specification Option B**:
```
Γ₀ = {} (or {I: ...} if pre-declared)
Γ₁ = {} (FOR doesn't add I to table)
```

### Step 5: Analyze Line 2
```
Expression: ( I )
Operation: MEM_LOAD

Check: Does I exist in Γ₁?
```

**If Option A (I implicitly declared in FOR)**:
- I was in FOR scope
- FOR scope ended after Line 1
- I NOT visible on Line 2
- **Error**: Variable 'I' not declared

**If Option B (I must be pre-declared)**:
- If I was declared before Line 1: Line 2 is valid
- If I was NOT declared: Line 1 already failed (I undefined in FOR body)

### Step 6: Expected Behavior

**Based on RA3 specification**: Variables must be explicitly declared via MEM_STORE before use.

**Correct Program**:
```
Line 1: ( 0 I )                           ← Declare I
Line 2: ( (1) (10) (1) ( (I 2 *) ) FOR )  ← Use I in FOR
Line 3: ( I )                             ← Use I (still in scope)
```

**Line 2 in original program**: Likely **ERROR** (I not declared).

**Therefore**: Line 2 causes an error unless I was explicitly declared before Line 1.

---

## Q35: IFELSE with Both Branches as Expressions ⭐⭐⭐

**Time Budget**: 5 minutes

**Question**: Derive the type of `(((A 10 >) (B 5 >) &&) (((A B +) 2.0 |)) ((A B *)) IFELSE)` given `Γ = {A: (int, inicializada), B: (int, inicializada)}`.

**Answer**:

### Step 1: Evaluate Condition - Outer AND
```
Expression: ((A 10 >) (B 5 >) &&)

Left: (A 10 >)
  Γ ⊢ A : int
  Γ ⊢ 10 : int
  Γ ⊢ (A 10 >) : boolean

Right: (B 5 >)
  Γ ⊢ B : int
  Γ ⊢ 5 : int
  Γ ⊢ (B 5 >) : boolean

Operator &&:
  tipos_compativeis_logico(boolean, boolean) = TRUE
  Γ ⊢ ((A 10 >) (B 5 >) &&) : boolean
```

### Step 2: Evaluate True Branch
```
Expression: ((A B +) 2.0 |)

Inner: (A B +)
  Γ ⊢ A : int
  Γ ⊢ B : int
  promover_tipo(int, int) = int
  Γ ⊢ (A B +) : int

Outer: (<inner> 2.0 |)
  Γ ⊢ <inner> : int
  Γ ⊢ 2.0 : real
  Operator | always returns real
  Γ ⊢ ((A B +) 2.0 |) : real
```

### Step 3: Evaluate False Branch
```
Expression: ((A B *))

Γ ⊢ A : int
Γ ⊢ B : int
promover_tipo(int, int) = int
Γ ⊢ (A B *) : int
```

### Step 4: Check Branch Compatibility
```
True branch: real
False branch: int

promover_tipo(real, int) = real    ✓
```

**Compatibility**: YES (int promotes to real)

### Step 5: Infer IFELSE Type
```
IFELSE type = promover_tipo(real, int) = real
```

### Step 6: Complete Derivation Tree
```
                [Condition: AND]
Γ ⊢ (A 10 >):bool  Γ ⊢ (B 5 >):bool
─────────────────────────────────────
Γ ⊢ ((A 10 >) (B 5 >) &&) : boolean

      [True Branch]                [False Branch]
Γ ⊢ (A B +):int  Γ ⊢ 2.0:real     Γ ⊢ A:int  Γ ⊢ B:int
────────────────────────────────   ──────────────────────
Γ ⊢ ((A B +) 2.0 |) : real         Γ ⊢ (A B *) : int

                        [IFELSE]
Γ ⊢ <cond>:bool  Γ ⊢ <true>:real  Γ ⊢ <false>:int  promover_tipo(real,int)=real
────────────────────────────────────────────────────────────────────────────────────
      Γ ⊢ (((A 10 >) (B 5 >) &&) (((A B +) 2.0 |)) ((A B *)) IFELSE) : real
```

**Therefore**: The IFELSE expression has type `real`.

---

## Q36: WHILE with Truthiness Condition ⭐⭐

**Time Budget**: 4 minutes

**Question**: Is `((X) (((X 1 -) X)) WHILE)` valid given `Γ = {X: (int, inicializada)}`? Explain the condition evaluation.

**Answer**:

### Step 1: Evaluate Condition
```
Expression: (X)
Operation: MEM_LOAD (retrieve variable value)

Γ ⊢ X : int    (from symbol table)
```

### Step 2: Check WHILE Condition Requirements
**WHILE Condition**:
- Must be "boolean-compatible"
- Uses PERMISSIVE mode
- Accepts: int, real, boolean

**Current Condition**: `int` ✓

### Step 3: Truthiness Conversion
```
Condition type: int
Truthiness depends on runtime value of X:
  If X = 0 → para_booleano(0, int) = false
  If X ≠ 0 → para_booleano(X, int) = true
```

**Semantic Analysis**: Type is valid (int is boolean-compatible)
**Runtime Behavior**: Loop runs while X ≠ 0

### Step 4: Evaluate Body
```
Expression: (((X 1 -) X))
Pattern: ((value VAR))

Inner: (X 1 -)
  Γ ⊢ X : int
  Γ ⊢ 1 : int
  promover_tipo(int, int) = int
  Γ ⊢ (X 1 -) : int

Outer (MEM_STORE):
  Value: (X 1 -) → type: int
  Variable: X
  Type: int
```

### Step 5: WHILE Type
```
WHILE type = typeof(body) = int
```

### Step 6: Validation Result
**Answer**: YES, `((X) (((X 1 -) X)) WHILE)` is VALID ✓

### Step 7: Semantic Analysis
```
Γ ⊢ X : int    para_booleano(X, int) = (X ≠ 0)    Γ ⊢ (((X 1 -) X)) : int
──────────────────────────────────────────────────────────────────────────── (WHILE)
              Γ ⊢ ((X) (((X 1 -) X)) WHILE) : int
```

### Step 8: Runtime Behavior Analysis
```
Assuming X initially = 5:

Iteration 1: X = 5 (true) → execute body → X = 5 - 1 = 4
Iteration 2: X = 4 (true) → execute body → X = 4 - 1 = 3
Iteration 3: X = 3 (true) → execute body → X = 3 - 1 = 2
Iteration 4: X = 2 (true) → execute body → X = 2 - 1 = 1
Iteration 5: X = 1 (true) → execute body → X = 1 - 1 = 0
Iteration 6: X = 0 (false) → exit loop
```

**Key Points**:
- Condition is variable (not literal), so value changes
- Loop terminates when X reaches 0
- This is a valid countdown loop pattern

**Therefore**: The expression is semantically valid. WHILE accepts int condition via truthiness.

---

# Category D: Symbol Table (Q37-Q40)

## Q37: Symbol Table Evolution (3 Lines) ⭐⭐

**Time Budget**: 4 minutes

**Question**: Track the symbol table evolution for:
```
Line 1: ( 100 A )
Line 2: ( A 50 + )
Line 3: ( 200 B )
```

**Answer**:

### Initial State
```
Γ₀ = {}    (empty symbol table)
```

### Step 1: Process Line 1
```
Expression: ( 100 A )
Operation: MEM_STORE

Γ₀ ⊢ 100 : int
Store value 100 in variable A

Symbol Table Update:
Γ₁ = {
  A: {
    tipo: int,
    inicializada: true,
    escopo: 0,
    linha_declaracao: 1,
    linha_ultimo_uso: 1
  }
}
```

### Step 2: Process Line 2
```
Expression: ( A 50 + )
Operation: Uses variable A

Validation:
1. Does A exist? Γ₁.buscar("A") = {A: (int, true)} ✓
2. Is A initialized? true ✓
3. Type of A? int ✓

Type Derivation:
Γ₁ ⊢ A : int       (from symbol table)
Γ₁ ⊢ 50 : int      (INT-LITERAL)
promover_tipo(int, int) = int
Γ₁ ⊢ (A 50 +) : int

Symbol Table Update:
Γ₂ = {
  A: {
    tipo: int,
    inicializada: true,
    escopo: 0,
    linha_declaracao: 1,
    linha_ultimo_uso: 2    ← UPDATED
  }
}
```

### Step 3: Process Line 3
```
Expression: ( 200 B )
Operation: MEM_STORE

Γ₂ ⊢ 200 : int
Store value 200 in variable B

Symbol Table Update:
Γ₃ = {
  A: {
    tipo: int,
    inicializada: true,
    escopo: 0,
    linha_declaracao: 1,
    linha_ultimo_uso: 2
  },
  B: {
    tipo: int,
    inicializada: true,
    escopo: 0,
    linha_declaracao: 3,
    linha_ultimo_uso: 3
  }
}
```

### Step 4: Summary Table

| Line | Operation | Variables Added | Variables Used | Γ State |
|------|-----------|-----------------|----------------|---------|
| 0 | (initial) | - | - | `{}` |
| 1 | `(100 A)` | A | - | `{A: (int, true, decl=1, uso=1)}` |
| 2 | `(A 50 +)` | - | A | `{A: (int, true, decl=1, uso=2)}` |
| 3 | `(200 B)` | B | - | `{A: (..., uso=2), B: (int, true, decl=3, uso=3)}` |

### Step 5: Key Operations

| Symbol Table Method | Line 1 | Line 2 | Line 3 |
|---------------------|--------|--------|--------|
| `adicionar()` | A | - | B |
| `buscar()` | - | A | - |
| `marcar_inicializada()` | A | - | B |
| `registrar_uso()` | A | A | B |

**Therefore**: Symbol table evolves from `Γ₀ = {}` to `Γ₃ = {A: (int, ...), B: (int, ...)}`.

---

## Q38: Variable Initialization Check ⭐⭐

**Time Budget**: 3 minutes

**Question**: Why does this program fail?
```
Line 1: ( X Y + )
```

**Answer**:

### Step 1: Initial Symbol Table
```
Γ₀ = {}    (empty - no variables declared)
```

### Step 2: Attempt to Evaluate Line 1
```
Expression: ( X Y + )

Evaluate Left Operand:
  Operation: MEM_LOAD (retrieve X)
  Check: Γ₀.buscar("X") = None    ❌
```

### Step 3: Error Details (First Error)
- **Error Location**: Line 1, operand X
- **Error Type**: `memoria`
- **Error Message**: `"Variável 'X' não declarada ou não inicializada"`
- **Violated Rule**: Variables must be declared before use

### Step 4: Why This Is an Error
**Reason**: Cannot use variables before declaring them
- X has never been assigned a value (no MEM_STORE operation)
- X doesn't exist in symbol table
- Cannot determine X's type
- Cannot retrieve X's value

### Step 5: Similar Error for Y
Even if X were fixed, Y would cause the same error:
```
Γ.buscar("Y") = None    ❌
Error: "Variável 'Y' não declarada ou não inicializada"
```

### Step 6: How to Fix
**Corrected Program**:
```
Line 1: ( 10 X )      ← Declare and initialize X
Line 2: ( 20 Y )      ← Declare and initialize Y
Line 3: ( X Y + )     ← Now valid
```

**Symbol Table Evolution**:
```
Γ₀ = {}
Γ₁ = {X: (int, true)}
Γ₂ = {X: (int, true), Y: (int, true)}
Γ₃ = {X: (int, true, uso=3), Y: (int, true, uso=3)}
```

### Step 7: Implementation
- **File**: `src/RA3/functions/python/tabela_simbolos.py`
- **Method**: `verificar_inicializacao(nome)`
- **Behavior**: Raises `ErroSemantico` if variable not found or not initialized

**Therefore**: The program fails because X (and Y) are used before being declared.

---

## Q39: Variable Type Tracking ⭐⭐

**Time Budget**: 4 minutes

**Question**: Track the symbol table for:
```
Line 1: ( 10.5 X )
Line 2: ( (X 2 *) Y )
Line 3: ( X Y + )
```
What are the types of X and Y?

**Answer**:

### Step 1: Process Line 1
```
Expression: ( 10.5 X )
Operation: MEM_STORE

Γ₀ ⊢ 10.5 : real    (REAL-LITERAL - has .5)

Store value 10.5 (real) in variable X

Γ₁ = {
  X: {
    tipo: real,            ← Type determined by value
    inicializada: true,
    linha_declaracao: 1,
    linha_ultimo_uso: 1
  }
}
```

**X's Type**: `real`

### Step 2: Process Line 2
```
Expression: ( (X 2 *) Y )
Operation: MEM_STORE with expression value

Inner Expression: (X 2 *)
  Γ₁ ⊢ X : real      (from symbol table)
  Γ₁ ⊢ 2 : int       (INT-LITERAL)
  promover_tipo(real, int) = real
  Γ₁ ⊢ (X 2 *) : real

Store value (X 2 *) of type real in variable Y

Γ₂ = {
  X: {tipo: real, inicializada: true, linha_ultimo_uso: 2},
  Y: {
    tipo: real,            ← Type determined by expression (X 2 *)
    inicializada: true,
    linha_declaracao: 2,
    linha_ultimo_uso: 2
  }
}
```

**Y's Type**: `real`

### Step 3: Process Line 3
```
Expression: ( X Y + )

Γ₂ ⊢ X : real      (from symbol table)
Γ₂ ⊢ Y : real      (from symbol table)

promover_tipo(real, real) = real

Γ₂ ⊢ (X Y +) : real

Γ₃ = {
  X: {tipo: real, linha_ultimo_uso: 3},
  Y: {tipo: real, linha_ultimo_uso: 3}
}
```

### Step 4: Summary Table

| Variable | Type | Declared Line | Type Determined By |
|----------|------|---------------|-------------------|
| X | real | 1 | Literal value 10.5 |
| Y | real | 2 | Expression (X 2 *) → real |

### Step 5: Type Propagation Flow
```
10.5 (real literal)
  ↓
X : real (stored in Line 1)
  ↓
(X 2 *) : real (expression in Line 2)
  ↓
Y : real (stored in Line 2)
  ↓
(X Y +) : real (expression in Line 3)
```

### Step 6: Key Point
**Type Assignment**: Variable type is determined by the FIRST value stored
- X's type = type of `10.5` = `real`
- Y's type = type of `(X 2 *)` = `real`

**Once assigned, type doesn't change** (no type reassignment in this language)

**Therefore**: Both X and Y have type `real`.

---

## Q40: Symbol Table with RES References ⭐⭐⭐

**Time Budget**: 5 minutes

**Question**: Track the symbol table for:
```
Line 1: ( 5 A )
Line 2: ( (A 3 +) B )
Line 3: ( 2 RES C )
```
What variable types and RES reference does Line 3 contain?

**Answer**:

### Step 1: Process Line 1
```
Expression: ( 5 A )
Operation: MEM_STORE

Γ₀ ⊢ 5 : int

Γ₁ = {
  A: {tipo: int, inicializada: true, linha_declaracao: 1}
}

Line 1 Result Type: int
```

### Step 2: Process Line 2
```
Expression: ( (A 3 +) B )
Operation: MEM_STORE with expression

Inner: (A 3 +)
  Γ₁ ⊢ A : int
  Γ₁ ⊢ 3 : int
  promover_tipo(int, int) = int
  Γ₁ ⊢ (A 3 +) : int

Store in B:
  Type: int

Γ₂ = {
  A: {tipo: int, linha_ultimo_uso: 2},
  B: {tipo: int, inicializada: true, linha_declaracao: 2}
}

Line 2 Result Type: int
```

### Step 3: Process Line 3 - RES Resolution
```
Expression: ( 2 RES C )
Operation: MEM_STORE with RES value

RES Evaluation:
  Γ₂ ⊢ 2 : int       (RES argument)
  Current line: 3
  Referenced line: 3 - 2 = 1

Validate RES:
  Referenced line 1: Valid (1 ≤ 1 < 3) ✓
  Line 1 result type: int
  Γ₂ ⊢ (2 RES) : int

Store in C:
  Value type: int
  Variable: C

Γ₃ = {
  A: {tipo: int, linha_ultimo_uso: 2},
  B: {tipo: int, linha_ultimo_uso: 2},
  C: {tipo: int, inicializada: true, linha_declaracao: 3}
}
```

### Step 4: Answer the Questions

**Variable Types**:
- A: `int` (from literal 5)
- B: `int` (from expression (A 3 +))
- C: `int` (from RES reference to Line 1)

**RES Reference**:
- Argument: `2`
- Referenced Line: `3 - 2 = 1`
- Referenced Line Type: `int`
- Referenced Line Result: `5` (value of A)

### Step 5: Complete Type Flow Diagram
```
Line 1: 5 (int) → A : int
           ↓
Line 2: (A 3 +) : int → B : int
           ↓
Line 3: 2 RES → references Line 1 → int → C : int
```

### Step 6: Symbol Table Final State
```
Γ₃ = {
  A: {tipo: int, inicializada: true, linha_declaracao: 1, linha_ultimo_uso: 2},
  B: {tipo: int, inicializada: true, linha_declaracao: 2, linha_ultimo_uso: 2},
  C: {tipo: int, inicializada: true, linha_declaracao: 3, linha_ultimo_uso: 3}
}
```

### Step 7: RES Reference Details

| RES Argument | Current Line | Referenced Line | Referenced Type | Valid? |
|--------------|--------------|-----------------|-----------------|--------|
| 2 | 3 | 1 | int | ✓ |

**Validation**:
- `1 ≤ 1 < 3` ✓
- Line 1 exists ✓
- Line 1 has type `int` ✓

**Therefore**: Line 3 creates variable C with type `int`, referencing Line 1's result via `(2 RES)`.

---

# End of Question Bank

---

## Performance Tracking Template

Use this table to track your progress on all 40 questions:

| Q# | Category | Difficulty | Time Budget | Attempt 1 | Attempt 2 | Attempt 3 | Mastered? |
|----|----------|------------|-------------|-----------|-----------|-----------|-----------|
| Q1 | Type Inference | ⭐ | 2 min | | | | |
| Q2 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q3 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q4 | Type Inference | ⭐ | 2 min | | | | |
| Q5 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q6 | Type Inference | ⭐⭐ | 4 min | | | | |
| Q7 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q8 | Type Inference | ⭐⭐⭐ | 5 min | | | | |
| Q9 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q10 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q11 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q12 | Type Inference | ⭐ | 2 min | | | | |
| Q13 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q14 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q15 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q16 | Type Inference | ⭐⭐ | 3 min | | | | |
| Q17 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q18 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q19 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q20 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q21 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q22 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q23 | Error Detection | ⭐⭐ | 4 min | | | | |
| Q24 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q25 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q26 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q27 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q28 | Error Detection | ⭐⭐ | 3 min | | | | |
| Q29 | Control Structures | ⭐⭐ | 4 min | | | | |
| Q30 | Control Structures | ⭐⭐ | 3 min | | | | |
| Q31 | Control Structures | ⭐⭐ | 4 min | | | | |
| Q32 | Control Structures | ⭐⭐⭐ | 5 min | | | | |
| Q33 | Control Structures | ⭐⭐⭐ | 5 min | | | | |
| Q34 | Control Structures | ⭐⭐ | 4 min | | | | |
| Q35 | Control Structures | ⭐⭐⭐ | 5 min | | | | |
| Q36 | Control Structures | ⭐⭐ | 4 min | | | | |
| Q37 | Symbol Table | ⭐⭐ | 4 min | | | | |
| Q38 | Symbol Table | ⭐⭐ | 3 min | | | | |
| Q39 | Symbol Table | ⭐⭐ | 4 min | | | | |
| Q40 | Symbol Table | ⭐⭐⭐ | 5 min | | | | |

**Scoring**:
- ✓ = Completed correctly within time budget
- ~ = Completed correctly but exceeded time
- ✗ = Incorrect or incomplete

**Mastery Criteria**: 3 consecutive ✓ marks

---

## Study Recommendations

### Week Before Defense
- **Day 1-2**: Complete Q1-Q16 (Type Inference)
- **Day 3-4**: Complete Q17-Q28 (Error Detection)
- **Day 5**: Complete Q29-Q36 (Control Structures)
- **Day 6**: Complete Q37-Q40 (Symbol Table)
- **Day 7**: Random selection, timed practice

### Day Before Defense
- Review all ⭐⭐⭐ questions (Q8, Q32, Q33, Q35, Q40)
- Practice 5 random questions under timed conditions
- Review common mistakes from tracking table

### Day of Defense
- Quick review of 3 random questions
- Read quick reference cheat sheet
- Calm confidence!

---

**Good luck with your defense preparation!** 🎓

*Remember*: Clear and correct beats fast and wrong. Take your time, show your work, explain your reasoning.

---

*Last updated: 2025-01-19*
*RA3_1 Defense Preparation Team*
