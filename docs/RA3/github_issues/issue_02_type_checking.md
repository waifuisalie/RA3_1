# Issue #2: Implement Type Checking and Semantic Analysis

## Labels
- `phase-3-semantic`
- `type-checking`
- `high-priority`

## Assignee
**Aluno 2** (Task from section 7.2 of requirements)

---

## Description

Implement the core semantic analyzer that traverses the AST and performs type checking.

This module is responsible for ensuring type safety in the RPN language by validating that operations are performed between compatible types, implementing type coercion where appropriate, and reporting clear error messages.

---

## Responsibilities

- Traverse syntax tree from RA2
- Apply semantic rules from attribute grammar
- Detect and report type errors
- Implement type coercion (int → real)
- Generate clear error messages with line numbers

---

## Specific Tasks

### 1. AST Traversal (`analisarSemantica()`)

- [ ] Implement post-order tree traversal algorithm

- [ ] For each node, determine its type based on:
  - Literal values (int vs real detection)
  - Operator type rules
  - Child node types

- [ ] Annotate each AST node with `tipo` attribute

- [ ] Maintain current line number for error reporting

### 2. Type Verification Rules

#### Arithmetic Operators (`+`, `-`, `*`, `|`)

- [ ] Accept int/int → int
- [ ] Accept real/real → real
- [ ] Accept int/real or real/int → real (with promotion)

#### Integer-Only Operators (`/`, `%`)

- [ ] Accept only int/int → int
- [ ] Error if any operand is real

#### Exponentiation (`^`)

- [ ] Base can be int or real
- [ ] Exponent MUST be positive integer
- [ ] Result type matches base type

#### Relational Operators (`>`, `<`, `>=`, `<=`, `==`, `!=`)

- [ ] Accept int or real operands
- [ ] Always return boolean

#### Logical Operators (`&&`, `||`)

- [ ] Accept boolean operands only
- [ ] Return boolean

#### Unary NOT (`!`)

- [ ] Accept boolean operand only
- [ ] Return boolean

### 3. Type Coercion Implementation

- [ ] Create `promover_tipo(tipo1, tipo2)` function:
  ```python
  def promover_tipo(tipo1, tipo2):
      if tipo1 == 'real' or tipo2 == 'real':
          return 'real'
      return 'int'
  ```

- [ ] Apply automatically in mixed-type arithmetic operations

- [ ] Track coercion in AST annotations

### 4. Error Detection and Reporting

- [ ] Format errors as:
  ```
  ERRO SEMÂNTICO [Linha X]: <descrição>
  Contexto: <trecho do código>
  ```

- [ ] Error types to detect:
  - Type mismatch in operations
  - Real number in integer-only operations
  - Non-integer exponent in power operation
  - Non-boolean in logical operations
  - Non-boolean condition in control structures

