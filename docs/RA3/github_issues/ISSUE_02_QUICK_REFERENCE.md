# Issue #2 Quick Reference Card

**Print this or keep it open while implementing!**

---

## File Structure to Create

```
src/RA3/functions/python/
├── gerador_erros.py          [STEP 1] Error handling
├── verificador_tipos.py       [STEP 2] Type validation
└── analisador_semantico.py    [STEP 3] AST traversal

tests/RA3/
└── test_verificador_tipos.py  [STEP 4] Unit tests
```

---

## Step 1: gerador_erros.py (Simple!)

```python
# Error categories
CATEGORIA_TIPO = 'tipo'
CATEGORIA_MEMORIA = 'memoria'
CATEGORIA_CONTROLE = 'controle'
CATEGORIA_OUTRO = 'outro'

class ErroSemantico(Exception):
    def __init__(self, linha, descricao, contexto=None, categoria='outro'):
        self.linha = linha
        self.descricao = descricao
        self.contexto = contexto
        self.categoria = categoria

    def __str__(self):
        msg = f"ERRO SEMÂNTICO [Linha {self.linha}]: {self.descricao}"
        if self.contexto:
            msg += f"\nContexto: {self.contexto}"
        return msg
```

---

## Step 2: verificador_tipos.py (11 Functions)

### Remember: Each function validates ONE operator category

| Function | Operators | Input Types | Rules |
|----------|-----------|-------------|-------|
| `verificar_aritmetica()` | +, -, *, \| | numeric, numeric | Promote: int+real→real |
| `verificar_divisao_inteira()` | /, % | int, int | STRICT! No real operands |
| `verificar_potencia()` | ^ | numeric, int | Base numeric, exponent MUST int |
| `verificar_comparacao()` | >, <, >=, <=, ==, != | numeric, numeric | Returns boolean always |
| `verificar_logico_binario()` | &&, \|\| | truthy, truthy | Returns boolean always |
| `verificar_logico_unario()` | ! | truthy | Returns boolean always |
| `verificar_controle_for()` | FOR | int, int, int, any | Init/end/step must all be int |
| `verificar_controle_while()` | WHILE | truthy, any | Condition permissive, returns body type |
| `verificar_controle_ifelse()` | IFELSE | truthy, T, T | **CRITICAL: Both branches SAME type!** |

### Template for Each Function

```python
def verificar_NOME(tipos..., linha, contexto=None) -> str:
    """
    Verify OPERATOR rules

    Args:
        tipo_esq: Left operand type
        tipo_dir: Right operand type
        linha: Line number
        contexto: Code snippet

    Returns:
        Result type (int, real, or boolean)

    Raises:
        ErroSemantico: If type rules violated
    """
    # Step 1: Check first condition
    if not condition1:
        raise ErroSemantico(linha, "Error description", contexto, CATEGORIA_TIPO)

    # Step 2: Apply rules
    result = compute_result_type()

    # Step 3: Return result
    return result
```

---

## Step 3: analisador_semantico.py (Complex But Structured!)

### Three Parts:

#### Part 1: NoAnotado Class (Just a data holder)
```python
class NoAnotado:
    def __init__(self, label, filhos=None, tipo=None, linha=None, contexto=None):
        self.label = label
        self.filhos = filhos or []
        self.tipo = tipo          # ← THIS is what we add!
        self.linha = linha
        self.contexto = contexto
```

#### Part 2: Helper Functions
```python
def inferir_tipo_literal(valor):
    """Is it '5' (int) or '5.0' (real)?"""
    if '.' in valor:
        return 'real'
    return 'int'

def extrair_contexto(no):
    """Get code snippet from node"""
    return no.get('expressao_original', '...')

def obter_numero_linha(no):
    """Get line number from node"""
    return no.get('numero_linha', 0)
```

