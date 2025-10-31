# Proof Templates: Fill-in-the-Blank Worksheets
## RA3 Defense Practice Drills

**Purpose**: Practice type derivations with structured fill-in-the-blank templates
**How to Use**: Print this file, fill in blanks with pencil, check answers at end
**Time Budget**: 15-30 minutes per template (initially), 5-10 minutes when fluent
**Recommended Practice**: Complete each template 3-5 times until automatic

---

## Template Categories

1. **Simple Binary Arithmetic** (4 templates)
2. **Nested Expressions** (2 templates)
3. **IFELSE Derivations** (2 templates)
4. **Symbol Table Evolution** (2 templates)
5. **RES Reference Resolution** (2 templates)
6. **Error Detection** (3 templates)

**Total**: 15 practice templates

---

## Instructions

### How to Fill Templates

1. **Read the given expression** at the top
2. **Fill in each blank** following the structure
3. **Draw derivation trees** in designated areas
4. **Write formal notation** for each step
5. **Check your answer** against answer key at end

### Notation Reminders

- `Γ ⊢ e : T` means "Under environment Γ, expression e has type T"
- `promover_tipo(T₁, T₂)` promotes to higher type in hierarchy
- `tipos_compativeis_X()` checks compatibility for operator X
- Rules: INT-LITERAL, REAL-LITERAL, ADD-PROMOTE, etc.

### Blank Types

- `[___]` = Fill in a value (type, operator, etc.)
- `[_____________]` = Fill in a longer explanation
- `[DRAW]` = Draw a derivation tree
- `[YES/NO]` = Choose one

---

# Category 1: Simple Binary Arithmetic

## Template 1.1: Integer Addition

**Given Expression**: `(5 3 +)`

**Target**: Prove this expression has a type

---

### STEP 1: IDENTIFY COMPONENTS

Left operand: `[___]`
Right operand: `[___]`
Operator: `[___]`

---

### STEP 2: DERIVE LEFT OPERAND TYPE

Is 5 a literal? `[YES/NO]`

Does it have a decimal point? `[YES/NO]`

Therefore: `Γ ⊢ 5 : [___]`

Rule name: `[_______________]`

---

### STEP 3: DERIVE RIGHT OPERAND TYPE

Is 3 a literal? `[YES/NO]`

Does it have a decimal point? `[YES/NO]`

Therefore: `Γ ⊢ 3 : [___]`

Rule name: `[_______________]`

---

### STEP 4: CHECK OPERATOR COMPATIBILITY

Operator + is `[STRICT/PERMISSIVE]`

Function to check: `tipos_compativeis_[_______________](int, int)`

Result: `[TRUE/FALSE]`

Why? `[_________________________________________________]`

---

### STEP 5: INFER RESULT TYPE

Type promotion: `promover_tipo(int, int) = [___]`

Therefore: `Γ ⊢ (5 3 +) : [___]`

Rule name: `[_______________]`

---

### STEP 6: DRAW COMPLETE DERIVATION TREE

```
[DRAW TREE HERE]




```

---

## Template 1.2: Mixed Type Addition

**Given Expression**: `(7 2.5 +)`

**Target**: Prove this expression has type real

---

### STEP 1: IDENTIFY COMPONENTS

Left operand: `[___]`
Right operand: `[___]`
Operator: `[___]`

---

### STEP 2: DERIVE LEFT OPERAND TYPE

Is 7 a literal? `[YES/NO]`

Does it have a decimal point? `[YES/NO]`

Therefore: `Γ ⊢ 7 : [___]`

---

### STEP 3: DERIVE RIGHT OPERAND TYPE

Is 2.5 a literal? `[YES/NO]`

Does it have a decimal point? `[YES/NO]`

Therefore: `Γ ⊢ 2.5 : [___]`

---

### STEP 4: CHECK OPERATOR COMPATIBILITY

Operator + accepts: `[int/int, int/real, real/int, real/real]` (circle all that apply)

Is the combination (int, real) compatible? `[YES/NO]`

---

### STEP 5: INFER RESULT TYPE

Type promotion: `promover_tipo([___], [___]) = [___]`

Why does int + real → real? `[_________________________________________________]`

Therefore: `Γ ⊢ (7 2.5 +) : [___]`

---

### STEP 6: WRITE FORMAL DERIVATION

```
────────────── ([___])    ────────────── ([___])
 Γ ⊢ 7 : [___]            Γ ⊢ 2.5 : [___]
──────────────────────────────────────────────── ([_______________])
            Γ ⊢ (7 2.5 +) : [___]
```

---

## Template 1.3: Integer Division (STRICT)

**Given Expression**: `(10 3 /)`

**Target**: Prove type and explain why (10 3.0 /) would fail

---

### STEP 1: DERIVE OPERAND TYPES

`Γ ⊢ 10 : [___]` (Rule: `[_______________]`)

`Γ ⊢ 3 : [___]` (Rule: `[_______________]`)

---

### STEP 2: CHECK OPERATOR COMPATIBILITY