- [ ] Collect all errors in list (don't stop at first error)

- [ ] Write errors to console and `outputs/RA3/erros_semanticos.md`

### 5. Test Functions

- [ ] Create unit tests for each operator category

- [ ] Test type promotion scenarios

- [ ] Test error detection for each error type

- [ ] Test with nested expressions

---

## Interface Specification

### Input
- **`arvoreSintatica`**: AST from RA2 parser
- **`gramaticaAtributos`**: From Issue #1
- **`tabelaSimbolos`**: From Issue #1

### Output
- **`arvoreAnotada`**: AST with type annotations on each node
- **`erros`**: List of semantic errors found

### Provides To
- Issue #3 (Memory validation - receives type-annotated AST)
- Issue #4 (AST generation - receives type-annotated AST)

---

## Acceptance Criteria

- [ ] Correctly identifies types for all literal values
- [ ] Applies type rules for all operators
- [ ] Detects integer-only operator violations
- [ ] Validates exponent is integer in power operations
- [ ] Implements type promotion correctly
- [ ] Generates clear error messages with line numbers
- [ ] All errors collected before stopping
- [ ] **Unit tests cover:**
  - Each arithmetic operator with int/int, real/real, mixed
  - Integer division and modulo with non-integer detection
  - Power operation with non-integer exponent detection
  - Relational operators returning boolean
  - Logical operators with type validation
- [ ] Code follows PEP 8 with comprehensive docstrings
- [ ] Error messages follow specified format exactly

---

## Unit Testing Requirements

Create unit tests in `tests/RA3/test_verificador_tipos.py`:

```python
def test_adicao_inteiros():
    """Test integer addition: (5 3 +) → int"""
    # Should infer type as int

def test_adicao_reais():
    """Test real addition: (5.5 2.0 +) → real"""
    # Should infer type as real

def test_promocao_tipo():
    """Test type promotion: (5 3.5 +) → real"""
    # Should promote int to real

def test_divisao_inteira_com_real():
    """Test integer division with real: (5.5 2 /) → ERROR"""
    # Should raise type error

def test_modulo_com_real():
    """Test modulo with real: (10.5 3 %) → ERROR"""
    # Should raise type error

def test_potencia_expoente_real():
    """Test power with real exponent: (2 3.5 ^) → ERROR"""
    # Should raise type error

def test_potencia_expoente_negativo():
    """Test power with negative exponent: (2 -3 ^) → ERROR"""
    # Should raise type error

def test_operador_relacional_retorna_boolean():
    """Test relational operator: (5 3 >) → boolean"""
    # Should infer type as boolean

def test_operador_logico_valida_boolean():
    """Test logical operator with non-boolean: (5 3 &&) → ERROR"""
    # Should raise type error

def test_expressao_aninhada():
    """Test nested expression: ((5 3 +) (2 4 *) |) → int"""
    # Should correctly infer types through nesting
```

---

## Grading Impact

- **-30%** if type verification not implemented correctly
- **-10%** per type rule not verified (e.g., exponent integer)
- **Forms base of 70% functionality grade**

---

## Dependencies

### Requires
- Issue #1 (Grammar and Symbol Table)
- RA2 AST from `src/RA2/functions/python/gerarArvore.py`

### Blocks
- Issue #3 (Memory & Control Flow Validation)
- Issue #4 (AST Generation & Integration)

---

## Files to Create

```
src/RA3/functions/python/
├── analisador_semantico.py    # Main semantic analyzer
├── verificador_tipos.py        # Type checking logic
└── gerador_erros.py            # Error message formatting

tests/RA3/
└── test_verificador_tipos.py   # Unit tests
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 6.1 (Semantic Analyzer Specification)
  - Section 7.2 (Aluno 2 Tasks)
  - Lines 297-307 (Error message format)

- **Type Rules Examples:** Lines 258-340 in requirements

- **Operators:** `src/RA2/functions/python/configuracaoGramatica.py` lines 36-38

---

## Implementation Tips

### Post-Order Traversal Example

```python
def analisar_no(no, tabela_simbolos):
    """
    Analyze node in post-order (children first, then parent)

    Args:
        no: AST node to analyze
        tabela_simbolos: Symbol table for variable lookup

    Returns:
        tipo_inferido: Inferred type for this node
    """
    # Base case: leaf nodes (literals, variables)
    if no.tipo == 'LITERAL':
        return inferir_tipo_literal(no.valor)

    if no.tipo == 'VARIAVEL':
        return tabela_simbolos.buscar(no.nome)['tipo']

    # Recursive case: operators
    if no.tipo == 'OPERADOR':
        # First analyze children
        tipos_filhos = [analisar_no(filho, tabela_simbolos)
                       for filho in no.filhos]

        # Then apply operator type rules
        return aplicar_regra_operador(no.operador, tipos_filhos)
```

### Type Checking for Division Example

```python
def verificar_divisao_inteira(tipo_esq, tipo_dir, linha):
    """
    Verify integer division operands are both integers

    Args:
        tipo_esq: Type of left operand
        tipo_dir: Type of right operand
        linha: Line number for error reporting

    Returns:
        'int' if valid, raises error otherwise
    """
    if tipo_esq != 'int' or tipo_dir != 'int':
        raise ErroSemantico(
            f"ERRO SEMÂNTICO [Linha {linha}]: "
            f"Divisão inteira requer operandos inteiros, "
            f"mas encontrado '{tipo_esq}' e '{tipo_dir}'"
        )
    return 'int'
```

### Error Message Format Example

```python
class ErroSemantico(Exception):
    def __init__(self, linha, descricao, contexto):
        self.linha = linha
        self.descricao = descricao
        self.contexto = contexto

    def __str__(self):
        return (
            f"ERRO SEMÂNTICO [Linha {self.linha}]: {self.descricao}\n"
            f"Contexto: {self.contexto}"
        )

# Usage:
raise ErroSemantico(
    linha=5,
    descricao="Divisão inteira requer operandos inteiros, mas encontrado 'real'",
    contexto="(5.5 2 /)"
)
```

---

## Notes

- Type promotion only applies to arithmetic operators (`+`, `-`, `*`, `|`)
- Division (`/`) and modulo (`%`) are **strictly integer-only**
- Power (`^`) allows real base but exponent must be **positive integer**
- Boolean type is internal only - cannot be stored in memory
- Collect **all** errors before stopping (don't fail-fast)
- Error messages must include line numbers for debugging
- This is a **high-priority** issue as it implements the core semantic checking
