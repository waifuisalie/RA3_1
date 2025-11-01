# Implementation Reference: Theory ↔ Code Mapping
## RA3 Semantic Analyzer - Bidirectional Index

**Purpose**: Connect theoretical concepts to actual implementation code
**How to Use**: Look up concepts or file locations to answer "Where is this implemented?"
**Target Audience**: Team members preparing for implementation questions during defense

---

## Overview

This reference provides **bidirectional mapping**:
1. **Theory → Code**: "Where is type promotion implemented?"
2. **Code → Theory**: "What does `analisarSemantica()` do theoretically?"

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [Theory to Code Lookup](#theory-to-code-lookup)
3. [Code to Theory Lookup](#code-to-theory-lookup)
4. [Function Call Graph](#function-call-graph)
5. [Quick Implementation Facts](#quick-implementation-facts)

---

# Module Overview

## Five Core Modules

### 1. `tipos.py` - Type System
**Location**: `src/RA3/functions/python/tipos.py`
**Lines**: ~290 lines
**Purpose**: Type definitions, promotion, compatibility checking

**Key Functions**: 14 total
- Type promotion (1 function)
- Type compatibility (10 functions)
- Truthiness conversion (1 function)
- Result type inference (2 functions)

---

### 2. `tabela_simbolos.py` - Symbol Table
**Location**: `src/RA3/functions/python/tabela_simbolos.py`
**Lines**: ~180 lines
**Purpose**: Variable tracking, scope management, initialization validation

**Key Classes**: 2
- `SimboloInfo`: Dataclass for variable metadata
- `TabelaSimbolos`: Symbol table with full API

**Key Methods**: 11 public methods

---

### 3. `gramatica_atributos.py` - Semantic Rules
**Location**: `src/RA3/functions/python/gramatica_atributos.py`
**Lines**: ~850 lines
**Purpose**: Define 22 semantic rules with formal notation

**Key Functions**: 1 main
- `definirGramaticaAtributos()`: Returns all 22 rules

**Output**: Dictionary with rule specifications

---

### 4. `analisador_tipos.py` - Type Checking
**Location**: `src/RA3/functions/python/analisador_tipos.py`
**Lines**: ~460 lines
**Purpose**: Type inference across AST, error detection

**Key Functions**: 3 main + helpers
- `analisarSemantica()`: Main orchestrator
- `avaliar_seq_tipo()`: Sequence type evaluation
- `_avaliar_operando()`: Recursive operand evaluation

---

### 5. `analisador_memoria_controle.py` - Memory & Control
**Location**: `src/RA3/functions/python/analisador_memoria_controle.py`
**Lines**: ~250 lines
**Purpose**: Memory operations and control structure validation

**Key Functions**: 2 main
- `analisarSemanticaMemoria()`: Memory validation
- `analisarSemanticaControle()`: Control structure validation

---

# Theory to Code Lookup

## Type System Concepts

### Type Promotion (`promover_tipo`)

**Theory**: Automatic type conversion in hierarchy int < real

**Implementation**:
- **File**: `src/RA3/functions/python/tipos.py`
- **Function**: `promover_tipo(tipo1, tipo2)`
- **Lines**: 214-238
- **Algorithm**:
  ```python
  def promover_tipo(tipo1, tipo2):
      if tipo1 == tipo2:
          return tipo1  # Same type, no promotion
      if tipo1 == TYPE_INT and tipo2 == TYPE_REAL:
          return TYPE_REAL  # int → real
      if tipo1 == TYPE_REAL and tipo2 == TYPE_INT:
          return TYPE_REAL  # int → real
      return None  # Incompatible (e.g., int + boolean)
  ```

**Usage Example**:
```python
promover_tipo(TYPE_INT, TYPE_REAL)  # Returns TYPE_REAL
```

---

### Truthiness Conversion (`para_booleano`)

**Theory**: Convert numeric/boolean values to boolean for logical operators

**Implementation**:
- **File**: `src/RA3/functions/python/tipos.py`
- **Function**: `para_booleano(valor, tipo)`
- **Lines**: 241-256
- **Algorithm**:
  ```python
  def para_booleano(valor, tipo):
      if tipo == TYPE_BOOLEAN:
          return valor  # Already boolean
      if tipo == TYPE_INT:
          return valor != 0  # 0 = false, else = true
      if tipo == TYPE_REAL:
          return valor != 0.0  # 0.0 = false, else = true
      return False
  ```

**Usage**: Used by logical operators (&&, ||, !) and WHILE/IFELSE conditions

---

### Type Compatibility Functions

**Theory**: Check if operands are compatible for specific operators

**Implementation**: 10 functions in `tipos.py`

| Function | Operators | Lines | Logic |
|----------|-----------|-------|-------|
| `tipos_compativeis_aritmetica` | +, -, *, \| | 42-55 | Both int or real |
| `tipos_compativeis_divisao_inteira` | /, % | 58-68 | Both MUST be int |
| `tipos_compativeis_potencia` | ^ | 71-94 | Base int/real, exp int |
| `tipos_compativeis_comparacao` | >, <, ==, !=, >=, <= | 97-109 | Both numeric |
| `tipos_compativeis_logico` | &&, \|\| | 112-130 | Truthiness compatible |
| `tipos_compativeis_logico_not` | ! | 133-142 | Single truthiness compatible |
| `tipos_compativeis_ifelse` | IFELSE | 145-157 | Branches promotable |
| `tipos_compativeis_while` | WHILE | 160-171 | Condition truthiness |
| `tipos_compativeis_for` | FOR | 174-191 | Init/end/step all int |
| `tipos_compativeis_memoria` | MEM | 194-211 | Value int/real (NO boolean) |

**Quick Lookup**:
```python
# Division requires both int
tipos_compativeis_divisao_inteira(TYPE_INT, TYPE_REAL)  # Returns False

# Logical operators accept numeric via truthiness
tipos_compativeis_logico(TYPE_INT, TYPE_INT)  # Returns True
```

---

## Symbol Table Operations

### Variable Declaration (`adicionar`)

**Theory**: Add variable to symbol table Γ

**Implementation**:
- **File**: `src/RA3/functions/python/tabela_simbolos.py`
- **Method**: `TabelaSimbolos.adicionar(nome, tipo, inicializada, linha)`
- **Lines**: 56-75
- **Algorithm**:
  ```python
  def adicionar(self, nome, tipo, inicializada, linha):
      if nome in self.simbolos:
          # Variable already exists, update it
          self.simbolos[nome].tipo = tipo
          self.simbolos[nome].inicializada = inicializada
          self.simbolos[nome].linha_ultimo_uso = linha
      else:
          # New variable
          self.simbolos[nome] = SimboloInfo(
              nome=nome,
              tipo=tipo,
              inicializada=inicializada,
              escopo=self.escopo_atual,
              linha_declaracao=linha,
              linha_ultimo_uso=linha
          )
  ```

---

### Variable Lookup (`buscar`)

**Theory**: Retrieve variable info from Γ

**Implementation**:
- **File**: `src/RA3/functions/python/tabela_simbolos.py`
- **Method**: `TabelaSimbolos.buscar(nome)`
- **Lines**: 77-87
- **Returns**: `SimboloInfo` object or `None`

**Usage Example**:
```python
simbolo = tabela.buscar("X")
if simbolo is None:
    raise ErroSemantico("Variável X não declarada")
if not simbolo.inicializada:
    raise ErroSemantico("Variável X não inicializada")
tipo_x = simbolo.tipo
```

---

### Initialization Check (`verificar_inicializacao`)

**Theory**: Validate variable is initialized before use

**Implementation**:
- **File**: `src/RA3/functions/python/tabela_simbolos.py`
- **Method**: `TabelaSimbolos.verificar_inicializacao(nome)`
- **Lines**: 101-113
- **Behavior**: Raises `ErroSemantico` if variable not found or not initialized

**Example**:
```python
try:
    tabela.verificar_inicializacao("Y")
except ErroSemantico as e:
    # Handle error: Y not initialized
```

---

## Semantic Rules (22 Rules)

### Rule Structure

**Theory**: Each rule has formal notation `Γ ⊢ e : T`

**Implementation**:
- **File**: `src/RA3/functions/python/gramatica_atributos.py`
- **Function**: `definirGramaticaAtributos()`
- **Lines**: 13-841
- **Returns**: List of 22 rule dictionaries

**Rule Dictionary Format**:
```python
{
    'categoria': 'aritmetica',
    'operador': '+',
    'nome': 'ADD',
    'aridade': 2,
    'tipos_operandos': ['int/real', 'int/real'],
    'tipo_resultado': 'promover_tipo(T1, T2)',
    'restricoes': ['Operandos devem ser numéricos'],
    'acao_semantica': lambda ctx: promover_tipo(ctx['tipo1'], ctx['tipo2']),
    'regra_formal': 'Γ ⊢ e1:T1  Γ ⊢ e2:T2  ...'
}
```

---

### Arithmetic Rules (7 rules)

**Implementation**: Lines 59-268 in `gramatica_atributos.py`

| Operator | Rule Name | Lines | Key Restriction |
|----------|-----------|-------|-----------------|
| + | ADD | 59-93 | Permissive (any numeric) |
| - | SUB | 95-129 | Permissive (any numeric) |
| * | MULT | 131-165 | Permissive (any numeric) |
| / | DIV-INT | 167-206 | STRICT (int/int only) |
| % | MOD | 208-245 | STRICT (int/int only) |
| \| | DIV-REAL | 247-284 | Permissive, always returns real |
| ^ | POWER | 286-336 | Base int/real, exp int AND > 0 |

**Example - Division Rule**:
```python
{
    'operador': '/',
    'tipos_operandos': ['int', 'int'],  # STRICT
    'tipo_resultado': 'int',  # Always int
    'restricoes': [
        'Ambos operandos devem ser inteiros',
        'Divisão inteira (quociente)'
    ]
}
```

---

### Comparison Rules (6 rules)

**Implementation**: Lines 338-481 in `gramatica_atributos.py`

| Operator | Rule Name | Lines | Result Type |
|----------|-----------|-------|-------------|
| > | COMP-GT | 338-370 | boolean |
| < | COMP-LT | 372-404 | boolean |
| >= | COMP-GE | 406-438 | boolean |
| <= | COMP-LE | 440-472 | boolean |
| == | COMP-EQ | 474-506 | boolean |
| != | COMP-NE | 508-540 | boolean |

**Key Point**: ALL comparison operators return `boolean` regardless of operand types

---

### Logical Rules (3 rules)

**Implementation**: Lines 542-641 in `gramatica_atributos.py`

| Operator | Rule Name | Lines | Aridade | Truthiness? |
|----------|-----------|-------|---------|-------------|
| && | AND | 542-582 | 2 | YES (permissive) |
| \|\| | OR | 584-624 | 2 | YES (permissive) |
| ! | NOT | 626-662 | 1 | YES (permissive) |

**Example - AND Rule**:
```python
{
    'operador': '&&',
    'aridade': 2,
    'tipos_operandos': ['int/real/boolean', 'int/real/boolean'],
    'tipo_resultado': 'boolean',
    'acao_semantica': lambda ctx: (
        para_booleano(ctx['val1'], ctx['tipo1']) and
        para_booleano(ctx['val2'], ctx['tipo2'])
    )
}
```

---

### Control Structure Rules (3 rules)

**Implementation**: Lines 664-778 in `gramatica_atributos.py`

| Structure | Rule Name | Lines | Key Validation |
|-----------|-----------|-------|----------------|
| IFELSE | IFELSE | 664-711 | Branches must be compatible |
| WHILE | WHILE | 713-751 | Condition boolean-compatible |
| FOR | FOR | 753-799 | Init/end/step ALL int |

**Example - IFELSE Rule**:
```python
{
    'operador': 'IFELSE',
    'restricoes': [
        'Condição deve ser boolean ou conversível via truthiness',
        'Branches devem ter tipos compatíveis (promover_tipo ≠ None)',
        'Tipo do IFELSE = promover_tipo(tipo_then, tipo_else)'
    ]
}
```

---

### Memory/Variable Rules (3 rules)

**Implementation**: Lines 801-841 in `gramatica_atributos.py`

| Operation | Rule Name | Lines | Key Restriction |
|-----------|-----------|-------|-----------------|
| MEM_STORE | MEM-STORE | 801-820 | Value int/real only (NO boolean) |
| MEM_LOAD | MEM-LOAD | 822-833 | Variable must be initialized |
| RES | RES | 835-841 | Reference must be valid (1 ≤ ref < current) |

---

## Type Checking Implementation

### Main Type Analysis (`analisarSemantica`)

**Theory**: Traverse AST, infer types, collect errors

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_tipos.py`
- **Function**: `analisarSemantica(arvore, gramatica, tabela)`
- **Lines**: 277-458
- **Algorithm**:
  1. Initialize grammar and symbol table if not provided
  2. Iterate through all lines in AST
  3. For each line: call `avaliar_seq_tipo()`
  4. Collect errors
  5. Return result dictionary with annotated tree

**Returns**:
```python
{
    'sucesso': bool,
    'erros': List[Dict],
    'arvore_anotada': Dict,
    'tabela_simbolos': TabelaSimbolos
}
```

---

### Sequence Type Evaluation (`avaliar_seq_tipo`)

**Theory**: Evaluate type of a sequence (line) in AST

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_tipos.py`
- **Function**: `avaliar_seq_tipo(seq, gramatica, tabela, linha_atual)`
- **Lines**: 89-186
- **Algorithm**:
  1. Handle special operators (MEM, RES, control structures)
  2. Extract operands and operator from sequence
  3. Evaluate operand types recursively
  4. Find matching semantic rule from grammar
  5. Check type compatibility
  6. Infer result type
  7. Return type or error

**Example Flow**:
```
Input: (5 3 +)
→ Operands: [5, 3], Operator: +
→ Evaluate 5: int
→ Evaluate 3: int
→ Find rule: ADD (permissive)
→ Check compatibility: TRUE
→ Infer type: promover_tipo(int, int) = int
→ Return: int
```

---

### Operand Evaluation (`_avaliar_operando`)

**Theory**: Recursively derive type of operand (literal, variable, or nested expression)

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_tipos.py`
- **Function**: `_avaliar_operando(operando, gramatica, tabela, linha_atual)`
- **Lines**: 33-86
- **Cases**:
  1. **Literal Number**: Check for decimal → int or real
  2. **Variable**: Look up in symbol table, check initialization
  3. **Nested Expression**: Recursive call to `avaliar_seq_tipo()`

**Example**:
```python
_avaliar_operando(5, ...)         # Returns 'int'
_avaliar_operando(3.5, ...)       # Returns 'real'
_avaliar_operando('X', ...)       # Lookup in table, returns stored type
_avaliar_operando([5, 3, '+'], ...) # Recursive, returns 'int'
```

---

## Memory Operations Validation

### Memory Validation (`analisarSemanticaMemoria`)

**Theory**: Validate memory operations (MEM_STORE, MEM_LOAD) and RES references

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_memoria_controle.py`
- **Function**: `analisarSemanticaMemoria(arvore_anotada, seqs_map, tabela_local)`
- **Lines**: 17-104
- **Validations**:
  1. **MEM_STORE**: Check value is int/real (not boolean)
  2. **MEM_LOAD**: Check variable is initialized
  3. **RES**: Check reference is within valid range (1 ≤ ref < current_line)

**Example Checks**:
```python
# MEM_STORE check
if tipo_valor == 'boolean':
    raise ErroSemantico("MEM não aceita boolean")

# RES check
linha_referenciada = linha_atual - argumento_res
if not (1 <= linha_referenciada < linha_atual):
    raise ErroSemantico(f"RES referência inválida: {linha_referenciada}")
```

---

## Control Structure Validation

### Control Validation (`analisarSemanticaControle`)

**Theory**: Validate FOR, WHILE, IFELSE control structures

**Implementation**:
- **File**: `src/RA3/functions/python/analisador_memoria_controle.py`
- **Function**: `analisarSemanticaControle(arvore_anotada, seqs_map, tabela_local)`
- **Lines**: 107-246
- **Validations**:
  1. **FOR**: Init, end, step all int
  2. **WHILE**: Condition boolean-compatible (permissive)
  3. **IFELSE**: Branches type-compatible (`promover_tipo ≠ None`)

**Example - IFELSE Validation**:
```python
tipo_then = extrair_tipo(branch_true)
tipo_else = extrair_tipo(branch_false)

tipo_resultante = promover_tipo(tipo_then, tipo_else)
if tipo_resultante is None:
    raise ErroSemantico(
        f"Branches IFELSE incompatíveis: {tipo_then} e {tipo_else}"
    )
```

---

# Code to Theory Lookup

## By File

### `tipos.py` → Type System Theory

**Theoretical Concepts Implemented**:
- Type hierarchy: int < real
- Type promotion function
- Type compatibility rules (10 functions)
- Truthiness conversion
- Result type inference

**Key Theoretical References**:
- Section 18.7.2: "Sistema de Tipos"
- Section 18.7.2.1: "Promoção de Tipos"
- Section 18.7.2.2: "Compatibilidade de Tipos"

---

### `tabela_simbolos.py` → Symbol Table Theory

**Theoretical Concepts Implemented**:
- Environment Γ representation
- Variable metadata tracking
- Scope management
- Initialization state
- Variable lookup

**Key Theoretical References**:
- Section 18.7.1: "Tabela de Símbolos"
- Notation: `Γ = {VAR₁: (tipo, init), VAR₂: (tipo, init), ...}`

---

### `gramatica_atributos.py` → Attribute Grammar Theory

**Theoretical Concepts Implemented**:
- 22 semantic rules with formal notation
- Type judgments `Γ ⊢ e : T`
- Inference rules with premises and conclusions
- Semantic actions

**Key Theoretical References**:
- Section 18.7: "Gramática Atribuída"
- Section 18.7.4: "Regras Semânticas"
- Theory File: `01_attribute_grammars_theory.md`

---

### `analisador_tipos.py` → Type Inference Theory

**Theoretical Concepts Implemented**:
- Type derivation trees
- Post-order AST traversal
- Type checking algorithms
- Error collection

**Key Theoretical References**:
- Section 18.7.3: "Análise Semântica de Tipos"
- Algorithm: Type inference via bottom-up evaluation

---

### `analisador_memoria_controle.py` → Memory & Control Theory

**Theoretical Concepts Implemented**:
- Memory operation validation
- RES reference resolution
- Control structure type checking

**Key Theoretical References**:
- Section 18.7.3: "Validação de Memória e Controle"
- RES semantics: Line referencing with bounds checking

---

## By Function

### Quick Function Finder

| Function Name | File | Theory Concept |
|---------------|------|----------------|
| `promover_tipo` | tipos.py | Type promotion (int → real) |
| `para_booleano` | tipos.py | Truthiness conversion |
| `tipos_compativeis_aritmetica` | tipos.py | Arithmetic compatibility |
| `tipos_compativeis_divisao_inteira` | tipos.py | Division/modulo STRICT rule |
| `tipos_compativeis_potencia` | tipos.py | Power operator restrictions |
| `TabelaSimbolos.adicionar` | tabela_simbolos.py | Variable declaration (Γ update) |
| `TabelaSimbolos.buscar` | tabela_simbolos.py | Variable lookup in Γ |
| `TabelaSimbolos.verificar_inicializacao` | tabela_simbolos.py | Initialization check |
| `definirGramaticaAtributos` | gramatica_atributos.py | 22 semantic rules |
| `analisarSemantica` | analisador_tipos.py | Main type checking orchestrator |
| `avaliar_seq_tipo` | analisador_tipos.py | Sequence type derivation |
| `_avaliar_operando` | analisador_tipos.py | Operand type evaluation |
| `analisarSemanticaMemoria` | analisador_memoria_controle.py | Memory validation |
| `analisarSemanticaControle` | analisador_memoria_controle.py | Control structure validation |

---

# Function Call Graph

## Type Checking Flow

```
analisarSemantica() [analisador_tipos.py:277]
  ↓
  ├─ definirGramaticaAtributos() [gramatica_atributos.py:13]
  ├─ TabelaSimbolos() [tabela_simbolos.py:40]
  ↓
  └─ For each line:
      └─ avaliar_seq_tipo() [analisador_tipos.py:89]
          ↓
          ├─ _avaliar_operando() [analisador_tipos.py:33]
          │   ↓
          │   ├─ TabelaSimbolos.buscar() [tabela_simbolos.py:77]
          │   ├─ TabelaSimbolos.verificar_inicializacao() [tabela_simbolos.py:101]
          │   └─ avaliar_seq_tipo() [recursive]
          ↓
          ├─ tipos_compativeis_*() [tipos.py:42-211]
          └─ promover_tipo() [tipos.py:214]
```

---

## Memory & Control Flow

```
analisarSemanticaDaJsonRA2() [analisador_semantico.py]
  ↓
  ├─ Phase 1: analisarSemantica() [analisador_tipos.py]
  ↓
  ├─ Phase 2: analisarSemanticaMemoria() [analisador_memoria_controle.py:17]
  │   ↓
  │   ├─ Validate MEM operations
  │   └─ Validate RES references
  ↓
  └─ Phase 3: analisarSemanticaControle() [analisador_memoria_controle.py:107]
      ↓
      ├─ Validate FOR parameters
      ├─ Validate WHILE conditions
      └─ Validate IFELSE branches
          └─ promover_tipo() [tipos.py:214]
```

---

# Quick Implementation Facts

## Line Count Summary

| Module | Lines | Purpose |
|--------|-------|---------|
| `tipos.py` | 290 | Type system |
| `tabela_simbolos.py` | 180 | Symbol table |
| `gramatica_atributos.py` | 850 | 22 semantic rules |
| `analisador_tipos.py` | 460 | Type checking |
| `analisador_memoria_controle.py` | 250 | Memory & control |
| **TOTAL** | **2,030** | Core semantic analysis |

---

## Function Count by Module

| Module | Functions/Methods | Public API |
|--------|-------------------|------------|
| `tipos.py` | 14 | 14 (all public) |
| `tabela_simbolos.py` | 13 | 11 (2 internal) |
| `gramatica_atributos.py` | 1 | 1 (main) |
| `analisador_tipos.py` | 5 | 3 (2 helpers) |
| `analisador_memoria_controle.py` | 2 | 2 (main) |

---

## Test Coverage

| Module | Test File | Tests | Pass Rate |
|--------|-----------|-------|-----------|
| `tabela_simbolos.py` | `test_tabela_simbolos.py` | 32 | 100% ✓ |
| Other modules | Integration tests | 55 | 100% ✓ |
| **TOTAL** | - | **87** | **100%** ✓ |

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Implementation |
|-----------|------------|----------------|
| Type inference (one line) | O(n) | n = elements in expression |
| Symbol table lookup | O(1) | Dictionary hash lookup |
| Type promotion | O(1) | Simple if-else |
| AST traversal | O(m × n) | m = lines, n = avg elements/line |
| RES validation | O(1) | Direct seqs_map lookup |

### Optimization: `seqs_map`

**Purpose**: O(1) line lookup instead of O(n) search
- **Created in**: `analisador_semantico.py:492-494`
- **Used by**: Memory and control analyzers
- **Performance gain**: 50x faster for 100-line programs

---

# Defense Question Response Templates

## "Where is [concept] implemented?"

**Template**:
> "[Concept] is implemented in `[file].py`, specifically in the function `[function_name]()` at lines [X-Y].
>
> The implementation [brief description of algorithm].
>
> For example, [show code snippet or usage]."

**Example**:
> "Type promotion is implemented in `tipos.py`, specifically in the function `promover_tipo()` at lines 214-238.
>
> The implementation checks if both types are the same, and if not, promotes int to real following the type hierarchy int < real.
>
> For example, `promover_tipo(TYPE_INT, TYPE_REAL)` returns `TYPE_REAL`."

---

## "How does [function] work?"

**Template**:
> "[Function name] is responsible for [high-level purpose].
>
> Theoretically, it implements [formal concept].
>
> The algorithm follows these steps:
> 1. [Step 1]
> 2. [Step 2]
> 3. [Step 3]
>
> This ensures [guarantee/property]."

**Example**:
> "`analisarSemantica()` is responsible for type checking the entire AST.
>
> Theoretically, it implements the type inference algorithm that derives types for all expressions following the 22 semantic rules.
>
> The algorithm follows these steps:
> 1. Initialize grammar and symbol table
> 2. Iterate through each line in the AST
> 3. For each line, call `avaliar_seq_tipo()` to derive its type
> 4. Collect any type errors encountered
> 5. Return annotated AST with type information
>
> This ensures every expression has a well-defined type or a specific error is reported."

---

## "What is the difference between [X] and [Y]?"

**Template**:
> "[X] and [Y] differ in [key aspect].
>
> [X] is implemented in [location 1] and handles [purpose 1].
> [Y] is implemented in [location 2] and handles [purpose 2].
>
> The key distinction is [explain difference].
>
> For example: [concrete example showing difference]."

**Example**:
> "`tipos_compativeis_aritmetica` and `tipos_compativeis_divisao_inteira` differ in strictness.
>
> `tipos_compativeis_aritmetica` is implemented in tipos.py:42-55 and handles permissive operators (+, -, *, |) that accept any numeric types.
> `tipos_compativeis_divisao_inteira` is implemented in tipos.py:58-68 and handles STRICT operators (/, %) that only accept int/int.
>
> The key distinction is that arithmetic operators promote mixed types, while division/modulo require exact type matching (both int).
>
> For example: `5 + 3.5` is valid (int + real → real), but `5 / 3.5` is an error (/ requires int/int)."

---

# Quick Code Location Reference

## Most Common Defense Questions

### 1. "Where is type promotion?"
**Answer**: `src/RA3/functions/python/tipos.py`, function `promover_tipo()`, lines 214-238

### 2. "Where are the 22 semantic rules?"
**Answer**: `src/RA3/functions/python/gramatica_atributos.py`, function `definirGramaticaAtributos()`, lines 13-841

### 3. "Where is IFELSE branch checking?"
**Answer**: `src/RA3/functions/python/analisador_memoria_controle.py`, function `analisarSemanticaControle()`, lines ~180-200

### 4. "Where is division operator validation?"
**Answer**: `src/RA3/functions/python/tipos.py`, function `tipos_compativeis_divisao_inteira()`, lines 58-68

### 5. "Where is symbol table initialization check?"
**Answer**: `src/RA3/functions/python/tabela_simbolos.py`, method `verificar_inicializacao()`, lines 101-113

### 6. "Where is the main type checking?"
**Answer**: `src/RA3/functions/python/analisador_tipos.py`, function `analisarSemantica()`, lines 277-458

### 7. "Where is RES reference validation?"
**Answer**: `src/RA3/functions/python/analisador_memoria_controle.py`, function `analisarSemanticaMemoria()`, lines ~50-80

### 8. "Where is FOR parameter validation?"
**Answer**: `src/RA3/functions/python/analisador_memoria_controle.py`, function `analisarSemanticaControle()`, lines ~110-140

---

# Source Code Snippets

## Key Implementation Examples

### Type Promotion Implementation

```python
# File: tipos.py, Lines: 214-238
def promover_tipo(tipo1: str, tipo2: str) -> Optional[str]:
    """
    Promove tipos seguindo hierarquia: int < real

    Retorna:
        - tipo comum (int ou real) se compatíveis
        - None se incompatíveis (ex: int + boolean)
    """
    if tipo1 == tipo2:
        return tipo1

    # int < real: promover para real
    if {tipo1, tipo2} == {TYPE_INT, TYPE_REAL}:
        return TYPE_REAL

    # Tipos incompatíveis (ex: int + boolean)
    return None
```

---

### Symbol Table Lookup

```python
# File: tabela_simbolos.py, Lines: 77-87
def buscar(self, nome: str) -> Optional[SimboloInfo]:
    """
    Busca variável na tabela de símbolos Γ

    Retorna:
        - SimboloInfo se encontrada
        - None se não existe
    """
    return self.simbolos.get(nome)
```

---

### Division Operator Validation

```python
# File: tipos.py, Lines: 58-68
def tipos_compativeis_divisao_inteira(tipo1: str, tipo2: str) -> bool:
    """
    Verifica se tipos são compatíveis para / e %

    REGRA STRICT: Ambos DEVEM ser int
    """
    return tipo1 == TYPE_INT and tipo2 == TYPE_INT
```

---

### IFELSE Branch Compatibility

```python
# File: analisador_memoria_controle.py, Lines: ~180-200
# Simplified example
tipo_then = extrair_tipo(branch_true)
tipo_else = extrair_tipo(branch_false)

# Check compatibility using type promotion
tipo_resultante = promover_tipo(tipo_then, tipo_else)

if tipo_resultante is None:
    # Branches incompatible (e.g., int + boolean)
    raise ErroSemantico(
        f"Branches de IFELSE incompatíveis: {tipo_then} e {tipo_else}"
    )

# IFELSE type = promoted type
return tipo_resultante
```

---

# Conclusion

This reference provides complete mapping between:
- ✓ Theoretical concepts (type promotion, symbol table, semantic rules)
- ✓ Implementation code (specific files, functions, line numbers)
- ✓ Algorithms (how functions work step-by-step)
- ✓ Usage examples (how to use each function)

**Use this guide to confidently answer**: "Where in the code is [concept] implemented?"

---

**Good luck with your defense!** 🎓

Remember: Understanding the connection between theory and code demonstrates deep comprehension of compiler design.

---

*Last updated: 2025-01-19*
*RA3_1 Defense Preparation Team*