Operator / is `[STRICT/PERMISSIVE]`

It ONLY accepts: `[___]/[___]` (fill in types)

Function to check: `tipos_compativeis_[_______________](int, int)`

Result: `[TRUE/FALSE]`

---

### STEP 3: INFER RESULT TYPE

For integer division, result type is ALWAYS: `[___]`

Therefore: `Γ ⊢ (10 3 /) : [___]`

---

### STEP 4: ERROR CASE ANALYSIS

Why does `(10 3.0 /)` fail?

Operand types: `([___], [___])`

Operator / requirement: `([___], [___])`

Compatibility check: `tipos_compativeis_divisao_inteira([___], [___]) = [___]`

Error message: `"[_________________________________________________]"`

---

### STEP 5: DRAW CORRECT DERIVATION

```
[DRAW TREE FOR (10 3 /)]




```

---

## Template 1.4: Power Operator (SPECIAL)

**Given Expression**: `(2.5 3 ^)`

**Target**: Prove type and explain exponent restriction

---

### STEP 1: IDENTIFY OPERAND ROLES

Base: `[___]` → Type: `[___]`
Exponent: `[___]` → Type: `[___]`

---

### STEP 2: CHECK BASE COMPATIBILITY

Base can be: `[int/real/boolean]` (circle all that apply)

Is 2.5 a valid base? `[YES/NO]`

---

### STEP 3: CHECK EXPONENT COMPATIBILITY

Exponent MUST be: `[___]`

Exponent MUST be: `[positive/negative/any value]` (circle one)

Is 3 a valid exponent? `[YES/NO]`

---

### STEP 4: INFER RESULT TYPE

For power operator, result type = `typeof([___])`

Therefore: `Γ ⊢ (2.5 3 ^) : [___]`

---

### STEP 5: ERROR CASES

Why does `(2.5 3.0 ^)` fail?

`[_________________________________________________]`

Why does `(2.5 -3 ^)` fail?

`[_________________________________________________]`

---

### STEP 6: WRITE FORMAL DERIVATION

```
Γ ⊢ 2.5 : [___]    Γ ⊢ 3 : [___]    3 > 0 : [___]
──────────────────────────────────────────────────── (POWER)
              Γ ⊢ (2.5 3 ^) : [___]
```

---

# Category 2: Nested Expressions

## Template 2.1: Two-Level Nesting

**Given Expression**: `((5 3 +) 2 *)`

**Target**: Prove type using inside-out evaluation

---

### STEP 1: IDENTIFY STRUCTURE

Inner expression: `[___________]`
Outer left operand: `[___________]`
Outer right operand: `[___]`
Outer operator: `[___]`

---

### STEP 2: EVALUATE INNER EXPRESSION

`Γ ⊢ 5 : [___]` (Rule: `[_______________]`)

`Γ ⊢ 3 : [___]` (Rule: `[_______________]`)

`promover_tipo([___], [___]) = [___]`

`Γ ⊢ (5 3 +) : [___]` (Rule: `[_______________]`)

---

### STEP 3: EVALUATE OUTER EXPRESSION

Now we have: `([___] 2 *)`

`Γ ⊢ [___] : [___]` (from inner evaluation)

`Γ ⊢ 2 : [___]` (Rule: `[_______________]`)

---

### STEP 4: CHECK OUTER COMPATIBILITY

Operator * is `[STRICT/PERMISSIVE]`

Operand types: `([___], [___])`

Compatible? `[YES/NO]`

---

### STEP 5: INFER FINAL TYPE

`promover_tipo([___], [___]) = [___]`

`Γ ⊢ ((5 3 +) 2 *) : [___]`

---

### STEP 6: DRAW COMPLETE DERIVATION TREE

```
[DRAW TREE SHOWING BOTH LEVELS]






```

---

## Template 2.2: Three-Level Nesting

**Given Expression**: `(((10 5 -) (3 2 +) /) 2 ^)`

**Target**: Prove type with multiple nested operations

---

### STEP 1: IDENTIFY ALL LEVELS

Level 1 (innermost left): `[___________]`
Level 1 (innermost right): `[___________]`
Level 2 (middle): `[___________]`
Level 3 (outermost): `[___________]`

---

### STEP 2: EVALUATE INNERMOST LEFT

Expression: `(10 5 -)`

`Γ ⊢ 10 : [___]`
`Γ ⊢ 5 : [___]`
`promover_tipo([___], [___]) = [___]`
`Γ ⊢ (10 5 -) : [___]`

---

### STEP 3: EVALUATE INNERMOST RIGHT

Expression: `(3 2 +)`

`Γ ⊢ 3 : [___]`
`Γ ⊢ 2 : [___]`
`promover_tipo([___], [___]) = [___]`
`Γ ⊢ (3 2 +) : [___]`

---

### STEP 4: EVALUATE MIDDLE LEVEL

Expression: `((10 5 -) (3 2 +) /)`

Left operand type: `[___]` (from Step 2)
Right operand type: `[___]` (from Step 3)

