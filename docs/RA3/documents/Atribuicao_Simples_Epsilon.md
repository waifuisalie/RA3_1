# 📚 Atribuição Simples e o Papel do Epsilon na Gramática LL(1)

> **Documento Técnico**: Explicação detalhada sobre por que atribuições simples não precisam de um símbolo terminal MEM e como a produção epsilon em `SEQUENCIA_PRIME` permite essa construção.

---

## 📌 Informações do Documento

**Projeto**: Compilador RA3_1
**Disciplina**: Compiladores (2025-2)
**Tópico**: Gramática LL(1) Pós-Fixada - Atribuições Simples
**Criado em**: 2025-10-22
**Última Atualização**: 2025-10-22

---

## 🎯 Contexto do Problema

### Pergunta Inicial:
> "Por que não precisamos inserir 'MEM' como terminal na gramática se ele representa atribuição a uma variável?"

### Resposta Resumida:
**MEM é um conceito semântico, não um token sintático**. A atribuição simples é reconhecida pela **estrutura sintática** (dois operandos sem operador) e pela **produção epsilon** em `SEQUENCIA_PRIME`, sendo interpretada posteriormente na análise semântica (RA3).

---

## 🧩 Parte 1: MEM - Conceito vs Token

### 1.1 O que é MEM?

**MEM** no contexto do projeto significa **MEMória** - uma posição de armazenamento para valores.

#### Nos PDFs de especificação:
- **Comandos_Fase_1.pdf**: Descreve variáveis como "posições de memória (MEM)"
- **Comandos_Fase_2.pdf**: Define a sintaxe `(valor VARIAVEL)` para atribuição
- **Comandos_Fase_3.pdf**: Especifica validação semântica de atribuições

#### Interpretação correta:
```
(5.5 A)      ✅ CORRETO - A é uma VARIÁVEL (tipo MEM)
(5.5 X)      ✅ CORRETO - X é uma VARIÁVEL (tipo MEM)
(5.5 TEMP)   ✅ CORRETO - TEMP é uma VARIÁVEL (tipo MEM)
```

**MEM não aparece explicitamente na sintaxe** - é uma propriedade semântica da variável.

---

### 1.2 MEM como Conceito em 3 Níveis

| Fase | Onde MEM aparece | Como é representado |
|------|------------------|---------------------|
| **RA1** (Léxico/Assembly) | Geração de código Assembly | Endereços de memória: `A_MEM`, `X_MEM` |
| **RA2** (Sintático) | Gramática LL(1) | Produção `OPERANDO → variavel` |
| **RA3** (Semântico) | Tabela de símbolos | Mapeamento variável → tipo MEM |

#### Exemplo de Geração Assembly (RA1):
```assembly
; Código fonte: (5.5 A)
LDI R16, 5         ; Carrega parte inteira
LDI R17, 5         ; Carrega parte decimal (representação simplificada)
STS A_MEM, R16     ; Armazena na MEMÓRIA de A ← Aqui está MEM!
STS A_MEM+1, R17   ; Armazena parte decimal
```

**MEM** aparece no **rótulo de endereço** `A_MEM`, não como um token sintático.

---

### 1.3 Por que MEM NÃO é um Terminal?

#### Razão 1: Notação RPN (Reverse Polish Notation)

A linguagem usa **notação pós-fixada pura**:
```
(operando1 operando2 ... operandoN operador)
```

Para atribuição simples:
```
(5.5 A)
```

**Interpretação RPN**:
- `5.5` = valor (operando 1)
- `A` = variável (operando 2)
- **Operador implícito** = atribuição por justaposição

Se MEM fosse um token, teríamos:
```
(5.5 A MEM)      ← MEM seria operador de atribuição explícito
```

Isso **quebraria a notação RPN** porque:
- RPN permite operador implícito para atribuições
- Adicionar MEM seria **redundante**
- A estrutura `(valor variável)` já é **auto-explicativa**

---

#### Razão 2: MEM é Implícito no Tipo VARIAVEL

Quando o analisador léxico (RA1) encontra um identificador:

```python
# src/RA1/functions/python/analisador_lexico.py
def identificar_token(lexema):
    if lexema.isupper() and len(lexema) <= 10:  # Exemplo simplificado
        return Token(Tipo_de_Token.VARIAVEL, lexema)
```

**O token `VARIAVEL` já carrega a semântica de "posição de memória"**:
- Não precisa de um modificador `MEM`
- A ação de "armazenar em memória" é **implícita** no uso de variável como destino

---

#### Razão 3: Separação de Responsabilidades

| Fase | Responsabilidade | Como trata MEM |
|------|------------------|----------------|
| **RA1** | Reconhecer tokens | `VARIAVEL` = identificador que **pode** ser MEM |
| **RA2** | Validar sintaxe | `(valor variavel)` é estrutura **sintaticamente válida** |
| **RA3** | Validar semântica | Confirma que variável está sendo usada como **destino de atribuição** |

**MEM é resolvido na Fase 3 (semântica)**, não na Fase 2 (sintaxe).

