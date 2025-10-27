# Issue #2 Visual Guide and Flow Diagrams

---

## Overall Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  COMPILADOR RPN - FASES 1, 2, 3                                 │
└─────────────────────────────────────────────────────────────────┘

INPUT FILE
   │
   │ (5 3 +)
   │ (10.5 2.0 *)
   │ (x 3 >)
   │
   ▼
┌─────────────────────────────────────────┐
│  FASE 1: ANÁLISE LÉXICA (RA1) ✓         │
│  Tokenização                             │
└─────────────────────────────────────────┘
   │ outputs/RA1/tokens/tokens_gerados.txt
   │ ( 5 3 + )
   │ ( 10.5 2.0 * )
   │ ( X 3 > )
   │
   ▼
┌─────────────────────────────────────────┐
│  FASE 2: ANÁLISE SINTÁTICA (RA2) ✓      │
│  Parsing LL(1)                          │
│  Geração de AST                         │
└─────────────────────────────────────────┘
   │ outputs/RA2/arvore_sintatica.json
   │ {
   │   "label": "PROGRAMA",
   │   "filhos": [
   │     {"label": "LINHA", "filhos": [...]}
   │   ]
   │ }
   │
   ▼
┌─────────────────────────────────────────┐
│  FASE 3: ANÁLISE SEMÂNTICA (RA3) ⭐ NEW │
│  Type Checking                          │
│  Type Annotation                        │
└─────────────────────────────────────────┘
   │ analisador_semantico.py
   │   ├─ analisar_no()
   │   │   ├─ verificador_tipos.py
   │   │   └─ gerador_erros.py
   │   └─ Retorna: (arvore_anotada, erros)
   │
   ▼
   │ outputs/RA3/arvore_anotada.json
   │ {
   │   "label": "PROGRAMA",
   │   "tipo": "int",        ← TYPE ADDED!
   │   "filhos": [
   │     {"label": "LINHA", "tipo": "int", ...}
   │   ]
   │ }
   │
   ▼ (used by Issue #3 and #4)
```

---

## Module Interaction Diagram

```
                    ENTRADA
                      │
                      ▼
        ┌─────────────────────────────┐
        │  analisador_semantico.py    │
        │  (AST Traversal)            │
        │                             │
        │  analisarSemantica()        │
        │    ├─ analisar_no()         │
        │    │  (recursivo)           │
        │    └─ POST-ORDER            │
        └────────────┬────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌──────┐  ┌─────────┐
    │ tipos  │  │ver-  │  │tabela_  │
    │        │  │ifi-  │  │simbolos │
    │ .py    │  │cador │  │         │
    │        │  │tipos │  │         │
    │        │  │.py   │  │         │
    └────────┘  └──────┘  └─────────┘
                   │
                   │ raises
                   ▼
            ┌──────────────┐
            │ gerador_     │
            │ erros.py     │
            │ ErroSemantico│
            └──────────────┘

         SAÍDA:
         ┌──────────────────────┐
         │ (arvore_anotada,     │
         │  lista_erros)        │
         └──────────────────────┘
```

---

## Module 1: gerador_erros.py

```
┌──────────────────────────────────┐
│  gerador_erros.py               │
│  (~100 linhas)                  │
│                                 │
│  Categorias de Erro:            │
│  ├─ CATEGORIA_TIPO              │
│  ├─ CATEGORIA_MEMORIA           │
│  ├─ CATEGORIA_CONTROLE          │
│  └─ CATEGORIA_OUTRO             │
│                                 │
│  Classe:                        │
│  └─ ErroSemantico               │
│      ├─ linha (int)             │
│      ├─ descricao (str)         │
│      ├─ contexto (str)          │
│      ├─ categoria (str)         │
│      └─ __str__() → formatted   │
└──────────────────────────────────┘

Uso:
raise ErroSemantico(
    linha=5,
    descricao="Tipos incompatíveis",
    contexto="(5.5 2 /)",
    categoria=CATEGORIA_TIPO
)

Output:
ERRO SEMÂNTICO [Linha 5]: Tipos incompatíveis
Contexto: (5.5 2 /)
```

---

## Module 2: verificador_tipos.py

```
┌─────────────────────────────────────────────────┐
│  verificador_tipos.py                           │
│  (~300 linhas)                                  │
│                                                 │
│  11 Funções de Verificação:                    │
│  ├─ verificar_aritmetica()                     │
│  ├─ verificar_divisao_inteira()                │
│  ├─ verificar_potencia()                       │
│  ├─ verificar_comparacao()                     │
│  ├─ verificar_logico_binario()                 │
│  ├─ verificar_logico_unario()                  │
│  ├─ verificar_controle_for()                   │
│  ├─ verificar_controle_while()                 │
│  ├─ verificar_controle_ifelse()                │
│  └─ ...                                         │
└─────────────────────────────────────────────────┘

Padrão Geral:
┌─────────────────────────────────┐
│ verificar_OPERADOR()            │
├─────────────────────────────────┤
│ Input:                          │
│ - tipo_esq/dir: str             │
│ - operador: str                 │
│ - linha: int                    │
│ - contexto: str (optional)      │
├─────────────────────────────────┤
│ Output:                         │
│ - tipo_resultado: str (int,     │
│   real, or boolean)             │
├─────────────────────────────────┤
│ Raises:                         │
│ - ErroSemantico (if rules fail) │
└─────────────────────────────────┘

Exemplo de Fluxo:
┌─────────────────────┐
│ verificar_divisao   │
│ _inteira()          │
├─────────────────────┤
│ Input: 'real', 'int'│
├─────────────────────┤
│ Step 1: Check types │
│ tipo_esq == 'real'  │
│ ✗ Not int!          │
├─────────────────────┤
│ Step 2: Raise error │
│ ErroSemantico(...)  │
└─────────────────────┘
```

---

## Module 3: analisador_semantico.py

```
┌────────────────────────────────────────────────┐
│  analisador_semantico.py                       │
│  (~350 linhas)                                 │
│                                                │
│  Componentes:                                 │
│  ├─ Classe NoAnotado                          │
│  │  └─ label, filhos, tipo, linha, contexto   │
│  ├─ Helper Functions                          │
│  │  ├─ inferir_tipo_literal()                 │
│  │  ├─ extrair_contexto()                     │
│  │  └─ obter_numero_linha()                   │
│  └─ Análise Recursiva                         │
│     ├─ analisar_no() [RECURSIVO]              │
│     └─ analisarSemantica() [ENTRADA]          │
└────────────────────────────────────────────────┘

Algoritmo de Post-Order:

        PROGRAMA
           │
         LINHA
           │
           (+)
          /   \
         /     \
       (5)    (3)

Ordem de Análise:
1. Analise (5) → tipo = int
2. Analise (3) → tipo = int
3. Analise (+)
   - tipos_filhos = [int, int]
   - aplica regra: int + int = int
   - tipo = int
4. Analise LINHA
   - herança do tipo int
5. Analise PROGRAMA
   - herança do tipo int
```

---

## Type Inference Flow

```
┌─────────────────────────────────────────────────┐
│  COMO DETERMINAR O TIPO DE CADA NÓ             │
└─────────────────────────────────────────────────┘

PASSO 1: É uma folha (terminal)?
         ↓
    ┌────────────────┐
    │ É um literal?  │
    └────────────────┘
         ↙   ↘
       sim    não
        │      │
        ▼      ▼
    Infere   É uma
    int/real variável?
        │      │
        │      ├─ sim → Procura em
        │      │        tabela_simbolos
        │      │        → obtém tipo
        │      │
        │      └─ não → Herdará de
        │               seus filhos

PASSO 2: É um operador?
         ↓
    ┌────────────────────┐
    │ Qual categoria?    │
    └────────────────────┘
         │
    ┌────┼────┬────────┬──────┐
    │    │    │        │      │
   arit.│comp│lógico │contro-│
   ~    │ ~  │  ~    │le ~   │
    │    │    │        │      │
    ▼    ▼    ▼        ▼      ▼
  +,-,* > < && || for while if
    │    │    │        │      │
    └─►verificar_CATEGORIA()◄─┘
         │
         ├─ Checa tipos operandos
         ├─ Aplica regras semânticas
         └─ Retorna tipo_resultado
              │
              ▼
          Resultado: tipo_operacao

PASSO 3: É um não-terminal gramatical?
         ↓
         └─ Herda de seus filhos
            (normalmente último)
```

---

## Type Annotation Example

### Input from RA2:
```json
{
  "label": "SEQUENCIA",
  "filhos": [
    {
      "label": "5",
      "filhos": []
    },
    {
      "label": "+",
      "filhos": []
    },
    {
      "label": "3",
      "filhos": []
    }
  ]
}
```

### Processing Steps:

```
PASSO 1: Analyze filhos[0] (label="5")
         ├─ É literal? Sim
         ├─ inferir_tipo_literal("5")
         ├─ Sem ponto decimal
         └─ tipo = 'int'

         Resultado: {"label": "5", "tipo": "int"}

PASSO 2: Analyze filhos[1] (label="+")
         ├─ É operador? Sim
         ├─ Quais tipos filhos têm? [?]
         ├─ (precisa processar filhos primeiro!)
         └─ ERRO: Não seguiu post-order!

CORREÇÃO: Processa children primeiro (post-order)

PASSO 1A: Analyze filho 0 ("5")
          └─ tipo = 'int'

PASSO 1B: Analyze filho 1 ("+")
          ├─ É operador? Sim
          ├─ Precisa 2 filhos (filhos[0] e filhos[2])
          ├─ tipos_filhos = [?] → ainda não!

PASSO 1C: Analyze filho 2 ("3")
          └─ tipo = 'int'

PASSO 2: Agora com tipos dos filhos:
         Analyze filho 1 ("+")
         ├─ tipos_filhos = [int, int]
         ├─ verificar_aritmetica('int', 'int', '+', ...)
         ├─ Retorna 'int'
         └─ tipo = 'int'

PASSO 3: Voltar para SEQUENCIA (parent)
         ├─ É não-terminal
         ├─ Herdeia dos filhos
         ├─ filhos[-1].tipo = 'int' (último filho)
         └─ tipo = 'int'
```

### Output:
```json
{
  "label": "SEQUENCIA",
  "tipo": "int",
  "filhos": [
    {
      "label": "5",
      "tipo": "int",
      "filhos": []
    },
    {
      "label": "+",
      "tipo": "int",
      "filhos": []
    },
    {
      "label": "3",
      "tipo": "int",
      "filhos": []
    }
  ]
}
```

---

## Error Detection Example

```
Entrada: (5.5 2 /)

Parse Tree:
          LINHA
            │
           (/)
          /   \
       (5.5)  (2)

Análise:

PASSO 1: (5.5) → tipo = 'real' (tem ponto)
PASSO 2: (2) → tipo = 'int' (sem ponto)
PASSO 3: (/)
         ├─ tipos_filhos = [real, int]
         ├─ Chama: verificar_divisao_inteira('real', 'int', '/', 1)
         ├─ Check: tipo_esq != 'int' ?
         ├─ Sim! 'real' != 'int'
         ├─ Raises ErroSemantico:
         │   "Divisão inteira requer operandos inteiros,
         │    mas encontrado 'real' e 'int'"
         └─ Contexto: "(5.5 2 /)"

Output:
arvore_anotada = None (erro encontrado)
erros = [
  "ERRO SEMÂNTICO [Linha 1]: Divisão inteira requer operandos inteiros,
   mas encontrado 'real' e 'int'
   Contexto: (5.5 2 /)"
]
```

---

## Type Rule Matrix

### Operador: + (Adição)

```
Entrada                    Saída
────────────────────────────────────
(5 3 +)         int+int  →  int
(5.0 3 +)       real+int →  real  (PROMOTION!)
(5 3.0 +)       int+real →  real  (PROMOTION!)
(5.0 3.0 +)     real+real → real
(true 3 +)      bool+int → ERROR! ✗
(3 true +)      int+bool → ERROR! ✗
```

### Operador: / (Divisão Inteira)

```
Entrada                    Saída
────────────────────────────────────
(10 2 /)        int/int  →  int
(10.0 2 /)      real/int → ERROR! ✗ (NO PROMOTION!)
(10 2.0 /)      int/real → ERROR! ✗ (NO PROMOTION!)
(10.0 2.0 /)    real/real → ERROR! ✗
(true 2 /)      bool/int → ERROR! ✗
```

Key: Divisão é ESTRITA - NUNCA promove!

### Operador: ^ (Potência)

```
Entrada                    Saída
────────────────────────────────────
(2 3 ^)         int^int  →  int
(2.0 3 ^)       real^int →  real
(2 3.0 ^)       int^real → ERROR! ✗ (exponent must be int)
(2.0 3.0 ^)     real^real → ERROR! ✗ (exponent must be int)
(true 3 ^)      bool^int → ERROR! ✗
```

### Operador: > (Comparação)

```
Entrada                    Saída
────────────────────────────────────
(5 3 >)         int>int  →  boolean
(5.0 3 >)       real>int →  boolean
(5 3.0 >)       int>real →  boolean
(5.0 3.0 >)     real>real → boolean
(true false >)  bool>bool → ERROR! ✗
```

### Operador: && (E Lógico - Permissive Mode!)

```
Entrada                    Saída
────────────────────────────────────
(true false &&) bool&&bool → boolean
(5 3 &&)        int&&int  → boolean (PERMISSIVE!)
(5.0 0 &&)      real&&real → boolean (PERMISSIVE!)
(true 5 &&)     bool&&int → boolean (PERMISSIVE!)
Nota: 0/0.0 = false, outros = true
```

### Operador: IFELSE (CRÍTICO!)

```
(condition true_branch false_branch IFELSE)

Entrada                              Saída
────────────────────────────────────────────────
(true 5 10 IFELSE)     int, int     → int ✓
(true 5.0 2.5 IFELSE)  real, real   → real ✓
(true 5 2.5 IFELSE)    int, real    → ERROR! ✗
(true 5 10.0 IFELSE)   int, real    → ERROR! ✗

REGRINHA: Ambos ramos DEVEM ter mesmo tipo!!!
```

---

## Testing Flow

```
┌─────────────────────────────────┐
│  test_verificador_tipos.py      │
│  (~250 linhas)                  │
└─────────────────────────────────┘

Test Hierarchy:
├─ TestGerador (2-3 testes)
│  └─ formato de erro
│
├─ TestAritmetica (4-5 testes)
│  ├─ int+int
│  ├─ int+real (promotion)
│  ├─ invalid types
│  └─ ...
│
├─ TestDivisaoInteira (3-4 testes)
│  ├─ int/int OK
│  ├─ real/int ERROR
│  └─ ...
│
├─ TestPotencia (3-4 testes)
│  ├─ base any, exp int
│  ├─ base any, exp real ERROR
│  └─ ...
│
├─ TestComparacao (2-3 testes)
│  ├─ numeric → boolean
│  ├─ boolean ERROR
│  └─ ...
│
├─ TestLogico (3-4 testes)
│  ├─ permissive mode int
│  ├─ permissive mode real
│  └─ ...
│
├─ TestControle (4-5 testes)
│  ├─ FOR: all int
│  ├─ WHILE: permissive condition
│  ├─ IFELSE: branches match
│  └─ IFELSE: branches mismatch ERROR
│
└─ TestAnalisador (4-5 testes)
   ├─ post-order traversal
   ├─ nested expressions
   ├─ error collection
   └─ integration test

TOTAL: 20-30 testes cobrindo tudo
```

---

## Debugging Flowchart

```
Problema: Tipo do nó sempre None
    │
    ▼
┌──────────────────────┐
│ É literal ou var?    │
│ Definiste lógica?    │
└──────────────────────┘
    │ Não
    ▼
  FIX: Adiciona
       inferir_tipo_literal()

    │ Sim
    ▼
┌──────────────────────┐
│ É operador?          │
│ Tem case para ele?   │
└──────────────────────┘
    │ Não
    ▼
  FIX: Adiciona case
       elif label == OPERADOR:

    │ Sim
    ▼
┌──────────────────────┐
│ Filhos têm tipos?    │
│ Post-order OK?       │
└──────────────────────┘
    │ Não
    ▼
  FIX: Certifica que
       analisa filhos
       ANTES de pai

    │ Sim
    ▼
┌──────────────────────┐
│ verificador retorna  │
│ tipo válido?         │
└──────────────────────┘
    │ Não
    ▼
  FIX: Debug
       verificador_tipos
       print tipos entrada
```

---

## Time Breakdown

```
Implementação:
├─ gerador_erros.py
│  ├─ ErroSemantico class        10 min
│  ├─ Error formatting functions 15 min
│  └─ Testing                    15 min
│  └─ Subtotal:                  40 min
│
├─ verificador_tipos.py
│  ├─ Basic structure            15 min
│  ├─ 11 functions @ 15 min each 165 min (2h45m)
│  └─ Testing each function      60 min
│  └─ Subtotal:                  240 min (4h)
│
├─ analisador_semantico.py
│  ├─ NoAnotado class            15 min
│  ├─ Helper functions           30 min
│  ├─ Core algorithm (hard!)     120 min (2h)
│  ├─ All node types             90 min (1h30m)
│  └─ Testing                    45 min
│  └─ Subtotal:                  300 min (5h)
│
├─ test_verificador_tipos.py
│  ├─ Setup & imports            15 min
│  ├─ 25 test cases              90 min
│  └─ Running & debugging        30 min
│  └─ Subtotal:                  135 min (2h15m)
│
└─ Integration & debugging       60 min (1h)

TOTAL: ~10-16 HORAS DE TRABALHO
```

---

## Success Checklist

```
✓ All 3 modules created
✓ No import errors
✓ All 11 functions in verificador_tipos.py
✓ analisador_semantico handles all node types
✓ Post-order traversal correct
✓ Error format matches spec exactly
✓ 20+ tests passing
✓ Integrated with compilar.py
✓ Output files generated
✓ No crashes on test inputs

When ALL checked: Ready for Issue #3!
```

