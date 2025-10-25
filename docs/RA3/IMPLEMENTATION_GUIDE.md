# RA3 Implementation Guide: Using Issue #1 Foundation

**Author:** Aluno 1 (Stefan Benjamim Seixas Lourenço Rodrigues - waifuisalie)
**Date:** 2025-10-25
**Purpose:** Guide team members on implementing Issues #2, #3, #4, and #7 using the completed Issue #1 foundation

---

## Table of Contents

1. [What's Been Completed](#whats-been-completed)
2. [Architecture Overview](#architecture-overview)
3. [Using the Type System (`tipos.py`)](#using-the-type-system)
4. [Using the Symbol Table (`tabela_simbolos.py`)](#using-the-symbol-table)
5. [Using the Attribute Grammar (`gramatica_atributos.py`)](#using-the-attribute-grammar)
6. [Issue #2: Type Checking Implementation](#issue-2-type-checking-implementation)
7. [Issue #3: Memory & Control Validation](#issue-3-memory--control-validation)
8. [Issue #4: Integration & AST Generation](#issue-4-integration--ast-generation)
9. [Issue #7: Output Generators](#issue-7-output-generators)
10. [Testing Strategy](#testing-strategy)
11. [Common Pitfalls & Solutions](#common-pitfalls--solutions)

---

## What's Been Completed

### ✅ Issue #1: Grammar, Symbol Table, and Type System

The following modules are **fully implemented and tested** (32 unit tests passing):

#### `src/RA3/functions/python/tipos.py`
- **3 type constants**: `TYPE_INT`, `TYPE_REAL`, `TYPE_BOOLEAN`
- **Type promotion**: `promover_tipo(tipo1, tipo2)`
- **Truthiness conversion**: `para_booleano(valor, tipo)`
- **Compatibility checkers**: 14 functions for all operator categories
- **Result type inference**: Functions for arithmetic, comparison, logical operators

#### `src/RA3/functions/python/tabela_simbolos.py`
- **`TabelaSimbolos` class**: Complete symbol table implementation
- **Operations**: `adicionar()`, `buscar()`, `existe()`, `marcar_inicializada()`
- **Validation**: `verificar_inicializacao()`, `obter_tipo()`, `registrar_uso()`
- **Reporting**: `gerar_relatorio()`, `listar_simbolos()`
- **Scope tracking**: Ready for nested scopes

#### `src/RA3/functions/python/gramatica_atributos.py`
- **22 semantic rules** defined across 5 categories
- **Arithmetic operators**: `+`, `-`, `*`, `/`, `|`, `%`, `^` with type promotion rules
- **Comparison operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Logical operators**: `&&`, `||`, `!` with truthiness support
- **Control structures**: `FOR`, `WHILE`, `IFELSE` with formal rules
- **Special commands**: `MEM` (store/load), `RES`, `EPSILON` (identity)

#### `tests/RA3/test_tabela_simbolos.py`
- **32 passing unit tests** covering all symbol table functionality
- **All edge cases tested**: initialization tracking, scope management, error conditions

---

## Architecture Overview

### System Flow: RA1 → RA2 → RA3

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPILER PIPELINE                         │
└─────────────────────────────────────────────────────────────┘

  INPUT FILE (RPN expressions)
       │
       ├──→ RA1: Lexical Analysis
       │    └─→ tokens_gerados.txt
       │
       ├──→ RA2: Syntactic Analysis
       │    ├─→ Syntax tree (text)
       │    └─→ arvore_sintatica.json
       │
       └──→ RA3: Semantic Analysis  ⟵ YOU ARE HERE
            │
            ├─→ Issue #1 (✅ DONE)
            │   ├─ tipos.py (Type system)
            │   ├─ tabela_simbolos.py (Symbol tracking)
            │   └─ gramatica_atributos.py (Semantic rules)
            │
            ├─→ Issue #2 (TODO: Aluno 2)
            │   ├─ analisador_semantico.py (AST traversal)
            │   ├─ verificador_tipos.py (Type checking)
            │   └─ Uses: tipos.py, tabela_simbolos.py, gramatica_atributos.py
            │
            ├─→ Issue #3 (TODO: Aluno 3)
            │   ├─ validador_memoria.py (Memory validation)
            │   ├─ validador_controle.py (Control structures)
            │   └─ Uses: tabela_simbolos.py, tipos.py
            │
            ├─→ Issue #4 (TODO: Aluno 4)
            │   ├─ gerador_arvore_atribuida.py (Final AST)
            │   ├─ Update compilar.py (Integration)
            │   └─ Uses: All Issue #2 and #3 outputs
            │
            └─→ Issue #7 (TODO: Aluno 4)
                ├─ Generates 5 output markdown/JSON files
                └─ Uses: gramatica_atributos.py, Issue #2-4 results
```

### Data Flow Between Issues

```python
# Issue #1 provides (ALREADY DONE):
gramatica = definir_gramatica_atributos()  # 22 semantic rules
tabela = TabelaSimbolos()                   # Empty symbol table
tipos.promover_tipo(...)                    # Type utilities

# Issue #2 receives:
ast_from_ra2 = load_from_json("outputs/RA2/arvore_sintatica.json")

# Issue #2 produces:
ast_type_annotated = {
    'nodes': [...],  # Each node has 'tipo_inferido' attribute
    'errors': [...]   # Type errors found
}

# Issue #3 receives:
ast_type_annotated  # From Issue #2
tabela              # Updated during Issue #2

# Issue #3 produces:
validation_result = {
    'memory_errors': [...],
    'control_errors': [...],
    'tabela_updated': tabela  # With initialization info
}

# Issue #4 receives:
ast_type_annotated      # From Issue #2
validation_result       # From Issue #3

# Issue #4 produces:
attributed_ast = {
    'tipo_vertice': ...,
    'tipo_inferido': ...,
    'filhos': [...],
    'numero_linha': ...
}
```

---

## Using the Type System

### Import and Constants

```python
# Import the module
import tipos

# Use type constants
tipos.TYPE_INT       # 'int'
tipos.TYPE_REAL      # 'real'
tipos.TYPE_BOOLEAN   # 'boolean'

# Type sets
tipos.TIPOS_VALIDOS    # {'int', 'real', 'boolean'}
tipos.TIPOS_NUMERICOS  # {'int', 'real'}
tipos.TIPOS_TRUTHY     # {'int', 'real', 'boolean'}
```

### Type Promotion (Issue #2 will use this HEAVILY)

```python
# Promote types according to int < real hierarchy
resultado = tipos.promover_tipo('int', 'int')    # → 'int'
resultado = tipos.promover_tipo('int', 'real')   # → 'real'
resultado = tipos.promover_tipo('real', 'int')   # → 'real'

# Example: Checking arithmetic operation types
tipo_esq = 'int'
tipo_dir = 'real'
tipo_resultado = tipos.promover_tipo(tipo_esq, tipo_dir)  # → 'real'
```

### Truthiness Conversion (Issue #3 for logical operators)

```python
# Convert numeric/boolean values to boolean (permissive mode)
tipos.para_booleano(5, 'int')        # → True
tipos.para_booleano(0, 'int')        # → False
tipos.para_booleano(3.14, 'real')    # → True
tipos.para_booleano(0.0, 'real')     # → False
tipos.para_booleano(True, 'boolean') # → True

# Use in logical operator validation
def validar_operador_logico(operando1, operando2):
    # Convert operands to boolean using truthiness
    val1_bool = tipos.para_booleano(operando1['valor'], operando1['tipo'])
    val2_bool = tipos.para_booleano(operando2['valor'], operando2['tipo'])
    # Result is always boolean
    return tipos.TYPE_BOOLEAN
```

### Compatibility Checking (Issue #2 - Critical!)

```python
# Arithmetic operators (+, -, *, |)
if tipos.tipos_compativeis_aritmetica('int', 'real'):
    tipo_resultado = tipos.promover_tipo('int', 'real')

# Integer-only operators (/, %)
if tipos.tipos_compativeis_divisao_inteira('int', 'real'):
    # This returns False!
    # Raise semantic error
    raise ErroSemantico("Divisão inteira requer operandos inteiros")

# Power operator (^)
if tipos.tipos_compativeis_potencia('real', 'int'):
    # Base can be real, exponent must be int
    tipo_resultado = 'real'  # Type of base

# Comparison operators (>, <, ==, etc.)
if tipos.tipos_compativeis_comparacao('int', 'real'):
    tipo_resultado = tipos.TYPE_BOOLEAN  # Always boolean

# Logical operators (&&, ||)
if tipos.tipos_compativeis_logico('int', 'int'):
    # Permissive mode - accepts int via truthiness
    tipo_resultado = tipos.TYPE_BOOLEAN
```

### Type Result Functions (Issue #2 - Use these!)

```python
# These functions do compatibility checking AND return result type
try:
    # Arithmetic: handles all rules automatically
    tipo = tipos.tipo_resultado_aritmetica('int', 'real', '+')  # → 'real'
    tipo = tipos.tipo_resultado_aritmetica('int', 'int', '|')   # → 'real' (always)
    tipo = tipos.tipo_resultado_aritmetica('int', 'int', '/')   # → 'int'
    tipo = tipos.tipo_resultado_aritmetica('real', 'int', '^')  # → 'real'

    # Comparison: always returns boolean
    tipo = tipos.tipo_resultado_comparacao('int', 'real')  # → 'boolean'

    # Logical: always returns boolean
    tipo = tipos.tipo_resultado_logico('int', 'int')       # → 'boolean'
    tipo = tipos.tipo_resultado_logico_unario('int')       # → 'boolean'

except ValueError as e:
    # Incompatible types - create semantic error
    erros.append(ErroSemantico(linha, str(e)))
```

### Storage and Condition Validation (Issue #3)

```python
# Check if type can be stored in MEM
if tipos.tipo_compativel_armazenamento('int'):    # → True
if tipos.tipo_compativel_armazenamento('real'):   # → True
if tipos.tipo_compativel_armazenamento('boolean'):  # → False (ERROR!)

# Check if type can be used as condition (permissive mode)
if tipos.tipo_compativel_condicao('boolean'):  # → True
if tipos.tipo_compativel_condicao('int'):      # → True (via truthiness)
if tipos.tipo_compativel_condicao('real'):     # → True (via truthiness)
```

---

## Using the Symbol Table

### Creating and Initializing

```python
from tabela_simbolos import TabelaSimbolos, criar_tabela_simbolos

# Method 1: Direct instantiation
tabela = TabelaSimbolos()

# Method 2: Factory function
tabela = criar_tabela_simbolos()

# Both create empty symbol table ready to use
print(len(tabela))  # → 0
```

### Adding Symbols (Issue #2 and #3)

```python
import tipos

# Add initialized variable (e.g., from (5 CONTADOR MEM))
simbolo = tabela.adicionar(
    nome='CONTADOR',
    tipo=tipos.TYPE_INT,
    inicializada=True,
    linha=10
)

# Add uninitialized variable (placeholder)
simbolo = tabela.adicionar(
    nome='TEMP',
    tipo=tipos.TYPE_REAL,
    inicializada=False,
    linha=15
)

# Re-adding same variable updates it
simbolo = tabela.adicionar(
    nome='CONTADOR',
    tipo=tipos.TYPE_REAL,  # Type changed
    inicializada=True,      # Update initialization
    linha=20
)
```

### Searching and Validation (Issue #2 and #3 - Critical!)

```python
# Check if symbol exists
if tabela.existe('CONTADOR'):
    print("CONTADOR existe na tabela")

# Get symbol information
simbolo = tabela.buscar('CONTADOR')
if simbolo:
    print(f"Tipo: {simbolo.tipo}")
    print(f"Inicializada: {simbolo.inicializada}")
    print(f"Escopo: {simbolo.escopo}")
    print(f"Declarada na linha: {simbolo.linha_declaracao}")
else:
    print("Símbolo não encontrado")

# Check initialization (CRITICAL for Issue #3)
if tabela.verificar_inicializacao('CONTADOR'):
    # OK to use variable
    tipo = tabela.obter_tipo('CONTADOR')
else:
    # SEMANTIC ERROR!
    raise ErroSemantico(
        linha=linha_atual,
        descricao=f"Memória 'CONTADOR' utilizada sem inicialização",
        contexto="(CONTADOR)"
    )

# Get type directly
tipo = tabela.obter_tipo('CONTADOR')  # → 'int' or None if not found
```

### Marking Initialization (Issue #3 - Memory validation)

```python
# When processing (V MEM) command
def processar_mem_store(valor_tipo, nome_variavel, linha):
    # Validate type can be stored
    if not tipos.tipo_compativel_armazenamento(valor_tipo):
        raise ErroSemantico(
            linha=linha,
            descricao=f"Tipo '{valor_tipo}' não pode ser armazenado em memória",
            contexto=f"({nome_variavel} MEM)"
        )

    # Add to symbol table and mark as initialized
    tabela.adicionar(nome_variavel, valor_tipo, inicializada=True, linha=linha)
```

### Registering Usage (Optional but useful for statistics)

```python
# Register each time variable is used
tabela.registrar_uso('CONTADOR', linha=25)
tabela.registrar_uso('CONTADOR', linha=30)

# Get usage count
usos = tabela.obter_numero_usos('CONTADOR')  # → 2
```

### Generating Reports (Issue #4 and #7)

```python
# Generate full text report
relatorio = tabela.gerar_relatorio()
print(relatorio)
# Output:
# ======================================================================
# TABELA DE SÍMBOLOS
# ======================================================================
# Escopo atual: 0
# Total de símbolos: 3
# ----------------------------------------------------------------------
# Nome            Tipo       Inicializada    Linha Decl.  Usos
# ----------------------------------------------------------------------
# CONTADOR        int        SIM             10           2
# PI              real       SIM             15           1
# TEMP            int        NÃO             20           0
# ======================================================================

# List symbols programmatically
simbolos = tabela.listar_simbolos()
for simbolo in simbolos:
    print(f"{simbolo.nome}: {simbolo.tipo}")

# List only initialized symbols
inicializadas = tabela.listar_simbolos(apenas_inicializadas=True)
```

### Clearing Table (Between files)

```python
# Clear all symbols (each file = independent scope)
tabela.limpar()
print(len(tabela))  # → 0
```

---

## Using the Attribute Grammar

### Initializing the System (Issue #2 start)

```python
from gramatica_atributos import definir_gramatica_atributos, inicializar_sistema_semantico

# Method 1: Get grammar only
gramatica = definir_gramatica_atributos()

# Method 2: Get grammar + empty symbol table
gramatica, tabela = inicializar_sistema_semantico()

# Grammar structure:
# gramatica = {
#     'aritmetico': {'+': {...}, '-': {...}, ...},
#     'comparacao': {'>': {...}, '<': {...}, ...},
#     'logico': {'&&': {...}, '||': {...}, '!': {...}},
#     'controle': {'IFELSE': {...}, 'WHILE': {...}, 'FOR': {...}},
#     'comando': {'MEM_STORE': {...}, 'MEM_LOAD': {...}, 'RES': {...}}
# }
```

### Looking Up Semantic Rules (Issue #2)

```python
# Get rule for specific operator
regra_soma = gramatica['aritmetico']['+']

# Access rule properties
print(regra_soma['categoria'])        # 'aritmetico'
print(regra_soma['operador'])         # '+'
print(regra_soma['nome'])              # 'soma'
print(regra_soma['aridade'])           # 2
print(regra_soma['tipos_operandos'])   # [{'int', 'real'}, {'int', 'real'}]
print(regra_soma['descricao'])         # 'Operador soma com promoção de tipos'
print(regra_soma['restricoes'])        # ['Ambos operandos devem ser numéricos', ...]

# Formal rule (for documentation)
print(regra_soma['regra_formal'])
# Output:
# Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
# ───────────────────────────────────────────────────────
#     Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
```

### Applying Semantic Actions (Issue #2 - Example)

```python
# Example: Applying addition semantic action
regra = gramatica['aritmetico']['+']

# Simulate operands (would come from AST traversal)
operando1 = {'tipo': 'int', 'valor': 5}
operando2 = {'tipo': 'real', 'valor': 3.5}

# Apply semantic action (this is a lambda function)
resultado = regra['acao_semantica'](operando1, operando2, tabela)

print(resultado)
# Output:
# {
#     'tipo': 'real',          # Promoted from int+real
#     'valor': None,            # Runtime value
#     'operandos': [operando1, operando2]
# }
```

### Getting Result Type (Issue #2 - Pattern to use)

```python
# Pattern for determining result type from operator
def obter_tipo_resultado(operador, operando1, operando2, categoria='aritmetico'):
    regra = gramatica[categoria].get(operador)

    if not regra:
        raise ValueError(f"Operador desconhecido: {operador}")

    # tipo_resultado can be:
    # 1. A string: 'int', 'real', 'boolean'
    # 2. A callable: lambda op1, op2: promover_tipo(op1['tipo'], op2['tipo'])

    tipo_resultado = regra['tipo_resultado']

    if callable(tipo_resultado):
        # Call function with operands
        return tipo_resultado(operando1, operando2)
    else:
        # Direct type
        return tipo_resultado

# Usage
tipo = obter_tipo_resultado('+', operando1, operando2, 'aritmetico')
```

### Listing All Operators (Issue #7 - Documentation)

```python
from gramatica_atributos import listar_operadores_por_categoria

ops = listar_operadores_por_categoria()
# Returns:
# {
#     'aritmetico': ['+', '-', '*', '/', '|', '%', '^'],
#     'comparacao': ['>', '<', '>=', '<=', '==', '!='],
#     'logico': ['&&', '||', '!'],
#     'controle': ['IFELSE', 'WHILE', 'FOR'],
#     'comando': ['MEM_STORE', 'MEM_LOAD', 'RES', 'EPSILON']
# }

# Use for generating documentation
for categoria, operadores in ops.items():
    print(f"\n## {categoria.upper()}\n")
    for op in operadores:
        regra = gramatica[categoria][op]
        print(f"### {op} - {regra['nome']}")
        print(f"{regra['descricao']}\n")
        print("```")
        print(regra['regra_formal'])
        print("```\n")
```

### Getting Specific Rule (Helper function)

```python
from gramatica_atributos import obter_regra

# Search all categories for operator
regra = obter_regra('+')                    # Finds in 'aritmetico'
regra = obter_regra('IFELSE')               # Finds in 'controle'

# Search specific category (faster)
regra = obter_regra('>', categoria='comparacao')
```

---

## Issue #2: Type Checking Implementation

**Assignee:** Aluno 2
**Files to create:**
- `src/RA3/functions/python/analisador_semantico.py`
- `src/RA3/functions/python/verificador_tipos.py`
- `src/RA3/functions/python/gerador_erros.py`
- `tests/RA3/test_verificador_tipos.py`

### Overview

Issue #2 is responsible for **traversing the AST from RA2** and **annotating each node with type information** while **detecting type errors**.

### Algorithm: Post-Order Traversal

```python
def analisar_semanticamente(ast_node, tabela, gramatica, linha_atual):
    """
    Analyze AST node and infer types (post-order traversal)

    Args:
        ast_node: Node from RA2 AST
        tabela: TabelaSimbolos instance
        gramatica: Grammar from definir_gramatica_atributos()
        linha_atual: Current line number

    Returns:
        dict with 'tipo', 'valor', 'erros'
    """
    erros = []

    # Base case: Leaf nodes (literals, variables)
    if ast_node['tipo'] == 'LITERAL':
        return analisar_literal(ast_node)

    if ast_node['tipo'] == 'VARIAVEL':
        return analisar_variavel(ast_node, tabela, linha_atual, erros)

    # Recursive case: Operators
    if ast_node['tipo'] == 'OPERADOR':
        # First, analyze all children (post-order!)
        tipos_filhos = []
        for filho in ast_node['filhos']:
            resultado_filho = analisar_semanticamente(filho, tabela, gramatica, linha_atual)
            tipos_filhos.append(resultado_filho)
            erros.extend(resultado_filho.get('erros', []))

        # Then, apply operator type rule
        try:
            tipo_resultado = aplicar_regra_operador(
                ast_node['operador'],
                tipos_filhos,
                gramatica,
                linha_atual
            )

            return {
                'tipo': tipo_resultado,
                'valor': None,  # Runtime value
                'filhos': tipos_filhos,
                'erros': erros
            }
        except ErroSemantico as e:
            erros.append(e)
            return {
                'tipo': None,  # Type inference failed
                'valor': None,
                'filhos': tipos_filhos,
                'erros': erros
            }

    return {'tipo': None, 'valor': None, 'erros': erros}
```

### Analyzing Literals

```python
import tipos

def analisar_literal(ast_node):
    """
    Infer type from literal value

    Args:
        ast_node: {'tipo': 'LITERAL', 'valor': '5' or '3.14'}

    Returns:
        {'tipo': 'int' or 'real', 'valor': parsed_value}
    """
    valor_str = ast_node['valor']

    # Try integer first
    try:
        valor = int(valor_str)
        return {
            'tipo': tipos.TYPE_INT,
            'valor': valor,
            'erros': []
        }
    except ValueError:
        pass

    # Try float
    try:
        valor = float(valor_str)
        return {
            'tipo': tipos.TYPE_REAL,
            'valor': valor,
            'erros': []
        }
    except ValueError:
        return {
            'tipo': None,
            'valor': None,
            'erros': [ErroSemantico(
                linha=ast_node.get('linha', 0),
                descricao=f"Literal inválido: '{valor_str}'",
                contexto=valor_str
            )]
        }
```

### Analyzing Variables

```python
def analisar_variavel(ast_node, tabela, linha_atual, erros):
    """
    Look up variable type in symbol table

    Args:
        ast_node: {'tipo': 'VARIAVEL', 'nome': 'CONTADOR'}
        tabela: TabelaSimbolos instance
        linha_atual: Current line number
        erros: List to append errors

    Returns:
        {'tipo': tipo_da_variavel, 'valor': None}
    """
    nome = ast_node['nome'].upper()  # Variables are uppercase

    # Check if variable exists
    if not tabela.existe(nome):
        erros.append(ErroSemantico(
            linha=linha_atual,
            descricao=f"Variável '{nome}' não declarada",
            contexto=f"({nome})"
        ))
        return {'tipo': None, 'valor': None, 'erros': erros}

    # Get type from symbol table
    tipo = tabela.obter_tipo(nome)

    # Register usage (optional but useful)
    tabela.registrar_uso(nome, linha_atual)

    return {
        'tipo': tipo,
        'valor': None,  # Runtime value
        'erros': erros
    }
```

### Applying Operator Rules

```python
import tipos

def aplicar_regra_operador(operador, operandos, gramatica, linha):
    """
    Apply semantic rule for operator

    Args:
        operador: Operator symbol ('+', '-', '*', etc.)
        operandos: List of analyzed operands (each with 'tipo')
        gramatica: Attribute grammar
        linha: Line number for errors

    Returns:
        Inferred type string

    Raises:
        ErroSemantico: If type incompatibility
    """
    # Determine category
    categoria = determinar_categoria(operador, gramatica)

    if categoria == 'aritmetico':
        return aplicar_regra_aritmetica(operador, operandos, linha)
    elif categoria == 'comparacao':
        return aplicar_regra_comparacao(operador, operandos, linha)
    elif categoria == 'logico':
        return aplicar_regra_logica(operador, operandos, linha)
    # ... etc

    raise ErroSemantico(
        linha=linha,
        descricao=f"Operador desconhecido: {operador}",
        contexto=operador
    )


def aplicar_regra_aritmetica(operador, operandos, linha):
    """Apply arithmetic operator rules using tipos.py"""
    if len(operandos) != 2:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer 2 operandos",
            contexto=operador
        )

    tipo1 = operandos[0]['tipo']
    tipo2 = operandos[1]['tipo']

    # Use tipos.py function - it validates AND returns result
    try:
        tipo_resultado = tipos.tipo_resultado_aritmetica(tipo1, tipo2, operador)
        return tipo_resultado
    except ValueError as e:
        raise ErroSemantico(
            linha=linha,
            descricao=str(e),
            contexto=f"({tipo1} {tipo2} {operador})"
        )


def aplicar_regra_comparacao(operador, operandos, linha):
    """Apply comparison operator rules"""
    if len(operandos) != 2:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer 2 operandos",
            contexto=operador
        )

    tipo1 = operandos[0]['tipo']
    tipo2 = operandos[1]['tipo']

    # All comparison operators return boolean
    try:
        return tipos.tipo_resultado_comparacao(tipo1, tipo2)
    except ValueError as e:
        raise ErroSemantico(
            linha=linha,
            descricao=str(e),
            contexto=f"({tipo1} {tipo2} {operador})"
        )


def aplicar_regra_logica(operador, operandos, linha):
    """Apply logical operator rules (permissive mode)"""
    if operador == '!':
        # Unary NOT
        if len(operandos) != 1:
            raise ErroSemantico(
                linha=linha,
                descricao="Operador '!' requer 1 operando",
                contexto=operador
            )

        tipo = operandos[0]['tipo']
        return tipos.tipo_resultado_logico_unario(tipo)
    else:
        # Binary AND, OR
        if len(operandos) != 2:
            raise ErroSemantico(
                linha=linha,
                descricao=f"Operador '{operador}' requer 2 operandos",
                contexto=operador
            )

        tipo1 = operandos[0]['tipo']
        tipo2 = operandos[1]['tipo']
        return tipos.tipo_resultado_logico(tipo1, tipo2)
```

### Error Class Definition

```python
class ErroSemantico(Exception):
    """Semantic error with line number and context"""

    def __init__(self, linha, descricao, contexto=""):
        self.linha = linha
        self.descricao = descricao
        self.contexto = contexto
        self.categoria = self._inferir_categoria(descricao)

    def _inferir_categoria(self, descricao):
        """Infer error category from description"""
        desc_lower = descricao.lower()
        if 'tipo' in desc_lower:
            return 'tipo'
        if 'memória' in desc_lower or 'inicializ' in desc_lower:
            return 'memoria'
        if 'controle' in desc_lower or 'condição' in desc_lower:
            return 'controle'
        return 'outro'

    def __str__(self):
        return (
            f"ERRO SEMÂNTICO [Linha {self.linha}]: {self.descricao}\n"
            f"Contexto: {self.contexto}"
        )

    def para_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'linha': self.linha,
            'descricao': self.descricao,
            'contexto': self.contexto,
            'categoria': self.categoria
        }
```

### Complete Example: Analyzing Expression

```python
import tipos
from tabela_simbolos import criar_tabela_simbolos
from gramatica_atributos import definir_gramatica_atributos

# Setup
gramatica = definir_gramatica_atributos()
tabela = criar_tabela_simbolos()

# Example AST from RA2 for expression: (5 3.5 +)
ast = {
    'tipo': 'OPERADOR',
    'operador': '+',
    'linha': 1,
    'filhos': [
        {'tipo': 'LITERAL', 'valor': '5', 'linha': 1},
        {'tipo': 'LITERAL', 'valor': '3.5', 'linha': 1}
    ]
}

# Analyze
resultado = analisar_semanticamente(ast, tabela, gramatica, linha_atual=1)

print(resultado)
# Output:
# {
#     'tipo': 'real',  # Promoted from int + real
#     'valor': None,
#     'filhos': [
#         {'tipo': 'int', 'valor': 5, 'erros': []},
#         {'tipo': 'real', 'valor': 3.5, 'erros': []}
#     ],
#     'erros': []
# }
```

---

## Issue #3: Memory & Control Validation

**Assignee:** Aluno 3
**Files to create:**
- `src/RA3/functions/python/validador_memoria.py`
- `src/RA3/functions/python/validador_controle.py`
- `tests/RA3/test_validador_memoria.py`
- `tests/RA3/test_validador_controle.py`

### Overview

Issue #3 **receives the type-annotated AST from Issue #2** and performs **memory initialization checking** and **control structure validation**.

### Memory Validation: Tracking Initialization

```python
import tipos
from tabela_simbolos import TabelaSimbolos

class ValidadorMemoria:
    """Validates memory operations (MEM, RES)"""

    def __init__(self, tabela: TabelaSimbolos):
        self.tabela = tabela
        self.historico_resultados = []  # [(linha, tipo), ...]

    def validar_mem_store(self, nome_variavel, tipo_valor, linha):
        """
        Validate (V MEM) - memory write

        Args:
            nome_variavel: Variable name (e.g., 'CONTADOR')
            tipo_valor: Type being stored ('int', 'real', or 'boolean')
            linha: Line number

        Returns:
            tipo_valor (if valid)

        Raises:
            ErroSemantico: If trying to store boolean
        """
        # Check if type can be stored
        if not tipos.tipo_compativel_armazenamento(tipo_valor):
            raise ErroSemantico(
                linha=linha,
                descricao=f"Tipo '{tipo_valor}' não pode ser armazenado em memória. "
                         f"Apenas {tipos.TIPOS_NUMERICOS} são permitidos.",
                contexto=f"({nome_variavel} MEM)"
            )

        # Add to symbol table and mark as initialized
        self.tabela.adicionar(
            nome=nome_variavel.upper(),
            tipo=tipo_valor,
            inicializada=True,
            linha=linha
        )

        return tipo_valor

    def validar_mem_load(self, nome_variavel, linha):
        """
        Validate (MEM) - memory read

        Args:
            nome_variavel: Variable name
            linha: Line number

        Returns:
            Type of stored value

        Raises:
            ErroSemantico: If not initialized
        """
        nome = nome_variavel.upper()

        # Check if exists
        if not self.tabela.existe(nome):
            raise ErroSemantico(
                linha=linha,
                descricao=f"Memória '{nome}' utilizada sem inicialização",
                contexto=f"({nome})"
            )

        # Check if initialized
        if not self.tabela.verificar_inicializacao(nome):
            raise ErroSemantico(
                linha=linha,
                descricao=f"Memória '{nome}' utilizada sem inicialização",
                contexto=f"({nome})"
            )

        # Get type
        tipo = self.tabela.obter_tipo(nome)

        # Register usage
        self.tabela.registrar_uso(nome, linha)

        return tipo

    def registrar_resultado_linha(self, linha, tipo):
        """Register result type for RES references"""
        self.historico_resultados.append((linha, tipo))

    def validar_res_referencia(self, n_linhas_atras, linha_atual):
        """
        Validate (N RES) - result reference

        Args:
            n_linhas_atras: Number of lines to look back (must be int)
            linha_atual: Current line number

        Returns:
            Type of referenced result

        Raises:
            ErroSemantico: If reference is invalid
        """
        # Check N is non-negative
        if n_linhas_atras < 0:
            raise ErroSemantico(
                linha=linha_atual,
                descricao=f"Referência RES deve ter índice não-negativo, "
                         f"recebido {n_linhas_atras}",
                contexto=f"({n_linhas_atras} RES)"
            )

        # Calculate referenced line
        linha_referenciada = linha_atual - n_linhas_atras

        # Check line exists
        if linha_referenciada < 1:
            raise ErroSemantico(
                linha=linha_atual,
                descricao=f"Referência RES aponta para linha inexistente: "
                         f"{linha_referenciada}",
                contexto=f"({n_linhas_atras} RES)"
            )

        # Find type in history
        for linha, tipo in self.historico_resultados:
            if linha == linha_referenciada:
                return tipo

        # Not found
        raise ErroSemantico(
            linha=linha_atual,
            descricao=f"Linha {linha_referenciada} não possui resultado válido",
            contexto=f"({n_linhas_atras} RES)"
        )
```

### Control Structure Validation

```python
import tipos

class ValidadorControle:
    """Validates control structures (FOR, WHILE, IFELSE)"""

    def validar_while(self, ast_while, linha):
        """
        Validate WHILE structure

        RPN format: (condition body WHILE)

        Args:
            ast_while: {'tipo': 'WHILE', 'filhos': [cond_node, body_node]}
            linha: Line number

        Raises:
            ErroSemantico: If condition is not boolean-compatible
        """
        if len(ast_while['filhos']) != 2:
            raise ErroSemantico(
                linha=linha,
                descricao="WHILE requer 2 blocos: (condição) (corpo)",
                contexto="WHILE"
            )

        condicao = ast_while['filhos'][0]
        corpo = ast_while['filhos'][1]

        # Validate condition type (permissive mode)
        tipo_condicao = condicao.get('tipo_inferido')
        if not tipos.tipo_compativel_condicao(tipo_condicao):
            raise ErroSemantico(
                linha=linha,
                descricao=f"Condição de WHILE deve ser convertível para boolean, "
                         f"encontrado '{tipo_condicao}'",
                contexto=self._gerar_contexto_while(ast_while)
            )

        # WHILE returns type of last expression in body
        return corpo.get('tipo_inferido')

    def validar_for(self, ast_for, linha):
        """
        Validate FOR structure

        RPN format: (init end step body FOR)

        Args:
            ast_for: {'tipo': 'FOR', 'filhos': [init, end, step, body]}
            linha: Line number

        Raises:
            ErroSemantico: If init/end/step are not int
        """
        if len(ast_for['filhos']) != 4:
            raise ErroSemantico(
                linha=linha,
                descricao="FOR requer 4 blocos: (inicio) (fim) (passo) (corpo)",
                contexto="FOR"
            )

        init_node = ast_for['filhos'][0]
        end_node = ast_for['filhos'][1]
        step_node = ast_for['filhos'][2]
        body_node = ast_for['filhos'][3]

        # Validate init, end, step are ALL integers
        for i, (node, nome) in enumerate([(init_node, 'inicio'),
                                            (end_node, 'fim'),
                                            (step_node, 'passo')]):
            tipo = node.get('tipo_inferido')
            if tipo != tipos.TYPE_INT:
                raise ErroSemantico(
                    linha=linha,
                    descricao=f"Parâmetro '{nome}' do FOR deve ser int, "
                             f"encontrado '{tipo}'",
                    contexto=self._gerar_contexto_for(ast_for)
                )

        # FOR returns type of last expression in body
        return body_node.get('tipo_inferido')

    def validar_ifelse(self, ast_ifelse, linha):
        """
        Validate IFELSE structure

        RPN format: (condition true_branch false_branch IFELSE)

        Args:
            ast_ifelse: {'tipo': 'IFELSE', 'filhos': [cond, true, false]}
            linha: Line number

        Raises:
            ErroSemantico: If condition not boolean or branches have different types
        """
        if len(ast_ifelse['filhos']) != 3:
            raise ErroSemantico(
                linha=linha,
                descricao="IFELSE requer 3 blocos: (condição) (verdadeiro) (falso)",
                contexto="IFELSE"
            )

        condicao = ast_ifelse['filhos'][0]
        ramo_true = ast_ifelse['filhos'][1]
        ramo_false = ast_ifelse['filhos'][2]

        # Validate condition (permissive mode)
        tipo_condicao = condicao.get('tipo_inferido')
        if not tipos.tipo_compativel_condicao(tipo_condicao):
            raise ErroSemantico(
                linha=linha,
                descricao=f"Condição de IFELSE deve ser convertível para boolean, "
                         f"encontrado '{tipo_condicao}'",
                contexto=self._gerar_contexto_ifelse(ast_ifelse)
            )

        # Validate both branches have same type
        tipo_true = ramo_true.get('tipo_inferido')
        tipo_false = ramo_false.get('tipo_inferido')

        if tipo_true != tipo_false:
            raise ErroSemantico(
                linha=linha,
                descricao=f"Ramos do IFELSE devem ter o mesmo tipo. "
                         f"Ramo verdadeiro: '{tipo_true}', "
                         f"Ramo falso: '{tipo_false}'",
                contexto=self._gerar_contexto_ifelse(ast_ifelse)
            )

        # IFELSE returns type of branches (both same)
        return tipo_true

    def _gerar_contexto_while(self, ast_while):
        """Generate context string for error messages"""
        return f"(... WHILE)"

    def _gerar_contexto_for(self, ast_for):
        """Generate context string for error messages"""
        return f"(... FOR)"

    def _gerar_contexto_ifelse(self, ast_ifelse):
        """Generate context string for error messages"""
        return f"(... IFELSE)"
```

### Integration with Issue #2

```python
def validar_semantica_completa(ast_type_annotated, tabela, linha_atual):
    """
    Complete semantic validation (Issue #2 + Issue #3)

    Args:
        ast_type_annotated: AST with 'tipo_inferido' from Issue #2
        tabela: TabelaSimbolos (updated by Issue #2)
        linha_atual: Current line number

    Returns:
        {
            'erros_tipo': [...],      # From Issue #2
            'erros_memoria': [...],   # From Issue #3
            'erros_controle': [...],  # From Issue #3
            'ast_validado': ast
        }
    """
    # Issue #3 validators
    validador_mem = ValidadorMemoria(tabela)
    validador_ctrl = ValidadorControle()

    erros_memoria = []
    erros_controle = []

    # Traverse AST and validate
    def validar_node(node, linha):
        if node['tipo'] == 'MEM_LOAD':
            try:
                tipo = validador_mem.validar_mem_load(node['nome'], linha)
                node['tipo_inferido'] = tipo
            except ErroSemantico as e:
                erros_memoria.append(e)

        elif node['tipo'] == 'MEM_STORE':
            try:
                tipo = validador_mem.validar_mem_store(
                    node['nome'],
                    node['valor_tipo'],
                    linha
                )
            except ErroSemantico as e:
                erros_memoria.append(e)

        elif node['tipo'] == 'RES':
            try:
                tipo = validador_mem.validar_res_referencia(
                    node['n_linhas'],
                    linha
                )
                node['tipo_inferido'] = tipo
            except ErroSemantico as e:
                erros_memoria.append(e)

        elif node['tipo'] == 'WHILE':
            try:
                tipo = validador_ctrl.validar_while(node, linha)
                node['tipo_inferido'] = tipo
            except ErroSemantico as e:
                erros_controle.append(e)

        elif node['tipo'] == 'FOR':
            try:
                tipo = validador_ctrl.validar_for(node, linha)
                node['tipo_inferido'] = tipo
            except ErroSemantico as e:
                erros_controle.append(e)

        elif node['tipo'] == 'IFELSE':
            try:
                tipo = validador_ctrl.validar_ifelse(node, linha)
                node['tipo_inferido'] = tipo
            except ErroSemantico as e:
                erros_controle.append(e)

        # Recurse on children
        for filho in node.get('filhos', []):
            validar_node(filho, linha)

    # Start validation
    validar_node(ast_type_annotated, linha_atual)

    # Register line result for RES references
    if ast_type_annotated.get('tipo_inferido'):
        validador_mem.registrar_resultado_linha(
            linha_atual,
            ast_type_annotated['tipo_inferido']
        )

    return {
        'erros_tipo': ast_type_annotated.get('erros', []),
        'erros_memoria': erros_memoria,
        'erros_controle': erros_controle,
        'ast_validado': ast_type_annotated
    }
```

---

## Issue #4: Integration & AST Generation

**Assignee:** Aluno 4
**Files to create/modify:**
- `src/RA3/functions/python/gerador_arvore_atribuida.py`
- `compilar.py` (UPDATE)
- `tests/RA3/test_integracao.py`

### Overview

Issue #4 **integrates all three compiler phases** (RA1 → RA2 → RA3) and **generates the final attributed AST**.

### Updating `compilar.py` - Adding RA3 Phase

```python
#!/usr/bin/env python3

import sys
from pathlib import Path

# ... existing RA1 and RA2 imports ...

# RA3 imports
from src.RA3.functions.python import tipos
from src.RA3.functions.python.tabela_simbolos import criar_tabela_simbolos
from src.RA3.functions.python.gramatica_atributos import definir_gramatica_atributos
from src.RA3.functions.python.analisador_semantico import analisar_semanticamente
from src.RA3.functions.python.validador_memoria import ValidadorMemoria
from src.RA3.functions.python.validador_controle import ValidadorControle
from src.RA3.functions.python.gerador_arvore_atribuida import gerar_arvore_atribuida

def main():
    """Main compiler pipeline: RA1 → RA2 → RA3"""

    if len(sys.argv) < 2:
        print("Uso: python3 compilar.py <arquivo_entrada>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]

    print("=" * 70)
    print(f"  COMPILADOR RPN - Fases RA1 + RA2 + RA3")
    print("=" * 70)
    print(f"Entrada: {arquivo_entrada}\n")

    # ========================================================================
    # FASE RA1: ANÁLISE LÉXICA
    # ========================================================================
    print("[RA1] Análise Léxica...")

    try:
        tokens = executar_ra1(arquivo_entrada)  # Your existing function
        if tokens is None or tem_erros_lexicos():
            print("❌ Erros léxicos encontrados. Compilação abortada.")
            sys.exit(1)
        print("✅ Análise léxica concluída\n")
    except Exception as e:
        print(f"❌ Erro na análise léxica: {e}")
        sys.exit(1)

    # ========================================================================
    # FASE RA2: ANÁLISE SINTÁTICA
    # ========================================================================
    print("[RA2] Análise Sintática...")

    try:
        ast_ra2 = executar_ra2(tokens)  # Your existing function
        if ast_ra2 is None or tem_erros_sintaticos():
            print("❌ Erros sintáticos encontrados. Compilação abortada.")
            sys.exit(1)
        print("✅ Análise sintática concluída\n")
    except Exception as e:
        print(f"❌ Erro na análise sintática: {e}")
        sys.exit(1)

    # ========================================================================
    # FASE RA3: ANÁLISE SEMÂNTICA
    # ========================================================================
    print("[RA3] Análise Semântica...")

    try:
        # Initialize semantic analysis
        gramatica = definir_gramatica_atributos()
        tabela = criar_tabela_simbolos()

        all_errors = []
        attributed_trees = []

        # Process each line from AST
        for linha_num, ast_linha in enumerate(ast_ra2['linhas'], 1):
            # Issue #2: Type checking
            resultado_tipos = analisar_semanticamente(
                ast_linha,
                tabela,
                gramatica,
                linha_num
            )

            # Collect type errors
            all_errors.extend(resultado_tipos.get('erros', []))

            # Issue #3: Memory & control validation
            validador_mem = ValidadorMemoria(tabela)
            validador_ctrl = ValidadorControle()

            # Validate memory operations
            try:
                validar_memoria_linha(ast_linha, validador_mem, linha_num)
            except ErroSemantico as e:
                all_errors.append(e)

            # Validate control structures
            try:
                validar_controle_linha(ast_linha, validador_ctrl, linha_num)
            except ErroSemantico as e:
                all_errors.append(e)

            # Issue #4: Generate attributed AST
            arvore_atribuida = gerar_arvore_atribuida(
                resultado_tipos,
                linha_num
            )
            attributed_trees.append(arvore_atribuida)

        # Report results
        if all_errors:
            print(f"⚠️  {len(all_errors)} erro(s) semântico(s) encontrado(s):")
            for erro in all_errors[:10]:  # Show first 10
                print(f"  {erro}")
            if len(all_errors) > 10:
                print(f"  ... e mais {len(all_errors) - 10} erros")
            print()
        else:
            print("✅ Nenhum erro semântico encontrado\n")

        # Generate output files (Issue #7)
        print("[RA3] Gerando arquivos de saída...")
        gerar_outputs_ra3(gramatica, tabela, attributed_trees, all_errors)
        print("✅ Arquivos gerados em outputs/RA3/\n")

    except Exception as e:
        print(f"❌ Erro na análise semântica: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("=" * 70)
    print("  COMPILAÇÃO CONCLUÍDA")
    print("=" * 70)

    if all_errors:
        sys.exit(1)  # Exit with error code
    else:
        sys.exit(0)  # Success


if __name__ == '__main__':
    main()
```

### Generating Attributed AST

```python
# src/RA3/functions/python/gerador_arvore_atribuida.py

import json
from typing import Dict, List, Any

class NoArvoreAtribuida:
    """Node in attributed AST"""

    def __init__(self, tipo_vertice: str, tipo_inferido: str, numero_linha: int):
        self.tipo_vertice = tipo_vertice       # 'OPERADOR', 'LITERAL', etc.
        self.tipo_inferido = tipo_inferido     # 'int', 'real', 'boolean'
        self.numero_linha = numero_linha
        self.filhos = []
        self.valor = None
        self.operador = None

    def adicionar_filho(self, filho):
        """Add child node"""
        self.filhos.append(filho)

    def para_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'tipo_vertice': self.tipo_vertice,
            'tipo_inferido': self.tipo_inferido,
            'numero_linha': self.numero_linha,
            'filhos': [filho.para_dict() for filho in self.filhos],
            'valor': self.valor,
            'operador': self.operador
        }

    def para_texto(self, indent=0) -> str:
        """Convert to text representation"""
        prefixo = "  " * indent
        linhas = []

        linhas.append(f"{prefixo}[{self.tipo_vertice}] tipo: {self.tipo_inferido}")

        if self.operador:
            linhas.append(f"{prefixo}  operador: {self.operador}")
        if self.valor is not None:
            linhas.append(f"{prefixo}  valor: {self.valor}")

        for filho in self.filhos:
            linhas.append(filho.para_texto(indent + 1))

        return '\n'.join(linhas)


def gerar_arvore_atribuida(ast_type_annotated: Dict, linha: int) -> NoArvoreAtribuida:
    """
    Convert type-annotated AST to attributed AST

    Args:
        ast_type_annotated: AST from Issue #2 with 'tipo_inferido'
        linha: Line number

    Returns:
        NoArvoreAtribuida root node
    """
    tipo_node = ast_type_annotated['tipo']
    tipo_inferido = ast_type_annotated.get('tipo_inferido', 'unknown')

    # Create node
    node = NoArvoreAtribuida(tipo_node, tipo_inferido, linha)

    # Set attributes
    if 'valor' in ast_type_annotated:
        node.valor = ast_type_annotated['valor']

    if 'operador' in ast_type_annotated:
        node.operador = ast_type_annotated['operador']

    # Recursively convert children
    for filho_ast in ast_type_annotated.get('filhos', []):
        filho_node = gerar_arvore_atribuida(filho_ast, linha)
        node.adicionar_filho(filho_node)

    return node


def salvar_arvore_json(arvore: NoArvoreAtribuida, caminho: str):
    """Save attributed AST as JSON"""
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(arvore.para_dict(), f, indent=2, ensure_ascii=False)


def salvar_arvore_markdown(arvore: NoArvoreAtribuida, caminho: str):
    """Save attributed AST as markdown"""
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("# Árvore Sintática Atribuída\n\n")
        f.write("```\n")
        f.write(arvore.para_texto())
        f.write("\n```\n")
```

---

## Issue #7: Output Generators

**Assignee:** Aluno 4
**Files to create:**
- `src/RA3/functions/python/gerador_relatorios.py`

### Overview

Issue #7 generates **5 output files** based on the semantic analysis results.

### Required Outputs

1. `outputs/RA3/gramatica_atributos.md` - Grammar documentation
2. `outputs/RA3/arvore_atribuida.md` - AST in markdown
3. `outputs/RA3/arvore_atribuida.json` - AST in JSON
4. `outputs/RA3/julgamento_tipos.md` - Type judgment report
5. `outputs/RA3/erros_semanticos.md` - Error report

### Generating Grammar Documentation

```python
from datetime import datetime
from gramatica_atributos import definir_gramatica_atributos, listar_operadores_por_categoria

def gerar_gramatica_atributos_md(caminho: str):
    """Generate gramatica_atributos.md"""
    gramatica = definir_gramatica_atributos()
    ops_por_categoria = listar_operadores_por_categoria()

    linhas = []
    linhas.append("# Gramática de Atributos - Linguagem RPN\n")
    linhas.append(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    linhas.append("---\n\n")

    # For each category
    for categoria, operadores in ops_por_categoria.items():
        linhas.append(f"## {categoria.upper()}\n\n")

        for op in operadores:
            regra = gramatica[categoria][op]

            linhas.append(f"### {op} - {regra['nome']}\n\n")
            linhas.append(f"**Descrição:** {regra['descricao']}\n\n")
            linhas.append(f"**Aridade:** {regra['aridade']} operando(s)\n\n")

            linhas.append("**Restrições:**\n")
            for restricao in regra['restricoes']:
                linhas.append(f"- {restricao}\n")
            linhas.append("\n")

            linhas.append("**Regra Formal:**\n\n")
            linhas.append("```\n")
            linhas.append(regra['regra_formal'])
            linhas.append("\n```\n\n")
            linhas.append("---\n\n")

    # Write file
    with open(caminho, 'w', encoding='utf-8') as f:
        f.writelines(linhas)
```

### Generating Type Judgment Report

```python
def gerar_julgamento_tipos_md(historico_inferencias: List, caminho: str):
    """
    Generate julgamento_tipos.md

    Args:
        historico_inferencias: List of (linha, expressao, passos_inferencia, tipo_final)
    """
    linhas = []
    linhas.append("# Relatório de Julgamento de Tipos\n\n")
    linhas.append(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    linhas.append(f"**Total de expressões:** {len(historico_inferencias)}\n\n")
    linhas.append("---\n\n")

    for linha_num, expressao, passos, tipo_final in historico_inferencias:
        linhas.append(f"## Linha {linha_num}\n\n")
        linhas.append(f"**Expressão:** `{expressao}`\n\n")

        linhas.append("**Passos de Inferência:**\n\n")
        for i, passo in enumerate(passos, 1):
            linhas.append(f"{i}. {passo}\n")
        linhas.append("\n")

        linhas.append(f"**Tipo Resultante:** `{tipo_final}`\n\n")
        linhas.append("---\n\n")

    with open(caminho, 'w', encoding='utf-8') as f:
        f.writelines(linhas)
```

### Generating Error Report

```python
def gerar_erros_semanticos_md(erros: List, caminho: str):
    """
    Generate erros_semanticos.md

    Args:
        erros: List of ErroSemantico objects
    """
    linhas = []
    linhas.append("# Relatório de Erros Semânticos\n\n")
    linhas.append(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    if not erros:
        linhas.append("✅ **Nenhum erro semântico encontrado.**\n")
    else:
        linhas.append(f"⚠️ **Total de erros:** {len(erros)}\n\n")
        linhas.append("---\n\n")

        # Group by category
        erros_tipo = [e for e in erros if e.categoria == 'tipo']
        erros_memoria = [e for e in erros if e.categoria == 'memoria']
        erros_controle = [e for e in erros if e.categoria == 'controle']
        erros_outros = [e for e in erros if e.categoria == 'outro']

        # Type errors
        if erros_tipo:
            linhas.append(f"## Erros de Tipo ({len(erros_tipo)})\n\n")
            for i, erro in enumerate(erros_tipo, 1):
                linhas.append(f"### Erro #{i}\n\n")
                linhas.append(f"**Linha:** {erro.linha}\n\n")
                linhas.append(f"**Descrição:** {erro.descricao}\n\n")
                linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
                linhas.append("---\n\n")

        # Memory errors
        if erros_memoria:
            linhas.append(f"## Erros de Memória ({len(erros_memoria)})\n\n")
            for i, erro in enumerate(erros_memoria, 1):
                linhas.append(f"### Erro #{i}\n\n")
                linhas.append(f"**Linha:** {erro.linha}\n\n")
                linhas.append(f"**Descrição:** {erro.descricao}\n\n")
                linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
                linhas.append("---\n\n")

        # Control errors
        if erros_controle:
            linhas.append(f"## Erros de Controle ({len(erros_controle)})\n\n")
            for i, erro in enumerate(erros_controle, 1):
                linhas.append(f"### Erro #{i}\n\n")
                linhas.append(f"**Linha:** {erro.linha}\n\n")
                linhas.append(f"**Descrição:** {erro.descricao}\n\n")
                linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
                linhas.append("---\n\n")

        # Other errors
        if erros_outros:
            linhas.append(f"## Outros Erros ({len(erros_outros)})\n\n")
            for i, erro in enumerate(erros_outros, 1):
                linhas.append(f"### Erro #{i}\n\n")
                linhas.append(f"**Linha:** {erro.linha}\n\n")
                linhas.append(f"**Descrição:** {erro.descricao}\n\n")
                linhas.append(f"**Contexto:** `{erro.contexto}`\n\n")
                linhas.append("---\n\n")

    with open(caminho, 'w', encoding='utf-8') as f:
        f.writelines(linhas)
```

### Main Output Generation Function

```python
from pathlib import Path

def gerar_outputs_ra3(gramatica, tabela, arvores_atribuidas, erros):
    """
    Generate all 5 required output files

    Args:
        gramatica: From definir_gramatica_atributos()
        tabela: TabelaSimbolos with all symbols
        arvores_atribuidas: List of NoArvoreAtribuida (one per line)
        erros: List of ErroSemantico
    """
    # Create output directory
    output_dir = Path("outputs/RA3")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Grammar documentation
    gerar_gramatica_atributos_md(output_dir / "gramatica_atributos.md")

    # 2. Attributed AST (markdown)
    with open(output_dir / "arvore_atribuida.md", 'w', encoding='utf-8') as f:
        f.write("# Árvore Sintática Atribuída\n\n")
        for i, arvore in enumerate(arvores_atribuidas, 1):
            f.write(f"## Linha {i}\n\n")
            f.write("```\n")
            f.write(arvore.para_texto())
            f.write("\n```\n\n")

    # 3. Attributed AST (JSON)
    arvores_json = [arvore.para_dict() for arvore in arvores_atribuidas]
    with open(output_dir / "arvore_atribuida.json", 'w', encoding='utf-8') as f:
        json.dump(arvores_json, f, indent=2, ensure_ascii=False)

    # 4. Type judgment report (requires tracking during analysis)
    # gerar_julgamento_tipos_md(historico_inferencias, output_dir / "julgamento_tipos.md")

    # 5. Error report
    gerar_erros_semanticos_md(erros, output_dir / "erros_semanticos.md")

    print(f"✅ Gerado: {output_dir / 'gramatica_atributos.md'}")
    print(f"✅ Gerado: {output_dir / 'arvore_atribuida.md'}")
    print(f"✅ Gerado: {output_dir / 'arvore_atribuida.json'}")
    print(f"✅ Gerado: {output_dir / 'julgamento_tipos.md'}")
    print(f"✅ Gerado: {output_dir / 'erros_semanticos.md'}")
```

---

## Testing Strategy

### Unit Testing Each Module

```python
# tests/RA3/test_verificador_tipos.py (Issue #2)

import pytest
import tipos
from tabela_simbolos import criar_tabela_simbolos
from gramatica_atributos import definir_gramatica_atributos
from analisador_semantico import analisar_semanticamente

def test_adicao_inteiros():
    """Test integer addition: (5 3 +) → int"""
    gramatica = definir_gramatica_atributos()
    tabela = criar_tabela_simbolos()

    ast = {
        'tipo': 'OPERADOR',
        'operador': '+',
        'linha': 1,
        'filhos': [
            {'tipo': 'LITERAL', 'valor': '5'},
            {'tipo': 'LITERAL', 'valor': '3'}
        ]
    }

    resultado = analisar_semanticamente(ast, tabela, gramatica, 1)

    assert resultado['tipo'] == tipos.TYPE_INT
    assert len(resultado['erros']) == 0


def test_promocao_tipo():
    """Test type promotion: (5 3.5 +) → real"""
    gramatica = definir_gramatica_atributos()
    tabela = criar_tabela_simbolos()

    ast = {
        'tipo': 'OPERADOR',
        'operador': '+',
        'linha': 1,
        'filhos': [
            {'tipo': 'LITERAL', 'valor': '5'},
            {'tipo': 'LITERAL', 'valor': '3.5'}
        ]
    }

    resultado = analisar_semanticamente(ast, tabela, gramatica, 1)

    assert resultado['tipo'] == tipos.TYPE_REAL  # Promoted!
    assert len(resultado['erros']) == 0


def test_divisao_inteira_com_real_erro():
    """Test integer division with real: (5.5 2 /) → ERROR"""
    gramatica = definir_gramatica_atributos()
    tabela = criar_tabela_simbolos()

    ast = {
        'tipo': 'OPERADOR',
        'operador': '/',
        'linha': 1,
        'filhos': [
            {'tipo': 'LITERAL', 'valor': '5.5'},
            {'tipo': 'LITERAL', 'valor': '2'}
        ]
    }

    resultado = analisar_semanticamente(ast, tabela, gramatica, 1)

    assert len(resultado['erros']) > 0
    assert 'inteiro' in resultado['erros'][0].descricao.lower()
```

### Integration Testing

```python
# tests/RA3/test_integracao.py (Issue #4)

import pytest
from pathlib import Path
import subprocess

def test_compilar_arquivo_valido():
    """Test complete pipeline with valid file"""
    result = subprocess.run(
        ['python3', 'compilar.py', 'inputs/RA3/teste1_valido.txt'],
        capture_output=True,
        text=True
    )

    # Should succeed
    assert result.returncode == 0
    assert '✅' in result.stdout

    # Output files should exist
    assert Path('outputs/RA3/gramatica_atributos.md').exists()
    assert Path('outputs/RA3/arvore_atribuida.json').exists()
    assert Path('outputs/RA3/erros_semanticos.md').exists()


def test_compilar_arquivo_com_erros_tipo():
    """Test pipeline with type errors"""
    result = subprocess.run(
        ['python3', 'compilar.py', 'inputs/RA3/teste2_erros_tipos.txt'],
        capture_output=True,
        text=True
    )

    # Should complete but report errors
    assert result.returncode == 1
    assert 'erro(s) semântico(s)' in result.stdout.lower()
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Forgetting to Use `tipos.py` Functions

**Wrong:**
```python
# Manual type checking - error-prone!
if tipo1 == 'int' and tipo2 == 'real':
    return 'real'
elif tipo1 == 'real' and tipo2 == 'int':
    return 'real'
else:
    return 'int'
```

**Right:**
```python
# Use provided function - handles all cases
return tipos.promover_tipo(tipo1, tipo2)
```

### Pitfall 2: Not Checking Initialization Before Use

**Wrong:**
```python
# Assuming variable exists
tipo = tabela.obter_tipo('CONTADOR')
```

**Right:**
```python
# Always check initialization first (Issue #3 requirement!)
if not tabela.verificar_inicializacao('CONTADOR'):
    raise ErroSemantico(
        linha=linha,
        descricao=f"Memória 'CONTADOR' utilizada sem inicialização",
        contexto="(CONTADOR)"
    )
tipo = tabela.obter_tipo('CONTADOR')
```

### Pitfall 3: Storing Boolean in Memory

**Wrong:**
```python
# Allow any type in memory
tabela.adicionar('RESULT', tipo_qualquer, True, linha)
```

**Right:**
```python
# Validate type can be stored (Issue #3 requirement!)
if not tipos.tipo_compativel_armazenamento(tipo):
    raise ErroSemantico(
        linha=linha,
        descricao=f"Tipo '{tipo}' não pode ser armazenado em memória",
        contexto=f"({nome} MEM)"
    )
tabela.adicionar('RESULT', tipo, True, linha)
```

### Pitfall 4: Forgetting Post-Order Traversal

**Wrong:**
```python
# Pre-order - analyze parent before children
def analisar(node):
    tipo = calcular_tipo(node)  # Node type unknown yet!
    for filho in node.filhos:
        analisar(filho)
```

**Right:**
```python
# Post-order - analyze children first, then parent
def analisar(node):
    tipos_filhos = []
    for filho in node.filhos:
        tipos_filhos.append(analisar(filho))  # Children first!

    tipo = calcular_tipo(node, tipos_filhos)  # Then parent
    return tipo
```

### Pitfall 5: Not Using Semantic Rules from Grammar

**Wrong:**
```python
# Hardcoding rules - duplicates logic
if operador == '+':
    if tipo1 == 'int' and tipo2 == 'int':
        return 'int'
    # ... many lines of manual checking
```

**Right:**
```python
# Use pre-defined rules from grammar
regra = gramatica['aritmetico']['+']
resultado = regra['acao_semantica'](operando1, operando2, tabela)
return resultado['tipo']
```

---

## Quick Reference: Module APIs

### `tipos.py`

```python
# Constants
tipos.TYPE_INT, tipos.TYPE_REAL, tipos.TYPE_BOOLEAN
tipos.TIPOS_VALIDOS, tipos.TIPOS_NUMERICOS, tipos.TIPOS_TRUTHY

# Functions
tipos.promover_tipo(tipo1, tipo2) → str
tipos.para_booleano(valor, tipo) → bool
tipos.tipo_resultado_aritmetica(t1, t2, op) → str
tipos.tipo_resultado_comparacao(t1, t2) → str
tipos.tipo_resultado_logico(t1, t2) → str
tipos.tipo_compativel_armazenamento(tipo) → bool
tipos.tipo_compativel_condicao(tipo) → bool
```

### `tabela_simbolos.py`

```python
# Creation
tabela = TabelaSimbolos()
tabela = criar_tabela_simbolos()

# Operations
tabela.adicionar(nome, tipo, inicializada, linha) → SimboloInfo
tabela.buscar(nome) → SimboloInfo | None
tabela.existe(nome) → bool
tabela.verificar_inicializacao(nome) → bool
tabela.obter_tipo(nome) → str | None
tabela.registrar_uso(nome, linha) → bool
tabela.gerar_relatorio() → str
```

### `gramatica_atributos.py`

```python
# Initialization
gramatica = definir_gramatica_atributos()
gramatica, tabela = inicializar_sistema_semantico()

# Access
regra = gramatica['aritmetico']['+']
ops = listar_operadores_por_categoria()
regra = obter_regra('+', categoria='aritmetico')

# Rule properties
regra['categoria'], regra['operador'], regra['nome']
regra['aridade'], regra['tipos_operandos']
regra['tipo_resultado'], regra['acao_semantica']
regra['restricoes'], regra['descricao'], regra['regra_formal']
```

---

## Summary

### What You Have (Issue #1 ✅)

- **Complete type system** in `tipos.py`
- **Complete symbol table** in `tabela_simbolos.py`
- **22 semantic rules** in `gramatica_atributos.py`
- **32 passing unit tests**

### What to Build

- **Issue #2** (Aluno 2): Type checking using `tipos.py` + `gramatica_atributos.py`
- **Issue #3** (Aluno 3): Memory/control validation using `tabela_simbolos.py` + `tipos.py`
- **Issue #4** (Aluno 4): Integration in `compilar.py` + attributed AST generation
- **Issue #7** (Aluno 4): Output generators using all above modules

### Key Principles

1. **Always use Issue #1 modules** - don't reimplement!
2. **Post-order traversal** - analyze children before parents
3. **Check initialization** - before using variables (Issue #3)
4. **Validate storage** - boolean cannot be stored in MEM
5. **Collect all errors** - don't stop at first error
6. **Use semantic rules** - from `gramatica_atributos.py`

---

**Questions?** Check `src/RA3/demo_aluno1.py` for working examples!

**Good luck with RA3!** 🚀