#### Part 3: Recursive Analysis (Post-Order!)
```python
def analisar_no(no_dict, tabela_simbolos, numero_linha=0):
    """
    Algorithm:
    1. Get label and children
    2. Recursively analyze all children FIRST
    3. Determine type of current node
    4. Return annotated node
    """
    label = no_dict['label']
    filhos_dict = no_dict['filhos']

    # STEP 1: Analyze children (post-order!)
    filhos_anotados = [analisar_no(f, tabela, numero_linha) for f in filhos_dict]
    tipos_filhos = [f.tipo for f in filhos_anotados if f.tipo]

    # STEP 2: Determine this node's type
    tipo_node = None

    if label == '+':
        tipo_node = verificar_aritmetica(tipos_filhos[0], tipos_filhos[1], '+', numero_linha, contexto)

    elif label == '/':
        tipo_node = verificar_divisao_inteira(tipos_filhos[0], tipos_filhos[1], '/', numero_linha, contexto)

    # ... etc for all operators

    # STEP 3: Return annotated node
    return NoAnotado(label=label, filhos=filhos_anotados, tipo=tipo_node, linha=numero_linha)

def analisarSemantica(arvore_sintatica, tabela_simbolos=None):
    """Entry point - returns (annotated_tree, errors)"""
    ...
```

---

## Type Rules Cheat Sheet

### What Types Can Be Mixed?

| Operation | int+int | int+real | real+real | Allows Real? | Returns |
|-----------|---------|----------|-----------|--------------|---------|
| +, -, *, \| | int | real | real | YES | Promoted |
| /, % | int | ERROR | real | NO (strict!) | int |
| ^ base | int | int | real | YES | Matches base |
| ^ exponent | MUST int | ERROR | ERROR | NO (strict!) | - |
| >, <, >=, <=, ==, != | boolean | boolean | boolean | YES | boolean |
| &&, \|\| | boolean | boolean | boolean | YES (permissive) | boolean |
| ! | boolean | boolean | boolean | YES (permissive) | boolean |
| FOR init/end/step | int | ERROR | real | NO (strict!) | - |
| WHILE condition | boolean | boolean | boolean | YES (permissive) | body type |
| IFELSE branches | T | ERROR | T | Must match exactly | T |

### Key Differences

```
PROMOTION (Arithmetic):
int + real = real ✓

NO PROMOTION (Integer Division):
real / int = ERROR ✗

PERMISSIVE (Logical):
int && int = boolean ✓ (convert int to boolean)

STRICT MATCHING (IFELSE):
(true 5 2.5 IFELSE) = ERROR ✗ (int vs real mismatch)
```

---

## Type Inference Rules

### Literals
- `5` → int
- `5.0` → real
- `-3` → int (no point)

### Operators (Post-Order)
- `(5 3 +)` → int+int → int
- `(5 3.0 +)` → int+real → real (promoted)
- `(5 3 >)` → int,int → boolean (always)
- `(5 3 &&)` → int,int → boolean (permissive mode)
- `(true 5 10 IFELSE)` → boolean, int, int → int (if branches match!)

### Variables
- Look up in tabela_simbolos
- Use stored type

### Non-Terminals
- Inherit from children (usually last child)

---

## Testing Pyramid

```
         Test Full Integration
              ↑
              │
      Test Complex Trees (nested expressions)
              ↑
              │
        Test Each Operator
              ↑
              │
    Test Each Verification Function
              ↑
              │
    Test gerador_erros
```

### Minimal Test Suite

```python
# gerador_erros tests
test_error_format()
test_error_categories()

# verificador_tipos tests (2-3 per function)
test_aritmetica_promotion()
test_divisao_inteira_strict()
test_potencia_exponent_must_int()
test_ifelse_branches_match()
# ... etc

# analisador_semantico tests
test_literal_type_inference()
test_post_order_traversal()
test_error_collection()
```

---

## Common Mistakes