---

### 1.4 Contraste: Por que RES É um Terminal?

Para entender por que MEM não precisa ser terminal, vamos comparar com **RES**, que **É** um terminal.

#### RES Precisa Ser Token Explícito:

```
(2 RES)          ← RES é palavra-chave literal
```

**Tokenização**:
- `2` → Token: `NUMERO_REAL` (valor: 2)
- `RES` → Token: `RES` (palavra-chave)

**Por que RES é diferente de MEM?**

| Característica | MEM | RES |
|----------------|-----|-----|
| **Aparece na expressão?** | ❌ Não | ✅ Sim `(2 RES)` |
| **Altera significado do operando?** | ❌ Não | ✅ Sim (2 → ref. 2 linhas atrás) |
| **É palavra-chave?** | ❌ Não | ✅ Sim |
| **Na gramática LL(1)?** | ❌ Não | ✅ Sim (`OPERANDO_OPCIONAL`) |
| **Quando resolve?** | RA3 (semântica) | RA3 (semântica + runtime) |

#### RES Modifica o Significado:
```python
# Sem RES:
(2 A)          # Atribui o valor literal 2 a A

# Com RES:
(2 RES A)      # Atribui o resultado da linha (atual - 2) a A
```

**RES** altera a **interpretação do número**:
- `2` sozinho = valor literal
- `2 RES` = referência temporal

**MEM** não altera nada - apenas descreve o **tipo** da variável (que já é conhecido).

---

## 🧩 Parte 2: Gramática LL(1) e a Produção Epsilon

### 2.1 Gramática Atual (100% Pós-Fixada)

**Localização**: `src/RA2/functions/python/configuracaoGramatica.py`

```python
GRAMATICA_RPN = {
    'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
    'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['epsilon']],

    'LINHA': [['abre_parenteses', 'SEQUENCIA', 'fecha_parenteses']],

    'SEQUENCIA': [['OPERANDO', 'SEQUENCIA_PRIME']],
    'SEQUENCIA_PRIME': [
        ['OPERANDO', 'SEQUENCIA_PRIME'],  # Mais operandos
        ['OPERADOR_FINAL'],                # Operador explícito
        ['epsilon']                        # ← CHAVE: Permite atribuição sem operador
    ],

    'OPERANDO': [
        ['numero_real', 'OPERANDO_OPCIONAL'],
        ['variavel', 'OPERANDO_OPCIONAL'],
        ['LINHA']  # Subexpressão
    ],

    'OPERANDO_OPCIONAL': [['res'], ['epsilon']],

    'OPERADOR_FINAL': [
        ['ARITH_OP'],   # +, -, *, /, |, %, ^
        ['COMP_OP'],    # <, >, ==, <=, >=, !=
        ['LOGIC_OP'],   # &&, ||, !
        ['CONTROL_OP']  # for, while, ifelse
    ]
}
```

---

### 2.2 O Papel Crítico do Epsilon

#### Produção `SEQUENCIA_PRIME`:
```python
'SEQUENCIA_PRIME': [
    ['OPERANDO', 'SEQUENCIA_PRIME'],  # Recursão: mais operandos
    ['OPERADOR_FINAL'],                # Operação com operador explícito
    ['epsilon']                        # ← PERMITE TERMINAR SEM OPERADOR
]
```

#### Sem Epsilon, a Gramática Seria QUEBRADA:

```python
# GRAMÁTICA HIPOTÉTICA SEM EPSILON (ERRADA):
'SEQUENCIA_PRIME': [
    ['OPERANDO', 'SEQUENCIA_PRIME'],
    ['OPERADOR_FINAL']  # ← Obriga operador!
]

# Tentando derivar (5.5 A):
SEQUENCIA → OPERANDO SEQUENCIA_PRIME
         → number SEQUENCIA_PRIME
         → number OPERANDO SEQUENCIA_PRIME
         → number identifier SEQUENCIA_PRIME
         → number identifier OPERADOR_FINAL  # ❌ ERRO: (5.5 A ???)

# A gramática exigiria:
(5.5 A +)    # ← Operador obrigatório
(5.5 A <)
(5.5 A &&)
```

**Sem epsilon, atribuições simples seriam IMPOSSÍVEIS!**

---

### 2.3 Como Epsilon Funciona na Tabela LL(1)

#### Construção da Tabela LL(1):

```python
# FIRST e FOLLOW de SEQUENCIA_PRIME:
FIRST(SEQUENCIA_PRIME) = {number, identifier, (, +, -, *, /, <, >, ==, &&, ||, !, for, while, ifelse, epsilon}
FOLLOW(SEQUENCIA_PRIME) = {)}

# Entradas na Tabela LL(1):
M[SEQUENCIA_PRIME, number]     = ['OPERANDO', 'SEQUENCIA_PRIME']
M[SEQUENCIA_PRIME, identifier] = ['OPERANDO', 'SEQUENCIA_PRIME']
M[SEQUENCIA_PRIME, +]          = ['OPERADOR_FINAL']
M[SEQUENCIA_PRIME, -]          = ['OPERADOR_FINAL']
M[SEQUENCIA_PRIME, )]          = ['epsilon']  # ← CHAVE!
```