Operator / is `[STRICT/PERMISSIVE]`

Compatible? `[YES/NO]`

Result type: `[___]`

`Γ ⊢ ((10 5 -) (3 2 +) /) : [___]`

---

### STEP 5: EVALUATE OUTERMOST LEVEL

Expression: `(((10 5 -) (3 2 +) /) 2 ^)`

Base type: `[___]` (from Step 4)
Exponent: `2` → Type: `[___]`

Operator ^ requirements:
- Base: `[int/real]` (circle valid)
- Exponent: `[___]`
- Exponent > 0: `[YES/NO]`

Result type: `typeof([___]) = [___]`

`Γ ⊢ (((10 5 -) (3 2 +) /) 2 ^) : [___]`

---

### STEP 6: DRAW COMPLETE DERIVATION TREE

```
[DRAW TREE WITH ALL 3 LEVELS]








```

---

# Category 3: IFELSE Derivations

## Template 3.1: Compatible Branches

**Given Expression**: `((5 3 >) (10) (20) IFELSE)`

**Target**: Prove type and demonstrate branch compatibility

---

### STEP 1: IDENTIFY IFELSE COMPONENTS

Condition: `[___________]`
True branch: `[___]`
False branch: `[___]`

---

### STEP 2: EVALUATE CONDITION

Expression: `(5 3 >)`

`Γ ⊢ 5 : [___]`
`Γ ⊢ 3 : [___]`

Operator > is a `[comparison/logical/arithmetic]` operator

Result type: `[___]` (comparison operators ALWAYS return this type)

`Γ ⊢ (5 3 >) : [___]`

---

### STEP 3: EVALUATE TRUE BRANCH

Expression: `(10)`

`Γ ⊢ 10 : [___]`

---

### STEP 4: EVALUATE FALSE BRANCH

Expression: `(20)`

`Γ ⊢ 20 : [___]`

---

### STEP 5: CHECK BRANCH COMPATIBILITY

True branch type: `[___]`
False branch type: `[___]`

`promover_tipo([___], [___]) = [___]`

Are branches compatible? `[YES/NO]`

Why? `[_________________________________________________]`

---

### STEP 6: INFER IFELSE TYPE

IFELSE type = `promover_tipo(tipo_then, tipo_else)`

IFELSE type = `promover_tipo([___], [___]) = [___]`

`Γ ⊢ ((5 3 >) (10) (20) IFELSE) : [___]`

---

### STEP 7: WRITE FORMAL DERIVATION

```
Γ ⊢ (5 3 >) : [___]    Γ ⊢ 10 : [___]    Γ ⊢ 20 : [___]
promover_tipo([___], [___]) = [___]
──────────────────────────────────────────────────────────── (IFELSE)
        Γ ⊢ ((5 3 >) (10) (20) IFELSE) : [___]
```

---

## Template 3.2: Incompatible Branches (ERROR)

**Given Expression**: `((X 0 >) (100) ((5 3 >)) IFELSE)`

**Target**: Identify why this fails and explain the error

---

### STEP 1: EVALUATE CONDITION

Assume: `Γ = {X: (int, inicializada)}`

`Γ ⊢ X : [___]` (from symbol table)
`Γ ⊢ 0 : [___]`
`Γ ⊢ (X 0 >) : [___]`

---

### STEP 2: EVALUATE TRUE BRANCH

Expression: `(100)`

`Γ ⊢ 100 : [___]`

---

### STEP 3: EVALUATE FALSE BRANCH

Expression: `((5 3 >))`

`Γ ⊢ 5 : [___]`
`Γ ⊢ 3 : [___]`
`Γ ⊢ (5 3 >) : [___]`

---

### STEP 4: CHECK BRANCH COMPATIBILITY

True branch type: `[___]`
False branch type: `[___]`

`promover_tipo([___], [___]) = [___]`

Are branches compatible? `[YES/NO]`

---

### STEP 5: EXPLAIN ERROR

Why are int and boolean incompatible?

`[_________________________________________________]`

What is the error message?

`"[_________________________________________________]"`

Where is this checked in code?

File: `[_____________________________________________]`
Function: `[_____________________________________________]`

---

### STEP 6: FIX THE EXPRESSION

How could you fix this to make branches compatible?

Option 1: `[_________________________________________________]`

Option 2: `[_________________________________________________]`

---

# Category 4: Symbol Table Evolution

## Template 4.1: Three-Line Variable Tracking

**Given Program**:
```
Line 1: ( 10 X )
Line 2: ( X 5 + )
Line 3: ( 20 Y )
```

**Target**: Track Γ₀ → Γ₁ → Γ₂ → Γ₃

---

### INITIAL STATE

`Γ₀ = { [___] }` (empty or populated?)

---

### AFTER LINE 1: ( 10 X )

This is a `[MEM_STORE/MEM_LOAD/RES]` operation

Value stored: `[___]`
Variable name: `[___]`
Value type: `[___]`

