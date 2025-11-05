# Issue #5: Create Test Files for RA3 Validation

## Labels
- `phase-3-semantic`
- `testing`
- `deliverable`
- `high-priority`

## Assignee
**All team members** (collaborative effort)

---

## Description

Create comprehensive test files to validate all semantic analysis functionality.

The test files must cover all operators, commands, control structures, and include both valid cases and error cases to ensure the semantic analyzer correctly detects all types of semantic errors.

---

## Requirements Summary

- **Minimum:** 3 test files
- **Lines:** ≥10 lines per file
- **Coverage:** All operators, commands, control structures, and error cases

---

## Test Files to Create

### Test File 1: Valid Operations (`inputs/RA3/teste1_valido.txt`)

#### Must Include:

- [ ] **All arithmetic operators:** `+`, `-`, `*`, `|`, `/`, `%`, `^`
  - Integer operations: `(5 3 +)`
  - Real operations: `(5.5 2.0 |)`
  - Mixed operations (type promotion): `(10 3.5 *)`

- [ ] **All relational operators:** `>`, `<`, `>=`, `<=`, `==`, `!=`
  - With integers: `(5 3 >)`
  - With reals: `(5.5 3.2 <=)`

- [ ] **All logical operators:** `&&`, `||`, `!`
  - Boolean expressions: `((5 3 >) (2 1 <) &&)`

- [ ] **Memory operations:**
  - Store value: `(10 X MEM)`
  - Read value (after initialization): `(X)`

- [ ] **Result reference:** `(N RES)` with valid N
  - Reference previous line: `(2 RES)`

- [ ] **At least 1 WHILE loop**
  - With boolean condition
  - With body expression

- [ ] **At least 1 FOR loop**
  - With initialization, condition, increment
  - With body expression

- [ ] **At least 1 IFELSE conditional**
  - With boolean condition
  - With both branches

- [ ] **Nested expressions:** `((A B +) (C D *) |)`

- [ ] **Type promotion examples:** `(5 3.5 +)` → real

#### Example Structure:

```
(5 3 +)
(5.5 2.0 |)
(10 3.5 *)
(100 X MEM)
(X 2 ^)
(4 RES)
(5 3 >)
((5 3 >) (10) (20) IFELSE)
((2 4 +) (3 5 *) -)
(RESULTADO MEM)
```

---

### Test File 2: Semantic Errors - Type Violations (`inputs/RA3/teste2_erros_tipos.txt`)

#### Must Include Error Cases:

- [ ] **Real number in integer division:** `(5.5 2 /)`
  - Expected error: "Divisão inteira requer operandos inteiros"

- [ ] **Real number in modulo:** `(10.5 3 %)`
  - Expected error: "Resto requer operandos inteiros"

- [ ] **Real exponent:** `(2 3.5 ^)`
  - Expected error: "Expoente deve ser inteiro"

- [ ] **Negative exponent:** `(2 -3 ^)`
  - Expected error: "Expoente deve ser positivo"

- [ ] **Boolean in arithmetic:** Using comparison result in math
  - Example: `((5 3 >) 2 +)`
  - Expected error: "Operação aritmética não aceita tipo boolean"

- [ ] **Non-boolean in logical operator:** `(5 3 &&)`
  - Expected error: "Operador lógico requer operandos booleanos"

- [ ] **Non-boolean in control condition:** `(5 body WHILE)`
  - Expected error: "Condição de controle deve ser booleana"

#### Example Structure:

```
(5.5 2 /)
(10.5 3 %)
(2 3.5 ^)
(2 -3 ^)
((5 3 >) 2 +)
(5 3 &&)
((5 3 >) ! 10 +)
(10 (5 3 +) (2 1 -) IFELSE)
((3.5 2 /) 5 +)
(100 50.5 %)
```

---

### Test File 3: Semantic Errors - Memory & Control (`inputs/RA3/teste3_erros_memoria.txt`)

#### Must Include Error Cases:

- [ ] **Uninitialized memory read:** `(X)` before any `(V X)`
  - Expected error: "Memória 'X' utilizada sem inicialização"

- [ ] **Invalid RES reference - negative N:** `(-1 RES)`
  - Expected error: "Referência RES deve ter índice não-negativo"

- [ ] **Invalid RES reference - exceeds line count:** `(100 RES)` on line 5
  - Expected error: "Referência RES aponta para linha inexistente"

- [ ] **Boolean stored in memory:** `((5 3 >) COND MEM)`
  - Expected error: "Tipo 'boolean' não pode ser armazenado em memória"

- [ ] **Control structure errors:**
  - Non-boolean WHILE condition: `(10 body WHILE)`
  - Non-boolean IF condition: `(5 branch1 branch2 IFELSE)`
  - Malformed control structure

#### Example Structure:

```
(Y)
(10 X MEM)
(-1 RES)
(100 RES)
((5 3 >) BOOL MEM)
(BOOL)
(10 (5 3 +) WHILE)
(3.5 (10) (20) IFELSE)
(Z 2 +)
((X Y >) TEST MEM)
```

---

## Unit Test Requirements

Each developer must create unit tests for their module as part of their issue's acceptance criteria.

### Issue #1 Tests (Symbol Table) - In `tests/RA3/test_tabela_simbolos.py`

```python
def test_adicionar_simbolo()
def test_buscar_simbolo()
def test_simbolo_nao_existe()
def test_atualizar_inicializacao()
def test_verificar_inicializacao()
```

### Issue #2 Tests (Type Checking) - In `tests/RA3/test_verificador_tipos.py`