**Quando o parser vê `)` após um operando**:
1. Consulta `M[SEQUENCIA_PRIME, )]`
2. Encontra produção `['epsilon']`
3. Consome epsilon (não consome input)
4. Retorna para `LINHA`, que consome `)`
5. **Aceita a atribuição simples!**

---

### 2.4 Derivação Completa: `(5.5 A)`

#### Passo a Passo da Derivação LL(1):

```
Entrada: ( 5.5 A )
Pilha inicial: [$, PROGRAM]

Passo 1:
  Pilha: [$, PROGRAM]
  Entrada: ( 5.5 A )
  Ação: PROGRAM → LINHA PROGRAM_PRIME
  Nova pilha: [$, PROGRAM_PRIME, LINHA]

Passo 2:
  Pilha: [$, PROGRAM_PRIME, LINHA]
  Entrada: ( 5.5 A )
  Ação: LINHA → ( SEQUENCIA )
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA, (]

Passo 3:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA, (]
  Entrada: ( 5.5 A )
  Ação: Match ( ✓
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA]
  Nova entrada: 5.5 A )

Passo 4:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA]
  Entrada: 5.5 A )
  Ação: SEQUENCIA → OPERANDO SEQUENCIA_PRIME
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO]

Passo 5:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO]
  Entrada: 5.5 A )
  Ação: OPERANDO → numero_real OPERANDO_OPCIONAL
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL, numero_real]

Passo 6:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL, numero_real]
  Entrada: 5.5 A )
  Ação: Match numero_real (5.5) ✓
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL]
  Nova entrada: A )

Passo 7:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL]
  Entrada: A )
  Ação: OPERANDO_OPCIONAL → epsilon (lookahead = identifier)
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME]

Passo 8:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME]
  Entrada: A )
  Ação: SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO]

Passo 9:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO]
  Entrada: A )
  Ação: OPERANDO → variavel OPERANDO_OPCIONAL
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL, variavel]

Passo 10:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL, variavel]
  Entrada: A )
  Ação: Match variavel (A) ✓
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL]
  Nova entrada: )

Passo 11:
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME, OPERANDO_OPCIONAL]
  Entrada: )
  Ação: OPERANDO_OPCIONAL → epsilon (lookahead = ))
  Nova pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME]

Passo 12: ⭐ EPSILON CRÍTICO ⭐
  Pilha: [$, PROGRAM_PRIME, ), SEQUENCIA_PRIME]
  Entrada: )
  Ação: SEQUENCIA_PRIME → epsilon (lookahead = ))
  Nova pilha: [$, PROGRAM_PRIME, )]

  ← SEM EPSILON, O PARSER REJEITARIA AQUI!

Passo 13:
  Pilha: [$, PROGRAM_PRIME, )]
  Entrada: )
  Ação: Match ) ✓
  Nova pilha: [$, PROGRAM_PRIME]
  Nova entrada: $ (fim)

Passo 14:
  Pilha: [$, PROGRAM_PRIME]
  Entrada: $
  Ação: PROGRAM_PRIME → epsilon
  Nova pilha: [$]

✅ ACEITO: Derivação completa de (5.5 A)
```

---

### 2.5 Análise LL(1): Por que Não Há Conflitos?

#### Conjuntos FIRST e FOLLOW:

```python
FIRST(SEQUENCIA_PRIME) = {
    number, identifier, (,           # De OPERANDO
    +, -, *, /, |, %, ^,             # De ARITH_OP
    <, >, ==, <=, >=, !=,            # De COMP_OP
    &&, ||, !,                       # De LOGIC_OP
    for, while, ifelse,              # De CONTROL_OP
    epsilon                          # Da produção epsilon
}

FOLLOW(SEQUENCIA_PRIME) = {)}
```

#### Tabela LL(1) para SEQUENCIA_PRIME:

| Não-Terminal | Terminal | Produção |
|--------------|----------|----------|
| SEQUENCIA_PRIME | `number` | `OPERANDO SEQUENCIA_PRIME` |
| SEQUENCIA_PRIME | `identifier` | `OPERANDO SEQUENCIA_PRIME` |
| SEQUENCIA_PRIME | `(` | `OPERANDO SEQUENCIA_PRIME` |
| SEQUENCIA_PRIME | `+` | `OPERADOR_FINAL` |
| SEQUENCIA_PRIME | `-` | `OPERADOR_FINAL` |
| SEQUENCIA_PRIME | `)` | `epsilon` ⭐ |

**Sem conflitos**: Cada entrada (não-terminal, terminal) tem **exatamente uma** produção válida!

---

## 🧩 Parte 3: Análise Semântica - Como RA3 Reconhece Atribuição

### 3.1 Entrada do RA3: AST em JSON

O RA2 (análise sintática) gera uma **Árvore Sintática Abstrata (AST)** em JSON para o RA3.