Symbol table update:
```
Γ₁ = {
    X: {
        tipo: [___],
        inicializada: [___],
        escopo: [___],
        linha_declaracao: [___],
        linha_ultimo_uso: [___]
    }
}
```

---

### AFTER LINE 2: ( X 5 + )

This line `[uses/declares]` variable X

Validation checks:
1. Does X exist in Γ₁? `[YES/NO]`
2. Is X initialized? `[YES/NO]`
3. What is X's type? `[___]`

Expression evaluation:
`Γ₁ ⊢ X : [___]` (from symbol table)
`Γ₁ ⊢ 5 : [___]`
`promover_tipo([___], [___]) = [___]`
`Γ₁ ⊢ (X 5 +) : [___]`

Symbol table update:
```
Γ₂ = {
    X: {
        tipo: [___],
        inicializada: [___],
        escopo: [___],
        linha_declaracao: [___],
        linha_ultimo_uso: [___]  (UPDATED!)
    }
}
```

---

### AFTER LINE 3: ( 20 Y )

This is a `[MEM_STORE/MEM_LOAD/RES]` operation

Value stored: `[___]`
Variable name: `[___]`
Value type: `[___]`

Symbol table update:
```
Γ₃ = {
    X: {
        tipo: [___],
        inicializada: [___],
        escopo: [___],
        linha_declaracao: [___],
        linha_ultimo_uso: [___]
    },
    Y: {
        tipo: [___],
        inicializada: [___],
        escopo: [___],
        linha_declaracao: [___],
        linha_ultimo_uso: [___]
    }
}
```

---

### SUMMARY TABLE

| Line | Operation | Variables Added | Variables Used | Γ State |
|------|-----------|-----------------|----------------|---------|
| 0 | (initial) | - | - | Γ₀ = `[___]` |
| 1 | `(10 X)` | `[___]` | - | Γ₁ = `[___]` |
| 2 | `(X 5 +)` | - | `[___]` | Γ₂ = `[___]` |
| 3 | `(20 Y)` | `[___]` | - | Γ₃ = `[___]` |

---

## Template 4.2: Uninitialized Variable Error

**Given Program**:
```
Line 1: ( 10 X )
Line 2: ( Y )
```

**Target**: Identify error and explain symbol table check

---

### AFTER LINE 1

`Γ₁ = { X: ([___], [___]) }`

---

### LINE 2 VALIDATION

Expression: `( Y )`

This is a `[MEM_STORE/MEM_LOAD/RES]` operation

Check 1: Does Y exist in Γ₁?
- Lookup: `Γ₁.buscar("Y") = [___]`
- Result: `[YES/NO]`

Check 2: Is Y initialized?
- Lookup: `Γ₁.verificar_inicializacao("Y") = [___]`
- Result: `[PASS/FAIL]`

---

### ERROR ANALYSIS

Error type: `[tipo/memoria/controle/outro]`

Error message:
`"[_________________________________________________]"`

Where is this checked in code?
File: `[_______________________________________________]`
Line: `[___]`
Function: `[_______________________________________________]`

---

### HOW TO FIX

What line needs to be added before Line 2?

`[_________________________________________________]`

After the fix, what would Γ₁ contain?

`Γ₁ = { [_______________________________________________] }`

---

# Category 5: RES Reference Resolution

## Template 5.1: Simple RES Reference

**Given Program**:
```
Line 1: ( 5 3 + )
Line 2: ( 1 RES )
```

**Target**: Resolve RES reference and infer type

---

### LINE 1 EVALUATION

Expression: `( 5 3 + )`

`Γ₀ ⊢ 5 : [___]`
`Γ₀ ⊢ 3 : [___]`
`promover_tipo([___], [___]) = [___]`
`Γ₀ ⊢ ( 5 3 + ) : [___]`

Store result: `linha_1_tipo = [___]`

---

### LINE 2 EVALUATION

Expression: `( 1 RES )`

This is a `[MEM_STORE/MEM_LOAD/RES]` operation

RES operand: `[___]`
RES operand type: `[___]`

---

### RES REFERENCE CALCULATION

Current line number: `[___]`
RES argument: `[___]`
Referenced line = Current - RES argument = `[___] - [___] = [___]`

---

### RES VALIDATION

Check 1: Is referenced line valid?
- Referenced line: `[___]`
- Must be: `>= 1` and `< current_line`
- Valid? `[YES/NO]`

Check 2: Does referenced line exist?
- Lookup: `linha_[___]_tipo`
- Exists? `[YES/NO]`

---

### TYPE INFERENCE

Type of line `[___]`: `[___]`

Therefore: `Γ₀ ⊢ ( 1 RES ) : [___]`

---

### FORMAL DERIVATION

```
Γ₀ ⊢ ( 5 3 + ) : [___]    (linha 1)
Γ₀ ⊢ 1 : int    linha_atual = [___]    1 ≤ [___] - 1
─────────────────────────────────────────────────────────── (RES)
            Γ₀ ⊢ ( 1 RES ) : [___]    (linha 2)
```

---

## Template 5.2: RES with Calculation