```python
def test_adicao_inteiros()
def test_adicao_reais()
def test_promocao_tipo()
def test_divisao_inteira_com_real()  # Should error
def test_potencia_expoente_real()     # Should error
def test_operador_relacional_retorna_boolean()
def test_operador_logico_valida_boolean()
```

### Issue #3 Tests (Memory/Control) - In `tests/RA3/test_validador_memoria.py`

```python
def test_memoria_nao_inicializada()
def test_memoria_inicializada()
def test_res_referencia_valida()
def test_res_referencia_invalida()
def test_condicao_while_booleana()
def test_condicao_while_nao_booleana()  # Should error
```

### Issue #4 Tests (Integration) - In `tests/RA3/test_integracao.py`

```python
def test_gerar_ast_atribuida()
def test_gerar_json_valido()
def test_pipeline_completo()
def test_erros_impressos_corretamente()
```

---

## Acceptance Criteria

- [ ] 3+ test files created in `inputs/RA3/`
- [ ] Each file has ≥10 lines
- [ ] All operators covered across files:
  - Arithmetic: `+`, `-`, `*`, `|`, `/`, `%`, `^`
  - Relational: `>`, `<`, `>=`, `<=`, `==`, `!=`
  - Logical: `&&`, `||`, `!`
- [ ] All command types used:
  - `(V MEM)`, `(MEM)`, `(N RES)`
- [ ] All control structures tested:
  - `WHILE`, `FOR`, `IFELSE`
- [ ] Valid test file runs without errors
- [ ] Error test files trigger expected errors
- [ ] Unit tests created for each module (Issues #1-4)
- [ ] Unit tests cover both success and error paths
- [ ] Test documentation in `inputs/RA3/README_TESTS.md`
- [ ] Comments in test files explain what is being tested

---

## Grading Impact

- **-15%** if tests don't cover all cases
- **Required for robustness evaluation** (15% of grade)

---

## Dependencies

### Requires
None (can be created first)

### Blocks
- Issues #2, #3, #4 (need tests for validation)

---

## Files to Create

```
inputs/RA3/
├── teste1_valido.txt              # Valid operations
├── teste2_erros_tipos.txt         # Type errors
├── teste3_erros_memoria.txt       # Memory & control errors
└── README_TESTS.md                # Test documentation

tests/RA3/                         # Unit tests (by other issues)
├── __init__.py
├── test_tabela_simbolos.py        # Issue #1
├── test_verificador_tipos.py      # Issue #2
├── test_validador_memoria.py      # Issue #3
├── test_validador_controle.py     # Issue #3
└── test_integracao.py             # Issue #4
```

---

## Test Documentation (`README_TESTS.md`)

Create a file documenting:

```markdown
# RA3 Test Files

## Test Coverage

### teste1_valido.txt
- **Purpose:** Validate correct semantic analysis of valid programs
- **Lines:** X lines
- **Coverage:**
  - All arithmetic operators (7)
  - All relational operators (6)
  - All logical operators (3)
  - Memory operations (MEM, RES)
  - Control structures (WHILE, FOR, IFELSE)
  - Type promotion scenarios
  - Nested expressions

### teste2_erros_tipos.txt
- **Purpose:** Validate type error detection
- **Lines:** X lines
- **Expected Errors:**
  1. Line 1: Real in integer division
  2. Line 2: Real in modulo
  3. Line 3: Real exponent
  4. ...

### teste3_erros_memoria.txt
- **Purpose:** Validate memory and control error detection
- **Lines:** X lines
- **Expected Errors:**
  1. Line 1: Uninitialized memory
  2. Line 2: Invalid RES reference
  3. ...

## Running Tests

```bash
# Valid test (should pass)
python3 compilar.py inputs/RA3/teste1_valido.txt

# Type error test (should report errors)
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt

# Memory error test (should report errors)
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
```

## Expected Output

### Valid Test
- All phases complete successfully
- No errors reported
- All output files generated

### Error Tests
- Semantic errors reported to console
- Error report generated
- Specific error messages for each issue
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 9 (Test Files) - Lines 382-397

- **Test Requirements:** Lines 382-397 in requirements

- **Operators:** `src/RA2/functions/python/configuracaoGramatica.py`

---

## Implementation Tips

### Creating Effective Test Cases

1. **Start with simple cases:**
   ```
   (5 3 +)        # Basic addition
   (5.0 3.0 +)    # Real addition
   (5 3.0 +)      # Type promotion
   ```

2. **Build complexity gradually:**
   ```
   ((5 3 +) 2 *)              # One level nesting
   (((5 3 +) 2 *) (4 2 /) -)  # Two level nesting
   ```

3. **Test edge cases:**
   ```
   (0 RES)        # Reference current line
   (1 RES)        # Reference previous line
   (10 RES)       # Reference out of bounds (error)
   ```

4. **Test error boundaries:**
   ```
   (2 2 ^)        # Valid: int exponent
   (2 2.0 ^)      # Invalid: real exponent (error)
   (2 -2 ^)       # Invalid: negative exponent (error)
   ```

### Test File Comments

Add comments to explain test intent:

```
# Test 1: Basic arithmetic with integers
(5 3 +)

# Test 2: Type promotion (int + real = real)
(5 3.5 +)

# Test 3: Memory initialization
(100 COUNTER MEM)

# Test 4: Memory read after initialization (valid)
(COUNTER)

# ERROR Test 5: Should fail - real in integer division
(5.5 2 /)
```

---

## Notes

- Tests should be **comprehensive** but **readable**
- Include comments explaining what each line tests
- Error test files should have **expected errors** documented
- Unit tests are separate from integration tests
- This issue can be started **immediately** (no dependencies)
- Coordinate with other issues to ensure tests cover their functionality
- Tests will be used to validate Issues #2, #3, #4
