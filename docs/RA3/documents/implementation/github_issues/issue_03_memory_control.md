# Issue #3: Implement Memory and Control Flow Validation

## Labels
- `phase-3-semantic`
- `memory-validation`
- `control-flow`
- `high-priority`

## Assignee
**Aluno 3** (Task from section 7.3 of requirements)

---

## Description

Implement semantic validation for memory operations and control structures.

This module ensures that memory variables are initialized before use, validates special commands like `RES`, and verifies that control structures (FOR, WHILE, IFELSE) are correctly formed with boolean conditions.

---

## Responsibilities

- Validate memory initialization before use
- Verify correct usage of special commands
- Validate control structure formation
- Implement scope logic
- Complement type checking with memory/control validations

---

## Specific Tasks

### 1. Memory Validation (`analisarSemanticaMemoria()`)

#### `(V MEM)` - Memory Assignment

- [ ] Mark MEM as initialized in symbol table
- [ ] Store type of value V
- [ ] Verify V is not boolean type
- [ ] Add MEM to current scope

#### `(MEM)` - Memory Read

- [ ] Check if MEM exists in symbol table
- [ ] Check if MEM was initialized
- [ ] Error if uninitialized:
  ```
  ERRO SEMÂNTICO [Linha X]: Memória 'MEM' utilizada sem inicialização
  ```
- [ ] Retrieve and propagate MEM's type

#### `(N RES)` - Result Reference

- [ ] Verify N is non-negative integer literal
- [ ] Verify N doesn't exceed current line number
- [ ] Verify line (current - N) has valid result
- [ ] Propagate type from referenced line
- [ ] Error if invalid reference

### 2. Control Structure Validation (`analisarSemanticaControle()`)

#### General Validation

- [ ] Verify control structures use postfix notation correctly
- [ ] Count operands match control structure requirements

#### `WHILE` Loop

- [ ] Verify condition expression returns boolean type
- [ ] Verify body is valid expression/block
- [ ] Error if condition is not boolean

#### `FOR` Loop

- [ ] Verify initialization, condition, increment are valid
- [ ] Verify condition returns boolean
- [ ] Verify body is valid expression/block

#### `IFELSE` Conditional

- [ ] Verify condition returns boolean
- [ ] Verify both branches exist
- [ ] Verify both branches have compatible types (for type inference)
- [ ] Result type is promotion of branch types

### 3. Scope Management

- [ ] Implement scope stack for nested structures

- [ ] Push new scope on entering control structure

- [ ] Pop scope on exiting control structure

- [ ] Memory variables are file-scoped (persist across lines in same file)

- [ ] Verify variables defined in inner scope don't leak out

### 4. Error Reporting

- [ ] Error messages for uninitialized memory

- [ ] Error messages for invalid RES references

- [ ] Error messages for malformed control structures

- [ ] Error messages for non-boolean conditions

- [ ] Append errors to list from Issue #2

---

## Interface Specification