#### Exemplo: `(5.5 A)` → JSON

```json
{
  "tipo": "PROGRAM",
  "linhas": [
    {
      "numero_linha": 1,
      "tipo": "LINHA",
      "filhos": [
        {
          "tipo": "SEQUENCIA",
          "elementos": [
            {
              "tipo": "OPERANDO",
              "subtipo": "numero_real",
              "valor": "5.5",
              "res": false
            },
            {
              "tipo": "OPERANDO",
              "subtipo": "variavel",
              "valor": "A",
              "res": false
            }
          ],
          "operador": null
        }
      ]
    }
  ]
}
```

**Campo-chave**: `"operador": null` ← Indica que NÃO há operador explícito!

---

### 3.2 Algoritmo de Classificação Semântica

#### Regras de Reconhecimento:

```python
def analisar_semantica_linha(ast_linha):
    """
    Classifica o tipo de operação baseado na estrutura da AST
    """
    sequencia = ast_linha['filhos'][0]
    elementos = sequencia['elementos']
    operador = sequencia['operador']

    # REGRA 1: Dois operandos SEM operador = ATRIBUIÇÃO SIMPLES
    if len(elementos) == 2 and operador is None:
        operando_fonte = elementos[0]
        operando_destino = elementos[1]

        # Validação semântica
        if operando_destino['subtipo'] != 'variavel':
            raise ErroSemantico("Destino de atribuição deve ser variável")

        return {
            'tipo_operacao': 'ATRIBUICAO_SIMPLES',
            'valor_fonte': operando_fonte,
            'variavel_destino': operando_destino['valor']
        }

    # REGRA 2: N operandos COM operador = EXPRESSÃO COM ATRIBUIÇÃO
    elif operador is not None:
        # Último elemento é o destino
        if elementos[-1]['subtipo'] != 'variavel':
            raise ErroSemantico("Resultado de expressão deve ser atribuído a variável")

        return {
            'tipo_operacao': 'EXPRESSAO_COM_OPERADOR',
            'operador': operador,
            'operandos': elementos[:-1],
            'variavel_destino': elementos[-1]['valor']
        }

    # REGRA 3: Um operando sem operador = ERRO
    elif len(elementos) == 1:
        raise ErroSemantico("Expressão incompleta: falta destino ou operador")

    # REGRA 4: Estrutura inválida
    else:
        raise ErroSemantico(f"Estrutura não reconhecida: {len(elementos)} elementos sem operador")
```

---

### 3.3 Tabela de Decisão Semântica

| Estrutura AST | Operandos | Operador | Interpretação Semântica |
|---------------|-----------|----------|-------------------------|
| `(5.5 A)` | 2 | `null` | **ATRIBUIÇÃO SIMPLES** - `A = 5.5` |
| `(X Y)` | 2 | `null` | **ATRIBUIÇÃO SIMPLES** - `Y = X` |
| `((A B +) C)` | 3 | `+` | **EXPRESSÃO** - `C = A + B` |
| `((A B <) R)` | 3 | `<` | **COMPARAÇÃO** - `R = (A < B)` |
| `(A)` | 1 | `null` | **ERRO** - Atribuição sem destino |
| `(5.5)` | 1 | `null` | **ERRO** - Valor sem destino |
| `(A B C)` | 3 | `null` | **ERRO** - 3 elementos sem operador |

---

### 3.4 Validação Semântica Completa

#### Implementação do Validador:

```python
class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = {}
        self.resultados_linhas = []  # Para RES
        self.erros = []

    def validar_atribuicao_simples(self, fonte, destino, numero_linha):
        """
        Valida atribuição simples (valor variavel) e registra na tabela de símbolos
        """
        # 1. Validar tipo do valor fonte
        if fonte['subtipo'] == 'numero_real':
            tipo_fonte = 'FLOAT'
            valor = float(fonte['valor'])

        elif fonte['subtipo'] == 'variavel':
            # Verifica se a variável fonte foi declarada
            if fonte['valor'] not in self.tabela_simbolos:
                raise ErroSemantico(
                    f"Linha {numero_linha}: Variável '{fonte['valor']}' não declarada"
                )
            tipo_fonte = self.tabela_simbolos[fonte['valor']]['tipo']
            valor = None  # Será resolvido em runtime

        elif fonte['subtipo'] == 'LINHA':  # Subexpressão
            tipo_fonte = 'FLOAT'  # Resultado de subexpressão
            valor = None

        else:
            raise ErroSemantico(
                f"Linha {numero_linha}: Tipo de fonte inválido '{fonte['subtipo']}'"
            )

        # 2. Validar RES se presente
        if fonte.get('res'):
            n_linhas = int(fonte['valor'])
            if n_linhas > numero_linha:
                raise ErroSemantico(
                    f"Linha {numero_linha}: RES({n_linhas}) inválido - "
                    f"não há {n_linhas} linhas anteriores"
                )
            # Buscar resultado da linha (numero_linha - n_linhas)
            linha_ref = numero_linha - n_linhas
            if linha_ref < 1 or linha_ref > len(self.resultados_linhas):
                raise ErroSemantico(
                    f"Linha {numero_linha}: RES({n_linhas}) referencia linha inexistente"
                )

        # 3. Validar variável destino
        if destino['subtipo'] != 'variavel':
            raise ErroSemantico(
                f"Linha {numero_linha}: Destino deve ser variável, recebido '{destino['subtipo']}'"
            )

        # 4. Registrar/Atualizar na tabela de símbolos
        self.tabela_simbolos[destino['valor']] = {
            'tipo': tipo_fonte,
            'declarada_linha': numero_linha,
            'escopo': 'GLOBAL',
            'inicializada': True,
            'valor_inicial': valor if valor is not None else 'RUNTIME'
        }

        # 5. Registrar resultado da linha (para RES futuro)
        self.resultados_linhas.append({
            'linha': numero_linha,
            'variavel': destino['valor'],
            'tipo': tipo_fonte
        })

        return {
            'acao': 'ATRIBUICAO_SIMPLES',
            'variavel': destino['valor'],
            'tipo': tipo_fonte,
            'sucesso': True
        }
```