**Given Program**:
```
Line 1: ( 10 5 / )
Line 2: ( 3.5 2.0 + )
Line 3: ( 2 RES 1 RES + )
```

**Target**: Resolve multiple RES references

---

### LINE 1 EVALUATION

Expression: `( 10 5 / )`

Operator / is `[STRICT/PERMISSIVE]`
Operand types: `([___], [___])`
Compatible? `[YES/NO]`
Result type: `[___]`

`linha_1_tipo = [___]`

---

### LINE 2 EVALUATION

Expression: `( 3.5 2.0 + )`

Operand types: `([___], [___])`
Result type: `promover_tipo([___], [___]) = [___]`

`linha_2_tipo = [___]`

---

### LINE 3 EVALUATION - RES RESOLUTION

Expression: `( 2 RES 1 RES + )`

**First RES**: `2 RES`
- Current line: `[___]`
- Referenced line: `[___] - 2 = [___]`
- Type of line `[___]`: `[___]`
- `Γ₀ ⊢ ( 2 RES ) : [___]`

**Second RES**: `1 RES`
- Current line: `[___]`
- Referenced line: `[___] - 1 = [___]`
- Type of line `[___]`: `[___]`
- `Γ₀ ⊢ ( 1 RES ) : [___]`

---

### LINE 3 EVALUATION - ADDITION

Expression becomes: `( [___] [___] + )`

Operand types: `([___], [___])`

Operator + is `[STRICT/PERMISSIVE]`
Compatible? `[YES/NO]`
Result type: `promover_tipo([___], [___]) = [___]`

`Γ₀ ⊢ ( 2 RES 1 RES + ) : [___]`

---

### DRAW COMPLETE DERIVATION

```
[DRAW TREE SHOWING ALL 3 LINES AND RES RESOLUTIONS]








```

---

# Category 6: Error Detection

## Template 6.1: Division Type Error

**Given Expression**: `( 10 3.0 / )`

**Target**: Identify error, explain why, provide fix

---

### STEP 1: EVALUATE OPERANDS

`Γ ⊢ 10 : [___]` (Why? `[_________________________________]`)

`Γ ⊢ 3.0 : [___]` (Why? `[_________________________________]`)

---

### STEP 2: CHECK OPERATOR REQUIREMENTS

Operator / is `[STRICT/PERMISSIVE]`

Operator / ONLY accepts: `([___], [___])`

Current operand types: `([___], [___])`

---

### STEP 3: COMPATIBILITY CHECK

Function called: `tipos_compativeis_[_______________](int, real)`

Result: `[TRUE/FALSE]`

Why does this return false?

`[_________________________________________________]`

---

### STEP 4: ERROR DETAILS

Error type: `[tipo/memoria/controle/outro]`

Error message:
`"[_________________________________________________]"`

---

### STEP 5: HOW TO FIX

Option 1 (use different operator):
`[_________________________________________________]`

Option 2 (convert operand):
`[_________________________________________________]`

Which option is better and why?
`[_________________________________________________]`

---

## Template 6.2: MEM Boolean Error

**Given Expression**: `( (5 3 >) X )`

**Target**: Identify why boolean cannot be stored in memory

---

### STEP 1: EVALUATE VALUE TO STORE

Expression: `( 5 3 > )`

Operator > is a `[comparison/logical/arithmetic]` operator

Result type: `[___]`

`Γ ⊢ ( 5 3 > ) : [___]`

---

### STEP 2: IDENTIFY MEM OPERATION

Operation: `( [___] X )`

This is a `[MEM_STORE/MEM_LOAD/RES]` operation

Value to store: `[___]`
Value type: `[___]`
Variable name: `[___]`

---

### STEP 3: CHECK MEM RESTRICTIONS

MEM can store types: `[int, real, boolean]` (circle all that apply)

Current value type: `[___]`

Is this allowed? `[YES/NO]`

---

### STEP 4: ERROR DETAILS

Why is boolean not allowed in MEM?

`[_________________________________________________]`

Error message:
`"[_________________________________________________]"`

Where is this checked in code?
File: `[_______________________________________________]`

---

### STEP 5: HOW TO FIX

Option 1 (store different value):
`[_________________________________________________]`

Option 2 (use truthiness conversion):
`[_________________________________________________]`

Is Option 2 valid? `[YES/NO]` Why? `[_____________________________]`

---

## Template 6.3: FOR Parameter Type Error

**Given Expression**: `( 1.5 10.5 0.5 (X 2 *) FOR )`

**Target**: Identify why FOR requires integers

---

### STEP 1: IDENTIFY FOR PARAMETERS

Init: `[___]` → Type: `[___]`
End: `[___]` → Type: `[___]`
Step: `[___]` → Type: `[___]`
Body: `[___]`

---

### STEP 2: CHECK FOR REQUIREMENTS

FOR requires:
- Init type: `[___]`
- End type: `[___]`
- Step type: `[___]`

Current parameter types: `([___], [___], [___])`

---

### STEP 3: COMPATIBILITY CHECK

