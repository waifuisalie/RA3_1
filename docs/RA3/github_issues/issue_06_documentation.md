# Issue #6: Update Documentation for RA3

## Labels
- `phase-3-semantic`
- `documentation`
- `deliverable`

## Assignee
**All team members** (collaborative effort, coordinated by Aluno 4)

---

## Description

Update README and create comprehensive documentation for the RA3 semantic analyzer phase.

This issue ensures all project documentation is complete, accurate, and helpful for understanding, running, and evaluating the compiler.

---

## Required Documentation Updates

### 1. README.md Updates

#### Header Section

- [ ] **Institution:** Pontifícia Universidade Católica do Paraná (PUCPR)
- [ ] **Discipline:** Linguagens Formais e Autômatos
- [ ] **Professor:** Frank Alcantara
- [ ] **Year:** 2025
- [ ] **Group members** (alphabetical order):
  - Breno Rossi Duarte - breno-rossi
  - Francisco Bley Ruthes - fbleyruthes
  - Rafael Olivare Piveta - RafaPiveta
  - Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
- [ ] **Group name:** RA3_1

#### Phase 3 Overview

- [ ] Semantic analyzer description
- [ ] Attribute grammar explanation
- [ ] Type system description (int, real, boolean)
- [ ] Symbol table purpose
- [ ] Integration with RA1 and RA2

#### Compilation Instructions

```bash
# Basic usage
python3 compilar.py <input_file>

# Examples
python3 compilar.py inputs/RA3/teste1_valido.txt
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
```

#### Execution Examples

- [ ] Example with **valid** file execution
- [ ] Example with **error** file execution
- [ ] Show expected console output
- [ ] Show output file locations

#### Debugging Instructions

- [ ] How to run unit tests:
  ```bash
  python3 -m pytest tests/RA3/
  ```
- [ ] How to check semantic errors
- [ ] How to inspect attributed AST (JSON)
- [ ] How to read type judgment report

#### Control Structure Syntax

- [ ] Document exact RPN syntax for `FOR`
- [ ] Document exact RPN syntax for `WHILE`
- [ ] Document exact RPN syntax for `IFELSE`
- [ ] Provide examples of each structure
- [ ] Show valid and invalid uses

#### Type System Rules

- [ ] Operator type requirements table:
  | Operator | Operand Types | Result Type |
  |----------|---------------|-------------|
  | `+`, `-`, `*`, `|` | int/int, real/real, mixed | int/real/promoted |
  | `/`, `%` | **int only** | int |
  | `^` | base: int/real, exp: **int only** | matches base |
  | `>`, `<`, etc. | int/real | boolean |
  | `&&`, `||` | boolean | boolean |
  | `!` | boolean | boolean |

- [ ] Type promotion rules (int → real)
- [ ] Boolean type restrictions (cannot be stored in memory)

#### Test Routines

- [ ] How tests were validated
- [ ] Coverage of test cases
- [ ] Expected vs actual results
- [ ] How to verify test outputs

---

### 2. Create Contributing Guide (`CONTRIBUTING.md`)

- [ ] **How to create issues:**
  - Issue template
  - Required information
  - Labels to use

- [ ] **Pull request workflow:**
  - Branch naming conventions
  - Commit message format
  - PR description requirements
  - Review process

- [ ] **Code style requirements:**
  - PEP 8 for Python
  - Function naming conventions
  - Docstring format
  - Comment guidelines

- [ ] **Testing requirements:**
  - When to write tests
  - Test naming conventions
  - Test coverage expectations

- [ ] **Documentation standards:**
  - README sections
  - Code comments
  - Docstrings
  - Markdown formatting

---

### 3. Update CLAUDE.md

- [ ] **Add RA3 architecture section:**
  - Module structure
  - Data flow diagram
  - Component interactions

- [ ] **Document semantic analysis pipeline:**
  - Grammar → Symbol Table → Type Checking → Memory/Control → AST
  - Input/output of each stage

- [ ] **Add type system rules:**
  - Complete operator table
  - Type promotion function
  - Error conditions

- [ ] **Update project structure:**
  ```
  RA3_1/
  ├── src/RA3/functions/python/
  │   ├── gramatica_atributos.py
  │   ├── tabela_simbolos.py
  │   ├── tipos.py
  │   ├── analisador_semantico.py
  │   ├── verificador_tipos.py
  │   ├── validador_memoria.py
  │   ├── validador_controle.py
  │   └── gerador_arvore_atribuida.py
  ```

- [ ] **Add RA3 common patterns:**
  - How to add new type rules
  - How to add new validations
  - How to extend error reporting

---

### 4. Create Architecture Documentation (`docs/RA3/architecture.md`)

- [ ] **Component Diagram:**
  - Show all RA3 modules
  - Show dependencies
  - Show data flow

- [ ] **Data Structures:**
  - Symbol Table structure
  - AST node structure
  - Error object structure

- [ ] **Algorithms:**
  - AST traversal
  - Type inference
  - Scope management

---

### 5. Create Type System Specification (`docs/RA3/type_system.md`)