---

### 3.5 Exemplo Completo: Programa com 3 Linhas

#### Código Fonte:
```
(5.5 A)
(3.2 B)
((A B +) C)
```

#### Análise Semântica Linha por Linha:

##### **Linha 1: `(5.5 A)`**

```python
# AST recebido:
{
  "elementos": [
    {"subtipo": "numero_real", "valor": "5.5", "res": false},
    {"subtipo": "variavel", "valor": "A", "res": false}
  ],
  "operador": null
}

# Classificação:
len(elementos) == 2 and operador is None
→ ATRIBUIÇÃO SIMPLES

# Validação:
✓ Fonte: numero_real (5.5) - tipo FLOAT
✓ Destino: variavel (A) - válido

# Ação na Tabela de Símbolos:
tabela_simbolos['A'] = {
    'tipo': 'FLOAT',
    'declarada_linha': 1,
    'escopo': 'GLOBAL',
    'inicializada': True,
    'valor_inicial': 5.5
}

# Resultado:
✅ Linha 1 válida - A = 5.5
```

##### **Linha 2: `(3.2 B)`**

```python
# Classificação:
len(elementos) == 2 and operador is None
→ ATRIBUIÇÃO SIMPLES

# Validação:
✓ Fonte: numero_real (3.2) - tipo FLOAT
✓ Destino: variavel (B) - válido

# Ação na Tabela de Símbolos:
tabela_simbolos['B'] = {
    'tipo': 'FLOAT',
    'declarada_linha': 2,
    'escopo': 'GLOBAL',
    'inicializada': True,
    'valor_inicial': 3.2
}

# Resultado:
✅ Linha 2 válida - B = 3.2
```

##### **Linha 3: `((A B +) C)`**

```python
# AST recebido:
{
  "elementos": [
    {
      "subtipo": "LINHA",  # Subexpressão
      "elementos": [
        {"subtipo": "variavel", "valor": "A"},
        {"subtipo": "variavel", "valor": "B"},
      ],
      "operador": "+"
    },
    {"subtipo": "variavel", "valor": "C"}
  ],
  "operador": null
}

# Classificação:
len(elementos) == 2 and operador is None
→ ATRIBUIÇÃO SIMPLES (subexpressão → variável)

# Validação:
✓ Fonte: LINHA (subexpressão (A B +)) - tipo FLOAT (resultado aritmético)
  ✓ A existe em tabela_simbolos (linha 1)
  ✓ B existe em tabela_simbolos (linha 2)
  ✓ Operador + válido para FLOAT + FLOAT
✓ Destino: variavel (C) - válido

# Ação na Tabela de Símbolos:
tabela_simbolos['C'] = {
    'tipo': 'FLOAT',
    'declarada_linha': 3,
    'escopo': 'GLOBAL',
    'inicializada': True,
    'valor_inicial': 'RUNTIME',  # Calculado em execução
    'dependencias': ['A', 'B']
}

# Resultado:
✅ Linha 3 válida - C = A + B
```

#### Tabela de Símbolos Final:

```python
{
  'A': {'tipo': 'FLOAT', 'linha': 1, 'valor': 5.5},
  'B': {'tipo': 'FLOAT', 'linha': 2, 'valor': 3.2},
  'C': {'tipo': 'FLOAT', 'linha': 3, 'valor': 'RUNTIME', 'deps': ['A', 'B']}
}
```

---

## 🧩 Parte 4: Comparação Detalhada - MEM vs RES

### 4.1 Tabela Comparativa