Are init/end/step all integers? `[YES/NO]`

Which parameters are wrong?
- Init: `[CORRECT/WRONG]`
- End: `[CORRECT/WRONG]`
- Step: `[CORRECT/WRONG]`

---

### STEP 4: ERROR DETAILS

Error message:
`"[_________________________________________________]"`

Why does FOR require integers?

`[_________________________________________________]`

---

### STEP 5: HOW TO FIX

Corrected expression:
`[_________________________________________________]`

What changed?
- Init: `[___]` → `[___]`
- End: `[___]` → `[___]`
- Step: `[___]` → `[___]`

---

# Answer Keys

## Template 1.1 Answers

- Left operand: `5`
- Right operand: `3`
- Operator: `+`
- Is 5 a literal? `YES`
- Does it have decimal? `NO`
- `Γ ⊢ 5 : int`
- Rule: `INT-LITERAL`
- Is 3 a literal? `YES`
- Does it have decimal? `NO`
- `Γ ⊢ 3 : int`
- Operator + is: `PERMISSIVE`
- Function: `tipos_compativeis_aritmetica`
- Result: `TRUE`
- Why? "Addition accepts any numeric types (int/real in any combination)"
- `promover_tipo(int, int) = int`
- `Γ ⊢ (5 3 +) : int`
- Rule: `ADD` or `ADD-INT`

**Derivation Tree**:
```
─────────── (INT)    ─────────── (INT)
 Γ ⊢ 5:int            Γ ⊢ 3:int
──────────────────────────────────────── (ADD)
        Γ ⊢ (5 3 +) : int
```

---

## Template 1.2 Answers

- Left operand: `7`, Type: `int`
- Right operand: `2.5`, Type: `real`
- Is 7 a literal? `YES`, Decimal? `NO`
- `Γ ⊢ 7 : int`
- Is 2.5 a literal? `YES`, Decimal? `YES`
- `Γ ⊢ 2.5 : real`
- Operator + accepts: ALL (int/int, int/real, real/int, real/real)
- Compatible? `YES`
- `promover_tipo(int, real) = real`
- Why? "In the type hierarchy int < real, so int is promoted to real when mixed"
- `Γ ⊢ (7 2.5 +) : real`

**Formal Derivation**:
```
────────────── (INT)    ────────────── (REAL)
 Γ ⊢ 7 : int             Γ ⊢ 2.5 : real
──────────────────────────────────────────────── (ADD-PROMOTE)
          Γ ⊢ (7 2.5 +) : real
```

---

## Template 1.3 Answers

- `Γ ⊢ 10 : int` (Rule: `INT-LITERAL`)
- `Γ ⊢ 3 : int` (Rule: `INT-LITERAL`)
- Operator / is: `STRICT`
- Only accepts: `int/int`
- Function: `tipos_compativeis_divisao_inteira`
- Result: `TRUE`
- Result type: `int`
- `Γ ⊢ (10 3 /) : int`

**Error Case**:
- Operand types: `(int, real)`
- Requirement: `(int, int)`
- `tipos_compativeis_divisao_inteira(int, real) = FALSE`
- Error: `"Operador '/' requer operandos inteiros (recebeu int e real)"`

---

## Template 1.4 Answers

- Base: `2.5`, Type: `real`
- Exponent: `3`, Type: `int`
- Base can be: `int/real` (NOT boolean)
- Is 2.5 valid? `YES`
- Exponent must be: `int`
- Exponent must be: `positive`
- Is 3 valid? `YES`
- Result type = `typeof(base) = real`
- `Γ ⊢ (2.5 3 ^) : real`

**Error Cases**:
- `(2.5 3.0 ^)` fails: "Exponent must be int (received real)"
- `(2.5 -3 ^)` fails: "Exponent must be positive (received -3)"

---

## Template 2.1 Answers

- Inner: `(5 3 +)`
- Outer left: `(5 3 +)`
- Outer right: `2`
- Outer op: `*`

**Inner Evaluation**:
- `Γ ⊢ 5 : int` (INT-LITERAL)
- `Γ ⊢ 3 : int` (INT-LITERAL)
- `promover_tipo(int, int) = int`
- `Γ ⊢ (5 3 +) : int` (ADD)

**Outer Evaluation**:
- Now: `(int 2 *)`
- `Γ ⊢ int : int` (from inner)
- `Γ ⊢ 2 : int` (INT-LITERAL)
- Operator * is: `PERMISSIVE`
- Types: `(int, int)`
- Compatible? `YES`
- `promover_tipo(int, int) = int`
- `Γ ⊢ ((5 3 +) 2 *) : int`

---

## Template 2.2 Answers

**Levels**:
- Level 1 left: `(10 5 -)`
- Level 1 right: `(3 2 +)`
- Level 2: `((10 5 -) (3 2 +) /)`
- Level 3: `(((10 5 -) (3 2 +) /) 2 ^)`

**Innermost Left**:
- `Γ ⊢ 10 : int`, `Γ ⊢ 5 : int`
- `promover_tipo(int, int) = int`
- `Γ ⊢ (10 5 -) : int`

