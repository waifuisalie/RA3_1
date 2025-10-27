# Issue #2 Implementation Guide: Type Checking and Semantic Analysis

**Issue:** Implement Type Checking and Semantic Analysis
**Assignee:** Aluno 2
**Status:** TODO
**Blocking:** Issues #3, #4

---

## Table of Contents

1. [Quick Summary](#quick-summary)
2. [What Issue #1 Already Provided](#what-issue-1-already-provided)
3. [What You Need to Build](#what-you-need-to-build)
4. [Three Modules to Create](#three-modules-to-create)
5. [Implementation Steps](#implementation-steps)
6. [Detailed Function Specifications](#detailed-function-specifications)
7. [Test Requirements](#test-requirements)
8. [Integration Points](#integration-points)
9. [Critical Considerations](#critical-considerations)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## Quick Summary

**The Goal:** Take syntax trees from RA2 and add type information to every node, while checking that all operations have type-safe operands.

**Why Two Things Are Different:**
- **Issue #1:** Defined the RULES (e.g., "division requires integers")
- **Issue #2:** Enforces the RULES (e.g., "check if the actual operands in the tree are integers")

**What You're Creating:**
Three Python modules that work together:
1. `gerador_erros.py` - Format and categorize errors
2. `verificador_tipos.py` - Validate each operator's type rules
3. `analisador_semantico.py` - Traverse the tree and apply validation

---

## What Issue #1 Already Provided

Your foundation is ready in `/src/RA3/functions/python/`:

### ✅ tipos.py (Complete)

**Type Constants:**
```python
TYPE_INT = 'int'
TYPE_REAL = 'real'
TYPE_BOOLEAN = 'boolean'
```

**Utility Sets:**
```python
TIPOS_VALIDOS = {'int', 'real', 'boolean'}
TIPOS_NUMERICOS = {'int', 'real'}
TIPOS_TRUTHY = {'int', 'real', 'boolean'}  # Can convert to boolean
```

**Key Functions Available:**
- `promover_tipo(tipo1, tipo2)` → Returns promoted type (int+real=real, int+int=int)
- `para_booleano(valor, tipo)` → Converts value to boolean using truthiness rules
- `tipos_compativeis_aritmetica(tipo1, tipo2)` → Check if compatible for +,-,*
- `tipos_compativeis_divisao_inteira(tipo1, tipo2)` → Check if both are int (strict!)
- `tipos_compativeis_potencia(tipo_base, tipo_exp)` → Check base/exponent rules
- `tipos_compativeis_comparacao(tipo1, tipo2)` → Check if both numeric
- `tipos_compativeis_logico(tipo1, tipo2)` → Check if both truthy-convertible

**How to Use:**
```python
from tipos import TYPE_INT, TYPE_REAL, promover_tipo, tipos_compativeis_divisao_inteira

# Use in your verificador_tipos.py
tipo_resultado = promover_tipo('int', 'real')  # Returns 'real'
if tipos_compativeis_divisao_inteira('int', 'real'):  # Returns False, division error!
    raise ErroSemantico(...)
```

### ✅ gramatica_atributos.py (Complete)

**22 Semantic Rules Defined:**
- Arithmetic (7): +, -, *, |, /, %, ^
- Comparison (6): >, <, >=, <=, ==, !=
- Logical (3): &&, ||, !
- Control (3): FOR, WHILE, IFELSE
- Memory (3): MEM_STORE, MEM_LOAD, RES

**Structure of Each Rule:**
```python
{
    'categoria': 'aritmetico',
    'operador': '+',
    'aridade': 2,
    'tipos_operandos': [TIPOS_NUMERICOS, TIPOS_NUMERICOS],
    'tipo_resultado': lambda op1, op2: promover_tipo(op1['tipo'], op2['tipo']),
    'restricoes': [
        'Ambos operandos devem ser numéricos',
        'Resultado promovido para real se qualquer operando é real'
    ],
    'acao_semantica': lambda op1, op2, tabela: {...}
}
```

**How to Use:**
```python
from gramatica_atributos import obter_regra

regra_soma = obter_regra('+')
tipos_aceitos = regra_soma['tipos_operandos']  # Get what types are allowed
tipo_saida = regra_soma['tipo_resultado']('int', 'real')  # Get result type
```

### ✅ tabela_simbolos.py (Complete with 32 Tests)

**Available Methods:**
- `adicionar(nome, tipo, inicializada, linha)` - Add variable
- `buscar(nome)` - Get variable info (returns SimboloInfo or None)
- `obter_tipo(nome)` - Get variable's type
- `verificar_inicializacao(nome)` - Check if initialized (raises error if not)
- `marcar_inicializada(nome, linha)` - Mark as initialized
- `existe(nome)` - Check if variable exists

**How to Use:**
```python
from tabela_simbolos import TabelaSimbolos

tabela = TabelaSimbolos()
tabela.adicionar('X', 'int', False, linha=1)
tabela.marcar_inicializada('X', linha=2)

tipo_var = tabela.obter_tipo('X')  # Returns 'int'
```

---

## What You Need to Build

You need to create **three new Python modules** in `/src/RA3/functions/python/`:

### 1. gerador_erros.py (Error Handling)
**Purpose:** Standardize error creation and formatting
**Size:** ~80-120 lines
**Dependencies:** None (no imports needed)

### 2. verificador_tipos.py (Type Validation)
**Purpose:** Check type rules for each operator
**Size:** ~200-300 lines
**Dependencies:** `tipos.py`, `gerador_erros.py`

### 3. analisador_semantico.py (AST Traversal)
**Purpose:** Walk the syntax tree and apply type checking
**Size:** ~250-400 lines
**Dependencies:** `tipos.py`, `verificador_tipos.py`, `gramatica_atributos.py`, `gerador_erros.py`, `tabela_simbolos.py`

---

## Three Modules to Create

### Module 1: gerador_erros.py

**Purpose:** Define error structure and formatting

**What It Contains:**

```python
# Error categories
CATEGORIA_TIPO = 'tipo'              # Type checking errors
CATEGORIA_MEMORIA = 'memoria'        # Initialization/memory errors
CATEGORIA_CONTROLE = 'controle'      # Control structure errors
CATEGORIA_OUTRO = 'outro'            # Other errors

class ErroSemantico(Exception):
    """Exception for semantic errors with line context"""

    def __init__(self, linha: int, descricao: str, contexto: str = None,
                 categoria: str = 'outro'):
        """
        Args:
            linha: Line number where error occurred
            descricao: Error description (what went wrong)
            contexto: Code snippet context (the actual code line)
            categoria: Error type (tipo, memoria, controle, outro)
        """
        self.linha = linha
        self.descricao = descricao
        self.contexto = contexto
        self.categoria = categoria

    def __str__(self) -> str:
        """Format as specified: ERRO SEMÂNTICO [Linha X]: ..."""
        msg = f"ERRO SEMÂNTICO [Linha {self.linha}]: {self.descricao}"
        if self.contexto:
            msg += f"\nContexto: {self.contexto}"
        return msg
```

**Key Functions:**

```python
def formatar_erro_tipo(linha: int, operador: str, tipo_esq: str,
                       tipo_dir: str, contexto: str) -> str:
    """
    Format a type compatibility error

    Example output:
    ERRO SEMÂNTICO [Linha 5]: Divisão inteira requer operandos inteiros,
    mas encontrado 'real' e 'int'
    Contexto: (5.5 2 /)
    """
    descricao = f"Operador '{operador}' requer tipos específicos, " \
                f"mas encontrado '{tipo_esq}' e '{tipo_dir}'"
    return formatar_erro(linha, descricao, contexto)

def formatar_erro(linha: int, descricao: str, contexto: str = None) -> str:
    """Generic error formatter"""
    msg = f"ERRO SEMÂNTICO [Linha {linha}]: {descricao}"
    if contexto:
        msg += f"\nContexto: {contexto}"
    return msg
```

**Testing Strategy:**
```python
def test_erro_semantico_formato():
    erro = ErroSemantico(5, "Divisão com real", "(5.5 2 /)", CATEGORIA_TIPO)
    assert "ERRO SEMÂNTICO [Linha 5]" in str(erro)
    assert "Contexto: (5.5 2 /)" in str(erro)
```

---

### Module 2: verificador_tipos.py

**Purpose:** Validate type rules for each operator category

**Key Concept:** Each operator has specific type requirements. Your job is to check them.

**What It Contains:**

```python
from tipos import TYPE_INT, TYPE_REAL, TYPE_BOOLEAN, TIPOS_NUMERICOS
from tipos import promover_tipo, tipos_compativeis_divisao_inteira
from gerador_erros import ErroSemantico, CATEGORIA_TIPO

# ============================================================================
# VERIFICADORES POR CATEGORIA DE OPERADOR
# ============================================================================

def verificar_aritmetica(tipo_esq: str, tipo_dir: str, operador: str,
                         linha: int, contexto: str = None) -> str:
    """
    Verify arithmetic operators: +, -, *, |

    Rules:
    - Both operands must be numeric (int or real)
    - Result type is promoted: int+real=real, int+int=int, real+real=real

    Args:
        tipo_esq: Type of left operand
        tipo_dir: Type of right operand
        operador: The operator symbol (+, -, *, |)
        linha: Line number for error reporting
        contexto: Code snippet for error context

    Returns:
        Result type (int or real)

    Raises:
        ErroSemantico: If operands not numeric

    Example:
        >>> verificar_aritmetica('int', 'real', '+', 5, "(3 2.5 +)")
        'real'  # int + real = real
        >>> verificar_aritmetica('boolean', 'int', '+', 5)
        ErroSemantico: boolean não é tipo numérico
    """
    # Step 1: Check both are numeric
    if tipo_esq not in TIPOS_NUMERICOS or tipo_dir not in TIPOS_NUMERICOS:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer operandos numéricos, "
                     f"mas encontrado '{tipo_esq}' e '{tipo_dir}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    # Step 2: Promote and return result type
    return promover_tipo(tipo_esq, tipo_dir)


def verificar_divisao_inteira(tipo_esq: str, tipo_dir: str,
                              operador: str, linha: int,
                              contexto: str = None) -> str:
    """
    Verify integer-only operators: /, %

    STRICT RULE: Both operands must be EXACTLY int, no promotion!

    Rules:
    - Left operand must be int
    - Right operand must be int
    - NO floating-point allowed
    - Result is always int

    Args:
        tipo_esq: Type of left operand
        tipo_dir: Type of right operand
        operador: The operator (/ or %)
        linha: Line number
        contexto: Code snippet

    Returns:
        'int'

    Raises:
        ErroSemantico: If any operand is not int

    Example:
        >>> verificar_divisao_inteira('int', 'int', '/', 5, "(10 2 /)")
        'int'
        >>> verificar_divisao_inteira('real', 'int', '/', 5, "(5.5 2 /)")
        ErroSemantico: Divisão inteira requer operandos inteiros

    NOTE: This is DIFFERENT from arithmetic operators!
    - (5 3 +) with int/int → int (promotion applies)
    - (5.5 2 +) with real/int → real (promotion applies)
    - (5.5 2 /) with real/int → ERROR! (no promotion allowed)
    """
    # Step 1: Use the utility function from tipos.py
    if not tipos_compativeis_divisao_inteira(tipo_esq, tipo_dir):
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer operandos inteiros, "
                     f"mas encontrado '{tipo_esq}' e '{tipo_dir}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    return TYPE_INT


def verificar_potencia(tipo_base: str, tipo_exp: str, linha: int,
                       contexto: str = None) -> str:
    """
    Verify power operator: ^

    Rules:
    - Base can be int or real (numeric)
    - Exponent MUST be exactly int
    - Exponent should be positive (semantic check later, type check now)
    - Result type matches base type

    Args:
        tipo_base: Type of base (left operand)
        tipo_exp: Type of exponent (right operand)
        linha: Line number
        contexto: Code snippet

    Returns:
        Type matching base (int if base is int, real if base is real)

    Raises:
        ErroSemantico: If base not numeric OR exponent not int

    Example:
        >>> verificar_potencia('int', 'int', 5, "(2 3 ^)")
        'int'  # 2^3 = 8
        >>> verificar_potencia('real', 'int', 5, "(2.5 3 ^)")
        'real'  # 2.5^3 = 15.625
        >>> verificar_potencia('real', 'real', 5, "(2.0 3.5 ^)")
        ErroSemantico: Expoente deve ser inteiro

    KEY INSIGHT: Unlike +,-,* where int+real→real, here:
    - Base type conversion: int can be promoted to real IF written as real
    - Exponent type: MUST be int (no exceptions!)
    """
    # Step 1: Check base is numeric
    if tipo_base not in TIPOS_NUMERICOS:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Base da potência deve ser numérica, "
                     f"mas encontrado '{tipo_base}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    # Step 2: Check exponent is exactly int (STRICT!)
    if tipo_exp != TYPE_INT:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Expoente da potência deve ser inteiro, "
                     f"mas encontrado '{tipo_exp}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    # Step 3: Return type matching base
    return tipo_base


def verificar_comparacao(tipo_esq: str, tipo_dir: str, operador: str,
                         linha: int, contexto: str = None) -> str:
    """
    Verify comparison operators: >, <, >=, <=, ==, !=

    Rules:
    - Both operands must be numeric (int or real)
    - Both can be mixed (int + real is OK)
    - Result is ALWAYS boolean

    Args:
        tipo_esq: Type of left operand
        tipo_dir: Type of right operand
        operador: The comparison operator
        linha: Line number
        contexto: Code snippet

    Returns:
        TYPE_BOOLEAN (always!)

    Raises:
        ErroSemantico: If operands not numeric

    Example:
        >>> verificar_comparacao('int', 'int', '>', 5, "(5 3 >)")
        'boolean'  # 5 > 3 is true
        >>> verificar_comparacao('real', 'int', '>', 5, "(5.5 3 >)")
        'boolean'  # 5.5 > 3 is true
        >>> verificar_comparacao('boolean', 'int', '>', 5)
        ErroSemantico: Comparação requer operandos numéricos
    """
    # Step 1: Check both are numeric
    if tipo_esq not in TIPOS_NUMERICOS or tipo_dir not in TIPOS_NUMERICOS:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer operandos numéricos, "
                     f"mas encontrado '{tipo_esq}' e '{tipo_dir}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    # Step 2: Always return boolean
    return TYPE_BOOLEAN


def verificar_logico_binario(tipo_esq: str, tipo_dir: str, operador: str,
                             linha: int, contexto: str = None) -> str:
    """
    Verify binary logical operators: &&, ||

    PERMISSIVE MODE (Truthiness):
    - Accepts int, real, or boolean
    - Converts numeric to boolean: 0/0.0=false, else=true
    - Result is ALWAYS boolean

    Args:
        tipo_esq: Type of left operand (int, real, or boolean)
        tipo_dir: Type of right operand (int, real, or boolean)
        operador: The operator (&& or ||)
        linha: Line number
        contexto: Code snippet

    Returns:
        TYPE_BOOLEAN

    Raises:
        ErroSemantico: If operands not truthy-convertible

    Example:
        >>> verificar_logico_binario('int', 'int', '&&', 5, "(5 3 &&)")
        'boolean'  # true && true
        >>> verificar_logico_binario('boolean', 'int', '||', 5, "(true 0 ||)")
        'boolean'  # true || false
        >>> verificar_logico_binario('boolean', 'boolean', '||', 5)
        'boolean'

    IMPORTANT: This is "permissive mode" - int/real are accepted and converted!
    """
    from tipos import TIPOS_TRUTHY

    # Step 1: Check both can be converted to boolean
    if tipo_esq not in TIPOS_TRUTHY or tipo_dir not in TIPOS_TRUTHY:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '{operador}' requer operandos convertíveis a boolean, "
                     f"mas encontrado '{tipo_esq}' e '{tipo_dir}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    # Step 2: Always return boolean
    return TYPE_BOOLEAN


def verificar_logico_unario(tipo_operando: str, linha: int,
                            contexto: str = None) -> str:
    """
    Verify unary logical operator: ! (NOT)

    Postfix notation: (A !)

    PERMISSIVE MODE (Truthiness):
    - Accepts int, real, or boolean
    - Converts numeric to boolean
    - Result is ALWAYS boolean

    Args:
        tipo_operando: Type of operand
        linha: Line number
        contexto: Code snippet

    Returns:
        TYPE_BOOLEAN

    Raises:
        ErroSemantico: If operand not truthy-convertible

    Example:
        >>> verificar_logico_unario('boolean', 5, "(true !)")
        'boolean'  # !true = false
        >>> verificar_logico_unario('int', 5, "(5 !)")
        'boolean'  # !5 = !true = false
        >>> verificar_logico_unario('real', 5, "(0.0 !)")
        'boolean'  # !0.0 = !false = true
    """
    from tipos import TIPOS_TRUTHY

    if tipo_operando not in TIPOS_TRUTHY:
        raise ErroSemantico(
            linha=linha,
            descricao=f"Operador '!' requer operando convertível a boolean, "
                     f"mas encontrado '{tipo_operando}'",
            contexto=contexto,
            categoria=CATEGORIA_TIPO
        )

    return TYPE_BOOLEAN


def verificar_controle_for(tipo_init: str, tipo_end: str, tipo_step: str,
                           tipo_corpo: str, linha: int,
                           contexto: str = None) -> str:
    """
    Verify FOR loop structure

    Syntax: (init end step body FOR)

    Rules:
    - init must be int
    - end must be int
    - step must be int
    - body can be any type (result type is body type)

    Args:
        tipo_init: Type of init expression
        tipo_end: Type of end expression
        tipo_step: Type of step expression
        tipo_corpo: Type of loop body (all expressions in it)
        linha: Line number
        contexto: Code snippet

    Returns:
        Type of body (same as tipo_corpo)

    Raises:
        ErroSemantico: If init, end, or step not int

    Example:
        >>> verificar_controle_for('int', 'int', 'int', 'int', 5,
        ...                         "((1 10 1 body) FOR)")
        'int'
        >>> verificar_controle_for('real', 'int', 'int', 'int', 5)
        ErroSemantico: FOR requer init, end, step inteiros
    """
    # Step 1: Check all three are int
    if tipo_init != TYPE_INT:
        raise ErroSemantico(
            linha=linha,
            descricao=f"FOR: init deve ser inteiro, mas encontrado '{tipo_init}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    if tipo_end != TYPE_INT:
        raise ErroSemantico(
            linha=linha,
            descricao=f"FOR: end deve ser inteiro, mas encontrado '{tipo_end}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    if tipo_step != TYPE_INT:
        raise ErroSemantico(
            linha=linha,
            descricao=f"FOR: step deve ser inteiro, mas encontrado '{tipo_step}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    # Step 2: Return body type
    return tipo_corpo


def verificar_controle_while(tipo_condicao: str, tipo_corpo: str, linha: int,
                             contexto: str = None) -> str:
    """
    Verify WHILE loop structure

    Syntax: (condition body WHILE)

    Rules:
    - condition converted to boolean (permissive mode)
    - body can be any type (result type is body type)

    Args:
        tipo_condicao: Type of condition expression
        tipo_corpo: Type of loop body
        linha: Line number
        contexto: Code snippet

    Returns:
        Type of body

    Raises:
        ErroSemantico: If condition not truthy-convertible

    Example:
        >>> verificar_controle_while('int', 'real', 5, "((x 10 <) body WHILE)")
        'real'  # Condition is truthy, body is real
    """
    from tipos import TIPOS_TRUTHY

    if tipo_condicao not in TIPOS_TRUTHY:
        raise ErroSemantico(
            linha=linha,
            descricao=f"WHILE: condição deve ser convertível a boolean, "
                     f"mas encontrado '{tipo_condicao}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    return tipo_corpo


def verificar_controle_ifelse(tipo_condicao: str, tipo_true: str,
                              tipo_false: str, linha: int,
                              contexto: str = None) -> str:
    """
    Verify IFELSE conditional structure

    Syntax: (condition true_branch false_branch IFELSE)

    Rules:
    - condition converted to boolean (permissive mode)
    - CRITICAL: true_branch and false_branch MUST be same type!
    - result type is the branch type

    Args:
        tipo_condicao: Type of condition
        tipo_true: Type of true branch
        tipo_false: Type of false branch
        linha: Line number
        contexto: Code snippet

    Returns:
        Type of both branches (same type)

    Raises:
        ErroSemantico: If condition not truthy OR branches different types

    Example:
        >>> verificar_controle_ifelse('boolean', 'int', 'int', 5,
        ...                            "((x 5 >) 10 20 IFELSE)")
        'int'  # Both branches are int
        >>> verificar_controle_ifelse('boolean', 'int', 'real', 5)
        ErroSemantico: IFELSE: ramos devem ter mesmo tipo

    CRITICAL POINT: This is THE MOST IMPORTANT TYPE RULE!
    The branches MUST match exactly:
    - (true 5 10.0 IFELSE) → ERROR (int vs real)
    - (true 5 3 IFELSE) → OK (both int)
    - (true 5.0 2.5 IFELSE) → OK (both real)
    """
    from tipos import TIPOS_TRUTHY

    # Step 1: Check condition is truthy-convertible
    if tipo_condicao not in TIPOS_TRUTHY:
        raise ErroSemantico(
            linha=linha,
            descricao=f"IFELSE: condição deve ser convertível a boolean, "
                     f"mas encontrado '{tipo_condicao}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    # Step 2: Check both branches are SAME type
    if tipo_true != tipo_false:
        raise ErroSemantico(
            linha=linha,
            descricao=f"IFELSE: ambos ramos devem ter mesmo tipo, "
                     f"mas encontrado '{tipo_true}' e '{tipo_false}'",
            contexto=contexto,
            categoria=CATEGORIA_CONTROLE
        )

    # Step 3: Return branch type
    return tipo_true
```

**Key Principles for verificador_tipos.py:**

1. **One function per operator category** - Keep them separate for clarity
2. **Always raise ErroSemantico** - Don't return None or False, throw an exception
3. **Always include context** - Pass the code snippet for debugging
4. **Always return a type** - Or raise an exception (no None returns)
5. **Use utility functions from tipos.py** - Don't reimplement validation logic

---

### Module 3: analisador_semantico.py

**Purpose:** Traverse the syntax tree and apply type checking

**Core Concept:** Post-order traversal means you process children first, then the parent.

```python
from typing import Tuple, List, Dict, Any, Optional
import json

from tipos import TYPE_INT, TYPE_REAL, TYPE_BOOLEAN
from verificador_tipos import (
    verificar_aritmetica, verificar_divisao_inteira, verificar_potencia,
    verificar_comparacao, verificar_logico_binario, verificar_logico_unario,
    verificar_controle_for, verificar_controle_while, verificar_controle_ifelse
)
from gramatica_atributos import obter_regra
from gerador_erros import ErroSemantico, CATEGORIA_TIPO
from tabela_simbolos import TabelaSimbolos

# ============================================================================
# ESTRUTURA DE NÓ ANOTADO
# ============================================================================

class NoAnotado:
    """
    Represents an AST node with type annotation

    Original node from RA2:
        {
            "label": "SEQUENCIA",
            "filhos": [...]
        }

    After annotation:
        {
            "label": "SEQUENCIA",
            "tipo": "int",        # ← ADDED by semantic analyzer
            "filhos": [...],
            "linha": 5,           # ← Line number for error reporting
            "contexto": "(5 3 +)" # ← Original code snippet
        }
    """
    def __init__(self, label: str, filhos: List = None, tipo: str = None,
                 linha: int = None, contexto: str = None):
        self.label = label
        self.filhos = filhos or []
        self.tipo = tipo
        self.linha = linha
        self.contexto = contexto

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'label': self.label,
            'tipo': self.tipo,
            'filhos': [f.to_dict() for f in self.filhos],
            'linha': self.linha,
            'contexto': self.contexto
        }


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def inferir_tipo_literal(valor: str) -> str:
    """
    Distinguish between int and real literals

    Rules:
    - Contains '.' → real (5.0, 3.14, 0.0)
    - No '.' → int (5, 42, -3)
    - Must parse successfully to number

    Args:
        valor: String representation of literal

    Returns:
        TYPE_INT or TYPE_REAL

    Raises:
        ValueError: If not a valid number

    Example:
        >>> inferir_tipo_literal("5")
        'int'
        >>> inferir_tipo_literal("5.0")
        'real'
        >>> inferir_tipo_literal("3.14")
        'real'
        >>> inferir_tipo_literal("abc")
        ValueError: not a valid number
    """
    valor = valor.strip()

    # Try to parse as float
    try:
        num = float(valor)
    except ValueError:
        raise ValueError(f"'{valor}' não é um literal válido")

    # If contains decimal point, it's real
    if '.' in valor:
        return TYPE_REAL

    # Otherwise it's int
    return TYPE_INT


def extrair_contexto(no: Dict[str, Any]) -> str:
    """
    Extract original code snippet from node

    Walk up to find the expression_original or tokens field

    Returns string representation of the expression
    """
    # If available, use tokens to reconstruct
    if 'tokens' in no:
        return ' '.join(no['tokens'])

    # Otherwise use expression_original
    if 'expressao_original' in no:
        return no['expressao_original']

    # Fallback
    return f"({no.get('label', '?')})"


def obter_numero_linha(no: Dict[str, Any]) -> int:
    """Extract line number from node"""
    return no.get('numero_linha', no.get('linha', 0))


# ============================================================================
# ANÁLISE SEMÂNTICA - TRAVERSAL
# ============================================================================

def analisar_no(no_dict: Dict[str, Any], tabela_simbolos: TabelaSimbolos,
                numero_linha: int = 0) -> NoAnotado:
    """
    Analyze a single AST node and assign type (POST-ORDER TRAVERSAL)

    Algorithm:
    1. Recursively analyze all children first
    2. Determine type based on node label and children types
    3. Apply semantic rules for operators
    4. Return annotated node

    Args:
        no_dict: AST node from RA2 (dictionary with 'label' and 'filhos')
        tabela_simbolos: Symbol table for variable lookup
        numero_linha: Line number for error reporting

    Returns:
        NoAnotado: Annotated node with 'tipo' field populated

    Raises:
        ErroSemantico: If type checking fails

    Example:
        Input RA2 node:
        {
            "label": "SEQUENCIA",
            "filhos": [
                {"label": "5", "filhos": []},
                {"label": "+", "filhos": []},
                {"label": "3", "filhos": []}
            ]
        }

        Output:
        NoAnotado(
            label="SEQUENCIA",
            tipo="int",
            filhos=[...],
            contexto="(5 3 +)",
            linha=1
        )
    """

    # Extract metadata
    label = no_dict.get('label', '')
    filhos_dict = no_dict.get('filhos', [])
    contexto = extrair_contexto(no_dict)
    numero_linha = obter_numero_linha(no_dict) or numero_linha

    # ========================================================================
    # STEP 1: RECURSIVE CASE - Process children first (POST-ORDER)
    # ========================================================================

    filhos_anotados = []
    tipos_filhos = []

    for filho_dict in filhos_dict:
        filho_anotado = analisar_no(filho_dict, tabela_simbolos, numero_linha)
        filhos_anotados.append(filho_anotado)
        if filho_anotado.tipo:
            tipos_filhos.append(filho_anotado.tipo)

    # ========================================================================
    # STEP 2: DETERMINE TYPE OF CURRENT NODE
    # ========================================================================

    tipo_node = None

    # CASE 1: Literal number (terminal)
    # Label is a number like "5" or "3.14"
    if label not in ['(', ')', '+', '-', '*', '/', '%', '^', '|',
                     '>', '<', '>=', '<=', '==', '!=', '&&', '||', '!',
                     'for', 'while', 'ifelse', 'PROGRAM', 'LINHA', 'SEQUENCIA',
                     'OPERANDO', 'OPERADOR_FINAL', 'ARITH_OP', 'COMP_OP', 'LOGIC_OP']:
        # It's likely a literal
        try:
            tipo_node = inferir_tipo_literal(label)
        except ValueError:
            # Not a number, might be a variable reference
            tipo_node = None

    # CASE 2: Variable reference
    # Variable is used as operand (not assignment)
    if label.isupper() and label not in ['PROGRAM', 'LINHA', 'SEQUENCIA',
                                         'OPERANDO', 'OPERADOR_FINAL']:
        if tabela_simbolos.existe(label):
            tipo_node = tabela_simbolos.obter_tipo(label)
        else:
            # Variable not defined yet (will be caught by Issue #3)
            tipo_node = None

    # CASE 3: Operators
    # Determine type from operator and child types

    # Arithmetic operators: +, -, *
    if label == '+':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_aritmetica(tipos_filhos[0], tipos_filhos[1],
                                            '+', numero_linha, contexto)

    elif label == '-':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_aritmetica(tipos_filhos[0], tipos_filhos[1],
                                            '-', numero_linha, contexto)

    elif label == '*':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_aritmetica(tipos_filhos[0], tipos_filhos[1],
                                            '*', numero_linha, contexto)

    # Real division: |
    elif label == '|':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_aritmetica(tipos_filhos[0], tipos_filhos[1],
                                            '|', numero_linha, contexto)

    # Integer division: /
    elif label == '/':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_divisao_inteira(tipos_filhos[0], tipos_filhos[1],
                                                 '/', numero_linha, contexto)

    # Modulo: %
    elif label == '%':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_divisao_inteira(tipos_filhos[0], tipos_filhos[1],
                                                 '%', numero_linha, contexto)

    # Power: ^
    elif label == '^':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_potencia(tipos_filhos[0], tipos_filhos[1],
                                          numero_linha, contexto)

    # Comparison operators
    elif label in ['>', '<', '>=', '<=', '==', '!=']:
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_comparacao(tipos_filhos[0], tipos_filhos[1],
                                            label, numero_linha, contexto)

    # Logical AND: &&
    elif label == '&&':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_logico_binario(tipos_filhos[0], tipos_filhos[1],
                                               '&&', numero_linha, contexto)

    # Logical OR: ||
    elif label == '||':
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_logico_binario(tipos_filhos[0], tipos_filhos[1],
                                               '||', numero_linha, contexto)

    # Logical NOT: ! (unary)
    elif label == '!':
        if len(tipos_filhos) >= 1:
            tipo_node = verificar_logico_unario(tipos_filhos[0],
                                               numero_linha, contexto)

    # Control structures
    elif label == 'for':
        # FOR: (init end step body FOR)
        # Children order: init, end, step, body
        if len(tipos_filhos) >= 4:
            tipo_node = verificar_controle_for(
                tipos_filhos[0], tipos_filhos[1], tipos_filhos[2], tipos_filhos[3],
                numero_linha, contexto
            )

    elif label == 'while':
        # WHILE: (condition body WHILE)
        # Children: condition, body
        if len(tipos_filhos) >= 2:
            tipo_node = verificar_controle_while(
                tipos_filhos[0], tipos_filhos[1],
                numero_linha, contexto
            )

    elif label == 'ifelse':
        # IFELSE: (condition true_branch false_branch IFELSE)
        # Children: condition, true_branch, false_branch
        if len(tipos_filhos) >= 3:
            tipo_node = verificar_controle_ifelse(
                tipos_filhos[0], tipos_filhos[1], tipos_filhos[2],
                numero_linha, contexto
            )

    # CASE 4: Non-terminal symbols (pass through or inherit from children)
    # Grammar non-terminals: PROGRAM, LINHA, SEQUENCIA, OPERANDO, etc.
    # These don't have a type themselves; inherit from children
    elif label in ['PROGRAM', 'PROGRAM_PRIME', 'LINHA', 'SEQUENCIA',
                   'SEQUENCIA_PRIME', 'OPERANDO', 'OPERANDO_VAR_OPCIONAL',
                   'OPERADOR_FINAL', 'ARITH_OP', 'COMP_OP', 'LOGIC_OP',
                   'CONTROL_OP']:
        # Inherit type from last child or first typed child
        if tipos_filhos:
            tipo_node = tipos_filhos[-1]  # Use last child's type

    # ========================================================================
    # STEP 3: CREATE ANNOTATED NODE
    # ========================================================================

    no_anotado = NoAnotado(
        label=label,
        filhos=filhos_anotados,
        tipo=tipo_node,
        linha=numero_linha,
        contexto=contexto
    )

    return no_anotado


def analisarSemantica(arvore_sintatica: Dict[str, Any],
                      tabela_simbolos: TabelaSimbolos = None) -> Tuple[Dict[str, Any], List[str]]:
    """
    Main semantic analysis function - ENTRY POINT

    Orchestrates the analysis of entire syntax tree

    Args:
        arvore_sintatica: Complete AST from RA2 (from arvore_sintatica.json)
        tabela_simbolos: Optional symbol table (creates new if not provided)

    Returns:
        Tuple of:
        - arvore_anotada: Type-annotated syntax tree (dictionary form)
        - erros: List of error messages (strings)

    Example:
        from analisador_semantico import analisarSemantica
        from tabela_simbolos import TabelaSimbolos

        arvore = json.load(open('outputs/RA2/arvore_sintatica.json'))
        tabela = TabelaSimbolos()
        arvore_anotada, erros = analisarSemantica(arvore, tabela)

        if erros:
            print("Erros encontrados:")
            for erro in erros:
                print(erro)
        else:
            print("Análise bem-sucedida!")
            json.dump(arvore_anotada, open('outputs/RA3/arvore_anotada.json', 'w'))
    """

    if tabela_simbolos is None:
        tabela_simbolos = TabelaSimbolos()

    erros = []
    arvore_anotada = None

    try:
        # Analyze the entire tree
        arvore_anotada = analisar_no(arvore_sintatica, tabela_simbolos).to_dict()

    except ErroSemantico as e:
        erros.append(str(e))

    except Exception as e:
        # Catch unexpected errors
        erros.append(f"ERRO SEMÂNTICO: {str(e)}")

    return arvore_anotada, erros


# ============================================================================
# UTILITY FUNCTIONS FOR TESTING AND DEBUGGING
# ============================================================================

def imprimir_arvore_anotada(no: NoAnotado, indent: int = 0) -> None:
    """Pretty-print the annotated tree for debugging"""
    prefix = "  " * indent
    tipo_str = f" : {no.tipo}" if no.tipo else ""
    print(f"{prefix}{no.label}{tipo_str}")
    for filho in no.filhos:
        imprimir_arvore_anotada(filho, indent + 1)
```

**Key Principles for analisador_semantico.py:**

1. **Post-order traversal** - Process children before parent
2. **Distinguish literals from variables** - Use `inferir_tipo_literal()` to tell int from real
3. **Inherit types through grammar** - Non-terminals inherit from children
4. **Propagate errors** - Catch ErroSemantico and collect them
5. **Track line numbers** - Always maintain context for error reporting

---

## Implementation Steps

### Phase 1: Foundation (gerador_erros.py)

**Difficulty:** Easy
**Time:** 30-60 minutes

1. Create file `/src/RA3/functions/python/gerador_erros.py`
2. Define error categories
3. Implement `ErroSemantico` class
4. Test by creating and printing an error

**Checklist:**
- [ ] File created
- [ ] `ErroSemantico` class has `__init__` and `__str__`
- [ ] Error formats match specification exactly
- [ ] Can create error and print it

---

### Phase 2: Type Validation (verificador_tipos.py)

**Difficulty:** Medium
**Time:** 2-4 hours

1. Create file `/src/RA3/functions/python/verificador_tipos.py`
2. Import from `tipos.py` and `gerador_erros.py`
3. Implement one function at a time:
   - Start with `verificar_aritmetica()` (simplest)
   - Then `verificar_divisao_inteira()` (strict rules)
   - Then `verificar_potencia()` (base/exponent rules)
   - Then comparisons and logical operators
   - Finally control structures

4. Test each function individually

**Checklist:**
- [ ] All 11 verification functions created
- [ ] Each function validates its rules correctly
- [ ] Each function raises `ErroSemantico` on failure
- [ ] All functions accept `contexto` parameter
- [ ] Unit tests pass for each function

---

### Phase 3: AST Traversal (analisador_semantico.py)

**Difficulty:** Hard
**Time:** 4-6 hours

1. Create file `/src/RA3/functions/python/analisador_semantico.py`
2. Import all dependencies
3. Create `NoAnotado` class
4. Implement helper functions:
   - `inferir_tipo_literal()` - Distinguish int from real
   - `extrair_contexto()` - Get code snippet
   - `obter_numero_linha()` - Get line number

5. Implement `analisar_no()` recursive function carefully
6. Implement main `analisarSemantica()` entry point
7. Test with real AST from RA2

**Checklist:**
- [ ] `NoAnotado` class complete
- [ ] Helper functions working
- [ ] `analisar_no()` handles all 30+ node types
- [ ] Post-order traversal correct
- [ ] Error collection working
- [ ] Returns correct tuple `(arvore_anotada, erros)`

---

### Phase 4: Testing (test_verificador_tipos.py)

**Difficulty:** Medium
**Time:** 2-3 hours

1. Create `/tests/RA3/test_verificador_tipos.py`
2. Write tests for each operator category
3. Include both valid and invalid cases
4. Test error messages match format

**Checklist:**
- [ ] Tests for all 11 verification functions
- [ ] Valid cases pass
- [ ] Invalid cases raise correct errors
- [ ] Error messages follow format
- [ ] All 20+ tests pass

---

### Phase 5: Integration and Output

**Difficulty:** Easy
**Time:** 1-2 hours

1. Call from `compilar.py` after RA2 parsing
2. Save annotated tree to `outputs/RA3/arvore_anotada.json`
3. Save errors to `outputs/RA3/erros_semanticos.md`
4. Test with all input files

**Checklist:**
- [ ] Integration with `compilar.py` complete
- [ ] Output files generated correctly
- [ ] All test inputs processed
- [ ] No crashes or unexpected errors

---

## Detailed Function Specifications

See **Module 2: verificador_tipos.py** section above for complete specifications of all 11 functions with:
- Purpose and algorithm
- Type rules explained
- Example invocations
- Expected outputs and errors

---

## Test Requirements

### Test File: tests/RA3/test_verificador_tipos.py

Must include tests for:

```python
import unittest
from src.RA3.functions.python.verificador_tipos import *
from src.RA3.functions.python.gerador_erros import ErroSemantico, CATEGORIA_TIPO

class TestVerificadorTipos(unittest.TestCase):

    # ====== ARITHMETIC TESTS ======

    def test_aritmetica_int_int_soma(self):
        """(5 3 +) → int"""
        resultado = verificar_aritmetica('int', 'int', '+', 1, "(5 3 +)")
        self.assertEqual(resultado, 'int')

    def test_aritmetica_int_real_soma(self):
        """(5 3.5 +) → real (promotion)"""
        resultado = verificar_aritmetica('int', 'real', '+', 1, "(5 3.5 +)")
        self.assertEqual(resultado, 'real')

    def test_aritmetica_boolean_error(self):
        """(true 3 +) → ERROR"""
        with self.assertRaises(ErroSemantico):
            verificar_aritmetica('boolean', 'int', '+', 1, "(true 3 +)")

    # ====== INTEGER DIVISION TESTS ======

    def test_divisao_inteira_int_int(self):
        """(10 2 /) → int"""
        resultado = verificar_divisao_inteira('int', 'int', '/', 1, "(10 2 /)")
        self.assertEqual(resultado, 'int')

    def test_divisao_inteira_real_error(self):
        """(5.5 2 /) → ERROR (no promotion!)"""
        with self.assertRaises(ErroSemantico):
            verificar_divisao_inteira('real', 'int', '/', 1, "(5.5 2 /)")

    def test_modulo_int_int(self):
        """(10 3 %) → int"""
        resultado = verificar_divisao_inteira('int', 'int', '%', 1, "(10 3 %)")
        self.assertEqual(resultado, 'int')

    # ====== POWER TESTS ======

    def test_potencia_int_int(self):
        """(2 3 ^) → int"""
        resultado = verificar_potencia('int', 'int', 1, "(2 3 ^)")
        self.assertEqual(resultado, 'int')

    def test_potencia_real_int(self):
        """(2.5 3 ^) → real"""
        resultado = verificar_potencia('real', 'int', 1, "(2.5 3 ^)")
        self.assertEqual(resultado, 'real')

    def test_potencia_real_exponent_error(self):
        """(2 3.5 ^) → ERROR (exponent must be int)"""
        with self.assertRaises(ErroSemantico):
            verificar_potencia('int', 'real', 1, "(2 3.5 ^)")

    # ====== COMPARISON TESTS ======

    def test_comparacao_int_int(self):
        """(5 3 >) → boolean"""
        resultado = verificar_comparacao('int', 'int', '>', 1, "(5 3 >)")
        self.assertEqual(resultado, 'boolean')

    def test_comparacao_real_int(self):
        """(5.5 3 >) → boolean"""
        resultado = verificar_comparacao('real', 'int', '>', 1, "(5.5 3 >)")
        self.assertEqual(resultado, 'boolean')

    def test_comparacao_boolean_error(self):
        """(true false >) → ERROR"""
        with self.assertRaises(ErroSemantico):
            verificar_comparacao('boolean', 'boolean', '>', 1)

    # ====== LOGICAL TESTS ======

    def test_logico_binario_int_int(self):
        """(5 3 &&) → boolean (permissive mode)"""
        resultado = verificar_logico_binario('int', 'int', '&&', 1, "(5 3 &&)")
        self.assertEqual(resultado, 'boolean')

    def test_logico_binario_boolean_int(self):
        """(true 0 ||) → boolean (mixed permissive)"""
        resultado = verificar_logico_binario('boolean', 'int', '||', 1, "(true 0 ||)")
        self.assertEqual(resultado, 'boolean')

    def test_logico_unario_int(self):
        """(5 !) → boolean"""
        resultado = verificar_logico_unario('int', 1, "(5 !)")
        self.assertEqual(resultado, 'boolean')

    # ====== CONTROL STRUCTURE TESTS ======

    def test_for_all_int(self):
        """FOR with int parameters"""
        resultado = verificar_controle_for('int', 'int', 'int', 'int', 1)
        self.assertEqual(resultado, 'int')

    def test_for_real_init_error(self):
        """FOR with real init → ERROR"""
        with self.assertRaises(ErroSemantico):
            verificar_controle_for('real', 'int', 'int', 'int', 1)

    def test_while_int_condition(self):
        """WHILE with int condition (permissive)"""
        resultado = verificar_controle_while('int', 'real', 1)
        self.assertEqual(resultado, 'real')

    def test_ifelse_same_types(self):
        """IFELSE with matching branch types"""
        resultado = verificar_controle_ifelse('boolean', 'int', 'int', 1)
        self.assertEqual(resultado, 'int')

    def test_ifelse_different_types_error(self):
        """IFELSE with different branch types → ERROR"""
        with self.assertRaises(ErroSemantico):
            verificar_controle_ifelse('boolean', 'int', 'real', 1)


if __name__ == '__main__':
    unittest.main()
```

---

## Integration Points

### How It Fits Into The Pipeline

```
1. compilar.py calls Phase 1 (Tokenization - RA1)
   ↓
2. compilar.py calls Phase 2 (Parsing - RA2)
   Outputs: outputs/RA2/arvore_sintatica.json
   ↓
3. [NEW] compilar.py calls Phase 3 (Semantic Analysis - Issue #2)
   Input: outputs/RA2/arvore_sintatica.json
   ↓
   analisarSemantica()
     ├─ analisar_no() [recursive]
     │  ├─ inferir_tipo_literal()
     │  ├─ verificar_aritmetica()
     │  ├─ verificar_divisao_inteira()
     │  └─ (other verificador_tipos functions)
     └─ Returns: (arvore_anotada, erros)
   ↓
   Output: outputs/RA3/arvore_anotada.json
   Output: outputs/RA3/erros_semanticos.md
   ↓
4. compilar.py calls Phase 4 (Memory Validation - Issue #3)
   Uses: arvore_anotada from Issue #2
   ↓
5. compilar.py calls Phase 5 (AST Generation - Issue #4)
   Uses: arvore_anotada from Issue #2
```

### Code to Add to compilar.py

```python
# After Phase 2 (parsing), add Phase 3:

from src.RA3.functions.python.analisador_semantico import analisarSemantica
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos

print("\n" + "="*70)
print("FASE 3: ANÁLISE SEMÂNTICA")
print("="*70)

# Load the syntax tree from RA2 output
with open('outputs/RA2/arvore_sintatica.json', 'r', encoding='utf-8') as f:
    arvore_sintatica = json.load(f)

# Create symbol table for semantic analysis
tabela_simbolos = TabelaSimbolos()

# Run semantic analysis
arvore_anotada, erros_semanticos = analisarSemantica(arvore_sintatica, tabela_simbolos)

# Save annotated tree
with open('outputs/RA3/arvore_anotada.json', 'w', encoding='utf-8') as f:
    json.dump(arvore_anotada, f, indent=2, ensure_ascii=False)

# Report errors
if erros_semanticos:
    print("\nERROS SEMÂNTICOS ENCONTRADOS:")
    for erro in erros_semanticos:
        print(erro)

    # Save errors to file
    with open('outputs/RA3/erros_semanticos.md', 'w', encoding='utf-8') as f:
        f.write("# Erros Semânticos\n\n")
        for erro in erros_semanticos:
            f.write(f"{erro}\n\n")
else:
    print("\n✓ Análise semântica bem-sucedida (sem erros)")
```

---

## Critical Considerations

### 1. Literal Type Inference

**Problem:** Distinguish between `5` (int) and `5.0` (real)

**Solution:** Check for decimal point

```python
def inferir_tipo_literal(valor: str) -> str:
    # "5" → int (no point)
    # "5.0" → real (has point)
    # "-3" → int (negative, but no point)
    # "3.14" → real (has point)

    if '.' in valor:
        return 'real'
    return 'int'
```

**Critical:** Don't use `isinstance(float(...), float)` because `float("5")` works!

---

### 2. Integer Division Strictness

**Problem:** `/` and `%` have DIFFERENT rules than `+`, `-`, `*`

**Correct:**
```python
(5 3 +)          # int + int → int
(5.0 3 +)        # real + int → real (PROMOTION!)
(5 3 /)          # int / int → int
(5.0 3 /)        # real / int → ERROR! (NO PROMOTION!)
```

**Why?** The RPN language semantics require integer division to be strict.

---

### 3. Permissive Truthiness Mode

**Problem:** Logical operators and conditions accept int/real and convert them

**Rules:**
- `0` or `0.0` → `false`
- Any non-zero → `true`
- Used in: `&&`, `||`, `!`, WHILE condition, IFELSE condition

**Example:**
```python
(5 3 &&)           # 5 is truthy, 3 is truthy → true && true → true
(0 10 ||)          # 0 is falsy, 10 is truthy → false || true → true
(5 !)              # 5 is truthy → !true → false
((x 0 >) body WHILE)  # (x > 0) is boolean, body can be any type
```

**Critical:** This is permissive - NOT strict type checking!

---

### 4. IFELSE Type Matching (MOST IMPORTANT)

**Problem:** Both branches MUST have same type

**Correct:**
```python
(true 5 10 IFELSE)         # Both int → OK, result int
(true 5.0 2.5 IFELSE)      # Both real → OK, result real
(true 5 2.5 IFELSE)        # int vs real → ERROR!
```

**Why?** Type safety - you can't return different types depending on condition.

---

### 5. Post-Order Traversal

**Problem:** Child types must be known before processing parent

**Correct Order:**
```
Visit children first:
  (5 3 +)
   ↓
  5 → type is int
  3 → type is int
   ↓
Then visit parent (+):
  + receives [int, int]
  + applies verification
  + returns int
```

**Critical:** Never process parent before children!

---

### 6. Error Collection Strategy

**Problem:** Don't stop at first error

**Correct:**
```python
# Process ALL nodes even if errors found
erros = []
try:
    analyze_node_1()  # May raise error
except ErroSemantico as e:
    erros.append(e)

try:
    analyze_node_2()  # Continue analyzing
except ErroSemantico as e:
    erros.append(e)

return (tree, erros)  # Return partial result + all errors
```

**Critical:** Use try/catch, collect errors, continue processing.

---

## Troubleshooting Guide

### Problem: Literal Type Always Wrong

**Solution:** Debug `inferir_tipo_literal()`
```python
# Test it directly
assert inferir_tipo_literal("5") == 'int'
assert inferir_tipo_literal("5.0") == 'real'
assert inferir_tipo_literal("-3") == 'int'  # No point
```

### Problem: Integer Division Still Promotes

**Solution:** Check you're calling `verificar_divisao_inteira()`, not `verificar_aritmetica()`
```python
# WRONG: Uses arithmetic (allows promotion)
tipo = verificar_aritmetica('real', 'int', '/', linha, contexto)

# CORRECT: Uses integer division (strict)
tipo = verificar_divisao_inteira('real', 'int', '/', linha, contexto)
```

### Problem: Post-Order Not Working (Children Don't Have Types)

**Solution:** Make sure to recursively process children BEFORE accessing their types
```python
# WRONG: Access child type before analyzing
tipos_filhos = [f.tipo for f in filhos_dict]  # NOT YET ANALYZED!

# CORRECT: Analyze children first, then access types
filhos_anotados = [analisar_no(f, ...) for f in filhos_dict]
tipos_filhos = [f.tipo for f in filhos_anotados]  # NOW ANALYZED
```

### Problem: IFELSE Accepting Different Types

**Solution:** Check you're comparing `tipo_true != tipo_false`
```python
# Must be strict equality
if tipo_true != tipo_false:
    raise ErroSemantico(...)  # Always raise if different
```

### Problem: Contextual Information Lost in Errors

**Solution:** Make sure to pass `contexto` parameter to all verificador functions
```python
# WRONG: No context
verificar_aritmetica('int', 'int', '+', linha)

# CORRECT: Include context
verificar_aritmetica('int', 'int', '+', linha,
                     contexto="(5 3 +)")
```

---

## Summary of Expected Behavior

**Valid Program (No Errors):**
```
Input: (5 3 +)
Process:
  - 5 → type: int
  - 3 → type: int
  - + → verificar_aritmetica('int', 'int') → returns 'int'
Output: arvore_anotada with all nodes typed, erros = []
```

**Invalid Program (Error Caught):**
```
Input: (5.5 2 /)
Process:
  - 5.5 → type: real
  - 2 → type: int
  - / → verificar_divisao_inteira('real', 'int') → raises ErroSemantico
Output: arvore_anotada = None, erros = [error message]
```

---

## Files Checklist

### New Files to Create
- [ ] `/src/RA3/functions/python/gerador_erros.py` (~100 lines)
- [ ] `/src/RA3/functions/python/verificador_tipos.py` (~300 lines)
- [ ] `/src/RA3/functions/python/analisador_semantico.py` (~350 lines)
- [ ] `/tests/RA3/test_verificador_tipos.py` (~250 lines)

### Files to Modify
- [ ] `/compilar.py` - Add Phase 3 integration
- [ ] `/outputs/RA3/` - Create if missing

### Output Files Generated
- [ ] `/outputs/RA3/arvore_anotada.json` - Annotated syntax tree
- [ ] `/outputs/RA3/erros_semanticos.md` - Error report

---

## Next Steps After Completion

Once Issue #2 is complete, it enables:

1. **Issue #3 (Aluno 3):** Memory and Control Validation
   - Uses the type-annotated tree from Issue #2
   - Adds initialization checking
   - Validates control structures

2. **Issue #4 (Aluno 4):** AST Generation and Integration
   - Uses the type-annotated tree from Issue #2
   - Generates final attributed AST
   - Creates all markdown reports

This is why Issue #2 is critical - it's the foundation for everything that follows!