| Característica | MEM | RES |
|----------------|-----|-----|
| **Natureza** | Conceito semântico | Token sintático |
| **Aparece na expressão?** | ❌ Não (implícito) | ✅ Sim `(2 RES)` |
| **É palavra-chave?** | ❌ Não | ✅ Sim |
| **Na gramática LL(1)?** | ❌ Não (implícito em VARIAVEL) | ✅ Sim (`OPERANDO_OPCIONAL → res`) |
| **Mapeamento de token?** | ❌ Não tem | ✅ Sim (`Tipo_de_Token.RES`) |
| **Altera significado?** | ❌ Não | ✅ Sim (número → referência) |
| **Quando resolve?** | RA3 (atribuição) + RA1 (endereço) | RA3 (busca resultado anterior) |
| **Obrigatório?** | ❌ Não | ❌ Não (produção epsilon) |

---

### 4.2 Exemplos Práticos

#### Exemplo 1: Uso de MEM (Implícito)

```
Código: (5.5 A)

Tokenização (RA1):
  Token 1: ( → ABRE_PARENTESES
  Token 2: 5.5 → NUMERO_REAL (valor: 5.5)
  Token 3: A → VARIAVEL (valor: A)
  Token 4: ) → FECHA_PARENTESES

Sintaxe (RA2):
  Derivação: LINHA → ( SEQUENCIA )
             SEQUENCIA → OPERANDO SEQUENCIA_PRIME
             OPERANDO → numero_real epsilon
             SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME
             OPERANDO → variavel epsilon
             SEQUENCIA_PRIME → epsilon  ← SEM OPERADOR

  ✅ Aceito sintaticamente

Semântica (RA3):
  Classificação: 2 operandos + sem operador = ATRIBUIÇÃO
  Ação: A = 5.5 (armazenado em MEM)

  ✅ Válido semanticamente

Assembly (RA1):
  LDI R16, 5.5
  STS A_MEM, R16    ← MEM aparece aqui!
```

#### Exemplo 2: Uso de RES (Explícito)

```
Código:
  Linha 1: (10.0 X)
  Linha 2: (20.0 Y)
  Linha 3: (2 RES Z)    ← Recupera linha 1 (3 - 2 = 1)

Tokenização (RA1) - Linha 3:
  Token 1: ( → ABRE_PARENTESES
  Token 2: 2 → NUMERO_REAL (valor: 2)
  Token 3: RES → RES  ← PALAVRA-CHAVE
  Token 4: Z → VARIAVEL (valor: Z)
  Token 5: ) → FECHA_PARENTESES

Sintaxe (RA2) - Linha 3:
  Derivação: LINHA → ( SEQUENCIA )
             SEQUENCIA → OPERANDO SEQUENCIA_PRIME
             OPERANDO → numero_real OPERANDO_OPCIONAL
             OPERANDO_OPCIONAL → res  ← RES reconhecido!
             SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME
             OPERANDO → variavel epsilon
             SEQUENCIA_PRIME → epsilon

  ✅ Aceito sintaticamente

Semântica (RA3) - Linha 3:
  Classificação: 2 operandos (2 RES) + sem operador = ATRIBUIÇÃO
  RES ativo: sim (n = 2)
  Linha referenciada: 3 - 2 = 1
  Valor da linha 1: X = 10.0
  Ação: Z = 10.0 (recuperado de MEM de X)

  ✅ Válido semanticamente

Assembly (RA1) - Linha 3:
  LDS R16, X_MEM     ; Carrega X (resultado linha 1)
  STS Z_MEM, R16     ; Armazena em Z
```

---

### 4.3 Por que a Diferença?

#### MEM não precisa de token porque:
1. **Tipo implícito**: Todo identificador maiúsculo é variável (MEM)
2. **Ação óbvia**: `(valor variável)` só pode ser atribuição
3. **Não altera semântica**: A variável já "é" memória por definição
4. **Redundante**: Adicionar MEM seria como escrever `int x int;` em C

#### RES precisa de token porque:
1. **Modificador de semântica**: `2` ≠ `2 RES`
2. **Ambiguidade sem ele**: `(2 A)` seria ambíguo (atribuir 2 ou linha 2?)
3. **Referência temporal**: Requer busca histórica em runtime
4. **Não inferível**: Impossível deduzir sem palavra-chave explícita

---

## 🧩 Parte 5: Validação com Testes

### 5.1 Testes de Atribuição Simples

#### Arquivo: `inputs/RA2/teste_atribuicao.txt`

```
(5.5 A)
(10.0 B)
(-3.14 C)
(0.0 ZERO)
(999.999 MAX)
```

#### Resultado Esperado (RA2):

```
Linha 1: (5.5 A)          → ✅ 9 passos de derivação
Linha 2: (10.0 B)         → ✅ 9 passos de derivação
Linha 3: (-3.14 C)        → ✅ 9 passos de derivação
Linha 4: (0.0 ZERO)       → ✅ 9 passos de derivação
Linha 5: (999.999 MAX)    → ✅ 9 passos de derivação

RESULTADO: 5/5 SUCESSOS (100%)
```

#### Resultado Esperado (RA3):

```
Tabela de Símbolos:
  A:    FLOAT = 5.5    (linha 1)
  B:    FLOAT = 10.0   (linha 2)
  C:    FLOAT = -3.14  (linha 3)
  ZERO: FLOAT = 0.0    (linha 4)
  MAX:  FLOAT = 999.999 (linha 5)

Análise Semântica: ✅ 5/5 atribuições válidas
```