### ❌ WRONG
```python
# 1. Analyzing parent before children
tipo_parent = operador.tipo  # NOT YET SET!

# 2. Allowing promotion in division
if tipo1 in TIPOS_NUMERICOS and tipo2 in TIPOS_NUMERICOS:
    # WRONG: This allows real/int division!

# 3. Not collecting all errors
try:
    analyze_tree()
except ErroSemantico:
    return None  # WRONG: Early return!

# 4. Losing context
raise ErroSemantico(linha, descricao)  # Missing contexto!

# 5. Not distinguishing 5 from 5.0
tipo = 'int' if isinstance(valor, int) else 'real'
# WRONG: float("5") works!
```

### ✅ CORRECT
```python
# 1. Analyze children first (post-order)
filhos = [analisar_no(f) for f in filhos_dict]
tipo_parent = apply_rules(filhos[0].tipo, filhos[1].tipo)

# 2. Strict validation for division
if not tipos_compativeis_divisao_inteira(tipo1, tipo2):
    raise ErroSemantico(...)  # CORRECT: Strict check!

# 3. Collect errors
erros = []
try:
    analyze_tree()
except ErroSemantico as e:
    erros.append(e)
    continue  # CORRECT: Continue analyzing!

# 4. Include context
raise ErroSemantico(linha, descricao, contexto, CATEGORIA_TIPO)

# 5. Check for decimal point
tipo = 'real' if '.' in valor_str else 'int'
```

---

## Integration Checklist

- [ ] Three modules created and importable
- [ ] No import errors
- [ ] All 11 functions in verificador_tipos.py
- [ ] analisador_semantico handles 30+ node types
- [ ] Error messages match format exactly
- [ ] Tests pass (20+ test cases)
- [ ] Integration with compilar.py
- [ ] Outputs saved to files
- [ ] No crashes on test inputs

---

## Output Files Expected

After running Issue #2 on test input:

**inputs/RA3/teste1_valido.txt:**
```
(5 3 +)
(5.5 2.0 *)
(5 3 /)
(5 3 >)
((5 3 >) (2 1 <) &&)
```

**Outputs:**
- `outputs/RA3/arvore_anotada.json` - JSON with type annotations
- `outputs/RA3/erros_semanticos.md` - Error list (should be empty for teste1_valido)

**Example arvore_anotada.json structure:**
```json
{
  "label": "SEQUENCIA",
  "tipo": "int",
  "linha": 1,
  "contexto": "(5 3 +)",
  "filhos": [
    {
      "label": "5",
      "tipo": "int",
      "filhos": []
    },
    {
      "label": "3",
      "tipo": "int",
      "filhos": []
    },
    {
      "label": "+",
      "tipo": "int",
      "filhos": []
    }
  ]
}
```

---

## Estimated Time

| Step | Task | Time | Difficulty |
|------|------|------|------------|
| 1 | gerador_erros.py | 30-60 min | Easy |
| 2 | verificador_tipos.py | 2-4 hours | Medium |
| 3 | analisador_semantico.py | 4-6 hours | Hard |
| 4 | test_verificador_tipos.py | 2-3 hours | Medium |
| 5 | Integration & debugging | 1-2 hours | Easy |
| **Total** | **All of Issue #2** | **10-16 hours** | **Medium/Hard** |

---

## Quick Debug Commands

```python
# Test a single function
from src.RA3.functions.python.verificador_tipos import verificar_aritmetica
resultado = verificar_aritmetica('int', 'real', '+', 5, "(5 3.0 +)")
print(resultado)  # Should print 'real'

# Test error format
from src.RA3.functions.python.gerador_erros import ErroSemantico
e = ErroSemantico(5, "Test error", "(5.5 2 /)", "tipo")
print(str(e))  # Should print formatted error

# Test semantic analysis
from src.RA3.functions.python.analisador_semantico import analisarSemantica
arvore, erros = analisarSemantica(arvore_dict)
print(f"Erros: {len(erros)}")
print(f"Tipo raiz: {arvore['tipo']}")
```

---

## When You Get Stuck

1. **Check the type specifications** in the main guide
2. **Review the code examples** provided
3. **Run isolated tests** for one function
4. **Print debug info** - what types do children have?
5. **Check post-order** - are children analyzed before parent?
6. **Verify error format** - does it match specification exactly?

You got this! 💪