**Innermost Right**:
- `Γ ⊢ 3 : int`, `Γ ⊢ 2 : int`
- `promover_tipo(int, int) = int`
- `Γ ⊢ (3 2 +) : int`

**Middle Level**:
- Left: `int`, Right: `int`
- Operator / is: `STRICT`
- Compatible? `YES`
- `Γ ⊢ ((10 5 -) (3 2 +) /) : int`

**Outermost**:
- Base: `int`, Exponent: `2` (int)
- Requirements: base int/real, exp int, exp > 0
- Valid? `YES`
- Result: `typeof(int) = int`
- `Γ ⊢ (((10 5 -) (3 2 +) /) 2 ^) : int`

---

## Template 3.1 Answers

- Condition: `(5 3 >)`
- True branch: `(10)`
- False branch: `(20)`

**Condition**:
- `Γ ⊢ 5 : int`, `Γ ⊢ 3 : int`
- Operator > is: `comparison`
- Result: `boolean` (always)
- `Γ ⊢ (5 3 >) : boolean`

**Branches**:
- `Γ ⊢ 10 : int`
- `Γ ⊢ 20 : int`

**Compatibility**:
- True: `int`, False: `int`
- `promover_tipo(int, int) = int`
- Compatible? `YES`
- Why? "Both branches are same type"

**IFELSE Type**:
- `promover_tipo(int, int) = int`
- `Γ ⊢ ((5 3 >) (10) (20) IFELSE) : int`

---

## Template 3.2 Answers

**Evaluation** (assuming `Γ = {X: (int, inicializada)}`):
- `Γ ⊢ X : int`
- `Γ ⊢ 0 : int`
- `Γ ⊢ (X 0 >) : boolean`
- `Γ ⊢ 100 : int`
- `Γ ⊢ 5 : int`, `Γ ⊢ 3 : int`
- `Γ ⊢ (5 3 >) : boolean`

**Compatibility**:
- True: `int`, False: `boolean`
- `promover_tipo(int, boolean) = None`
- Compatible? `NO`

**Error**:
- Why? "int and boolean are incompatible types - there's no type promotion between them"
- Error: `"Branches de IFELSE incompatíveis: int e boolean"`
- File: `analisador_memoria_controle.py`
- Function: `analisarSemanticaControle`

**Fixes**:
- Option 1: Change false branch to int: `((X 0 >) (100) (50) IFELSE)`
- Option 2: Change true branch to boolean: `((X 0 >) ((1 1 ==)) ((5 3 >)) IFELSE)`

---

## Template 4.1 Answers

**Initial**: `Γ₀ = {}` (empty)

**After Line 1** `(10 X)`:
- Operation: `MEM_STORE`
- Value: `10`, Type: `int`
- Variable: `X`
- `Γ₁ = {X: {tipo: int, inicializada: true, escopo: 0, linha_declaracao: 1, linha_ultimo_uso: 1}}`

**After Line 2** `(X 5 +)`:
- Line: `uses` variable X
- Exists? `YES`
- Initialized? `YES`
- Type: `int`
- `Γ₁ ⊢ X : int`, `Γ₁ ⊢ 5 : int`
- `promover_tipo(int, int) = int`
- `Γ₁ ⊢ (X 5 +) : int`
- `Γ₂ = {X: {tipo: int, inicializada: true, escopo: 0, linha_declaracao: 1, linha_ultimo_uso: 2}}`

**After Line 3** `(20 Y)`:
- Operation: `MEM_STORE`
- Value: `20`, Type: `int`
- Variable: `Y`
- `Γ₃ = {X: {tipo: int, inicializada: true, escopo: 0, linha_declaracao: 1, linha_ultimo_uso: 2}, Y: {tipo: int, inicializada: true, escopo: 0, linha_declaracao: 3, linha_ultimo_uso: 3}}`

**Summary Table**:
| Line | Operation | Added | Used | Γ State |
|------|-----------|-------|------|---------|
| 0 | (initial) | - | - | `{}` |
| 1 | `(10 X)` | `X` | - | `{X: (int, true)}` |
| 2 | `(X 5 +)` | - | `X` | `{X: (int, true)}` |
| 3 | `(20 Y)` | `Y` | - | `{X: (int, true), Y: (int, true)}` |

---

## Template 4.2 Answers

**After Line 1**: `Γ₁ = {X: (int, true)}`

**Line 2 Validation** `(Y)`:
- Operation: `MEM_LOAD`
- Check 1: `Γ₁.buscar("Y") = None`
- Result: `NO`
- Check 2: `Γ₁.verificar_inicializacao("Y")` raises error
- Result: `FAIL`

**Error**:
- Type: `memoria`
- Message: `"Variável 'Y' não declarada ou não inicializada"`
- File: `tabela_simbolos.py`
- Line: ~50-60
- Function: `verificar_inicializacao`

**Fix**:
- Add before Line 2: `( <value> Y )`
- After fix: `Γ₁ = {X: (int, true), Y: (<type>, true)}`