### Input
- **`arvoreSintatica`**: AST (type-annotated from Issue #2)
- **`tabelaSimbolos`**: Symbol table from Issue #1

### Output
- **`errosSemanticos`**: List of memory/control errors
- **`tabelaSimbolos`**: Updated with memory initialization info

### Execution
Called sequentially after `analisarSemantica()` from Issue #2

### Collaborates With
Issue #2 (receives type-annotated tree, adds memory/control validation)

---

## Acceptance Criteria

- [ ] Detects uninitialized memory reads
- [ ] Validates `(V MEM)` marks memory as initialized
- [ ] Validates `(N RES)` references are in bounds and valid
- [ ] Prevents storing boolean values in memory
- [ ] Validates all control structure conditions are boolean
- [ ] Validates control structure formation in RPN
- [ ] Scope tracking works correctly for nested structures
- [ ] **Unit tests for:**
  - Memory initialization tracking
  - Uninitialized memory detection
  - RES reference validation (valid and invalid N)
  - Each control structure type
  - Boolean condition requirement
  - Nested scopes
  - Error cases for each validation
- [ ] Code follows PEP 8 with docstrings
- [ ] Error messages follow project format

---

## Unit Testing Requirements

Create unit tests in `tests/RA3/test_validador_memoria.py` and `test_validador_controle.py`:

### Memory Validation Tests

```python
def test_memoria_inicializada():
    """Test reading initialized memory: (X MEM) then (X)"""
    # Should succeed and propagate type

def test_memoria_nao_inicializada():
    """Test reading uninitialized memory: (X) without prior (V X)"""
    # Should raise error

def test_memoria_tipo_armazenado():
    """Test memory stores correct type"""
    # Type of (MEM) should match type of stored value

def test_boolean_nao_pode_ser_armazenado():
    """Test storing boolean in memory: ((5 3 >) MEM) → ERROR"""
    # Should raise error

def test_res_referencia_valida():
    """Test valid RES reference: (2 RES) on line 5"""
    # Should retrieve type from line 3

def test_res_referencia_invalida_negativa():
    """Test invalid RES with negative N: (-1 RES)"""
    # Should raise error

def test_res_referencia_invalida_fora_limites():
    """Test invalid RES exceeding line count: (100 RES) on line 5"""
    # Should raise error

def test_res_nao_inteiro():
    """Test RES with non-integer: (2.5 RES)"""
    # Should raise error
```

### Control Flow Tests

```python
def test_while_condicao_booleana():
    """Test WHILE with boolean condition"""
    # Should accept boolean expression

def test_while_condicao_nao_booleana():
    """Test WHILE with non-boolean condition: (5 body WHILE)"""
    # Should raise error

def test_for_estrutura_valida():
    """Test valid FOR structure"""
    # Should validate initialization, condition, increment

def test_ifelse_condicao_booleana():
    """Test IFELSE with boolean condition"""
    # Should accept boolean expression

def test_ifelse_condicao_nao_booleana():
    """Test IFELSE with non-boolean: (5 true-branch false-branch IFELSE)"""
    # Should raise error

def test_ifelse_tipo_ramos():
    """Test IFELSE branch type compatibility"""
    # Should promote types if needed

def test_estruturas_aninhadas():
    """Test nested control structures"""
    # Should handle scope correctly
```

---

## Grading Impact

- **-20%** if memory initialization not validated
- **-20%** if control structures not validated
- **Critical for semantic correctness**

---

## Dependencies

### Requires
- Issue #1 (Symbol Table)
- Issue #2 (Type-annotated AST)

### Blocks
- Issue #4 (Final Integration)

---

## Files to Create

```
src/RA3/functions/python/
├── validador_memoria.py        # Memory validation logic
├── validador_controle.py       # Control flow validation
└── gerenciador_escopo.py       # Scope management

tests/RA3/
├── test_validador_memoria.py   # Memory tests
└── test_validador_controle.py  # Control flow tests
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 4 (Special Commands) - Lines 120-135
  - Section 5 (Control Structures) - Lines 138-144
  - Section 7.3 (Aluno 3 Tasks)

- **Memory Commands:** Requirements lines 120-135
- **Control Structures:** Requirements lines 138-144

---

## Implementation Tips

### Memory Initialization Tracking

```python
class ValidadorMemoria:
    def __init__(self, tabela_simbolos):
        self.tabela = tabela_simbolos

    def validar_leitura_memoria(self, nome_memoria, linha):
        """
        Validate memory read operation

        Args:
            nome_memoria: Memory variable name
            linha: Current line number

        Returns:
            tipo: Type of stored value

        Raises:
            ErroSemantico: If memory not initialized
        """
        if nome_memoria not in self.tabela.simbolos:
            raise ErroSemantico(
                linha=linha,
                descricao=f"Memória '{nome_memoria}' utilizada sem inicialização",
                contexto=f"({nome_memoria})"
            )

        simbolo = self.tabela.simbolos[nome_memoria]
        if not simbolo['inicializada']:
            raise ErroSemantico(
                linha=linha,
                descricao=f"Memória '{nome_memoria}' utilizada sem inicialização",
                contexto=f"({nome_memoria})"
            )

        return simbolo['tipo']

    def validar_escrita_memoria(self, nome_memoria, tipo_valor, linha):
        """
        Validate memory write operation

        Args:
            nome_memoria: Memory variable name
            tipo_valor: Type of value being stored
            linha: Current line number

        Raises:
            ErroSemantico: If trying to store boolean
        """
        if tipo_valor == 'boolean':
            raise ErroSemantico(
                linha=linha,
                descricao="Tipo 'boolean' não pode ser armazenado em memória",
                contexto=f"({nome_memoria} MEM)"
            )

        self.tabela.adicionar(nome_memoria, tipo_valor, inicializada=True)
```

### RES Reference Validation

```python
def validar_res_referencia(self, n_linhas, linha_atual, historico_resultados):
    """
    Validate RES reference

    Args:
        n_linhas: Number of lines to look back
        linha_atual: Current line number
        historico_resultados: List of (linha, tipo) tuples

    Returns:
        tipo: Type of referenced result

    Raises:
        ErroSemantico: If reference is invalid
    """
    # Check N is non-negative
    if n_linhas < 0:
        raise ErroSemantico(
            linha=linha_atual,
            descricao=f"Referência RES deve ter índice não-negativo, recebido {n_linhas}",
            contexto=f"({n_linhas} RES)"
        )

    # Check N doesn't exceed available lines
    linha_referenciada = linha_atual - n_linhas
    if linha_referenciada < 1:
        raise ErroSemantico(
            linha=linha_atual,
            descricao=f"Referência RES aponta para linha inexistente: {linha_referenciada}",
            contexto=f"({n_linhas} RES)"
        )

    # Retrieve type from referenced line
    for linha, tipo in historico_resultados:
        if linha == linha_referenciada:
            return tipo

    raise ErroSemantico(
        linha=linha_atual,
        descricao=f"Linha {linha_referenciada} não possui resultado válido",
        contexto=f"({n_linhas} RES)"
    )
```

### Control Structure Condition Validation

```python
def validar_condicao_while(self, no_while, linha):
    """
    Validate WHILE loop condition

    Args:
        no_while: AST node for WHILE structure
        linha: Line number

    Raises:
        ErroSemantico: If condition is not boolean
    """
    # Assuming RPN format: (condition body WHILE)
    # First child should be condition
    no_condicao = no_while.filhos[0]

    if no_condicao.tipo_inferido != 'boolean':
        raise ErroSemantico(
            linha=linha,
            descricao=f"Condição de WHILE deve ser booleana, encontrado '{no_condicao.tipo_inferido}'",
            contexto=self.gerar_contexto(no_while)
        )
```

### Scope Management

```python
class GerenciadorEscopo:
    def __init__(self):
        self.pilha_escopos = [{}]  # Stack of scopes
        self.nivel_atual = 0

    def entrar_escopo(self):
        """Enter new scope (push)"""
        self.pilha_escopos.append({})
        self.nivel_atual += 1

    def sair_escopo(self):
        """Exit current scope (pop)"""
        if self.nivel_atual > 0:
            self.pilha_escopos.pop()
            self.nivel_atual -= 1

    def adicionar_variavel_local(self, nome, tipo):
        """Add variable to current scope"""
        self.pilha_escopos[-1][nome] = tipo

    def buscar_variavel(self, nome):
        """Search variable in scope stack (inner to outer)"""
        for escopo in reversed(self.pilha_escopos):
            if nome in escopo:
                return escopo[nome]
        return None
```

---

## Notes

- Memory variables (MEM) persist across lines in the **same file**
- Each file has independent memory scope
- Boolean type **cannot** be stored in memory
- `RES` references are **zero-based** or **one-based** depending on your design choice (document clearly!)
- Control structure conditions **must** be boolean
- Scope management is for control structures, not memory variables
- This is a **high-priority** issue as it catches critical runtime errors
- Coordinate with Issue #2 to ensure error lists are merged properly
