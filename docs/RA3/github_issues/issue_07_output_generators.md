# Issue #7: Setup Output Directory Structure and File Generators

## Labels
- `phase-3-semantic`
- `deliverable`
- `documentation`

## Assignee
**Aluno 4** (supports Issue #4, can be worked on in parallel)

---

## Description

Create output directory structure and implement generators for all required markdown/JSON files.

This issue provides the infrastructure for generating all deliverable output files, separating the report generation logic from the analysis logic.

---

## Directory Structure to Create

```
outputs/
├── RA1/                          # Existing
│   ├── tokens/
│   │   └── tokens_gerados.txt
│   └── assembly/
│       ├── programa_completo.S
│       └── registers.inc
├── RA2/                          # Existing
│   └── arvore_output.txt
└── RA3/                          # NEW - Create this
    ├── gramatica_atributos.md
    ├── arvore_atribuida.md
    ├── arvore_atribuida.json
    ├── julgamento_tipos.md
    └── erros_semanticos.md
```

---

## File Generator Implementations

### 1. Grammar Attributes Generator (`gramatica_atributos.md`)

- [ ] **Header with metadata:**
  - Timestamp (ISO 8601)
  - Phase information
  - Group name

- [ ] **Complete EBNF grammar:**
  - All production rules
  - Formatted clearly

- [ ] **Attribute definitions:**
  - Synthesized attributes
  - Inherited attributes

- [ ] **Semantic rules in formal notation:**
  ```
  Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
  ─────────────────────────────
        Γ ⊢ e₁ + e₂ : int
  ```

- [ ] **Type promotion function specification**

- [ ] **Examples for each operator category:**
  - Arithmetic operators
  - Relational operators
  - Logical operators
  - Control structures

- [ ] **Table of contents for navigation**

---

### 2. Attributed AST Generator (Markdown) (`arvore_atribuida.md`)

- [ ] **ASCII tree visualization:**
  ```
  PROGRAM [linha 1-10]
  ├── LINHA [linha 1] tipo: int
  │   ├── OPERANDO: 5 [tipo: int]
  │   ├── OPERANDO: 3 [tipo: int]
  │   └── OPERATOR: + [resultado: int]
  ├── LINHA [linha 2] tipo: real
  │   ├── OPERANDO: 5.5 [tipo: real]
  │   ├── OPERANDO: 2.0 [tipo: real]
  │   └── OPERATOR: | [resultado: real]
  ...
  ```

- [ ] **Each node shows:**
  - Node type (operator/operand/control)
  - Inferred type annotation
  - Line number
  - Value (if literal)
  - Operator symbol (if operator)

- [ ] **Proper indentation for hierarchy:**
  - Use `├──`, `└──`, `│` for tree structure
  - Indent children appropriately

- [ ] **Header with metadata:**
  - Input file name
  - Timestamp
  - Total lines analyzed

---

### 3. Attributed AST Generator (JSON) (`arvore_atribuida.json`)

- [ ] **Valid JSON structure:**
  ```json
  {
    "tipo_vertice": "PROGRAM",
    "tipo_inferido": null,
    "numero_linha": 0,
    "filhos": [
      {
        "tipo_vertice": "LINHA",
        "tipo_inferido": "int",
        "numero_linha": 1,
        "filhos": [
          {
            "tipo_vertice": "LITERAL",
            "valor": 5,
            "tipo_inferido": "int",
            "numero_linha": 1,
            "filhos": []
          },
          {
            "tipo_vertice": "LITERAL",
            "valor": 3,
            "tipo_inferido": "int",
            "numero_linha": 1,
            "filhos": []
          },
          {
            "tipo_vertice": "OPERATOR",
            "operador": "+",
            "tipo_inferido": "int",
            "numero_linha": 1,
            "filhos": []
          }
        ]
      }
    ]
  }
  ```

- [ ] **Required fields for each node:**
  - `tipo_vertice`: String (PROGRAM, LINHA, LITERAL, OPERATOR, etc.)
  - `tipo_inferido`: String (int, real, boolean) or null
  - `numero_linha`: Integer
  - `filhos`: Array of nodes
  - `valor`: (Optional) Literal value
  - `operador`: (Optional) Operator symbol

- [ ] **Pretty-printed with 2-space indentation**

- [ ] **Validate JSON after generation:**
  - Load with `json.load()` to verify validity

---

### 4. Type Judgment Generator (`julgamento_tipos.md`)

- [ ] **Header with analysis info:**
  - Input file name
  - Timestamp
  - Total expressions analyzed

- [ ] **For each expression/line:**
  ```markdown
  ## Linha 3: (10 3.5 *)

  ### Análise de Tipos:
  - Operando 1: 10 → tipo: int
  - Operando 2: 3.5 → tipo: real
  - Operador: *

  ### Regra Aplicada:
  Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
  ──────────────────────────────
  Γ ⊢ e₁ * e₂ : promover_tipo(int, real) = real

  ### Tipo Resultante: real

  ### Observação:
  Tipo promovido de int para real devido a operando real.
  ```

- [ ] **Show sub-expressions with types:**
  - Break down complex expressions
  - Show type at each step

- [ ] **Applied semantic rules:**
  - Reference specific grammar rule
  - Show formal notation

- [ ] **Type promotions (if any):**
  - Document when and why promotion occurred

- [ ] **Final result type**

- [ ] **Summary statistics at end:**
  - Total expressions
  - Type promotions count
  - Types distribution (int/real/boolean)

---

### 5. Semantic Errors Generator (`erros_semanticos.md`)

- [ ] **Header with summary:**
  - Input file name
  - Timestamp
  - Total errors found
  - Errors by category

- [ ] **Errors grouped by category:**

  **Type Errors:**
  ```markdown
  ## Erros de Tipo (5)

  ### Erro #1: Tipo Incompatível
  **Linha:** 5
  **Contexto:** `(5.5 2 /)`
  **Descrição:** Divisão inteira requer operandos inteiros, mas encontrado 'real'

  ### Erro #2: Expoente Inválido
  **Linha:** 7
  **Contexto:** `(2 3.5 ^)`
  **Descrição:** Expoente da potenciação deve ser inteiro, mas encontrado 'real'
  ```

  **Memory Errors:**
  ```markdown
  ## Erros de Memória (2)

  ### Erro #1: Memória Não Inicializada
  **Linha:** 3
  **Contexto:** `(X)`
  **Descrição:** Memória 'X' utilizada sem inicialização
  ```

  **Control Flow Errors:**
  ```markdown
  ## Erros de Controle de Fluxo (1)

  ### Erro #1: Condição Não Booleana
  **Linha:** 10
  **Contexto:** `(5 body WHILE)`
  **Descrição:** Condição de WHILE deve ser booleana, encontrado 'int'
  ```

- [ ] **Summary count:**
  - Total errors
  - Errors by category
  - Lines with errors

- [ ] **If no errors:**
  ```markdown
  # Relatório de Erros Semânticos

  ✅ **Nenhum erro semântico encontrado.**

  Todas as verificações foram concluídas com sucesso:
  - ✓ Verificação de tipos
  - ✓ Inicialização de memória
  - ✓ Estruturas de controle
  - ✓ Comandos especiais
  ```

---

## Helper Functions to Implement

### File I/O Utilities

- [ ] `criar_diretorio_saida()` - Create output directories if they don't exist

- [ ] `salvar_markdown(nome_arquivo, conteudo)` - Save markdown file with UTF-8 encoding

- [ ] `salvar_json(nome_arquivo, dados)` - Save and validate JSON file

- [ ] `gerar_timestamp()` - Generate ISO 8601 timestamp

### Formatting Utilities

- [ ] `formatar_regra_semantica(regra)` - Format semantic rules with Unicode characters

- [ ] `formatar_arvore_texto(no, nivel=0)` - Recursive ASCII tree formatter

- [ ] `formatar_erro(erro)` - Format error object as markdown section

- [ ] `agrupar_erros_por_categoria(erros)` - Group errors by type/memory/control

### Conversion Utilities

- [ ] `arvore_para_markdown(arvore)` - Convert AST to markdown representation

- [ ] `arvore_para_json(arvore)` - Convert AST to JSON-serializable dict

- [ ] `validar_json(caminho)` - Validate JSON file after saving

---

## Acceptance Criteria

- [ ] `outputs/RA3/` directory created automatically on first run

- [ ] All 5 files generated on successful analysis:
  - `gramatica_atributos.md`
  - `arvore_atribuida.md`
  - `arvore_atribuida.json`
  - `julgamento_tipos.md`
  - `erros_semanticos.md`

- [ ] Markdown files are properly formatted with headers, sections, lists

- [ ] JSON file is valid and parseable with `json.load()`

- [ ] Files contain all required information per specifications above

- [ ] Grammar document includes all operators from `configuracaoGramatica.py`

- [ ] Type judgment shows all inference steps clearly

- [ ] Error report is clear, actionable, and well-organized

- [ ] AST visualization (markdown) is readable and properly indented

- [ ] Files have proper encoding (UTF-8) to support Unicode characters

- [ ] Timestamps in ISO 8601 format (e.g., `2025-10-21T14:30:00`)

- [ ] Unit tests verify file generation:
  - Files are created
  - Content is correct
  - JSON is valid

- [ ] Error handling for I/O failures (permissions, disk space, etc.)

---

## Grading Impact

- **-15%** if output files missing or incomplete
- **All files are required deliverables**

---

## Dependencies

### Requires
- Issues #1, #2, #3 (data to output)

### Blocks
- Issue #4 (integration needs these generators)

---

## Files to Create

```
src/RA3/functions/python/
├── geradores/
│   ├── __init__.py
│   ├── gerador_gramatica.py      # Grammar markdown generator
│   ├── gerador_arvore.py         # AST markdown & JSON generator
│   ├── gerador_julgamento.py     # Type judgment generator
│   └── gerador_erros.py          # Error report generator
└── utils/
    ├── __init__.py
    ├── formatadores.py           # Formatting utilities
    └── io_utils.py               # File I/O utilities
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 11.4 (Output Files) - Lines 467-476
  - Lines 450-451 (JSON format)

---

## Implementation Tips

### ASCII Tree Formatting

```python
def formatar_arvore_texto(no, nivel=0, eh_ultimo=False):
    """
    Format AST as ASCII tree

    Args:
        no: AST node
        nivel: Current depth level
        eh_ultimo: True if this is last child

    Returns:
        String representation
    """
    # Determine prefix based on position
    if nivel == 0:
        prefix = ""
        connector = ""
    else:
        prefix = "│   " * (nivel - 1)
        connector = "└── " if eh_ultimo else "├── "

    # Format current node
    tipo_info = f"[tipo: {no.tipo_inferido}]" if no.tipo_inferido else ""
    valor_info = f": {no.valor}" if hasattr(no, 'valor') and no.valor else ""
    linha_info = f" [linha {no.numero_linha}]" if hasattr(no, 'numero_linha') else ""

    linha_atual = f"{prefix}{connector}{no.tipo_vertice}{valor_info} {tipo_info}{linha_info}\n"

    # Recursively format children
    resultado = [linha_atual]
    if hasattr(no, 'filhos') and no.filhos:
        for i, filho in enumerate(no.filhos):
            eh_ultimo_filho = (i == len(no.filhos) - 1)
            resultado.append(formatar_arvore_texto(filho, nivel + 1, eh_ultimo_filho))

    return ''.join(resultado)
```

### JSON Conversion

```python
import json
from typing import Any, Dict

class NoArvoreAtribuida:
    def para_json(self) -> Dict[str, Any]:
        """Convert node to JSON-serializable dict"""
        resultado = {
            'tipo_vertice': self.tipo_vertice,
            'tipo_inferido': self.tipo_inferido,
            'numero_linha': self.numero_linha,
            'filhos': [filho.para_json() for filho in self.filhos]
        }

        # Add optional fields if present
        if hasattr(self, 'valor') and self.valor is not None:
            resultado['valor'] = self.valor

        if hasattr(self, 'operador') and self.operador is not None:
            resultado['operador'] = self.operador

        return resultado

def salvar_ast_json(ast, caminho):
    """Save AST as formatted JSON"""
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(
            ast.para_json(),
            f,
            indent=2,
            ensure_ascii=False,
            sort_keys=False
        )

    # Validate
    with open(caminho, 'r', encoding='utf-8') as f:
        json.load(f)  # Will raise if invalid
```

### Error Grouping

```python
from collections import defaultdict
from typing import List

def agrupar_erros_por_categoria(erros: List) -> Dict[str, List]:
    """
    Group errors by category

    Args:
        erros: List of ErroSemantico objects

    Returns:
        Dict with keys 'tipo', 'memoria', 'controle'
    """
    grupos = defaultdict(list)

    for erro in erros:
        categoria = erro.categoria  # 'tipo', 'memoria', 'controle'
        grupos[categoria].append(erro)

    return dict(grupos)

def formatar_relatorio_erros(erros: List) -> str:
    """Generate error report markdown"""
    if not erros:
        return (
            "# Relatório de Erros Semânticos\n\n"
            "✅ **Nenhum erro semântico encontrado.**\n"
        )

    linhas = ["# Relatório de Erros Semânticos\n\n"]
    linhas.append(f"**Total de erros:** {len(erros)}\n\n")

    grupos = agrupar_erros_por_categoria(erros)

    # Type errors
    if 'tipo' in grupos:
        linhas.append(f"## Erros de Tipo ({len(grupos['tipo'])})\n\n")
        for i, erro in enumerate(grupos['tipo'], 1):
            linhas.append(f"### Erro #{i}: {erro.titulo}\n")
            linhas.append(f"**Linha:** {erro.linha}\n\n")
            linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
            linhas.append(f"**Descrição:** {erro.descricao}\n\n")
            linhas.append("---\n\n")

    # Similar for memory and control errors...

    return ''.join(linhas)
```

### Type Judgment Report

```python
def gerar_relatorio_julgamento(historico):
    """
    Generate type judgment report

    Args:
        historico: List of (linha, expressao, passos, tipo_final)
    """
    linhas = ["# Relatório de Julgamento de Tipos\n\n"]

    for linha_num, expressao, passos, tipo_final in historico:
        linhas.append(f"## Linha {linha_num}: `{expressao}`\n\n")

        linhas.append("### Análise de Tipos:\n")
        for passo in passos:
            linhas.append(f"- {passo}\n")
        linhas.append("\n")

        if 'promocao' in passos:
            linhas.append("### Observação:\n")
            linhas.append("Tipo promovido devido a operando real.\n\n")

        linhas.append(f"### Tipo Resultante: **{tipo_final}**\n\n")
        linhas.append("---\n\n")

    return ''.join(linhas)
```

### Directory Creation

```python
import os
from pathlib import Path

def criar_diretorio_saida():
    """Create output directory structure if it doesn't exist"""
    diretorio = Path("outputs/RA3")
    diretorio.mkdir(parents=True, exist_ok=True)
    print(f"✓ Diretório de saída: {diretorio}")
```

---

## Notes

- All files must use **UTF-8 encoding** for Unicode support
- JSON must be **valid and parseable** (test with `json.load()`)
- Markdown should be **properly formatted** for GitHub rendering
- Include **timestamps** for traceability
- Error reports should be **actionable** (clear what to fix)
- ASCII trees should be **readable** with proper indentation
- This issue can be worked on **in parallel** with Issues #1-3
- Coordinate with Issue #4 for integration
