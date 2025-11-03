# Issue #4: Generate Attributed AST and Integrate All Phases

## Labels
- `phase-3-semantic`
- `integration`
- `deliverable`
- `high-priority`

## Assignee
**Aluno 4** (Task from section 7.4 of requirements)

---

## Description

Generate the final attributed AST, create all required reports, and integrate the complete RA1+RA2+RA3 pipeline.

This is the final integration issue that ties together all three compiler phases and produces all required deliverable files (markdown reports and JSON AST).

---

## Responsibilities

- Transform annotated AST into final attributed AST structure
- Implement `main()` orchestrating all three phases
- Generate markdown and JSON output files
- Create comprehensive reports
- Test complete system with all test files

---

## Specific Tasks

### 1. Attributed AST Generation (`gerarArvoreAtribuida()`)

- [ ] Transform type-annotated AST into final structure

- [ ] Each node should contain:
  - `tipo_vertice`: Node type (operator, operand, control, etc.)
  - `tipo_inferido`: Inferred type (int, real, boolean)
  - `filhos`: Child nodes
  - `numero_linha`: Source line number
  - `valor`: Literal value (if applicable)
  - `operador`: Operator symbol (if applicable)

- [ ] Support both text and JSON output formats

- [ ] JSON format for interoperability with next phase

### 2. Report Generation

#### `outputs/RA3/arvore_atribuida.md`

- [ ] ASCII tree representation
- [ ] Include type annotations on each node
- [ ] Line numbers for traceability
- [ ] Also save as `arvore_atribuida.json`

#### `outputs/RA3/julgamento_tipos.md`

- [ ] List all type inference rules applied
- [ ] Show for each line: expression → types → result type
- [ ] Document type promotions that occurred
- [ ] Reference grammar rules used

#### `outputs/RA3/erros_semanticos.md`

- [ ] All errors from Issues #2 and #3
- [ ] Grouped by type (type errors, memory errors, control errors)
- [ ] Each with line number and context
- [ ] Summary count at end

#### Update `outputs/RA3/gramatica_atributos.md`

- [ ] Include timestamp of generation
- [ ] Grammar from Issue #1

### 3. Main Integration (`main()`)

- [ ] Implement command-line argument parsing:
  ```bash
  ./compilar.py <input_file>
  ```

