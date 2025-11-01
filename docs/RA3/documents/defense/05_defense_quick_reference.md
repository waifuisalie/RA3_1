# Quick Reference: RA3 Semantic Rules
## 1-Page Cheat Sheet for Defense

**Print this page and keep it with you!**

---

## Operator Type Signatures

### Arithmetic Operators

| Op | Name | Types Accepted | Result Type | Rule Type |
|----|------|----------------|-------------|-----------|
| `+` | Add | int/int, int/real, real/int, real/real | promover_tipo(T₁, T₂) | PERMISSIVE |
| `-` | Sub | int/int, int/real, real/int, real/real | promover_tipo(T₁, T₂) | PERMISSIVE |
| `*` | Mult | int/int, int/real, real/int, real/real | promover_tipo(T₁, T₂) | PERMISSIVE |
| `/` | DivInt | **int/int ONLY** | int | **STRICT** |
| `%` | Mod | **int/int ONLY** | int | **STRICT** |
| `\|` | DivReal | int/int, int/real, real/int, real/real | **real (ALWAYS)** | PERMISSIVE |
| `^` | Power | base(int/real), **exp(int ONLY, >0)** | typeof(base) | **SPECIAL** |

### Comparison Operators (ALL return boolean)

| Op | Types Accepted | Result Type |
|----|----------------|-------------|
| `>` `<` `>=` `<=` `==` `!=` | int/real (any combo) | **boolean** |

### Logical Operators (ALL return boolean, accept truthiness)

| Op | Name | Types Accepted | Result Type | Truthiness |
|----|------|----------------|-------------|------------|
| `&&` | AND | int/real/boolean | boolean | 0/0.0 = false |
| `\|\|` | OR | int/real/boolean | boolean | ≠0 = true |
| `!` | NOT | int/real/boolean (unary) | boolean | Inverts truth value |

### Memory Operators

| Op | Syntax | Types Accepted | Result Type | Restrictions |
|----|--------|----------------|-------------|--------------|
| MEM (store) | `(value VAR)` | **int/real ONLY** | stored type | **NO BOOLEAN!** |
| VAR (load) | `(VAR)` | any | variable type | Must be initialized |
| RES (ref) | `(N RES)` | int (line number) | referenced line type | N ≤ linha_atual - 1 |

### Control Structures

| Structure | Syntax | Parameter Types | Body | Result Type | Rules |
|-----------|--------|-----------------|------|-------------|-------|
| IFELSE | `(cond then else IFELSE)` | cond: boolean-compat | any | promover_tipo(then, else) | **Branches MUST be compatible** |
| WHILE | `(cond body WHILE)` | cond: boolean-compat | any | typeof(body) | Condition must be truthy-compatible |
| FOR | `(init end step body FOR)` | **ALL int** | any | typeof(body) | **init, end, step MUST be int** |

---

## Mnemonic Devices