---

## Template 5.1 Answers

**Line 1**:
- `Γ₀ ⊢ 5 : int`, `Γ₀ ⊢ 3 : int`
- `promover_tipo(int, int) = int`
- `Γ₀ ⊢ (5 3 +) : int`
- `linha_1_tipo = int`

**Line 2**:
- Operation: `RES`
- RES operand: `1`
- RES operand type: `int`

**Calculation**:
- Current line: `2`
- RES argument: `1`
- Referenced line = `2 - 1 = 1`

**Validation**:
- Referenced line: `1`
- Valid range: `>= 1 and < 2`
- Valid? `YES`
- Lookup: `linha_1_tipo = int`
- Exists? `YES`

**Type Inference**:
- Type of line 1: `int`
- `Γ₀ ⊢ (1 RES) : int`

---

## Template 5.2 Answers

**Line 1** `(10 5 /)`:
- Operator / is: `STRICT`
- Types: `(int, int)`
- Compatible? `YES`
- `linha_1_tipo = int`

**Line 2** `(3.5 2.0 +)`:
- Types: `(real, real)`
- `promover_tipo(real, real) = real`
- `linha_2_tipo = real`

**Line 3** `(2 RES 1 RES +)`:
- **First RES**: Current: `3`, Referenced: `3 - 2 = 1`, Type: `int`
  - `Γ₀ ⊢ (2 RES) : int`
- **Second RES**: Current: `3`, Referenced: `3 - 1 = 2`, Type: `real`
  - `Γ₀ ⊢ (1 RES) : real`

**Addition**:
- Expression: `(int real +)`
- Types: `(int, real)`
- Operator + is: `PERMISSIVE`
- Compatible? `YES`
- `promover_tipo(int, real) = real`
- `Γ₀ ⊢ (2 RES 1 RES +) : real`

---

## Template 6.1 Answers

**Operands**:
- `Γ ⊢ 10 : int` (no decimal point)
- `Γ ⊢ 3.0 : real` (has .0 decimal)

**Operator**:
- Operator / is: `STRICT`
- Accepts: `(int, int)`
- Current: `(int, real)`

**Compatibility**:
- Function: `tipos_compativeis_divisao_inteira(int, real)`
- Result: `FALSE`
- Why? "Division operator requires both operands to be integers, but received real"

**Error**:
- Type: `tipo`
- Message: `"Operador '/' requer operandos inteiros (recebeu int e real)"`

**Fixes**:
- Option 1: Use `|` instead: `(10 3.0 |)` (real division)
- Option 2: Convert 3.0 to 3: `(10 3 /)`
- Better: Option 1 (preserves semantic intent if real result desired)

---

## Template 6.2 Answers

**Value Evaluation**:
- Operator > is: `comparison`
- Result type: `boolean`
- `Γ ⊢ (5 3 >) : boolean`

**MEM Operation**:
- Operation: `MEM_STORE`
- Value: `(5 3 >)`
- Value type: `boolean`
- Variable: `X`

**Restrictions**:
- MEM can store: `int, real` (NOT boolean)
- Current type: `boolean`
- Allowed? `NO`

**Error**:
- Why? "Memory operations are restricted to numeric types only (int/real). Boolean values cannot be persisted in memory."
- Message: `"MEM não aceita valor do tipo boolean (apenas int ou real)"`
- File: `analisador_memoria_controle.py`

**Fixes**:
- Option 1: Store numeric value: `(100 X)` or `(0 X)`
- Option 2: Use truthiness conversion - NOT VALID
- Is Option 2 valid? `NO`
- Why? "Truthiness (para_booleano) converts FROM numeric TO boolean for logical ops, not the reverse"

---

## Template 6.3 Answers

**Parameters**:
- Init: `1.5`, Type: `real`
- End: `10.5`, Type: `real`
- Step: `0.5`, Type: `real`
- Body: `(X 2 *)`

**Requirements**:
- Init type: `int`
- End type: `int`
- Step type: `int`
- Current: `(real, real, real)`

**Compatibility**:
- All integers? `NO`
- Init: `WRONG` (real instead of int)
- End: `WRONG` (real instead of int)
- Step: `WRONG` (real instead of int)

**Error**:
- Message: `"FOR requer início, fim e passo inteiros (recebeu real, real, real)"`
- Why? "FOR implements integer-based iteration. The loop counter must be discrete (int) to ensure termination and predictable step increments."

**Fix**:
- Corrected: `(1 10 1 (X 2 *) FOR)`
- Changes:
  - Init: `1.5` → `1`
  - End: `10.5` → `10`
  - Step: `0.5` → `1`

---

**End of Templates**

**Practice Recommendations**:
1. Complete each template 3 times without looking at answers
2. Time yourself - aim for cookbook time budgets
3. Practice drawing derivation trees freehand
4. Verbalize each step as you write (simulate oral defense)
5. Create your own templates for mixed scenarios

**Good luck with your defense preparation!** 🎓