- [ ] **Type Hierarchy:**
  ```
  int <: real
  (no other subtyping)
  ```

- [ ] **Type Rules (Formal Notation):**
  - All operator rules in Γ ⊢ format
  - Type promotion function
  - Coercion rules

- [ ] **Error Conditions:**
  - Complete list of type errors
  - Examples of each

---

### 6. Create Testing Guide (`docs/RA3/testing_guide.md`)

- [ ] **Test File Structure:**
  - What each test file covers
  - How to add new tests

- [ ] **Unit Testing:**
  - How to write unit tests
  - How to run unit tests
  - Coverage expectations

- [ ] **Integration Testing:**
  - How to test complete pipeline
  - How to verify outputs

- [ ] **Test Validation:**
  - How to check if tests pass
  - How to debug failing tests

---

## Acceptance Criteria

- [ ] README contains all required institutional information
- [ ] README has clear compilation and execution instructions
- [ ] README documents control structure syntax completely
- [ ] README includes test validation methodology
- [ ] Examples in README match actual test files
- [ ] Code comments follow Google C++ Style Guide / PEP 8
- [ ] All major functions have docstrings with:
  - Purpose description
  - Parameter types and descriptions
  - Return type and description
  - Example usage (for complex functions)
- [ ] CLAUDE.md updated with RA3 information
- [ ] CONTRIBUTING.md explains workflow clearly
- [ ] Architecture documentation includes diagrams
- [ ] Type system specification is complete and formal
- [ ] Testing guide is comprehensive
- [ ] Markdown files are properly formatted
- [ ] No spelling or grammar errors

---

## Grading Impact

- **-15%** if README incomplete or poorly formatted
- **Part of "Organization and Legibility"** (15% of grade)

---

## Dependencies

### Requires
- Issues #1-4 (to document implemented functionality)

### Blocks
None (can be done in parallel with implementation)

---

## Files to Create/Update

```
README.md                          # UPDATE with RA3 section
CLAUDE.md                          # UPDATE with RA3 info
CONTRIBUTING.md                    # CREATE

docs/RA3/
├── architecture.md                # RA3 architecture docs
├── type_system.md                 # Type system specification
└── testing_guide.md               # Testing methodology
```

---

## References

- **Documentation:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
  - Section 10 (Repository) - Lines 400-411
  - Section 11.3 (Documentation) - Lines 459-465

- **README requirements:** Lines 459-465, 644-650 in requirements

---

## README.md Template

### Suggested Structure

```markdown
# RA3_1 - Compilador RPN com Análise Semântica

## Informações Institucionais
**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
**Disciplina:** Linguagens Formais e Autômatos
**Professor:** Frank Alcantara
**Ano:** 2025

## Integrantes do Grupo (ordem alfabética)
- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

**Nome do grupo no Canvas:** RA3_1

## Descrição do Projeto

### Visão Geral
Este é um compilador completo para a linguagem RPN (Reverse Polish Notation) simplificada, implementando três fases principais:

1. **RA1 - Análise Léxica:** Tokenização e geração de código Assembly RISC-V
2. **RA2 - Análise Sintática:** Parser LL(1) com geração de árvore sintática
3. **RA3 - Análise Semântica:** Verificação de tipos e validação semântica

### Fase 3: Análise Semântica
A Fase 3 implementa:
- **Gramática de Atributos** com regras de tipagem
- **Tabela de Símbolos** para rastreamento de variáveis
- **Verificação de Tipos** com promoção automática (int → real)
- **Validação de Memória** (inicialização antes do uso)
- **Validação de Estruturas de Controle** (FOR, WHILE, IFELSE)
- **Detecção de Erros Semânticos** com mensagens claras

### Sistema de Tipos
A linguagem suporta três tipos:
- **int:** Números inteiros
- **real:** Números de ponto flutuante
- **boolean:** Resultado de comparações (não armazenável em memória)

## Compilação e Execução

### Requisitos
- Python 3.8+
- pytest (para testes unitários)

### Instalação
```bash
git clone https://github.com/seu-usuario/RA3_1.git
cd RA3_1
pip install -r requirements.txt
```

### Uso Básico
```bash
python3 compilar.py <arquivo_entrada>
```

### Exemplos
```bash
# Arquivo válido
python3 compilar.py inputs/RA3/teste1_valido.txt

# Arquivo com erros de tipo
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt

# Arquivo com erros de memória
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
```

## Sintaxe da Linguagem

### Operadores Aritméticos
- `+`, `-`, `*`: Aceitam int ou real
- `|`: Divisão real (int ou real)
- `/`: Divisão inteira (apenas int)
- `%`: Resto (apenas int)
- `^`: Potência (base: int/real, expoente: int)

### Operadores Relacionais
- `>`, `<`, `>=`, `<=`, `==`, `!=`
- Aceitam: int ou real
- Retornam: boolean

### Operadores Lógicos
- `&&`, `||`: AND, OR (operandos boolean)
- `!`: NOT (operando boolean)

### Estruturas de Controle
```
# WHILE
(condição corpo WHILE)
Exemplo: ((5 3 >) (10 20 +) WHILE)