---

### 5.2 Testes de Atribuição com Expressões

#### Arquivo: `inputs/RA2/teste_atribuicao_expressoes.txt`

```
(5.5 A)
(3.2 B)
((A B +) C)
((A B -) D)
((A B *) E)
```

#### Resultado Esperado (RA3):

```
Linha 1: (5.5 A)          → ATRIBUIÇÃO SIMPLES    A = 5.5
Linha 2: (3.2 B)          → ATRIBUIÇÃO SIMPLES    B = 3.2
Linha 3: ((A B +) C)      → ATRIBUIÇÃO EXPRESSÃO  C = A + B = 8.7
Linha 4: ((A B -) D)      → ATRIBUIÇÃO EXPRESSÃO  D = A - B = 2.3
Linha 5: ((A B *) E)      → ATRIBUIÇÃO EXPRESSÃO  E = A * B = 17.6

Tabela de Símbolos:
  A: FLOAT = 5.5     (linha 1)
  B: FLOAT = 3.2     (linha 2)
  C: FLOAT = RUNTIME (linha 3, deps: [A, B])
  D: FLOAT = RUNTIME (linha 4, deps: [A, B])
  E: FLOAT = RUNTIME (linha 5, deps: [A, B])

Análise Semântica: ✅ 5/5 válidas (2 simples + 3 expressões)
```

---

### 5.3 Testes de Erro Semântico

#### Arquivo: `inputs/RA2/teste_erros_semanticos.txt`

```
(A)              # Erro: falta destino
(5.5)            # Erro: falta destino
(A B C)          # Erro: 3 elementos sem operador
(5.5 10.0)       # Erro: destino não é variável
((X Y +) Z)      # Erro: X não declarado
```

#### Resultado Esperado (RA3):

```
Linha 1: (A)              → ❌ ERRO: Expressão incompleta (falta destino)
Linha 2: (5.5)            → ❌ ERRO: Expressão incompleta (falta destino)
Linha 3: (A B C)          → ❌ ERRO: 3 elementos sem operador
Linha 4: (5.5 10.0)       → ❌ ERRO: Destino deve ser variável, recebido 'numero_real'
Linha 5: ((X Y +) Z)      → ❌ ERRO: Variável 'X' não declarada (linha 5)

Análise Semântica: ❌ 0/5 válidas (5 erros detectados)
```

---

## 🧩 Parte 6: Estrutura Proposta para RA3

### 6.1 Arquitetura do Analisador Semântico

```
src/RA3/
├── functions/
│   └── python/
│       ├── analisadorSemantico.py     # Classe principal
│       ├── tabelaSimbolos.py          # Gerenciamento de símbolos
│       ├── validadorTipos.py          # Verificação de tipos
│       ├── processadorRES.py          # Lógica de RES
│       └── errosSemanticos.py         # Exceções customizadas
└── outputs/
    ├── tabela_simbolos.json           # Tabela de símbolos gerada
    ├── erros_semanticos.txt           # Log de erros
    └── codigo_intermediario.txt       # Código intermediário (opcional)
```

---

### 6.2 Classe Principal: AnalisadorSemantico