### "STRICT TWO" - Only Accept int/int
- **/**ivision **I**nteger
- **%** **M**odulo

Remember: "Strict siblings slash and mod, integers only, that's their job!"

### "ALWAYS REAL" - Result is Always real
- **|** Pipe (division real)

Remember: "Pipe flows real numbers only!"

### "EXPONENT RULES" for ^
- **E**xponent must be **I**nteger
- **E**xponent must be **P**ositive (> 0)

Remember: "Power's exponent: Integer and Positive (EIP)!"

### "BBC" - IFELSE Branch Compatibility
- **B**ranches must **B**e **C**ompatible

Remember: "BBC - Both Branches Compatible!"

### "MNB" - Memory No Boolean
- **M**emory **N**o **B**oolean

Remember: "MNB - Memories Never Boolean!"

---

## Type Promotion Visual Matrix

```
Hierarchy:  int < real  (int can be promoted to real, not vice versa)

promover_tipo(T₁, T₂):
    ┌─────┬─────┬──────┐
    │     │ int │ real │
    ├─────┼─────┼──────┤
    │ int │ int │ real │
    ├─────┼─────┼──────┤
    │real │ real│ real │
    └─────┴─────┴──────┘

Rule: If ANY operand is real → result is real
Special: If types incompatible (e.g., int + boolean) → None (ERROR)
```

---

## Truthiness Conversion Table

| Value | Type | truthy() Result | Used In |
|-------|------|-----------------|---------|
| 0 | int | **false** | &&, \|\|, ! |
| 1, 5, -3, ... | int | **true** | &&, \|\|, ! |
| 0.0 | real | **false** | &&, \|\|, ! |
| 3.14, -2.5, ... | real | **true** | &&, \|\|, ! |
| true | boolean | **true** | &&, \|\|, ! |
| false | boolean | **false** | &&, \|\|, ! |

**Remember**: Zero is false, non-zero is true (for numeric types)

---

## Common Error Messages

| Error Message | Cause | Fix |
|---------------|-------|-----|
| "Operador '/' requer int+int" | Used real in division | Use `\|` or convert to int |
| "Expoente deve ser int" | Real exponent in power | Use int exponent |
| "Expoente deve ser positivo" | Negative/zero exponent | Use positive value |
| "Branches incompatíveis" | IFELSE type mismatch | Ensure compatible types |
| "MEM não aceita boolean" | Tried to store boolean | Don't use MEM with comparisons |
| "Variável não inicializada" | Used before MEM | Initialize with `(value VAR)` first |
| "RES referência inválida" | N too large | Check N ≤ linha_atual - 1 |
| "FOR requer int+int+int" | Non-int FOR params | Use integers for init/end/step |

---

## Quick Decision Tree for Type Derivation

```
Given: (e₁ e₂ op)

STEP 1: Derive operand types
   Γ ⊢ e₁ : T₁
   Γ ⊢ e₂ : T₂

STEP 2: Check operator category
   Is op in {+, -, *, |}?
      → Check both numeric? YES → Go to STEP 3

   Is op in {/, %}?
      → Check BOTH int? YES → Result: int
                         NO → ERROR

   Is op = ^?
      → Check base numeric? AND exp int? YES → Result: typeof(base)
                                          NO → ERROR

   Is op comparison {>, <, ...}?
      → Check both numeric? YES → Result: boolean

   Is op logical {&&, ||}?
      → Check truthy-compatible? YES → Result: boolean

STEP 3: Determine result type (for +, -, *, |)
   If op = |:
      → Result: real (ALWAYS)

   Else (op in {+, -, *}):
      → Result: promover_tipo(T₁, T₂)
```

---

## Symbol Table Checklist

When checking variable use:
1. ✓ Declared? (exists in Γ)
2. ✓ Initialized? (inicializada = true)
3. ✓ Correct type? (matches operation requirement)
4. ✓ Correct scope? (visible in current scope)

**Notation**: Γ = {VAR₁: (type, init), VAR₂: (type, init), ...}

---

## Formal Notation Quick Reference

### Type Judgment
```
Γ ⊢ e : T

Read as: "Under environment Γ, expression e has type T"
```

### Inference Rule Format
```
premise₁    premise₂    ...    premiseₙ
───────────────────────────────────────── (RULE-NAME)
             conclusion
```

### Example: Addition
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real    promover_tipo(int, real) = real
────────────────────────────────────────────────────────────────── (ADD-PROMOTE)
                    Γ ⊢ (e₁ e₂ +) : real
```

---

## 22 Semantic Rules Summary

| Category | Count | Rules |
|----------|-------|-------|
| Arithmetic | 7 | +, -, *, /, %, \|, ^ |
| Comparison | 6 | >, <, >=, <=, ==, != |
| Logical | 3 | &&, \|\|, ! |
| Control | 3 | IFELSE, WHILE, FOR |
| Memory | 3 | MEM_STORE, MEM_LOAD, RES |
| **TOTAL** | **22** | All operators covered |

---

## Type Compatibility Quick Lookup

| Question | Answer |
|----------|--------|
| Can + accept real? | YES (permissive) |
| Can / accept real? | NO (strict - int only) |
| Can ^ accept real base? | YES (but exp must be int) |
| Can MEM store boolean? | NO (int/real only) |
| Can IFELSE have int+real branches? | YES (promotes to real) |
| Can IFELSE have int+boolean branches? | NO (incompatible) |
| Can FOR have real parameters? | NO (all must be int) |
| Can WHILE have int condition? | YES (via truthiness) |
| Can comparison accept mixed types? | YES (int/real any combo) |
| Can logical accept numeric types? | YES (via truthiness) |

---

## Implementation File Quick Reference

| Concept | File | Key Function |
|---------|------|--------------|
| Type promotion | tipos.py | promover_tipo() |
| Type compatibility | tipos.py | tipos_compativeis_*() |
| Truthiness | tipos.py | para_booleano() |
| Semantic rules | gramatica_atributos.py | definirGramaticaAtributos() |
| Symbol table | tabela_simbolos.py | TabelaSimbolos class |
| Type checking | analisador_tipos.py | analisarSemantica() |
| Memory validation | analisador_memoria_controle.py | analisarSemanticaMemoria() |
| Control validation | analisador_memoria_controle.py | analisarSemanticaControle() |

---

## Last-Minute Reminders

### Before You Answer:
1. **Pause** - Take 5 seconds to think
2. **Plan** - Know which recipe to use
3. **Present** - Speak clearly as you write

### While Answering:
1. **Start with notation**: Γ ⊢ e : T
2. **Show steps**: "First..., Second..., Therefore..."
3. **Draw clearly**: Make derivation tree readable

### Common Mistakes to Avoid:
- ❌ Confusing `/` (int only) with `\|` (any numeric)
- ❌ Forgetting `^` exponent must be positive (not just int)
- ❌ Saying IFELSE can have any branch types (must be compatible!)
- ❌ Allowing boolean in MEM (it's forbidden!)
- ❌ Skipping initialization check for variables

### If Stuck:
1. Start with basics: Identify operand types
2. Check compatibility table above
3. Apply promotion if needed
4. Draw derivation tree step by step

---

## Critical Rules to Memorize

### The Three Rules You CANNOT Forget:
1. **Division `/` and modulo `%` = STRICT** (int/int only)
2. **IFELSE branches MUST be compatible** (use promover_tipo to check)
3. **MEM cannot store boolean** (int/real only)

### The Three Type Hierarchies:
1. **Promotion**: int < real (int promotes to real when mixed)
2. **Truthiness**: numeric → boolean (0/0.0 = false, else = true)
3. **No demotion**: real cannot become int automatically

### The Three Special Operators:
1. **`\|` always returns real** (even for int/int)
2. **`^` exponent must be int AND positive**
3. **Comparison always returns boolean** (regardless of operands)

---

**YOU'VE GOT THIS!**

This is your quick reference. Print it, review it, use it during practice.
Remember: Clear and correct beats fast and wrong.
Take your time, show your work, explain your reasoning.

**Good luck! 🎓**

---

*Last updated: 2025-01-19*
*RA3_1 Defense Preparation Team*