- [ ] Sequential execution:
  1. Call RA1 lexical analyzer (`exibirResultados()`)
  2. Check for lexical errors → exit if found
  3. Call RA2 parser (`parsear_todas_linhas()`)
  4. Check for syntax errors → exit if found
  5. Call RA3 semantic analyzer:
     - `definirGramaticaAtributos()` (Issue #1)
     - `analisarSemantica()` (Issue #2)
     - `analisarSemanticaMemoria()` (Issue #3)
     - `analisarSemanticaControle()` (Issue #3)
     - `gerarArvoreAtribuida()` (Issue #4)
  6. Generate all output files
  7. Print errors to console (if any)

- [ ] Create output directory structure if not exists

- [ ] Handle file I/O errors gracefully

### 4. System Testing

- [ ] Test with all 3 required test files (from Issue #5)

- [ ] Verify all output files generated correctly

- [ ] Verify error detection works end-to-end

- [ ] Test with intentional errors (lexical, syntactic, semantic)

- [ ] Verify JSON AST is valid and parseable

---

## Interface Specification

### Input
- **`arvoreAnotada`**: Type-annotated AST from Issues #2 and #3
- **Command-line:** `python3 compilar.py inputs/RA3/teste1.txt`

### Output
- `outputs/RA3/arvore_atribuida.md` (markdown)
- `outputs/RA3/arvore_atribuida.json` (JSON)
- `outputs/RA3/julgamento_tipos.md`
- `outputs/RA3/erros_semanticos.md`
- `outputs/RA3/gramatica_atributos.md`
- Console output: Errors (if any) or success message

### Manages
Complete compiler execution via CLI

---

## Acceptance Criteria

- [ ] `main()` calls all phases in correct order
- [ ] Stops on lexical/syntactic errors before semantic phase
- [ ] Generates all 4 required markdown files
- [ ] Generates valid JSON AST with required fields
- [ ] JSON includes: `tipo_vertice`, `tipo_inferido`, `filhos`, `numero_linha`
- [ ] Reports are properly formatted and human-readable
- [ ] Type judgment report shows all rules applied
- [ ] Error report groups errors logically
- [ ] Console output is clear and helpful
- [ ] Works with relative and absolute file paths
- [ ] **Integration tests:**
  - Run all 3 test files successfully
  - Verify output files exist and are valid
  - Verify error cases handled correctly
  - Verify JSON is parseable
- [ ] Code follows PEP 8 with docstrings
- [ ] Update `compilar.py` with RA3 integration

---

## Unit Testing Requirements

Create unit tests in `tests/RA3/test_integracao.py`:

```python
def test_gerar_ast_atribuida():
    """Test AST generation with all required fields"""
    # Should create AST with tipo_vertice, tipo_inferido, filhos, numero_linha

def test_gerar_json_valido():
    """Test JSON AST is valid and parseable"""
    # Should produce valid JSON that can be loaded

def test_pipeline_completo_valido():
    """Test complete pipeline with valid input file"""
    # RA1 → RA2 → RA3 should complete successfully

def test_pipeline_erro_lexico():
    """Test pipeline stops on lexical error"""
    # Should exit before RA3 if lexical error found

def test_pipeline_erro_sintatico():
    """Test pipeline stops on syntax error"""
    # Should exit before RA3 if syntax error found

def test_pipeline_erro_semantico():
    """Test pipeline completes but reports semantic errors"""
    # Should complete and generate error report

def test_arquivos_saida_gerados():
    """Test all output files are created"""
    # Should verify existence of all 5 output files

def test_erros_impressos_console():
    """Test errors are printed to console"""
    # Should display errors in readable format

def test_relatorio_julgamento_tipos():
    """Test type judgment report completeness"""
    # Should include all type inference steps

def test_relatorio_erros_agrupado():
    """Test error report grouping by category"""
    # Should group by type, memory, control errors
```

---

## Grading Impact

- **-30%** if attributed AST not generated correctly
- **-15%** if reports incomplete or incorrect
- **Critical for deliverables** (all markdown files required)

---

## Dependencies

### Requires
- Issue #1 (Grammar & Symbol Table)
- Issue #2 (Type Checking)
- Issue #3 (Memory & Control Validation)
- Existing `compilar.py` as base

### Blocks
None (final integration)

---

## Files to Create/Modify

```
compilar.py                             # UPDATE: Add RA3 integration

src/RA3/functions/python/
├── gerador_arvore_atribuida.py        # AST generation
├── gerador_relatorios.py               # Markdown report generation
└── integracao.py                       # Integration utilities

outputs/RA3/                            # CREATE directory
├── arvore_atribuida.md
├── arvore_atribuida.json
├── julgamento_tipos.md
├── erros_semanticos.md
└── gramatica_atributos.md

tests/RA3/
└── test_integracao.py                  # Integration tests
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 2 (Description) - Lines 64-86
  - Section 8 (Integration) - Lines 600-617
  - Section 11.4 (Output Files) - Lines 467-476

- **JSON Format:** Requirements lines 450-451
- **Output Files:** Requirements lines 467-476
- **Existing `compilar.py`:** Root directory

---

## Implementation Tips

### AST Node Structure (JSON)

```python
class NoArvoreAtribuida:
    def __init__(self, tipo_vertice, tipo_inferido, numero_linha):
        self.tipo_vertice = tipo_vertice
        self.tipo_inferido = tipo_inferido
        self.numero_linha = numero_linha
        self.filhos = []
        self.valor = None
        self.operador = None

    def para_json(self):
        """Convert to JSON-serializable dict"""
        return {
            'tipo_vertice': self.tipo_vertice,
            'tipo_inferido': self.tipo_inferido,
            'numero_linha': self.numero_linha,
            'filhos': [filho.para_json() for filho in self.filhos],
            'valor': self.valor,
            'operador': self.operador
        }
```

### Main Integration Example

```python
def main():
    """
    Main entry point for compiler

    Usage: python3 compilar.py <input_file>
    """
    # Parse command line
    if len(sys.argv) != 2:
        print("Uso: python3 compilar.py <arquivo_entrada>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]

    print(f"=== Compilando {arquivo_entrada} ===\n")

    # Phase 1: Lexical Analysis
    print("[RA1] Análise Léxica...")
    tokens = executar_ra1(arquivo_entrada)
    if tokens is None:
        print("❌ Erros léxicos encontrados. Compilação abortada.")
        sys.exit(1)
    print("✓ Análise léxica concluída\n")

    # Phase 2: Syntactic Analysis
    print("[RA2] Análise Sintática...")
    ast = executar_ra2(tokens)
    if ast is None:
        print("❌ Erros sintáticos encontrados. Compilação abortada.")
        sys.exit(1)
    print("✓ Análise sintática concluída\n")

    # Phase 3: Semantic Analysis
    print("[RA3] Análise Semântica...")
    resultado = executar_ra3(ast)

    if resultado['erros']:
        print(f"⚠️  {len(resultado['erros'])} erro(s) semântico(s) encontrado(s):\n")
        for erro in resultado['erros']:
            print(f"  {erro}")
        print()
    else:
        print("✓ Nenhum erro semântico encontrado\n")

    # Generate outputs
    print("[RA3] Gerando arquivos de saída...")
    gerar_todos_outputs(resultado)
    print("✓ Arquivos gerados em outputs/RA3/\n")

    print("=== Compilação concluída ===")
```

### Report Generation Example

```python
def gerar_relatorio_julgamento_tipos(historico_inferencias):
    """
    Generate type judgment report

    Args:
        historico_inferencias: List of (linha, expressao, regras, tipo_final)

    Returns:
        markdown_content: Report as markdown string
    """
    linhas = ["# Relatório de Julgamento de Tipos\n"]
    linhas.append(f"**Data:** {datetime.now().isoformat()}\n")
    linhas.append(f"**Total de expressões:** {len(historico_inferencias)}\n\n")

    for linha_num, expressao, regras_aplicadas, tipo_final in historico_inferencias:
        linhas.append(f"## Linha {linha_num}: `{expressao}`\n")

        linhas.append("### Análise de Tipos:\n")
        for passo in regras_aplicadas:
            linhas.append(f"- {passo}\n")

        linhas.append(f"\n### Tipo Resultante: **{tipo_final}**\n\n")
        linhas.append("---\n\n")

    return ''.join(linhas)
```

### JSON Validation

```python
import json

def salvar_ast_json(ast, caminho):
    """
    Save AST as JSON and validate

    Args:
        ast: Attributed AST root node
        caminho: Output file path

    Raises:
        ValueError: If JSON is invalid
    """
    # Convert to dict
    ast_dict = ast.para_json()

    # Save with pretty printing
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(ast_dict, f, indent=2, ensure_ascii=False)

    # Validate by reloading
    with open(caminho, 'r', encoding='utf-8') as f:
        json.load(f)  # Will raise exception if invalid

    print(f"✓ AST JSON válida salva em {caminho}")
```

### Error Report Grouping

```python
def gerar_relatorio_erros(erros):
    """
    Generate error report grouped by category

    Args:
        erros: List of ErroSemantico objects

    Returns:
        markdown_content: Error report as markdown
    """
    if not erros:
        return "# Relatório de Erros Semânticos\n\n✅ Nenhum erro semântico encontrado.\n"

    linhas = ["# Relatório de Erros Semânticos\n\n"]
    linhas.append(f"**Total de erros:** {len(erros)}\n\n")

    # Group by category
    erros_tipo = [e for e in erros if e.categoria == 'tipo']
    erros_memoria = [e for e in erros if e.categoria == 'memoria']
    erros_controle = [e for e in erros if e.categoria == 'controle']

    if erros_tipo:
        linhas.append(f"## Erros de Tipo ({len(erros_tipo)})\n\n")
        for i, erro in enumerate(erros_tipo, 1):
            linhas.append(f"### Erro #{i}\n")
            linhas.append(f"**Linha:** {erro.linha}\n\n")
            linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
            linhas.append(f"**Descrição:** {erro.descricao}\n\n")
            linhas.append("---\n\n")

    # Similar for memory and control errors...

    return ''.join(linhas)
```

---

## Notes

- This issue integrates **all previous work** (RA1, RA2, RA3)
- The pipeline must be **sequential** - stop on lexical/syntax errors
- All 5 output files are **required deliverables**
- JSON AST must be **valid and parseable** for next phase
- Console output should be **clear and helpful** for debugging
- Test with **all test files** from Issue #5
- This is a **high-priority** issue as it produces all deliverables
- Coordinate with Issue #7 for report generation utilities