```python
# src/RA3/functions/python/analisadorSemantico.py

import json
from typing import List, Dict, Any
from .tabelaSimbolos import TabelaSimbolos
from .errosSemanticos import ErroSemantico

class AnalisadorSemantico:
    """
    Analisador semântico para linguagem RPN pós-fixada.
    Valida tipos, declarações e escopo.
    """

    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        self.resultados_linhas = []  # Para RES
        self.erros = []
        self.linha_atual = 0

    def analisar_programa(self, caminho_ast_json: str) -> Dict[str, Any]:
        """
        Analisa programa completo a partir do JSON da AST

        Args:
            caminho_ast_json: Caminho para outputs/RA2/arvore_sintatica.json

        Returns:
            Dicionário com resultados da análise semântica
        """
        # Carregar AST
        with open(caminho_ast_json, 'r', encoding='utf-8') as f:
            ast = json.load(f)

        # Analisar cada linha
        for linha_ast in ast['linhas']:
            self.linha_atual = linha_ast['numero_linha']
            try:
                resultado = self._analisar_linha(linha_ast)
                self.resultados_linhas.append(resultado)
            except ErroSemantico as e:
                self.erros.append({
                    'linha': self.linha_atual,
                    'erro': str(e),
                    'tipo': e.__class__.__name__
                })

        # Gerar relatório
        return {
            'sucesso': len(self.erros) == 0,
            'total_linhas': len(ast['linhas']),
            'linhas_validas': len(self.resultados_linhas) - len(self.erros),
            'erros': self.erros,
            'tabela_simbolos': self.tabela_simbolos.exportar()
        }

    def _analisar_linha(self, linha_ast: Dict) -> Dict:
        """Analisa uma linha e classifica a operação"""
        sequencia = linha_ast['filhos'][0]
        elementos = sequencia['elementos']
        operador = sequencia.get('operador')

        # ATRIBUIÇÃO SIMPLES: (valor variavel)
        if len(elementos) == 2 and operador is None:
            return self._processar_atribuicao_simples(elementos[0], elementos[1])

        # EXPRESSÃO COM OPERADOR: (op1 op2 ... OPERADOR variavel)
        elif operador is not None:
            return self._processar_expressao(elementos[:-1], operador, elementos[-1])

        # ESTRUTURA DE CONTROLE: ((cond)(corpo) WHILE)
        elif self._eh_estrutura_controle(elementos):
            return self._processar_estrutura_controle(elementos, operador)

        else:
            raise ErroSemantico(f"Estrutura não reconhecida: {len(elementos)} elementos sem operador")

    def _processar_atribuicao_simples(self, fonte: Dict, destino: Dict) -> Dict:
        """Processa atribuição simples (valor variavel)"""
        # Validar destino
        if destino['subtipo'] != 'variavel':
            raise ErroSemantico(
                f"Destino de atribuição deve ser variável, recebido '{destino['subtipo']}'"
            )

        # Determinar tipo da fonte
        tipo_fonte = self._determinar_tipo(fonte)

        # Registrar na tabela de símbolos
        self.tabela_simbolos.adicionar_ou_atualizar(
            nome=destino['valor'],
            tipo=tipo_fonte,
            linha=self.linha_atual,
            valor_inicial=fonte.get('valor') if fonte['subtipo'] == 'numero_real' else None
        )

        return {
            'tipo_operacao': 'ATRIBUICAO_SIMPLES',
            'variavel': destino['valor'],
            'tipo': tipo_fonte,
            'linha': self.linha_atual
        }

    def _determinar_tipo(self, operando: Dict) -> str:
        """Determina o tipo de um operando"""
        if operando['subtipo'] == 'numero_real':
            return 'FLOAT'
        elif operando['subtipo'] == 'variavel':
            if operando['valor'] not in self.tabela_simbolos:
                raise ErroSemantico(f"Variável '{operando['valor']}' não declarada")
            return self.tabela_simbolos.obter(operando['valor'])['tipo']
        elif operando['subtipo'] == 'LINHA':
            return 'FLOAT'  # Resultado de subexpressão
        else:
            raise ErroSemantico(f"Tipo de operando desconhecido: '{operando['subtipo']}'")
```

---

## 🔗 Referências

### Documentos de Especificação

- **Fase 1**: `docs/RA1/documents/Comandos_Fase_1.pdf`
- **Fase 2**: `docs/RA2/documents/Comandos_Fase_2.pdf`
- **Fase 3**: `docs/RA3/documents/Comandos_Fase_3.pdf`

### Arquivos do Projeto Relacionados

- **Gramática LL(1)**: `src/RA2/functions/python/configuracaoGramatica.py`
- **Parser LL(1)**: `src/RA2/functions/python/parsear.py`
- **Gerador de Árvores**: `src/RA2/functions/python/gerarArvore.py`
- **Tabela LL(1)**: `src/RA2/functions/python/construirTabelaLL1.py`

### Testes

- **Testes Elaborados**: `inputs/RA2/teste_parser_elaborado.txt` (31 linhas, 100% sucesso)
- **Testes Simples**: `inputs/RA2/teste_parser_simples.txt`

---

## 📊 Resumo Executivo

### Por que MEM não é um terminal?

✅ **MEM é um conceito semântico** que descreve o tipo da variável, não uma palavra-chave sintática.

✅ **A gramática usa epsilon** em `SEQUENCIA_PRIME` para permitir atribuições sem operador explícito.

✅ **A estrutura `(valor variavel)` é auto-explicativa** - não precisa de token MEM.

✅ **MEM é resolvido em 3 fases**:
- RA1: Gera endereços de memória (`A_MEM`)
- RA2: Reconhece sintaxe válida via epsilon
- RA3: Classifica como atribuição semanticamente

✅ **Diferente de RES**, que altera o significado do operando e precisa ser explícito.

---

### Papel do Epsilon

✅ **Permite atribuições simples** sem exigir operador.

✅ **Mantém a gramática LL(1)** sem conflitos (95 entradas válidas).

✅ **Habilita notação RPN pura** onde `(valor variavel)` → atribuição implícita.

✅ **Derivação crítica**: `SEQUENCIA_PRIME → epsilon` quando lookahead é `)`.

---

### Próximos Passos

1. ✅ **RA2 Completo**: Parser 100% funcional (31/31 testes)
2. ⚠️ **Pendente**: Exportação JSON da AST (`outputs/RA2/arvore_sintatica.json`)
3. 🔜 **RA3 Planejado**: Implementar análise semântica baseada neste documento

---

**Fim do Documento**

---

**Criado por**: Claude (Anthropic) - Sonnet 4.5
**Data**: 2025-10-22
**Versão**: 1.0
**Projeto**: Compilador RA3_1