# FOR
(init condição incremento corpo FOR)

# IFELSE
(condição ramo_true ramo_false IFELSE)
Exemplo: ((5 3 >) (10) (20) IFELSE)
```

### Comandos de Memória
```
(valor VARIAVEL MEM)  # Armazenar
(VARIAVEL)            # Ler
(N RES)               # Referenciar linha anterior
```

## Arquivos de Saída

Após a execução, os seguintes arquivos são gerados em `outputs/RA3/`:

1. **gramatica_atributos.md** - Gramática de atributos completa
2. **arvore_atribuida.md** - Árvore sintática com tipos (texto)
3. **arvore_atribuida.json** - Árvore sintática com tipos (JSON)
4. **julgamento_tipos.md** - Relatório de inferência de tipos
5. **erros_semanticos.md** - Relatório de erros semânticos

## Testes

### Executar Testes Unitários
```bash
python3 -m pytest tests/RA3/
```

### Validar com Arquivos de Teste
Três arquivos de teste estão em `inputs/RA3/`:
- `teste1_valido.txt`: Casos válidos
- `teste2_erros_tipos.txt`: Erros de tipo
- `teste3_erros_memoria.txt`: Erros de memória/controle

## Depuração

### Ver Erros Detalhados
Erros são mostrados no console e salvos em `outputs/RA3/erros_semanticos.md`

### Inspecionar Árvore Sintática
```bash
cat outputs/RA3/arvore_atribuida.md
# ou
python3 -m json.tool outputs/RA3/arvore_atribuida.json
```

### Ver Julgamento de Tipos
```bash
cat outputs/RA3/julgamento_tipos.md
```

## Estrutura do Projeto
```
RA3_1/
├── compilar.py              # Ponto de entrada
├── src/
│   ├── RA1/                 # Análise léxica
│   ├── RA2/                 # Análise sintática
│   └── RA3/                 # Análise semântica
├── inputs/
│   └── RA3/                 # Arquivos de teste
├── outputs/
│   └── RA3/                 # Arquivos gerados
├── tests/
│   └── RA3/                 # Testes unitários
└── docs/
    └── RA3/                 # Documentação
```

## Contribuindo
Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

## Licença
Este projeto é desenvolvido como trabalho acadêmico para a disciplina de Linguagens Formais e Autômatos.

## Autores
Veja a lista de [contribuidores](https://github.com/seu-usuario/RA3_1/graphs/contributors).
```

---

## CONTRIBUTING.md Template

```markdown
# Guia de Contribuição

## Fluxo de Trabalho

### 1. Criar Issue
- Use templates de issue quando disponível
- Adicione labels apropriadas
- Descreva claramente o problema ou feature

### 2. Criar Branch
```bash
git checkout -b issue-#-descricao-curta
```

Exemplos:
- `issue-1-grammar-symbol-table`
- `issue-2-type-checking`

### 3. Fazer Commits
Formato da mensagem:
```
tipo(escopo): descrição curta

Descrição detalhada se necessário.

Refs: #numero-da-issue
```

Exemplos:
```
feat(grammar): implement attribute grammar structure

Created TabelaSimbolos class with add, search, update methods.
Defined type promotion rules for arithmetic operators.

Refs: #1
```

### 4. Criar Pull Request
- Título claro
- Descrever mudanças
- Referenciar issue: "Closes #1"
- Pedir review de pelo menos 1 membro

## Padrões de Código

### Python (PEP 8)
- Indentação: 4 espaços
- Linhas: máximo 100 caracteres
- Nomes de variáveis: snake_case
- Nomes de classes: PascalCase
- Nomes de constantes: UPPER_CASE

### Docstrings
```python
def funcao_exemplo(param1: int, param2: str) -> bool:
    """
    Breve descrição da função.

    Descrição mais detalhada se necessário.

    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2

    Returns:
        Descrição do retorno

    Raises:
        ErroSemantico: Quando e por que

    Example:
        >>> funcao_exemplo(5, "test")
        True
    """
    pass
```

## Testes

### Quando Escrever Testes
- Para toda função pública
- Para casos de erro
- Para edge cases

### Naming
```python
def test_nome_descritivo():
    """Test description in docstring"""
    pass
```

### Executar Testes
```bash
# Todos os testes
python3 -m pytest tests/

# Testes específicos
python3 -m pytest tests/RA3/test_tabela_simbolos.py

# Com cobertura
python3 -m pytest --cov=src/RA3 tests/RA3/
```

## Code Review

### Como Revisor
- Verifique lógica do código
- Teste localmente
- Cheque estilo (PEP 8)
- Verifique testes
- Seja construtivo nos comentários

### Como Autor
- Responda a todos os comentários
- Faça mudanças solicitadas
- Marque conversas como resolvidas
- Aguarde aprovação antes de merge
```

---

## Notes

- Documentation should be **clear and comprehensive**
- Examples should **match actual test files**
- Keep documentation **up to date** with code changes
- Use **proper markdown formatting** for readability
- Include **diagrams** where helpful (architecture, data flow)
- This issue coordinates with Issues #1-4 to document their work
