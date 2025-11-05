# Issue #1: Implement Attribute Grammar and Symbol Table Structure

## Labels
- `phase-3-semantic`
- `symbol-table`
- `type-checking`
- `high-priority`
- `deliverable`

## Assignee
**Aluno 1** (Task from section 7.1 of requirements)

---

## Description

Implement the attribute grammar definition and symbol table infrastructure for the RPN semantic analyzer.

This is the foundational issue for the entire semantic analysis phase. The attribute grammar defines the semantic rules for type checking, and the symbol table tracks variable initialization and types throughout the program.

---

## Responsibilities

- Define attribute grammar with synthesized and inherited attributes
- Create symbol table data structure for identifiers, types, and scopes
- Document complete grammar in EBNF format
- Implement auxiliary functions for symbol table management

---

## Specific Tasks

### 1. Attribute Grammar Definition (`definirGramaticaAtributos()`)

- [ ] Define synthesized attributes for each grammar symbol:
  - `tipo`: Type of expression (int, real, boolean)
  - `valor`: Calculated value (when applicable)

- [ ] Define inherited attributes:
  - `escopo`: Scope level of variables
  - `inicializada`: For memory variables, indicates initialization status

- [ ] Create type verification rules for arithmetic operators (`+`, `-`, `*`, `|`, `/`, `%`, `^`)

- [ ] Define type promotion rules (int → real)

- [ ] Document rules for relational operators (return boolean)

- [ ] Document rules for logical operators (`&&`, `||`, `!`)

- [ ] Define semantic actions for control structures (`FOR`, `WHILE`, `IFELSE`)

### 2. Symbol Table Implementation

- [ ] Create `TabelaSimbolos` class/structure with:
  - Dictionary for storing identifiers
  - Type information per identifier
  - Initialization status tracking
  - Scope level management

- [ ] Implement `inicializarTabelaSimbolos()` - Initialize empty table

- [ ] Implement `adicionarSimbolo(nome, tipo, escopo)` - Add new symbol

- [ ] Implement `buscarSimbolo(nome)` - Retrieve symbol information

- [ ] Implement `atualizarSimbolo(nome, atributo, valor)` - Update symbol attributes

- [ ] Implement `verificarInicializacao(nome)` - Check if memory is initialized

### 3. Documentation

- [ ] Create `outputs/RA3/gramatica_atributos.md` with:
  - Complete EBNF grammar
  - All production rules with attributes
  - Semantic rules in formal notation (Γ ⊢ format)
  - Type promotion function specification
  - Examples for each operator category

---

## Interface Specification

### Input
None (grammar is fixed)

### Output
- **`gramaticaAtributos`**: Dictionary/object containing:
  - Production rules
  - Attribute definitions
  - Semantic actions

- **`tabelaSimbolos`**: Initialized symbol table structure

### Provides To
- `analisarSemantica()` (Issue #2)
- `analisarSemanticaMemoria()` (Issue #3)

---

## Acceptance Criteria

- [ ] All attributes defined for every non-terminal and terminal
- [ ] Symbol table supports add, search, update, check operations
- [ ] Grammar documentation includes all operators from `configuracaoGramatica.py`
- [ ] Formal semantic rules documented for:
  - All arithmetic operators with type promotion
  - All relational operators (return boolean)
  - All logical operators
  - Control structures
- [ ] **Unit tests created for:**
  - Symbol table operations (add, search, update)
  - Initialization status tracking
  - Scope management
- [ ] Code follows PEP 8 style guide
- [ ] Functions have docstrings with parameter and return type descriptions

---

## Unit Testing Requirements

Create unit tests in `tests/RA3/test_tabela_simbolos.py`:

```python
def test_adicionar_simbolo():
    """Test adding a new symbol to the table"""
    # Should successfully add symbol with type and scope

def test_buscar_simbolo():
    """Test retrieving an existing symbol"""
    # Should return correct symbol information

def test_simbolo_nao_existe():
    """Test searching for non-existent symbol"""
    # Should return None or raise appropriate exception

def test_atualizar_inicializacao():
    """Test marking a symbol as initialized"""
    # Should update initialization status correctly

def test_verificar_inicializacao():
    """Test checking if symbol is initialized"""
    # Should return correct boolean status

def test_escopo_aninhado():
    """Test scope management with nested scopes"""
    # Should handle multiple scope levels correctly
```

---

## Grading Impact

- **-20%** if grammar incomplete or poorly documented
- **-10%** per missing type rule
- **Base for entire semantic analysis phase** (70% of total grade)

---

## Dependencies

### Requires
- RA2 grammar from `src/RA2/functions/python/configuracaoGramatica.py`

### Blocks
- Issue #2 (Type Checking)
- Issue #3 (Memory & Control Validation)
- Issue #4 (AST Generation)

---

## Files to Create

```
src/RA3/functions/python/
├── __init__.py
├── gramatica_atributos.py    # Main implementation
├── tabela_simbolos.py         # Symbol table class
└── tipos.py                   # Type system definitions (int, real, bool)

tests/RA3/
└── test_tabela_simbolos.py    # Unit tests

outputs/RA3/
└── gramatica_atributos.md     # Grammar documentation (generated)
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 6.1 (Semantic Analyzer Specification)
  - Section 7.1 (Aluno 1 Tasks)
  - Lines 258-340 (Type rules examples)

- **Current Grammar:** `src/RA2/functions/python/configuracaoGramatica.py`
  - Lines 14-39 (Grammar definition)
  - Lines 42-67 (Token mapping)

---

## Implementation Tips

### Type Promotion Function Example

```python
def promover_tipo(tipo1: str, tipo2: str) -> str:
    """
    Promotes types according to the hierarchy: int < real

    Args:
        tipo1: First type ('int', 'real', or 'boolean')
        tipo2: Second type ('int', 'real', or 'boolean')

    Returns:
        Promoted type ('int' or 'real')

    Example:
        promover_tipo('int', 'real') → 'real'
        promover_tipo('int', 'int') → 'int'
    """
    if tipo1 == 'real' or tipo2 == 'real':
        return 'real'
    return 'int'
```

### Symbol Table Structure Example

```python
class TabelaSimbolos:
    def __init__(self):
        self.simbolos = {}  # {nome: {tipo, inicializada, escopo}}
        self.escopo_atual = 0

    def adicionar(self, nome, tipo, inicializada=False):
        self.simbolos[nome] = {
            'tipo': tipo,
            'inicializada': inicializada,
            'escopo': self.escopo_atual
        }
```

### Semantic Rule Documentation Example

For addition operator in `gramatica_atributos.md`:

```markdown
#### Adição de Inteiros

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
      Γ ⊢ e₁ + e₂ : int
```

#### Adição com Promoção de Tipo

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
──────────────────────────────
     Γ ⊢ e₁ + e₂ : real
```
```

---

## Notes

- The attribute grammar must cover **all** operators defined in `configuracaoGramatica.py`
- Boolean type is used internally but **cannot be stored in memory** (MEM)
- Each file represents an independent memory scope
- Uninitialized memories will be detected in Issue #3, but the tracking structure is defined here
- This is a **high-priority** issue as it blocks all other semantic analysis work
