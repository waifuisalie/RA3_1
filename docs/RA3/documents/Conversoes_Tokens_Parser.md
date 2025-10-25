# 🔄 Conversões de Tokens no Parser LL(1)

> **Documento Técnico**: Explicação do fluxo de conversões entre tokens teóricos (gramática) e tokens reais (implementação) no parser LL(1).

---

## 📌 Informações do Documento

**Projeto**: Compilador RA3_1
**Disciplina**: Compiladores (2025-2)
**Tópico**: Conversões de Tokens - Teórico ↔ Real
**Criado em**: 2025-10-22

---

## 🎯 Visão Geral: 3 Representações de Tokens

O projeto usa **três representações diferentes** para o mesmo token:

| Representação | Tipo | Exemplo | Onde é Usado |
|---------------|------|---------|--------------|
| **1. Enum RA1** | `Tipo_de_Token` | `Tipo_de_Token.SOMA` | Analisador Léxico (RA1) |
| **2. Símbolo Real** | String | `'+'` | Tabela LL(1), entrada do parser |
| **3. Símbolo Teórico** | String | `'soma'` | Gramática, derivações, documentação |

### Por que 3 Representações?

1. **Enum RA1**: Permite type-safety no Python, identificação única sem ambiguidade
2. **Símbolo Real**: Formato conciso para tabela LL(1), próximo ao código-fonte
3. **Símbolo Teórico**: Legibilidade humana, evita confusão (`|` vs `divisao_real`)

---

## 🔧 Parte 1: TIPO_PARA_SIMBOLO (RA1 → Parser)

### 1.1 Definição (parsear.py, linhas 17-42)

```python
TIPO_PARA_SIMBOLO = {
    Tipo_de_Token.NUMERO_REAL: 'number',      # Enum → Real
    Tipo_de_Token.VARIAVEL: 'identifier',
    Tipo_de_Token.ABRE_PARENTESES: '(',
    Tipo_de_Token.SOMA: '+',
    Tipo_de_Token.SUBTRACAO: '-',
    Tipo_de_Token.MULTIPLICACAO: '*',
    Tipo_de_Token.DIVISAO_INTEIRA: '/',
    Tipo_de_Token.DIVISAO_REAL: '|',
    # ... 27 mapeamentos totais
}
```

### 1.2 Propósito

**Converter enums do RA1 para símbolos que a tabela LL(1) entende.**

### 1.3 Uso no Parser (parsear.py, linhas 52-60)

```python
def parsear(tabela_ll1: Dict, tokens_linha: List[Token]) -> List[str]:
    entrada = []
    for token in tokens_linha:
        # Lookup direto usando o TIPO do token (enum)
        simbolo = TIPO_PARA_SIMBOLO.get(token.tipo)

        if simbolo:
            entrada.append(simbolo)
        else:
            # Fallback: usa valor em minúsculas
            entrada.append(str(token.valor).lower())

    entrada.append('$')  # Fim de cadeia
    # ... continua parsing
```

### 1.4 Exemplo de Conversão

#### Entrada (RA1):
```python
tokens_linha = [
    Token(Tipo_de_Token.NUMERO_REAL, '5.5'),
    Token(Tipo_de_Token.VARIAVEL, 'A'),
    Token(Tipo_de_Token.SOMA, '+')
]
```

#### Conversão (TIPO_PARA_SIMBOLO):
```python
# Token 1:
TIPO_PARA_SIMBOLO.get(Tipo_de_Token.NUMERO_REAL) → 'number'

# Token 2:
TIPO_PARA_SIMBOLO.get(Tipo_de_Token.VARIAVEL) → 'identifier'

# Token 3:
TIPO_PARA_SIMBOLO.get(Tipo_de_Token.SOMA) → '+'
```

#### Saída (entrada do parser):
```python
entrada = ['number', 'identifier', '+', '$']
```

**Essa lista é usada para consultar a tabela LL(1)!**

---

## 🔧 Parte 2: MAPEAMENTO_TOKENS (Teórico ↔ Real)

### 2.1 Definição (configuracaoGramatica.py, linhas 43-68)

```python
MAPEAMENTO_TOKENS = {
    # Teórico → Real
    'numero_real': 'number',
    'variavel': 'identifier',
    'abre_parenteses': '(',
    'fecha_parenteses': ')',
    'soma': '+',
    'subtracao': '-',
    'multiplicacao': '*',
    'divisao_inteira': '/',
    'divisao_real': '|',
    'resto': '%',
    'potencia': '^',
    'menor': '<',
    'maior': '>',
    'igual': '==',
    # ... 27 mapeamentos totais
}
```

### 2.2 Propósito

**Converter entre nomes descritivos (gramática) e símbolos concisos (implementação).**

### 2.3 Conversão Teórico → Real (Construção da Tabela LL(1))

#### Função: `mapear_gramatica_para_tokens_reais()` (configuracaoGramatica.py, linhas 75-91)

```python
def mapear_gramatica_para_tokens_reais(gramatica_teorica):
    """Converte gramática com tokens teóricos para tokens reais"""
    gramatica_real = {}

    for nt, producoes in gramatica_teorica.items():
        gramatica_real[nt] = []
        for producao in producoes:
            producao_real = []
            for simbolo in producao:
                # Se é um token teórico, mapeia para o real
                if simbolo in MAPEAMENTO_TOKENS:
                    producao_real.append(MAPEAMENTO_TOKENS[simbolo])
                else:
                    producao_real.append(simbolo)
            gramatica_real[nt].append(producao_real)

    return gramatica_real
```

#### Exemplo:
```python
# Gramática ANTES (teórica):
'ARITH_OP': [['soma'], ['subtracao'], ['multiplicacao']]

# Gramática DEPOIS (real):
'ARITH_OP': [['+'], ['-'], ['*']]

# Usado para construir tabela LL(1):
M[ARITH_OP, +] = ['+']     # ← Símbolo real na tabela
M[ARITH_OP, -] = ['-']
M[ARITH_OP, *] = ['*']
```

---

### 2.4 Conversão Real → Teórico (Exibição de Derivações)

#### Uso no Parser (parsear.py, linhas 102-113)

```python
# Ao gerar derivação para exibição:
if producao == ['epsilon']:
    derivacao.append(f"{topo} → ε")
else:
    # Mapear produção para símbolos teóricos usando mapeamento REVERSO
    producao_teorica = []
    for simbolo in producao:
        # Buscar mapeamento reverso
        simbolo_teorico = None
        for teorico, real in MAPEAMENTO_TOKENS.items():
            if real == simbolo:
                simbolo_teorico = teorico
                break
        producao_teorica.append(simbolo_teorico if simbolo_teorico else simbolo)

    derivacao.append(f"{topo} → {' '.join(producao_teorica)}")
```

#### Exemplo:

**Produção da tabela LL(1) (real)**:
```python
M[ARITH_OP, +] = ['+']
```

**Conversão para derivação (teórico)**:
```python
# simbolo = '+'
for teorico, real in MAPEAMENTO_TOKENS.items():
    if real == '+':  # Encontrado!
        simbolo_teorico = 'soma'
        break

# Derivação exibida:
"ARITH_OP → soma"  # Em vez de "ARITH_OP → +"
```

**Por quê?** Derivações com `soma` são mais legíveis que `+` em contextos formais.

---

### 2.5 Conversão Teórico → Real (Visualização de Árvores)

#### Uso em gerarArvore.py (linhas 40, 46)

```python
def construir_no(simbolo_esperado):
    if index[0] >= len(producoes):
        # Converte nome do token TEÓRICO para valor REAL
        valor_real = MAPEAMENTO_TOKENS.get(simbolo_esperado, simbolo_esperado)
        return NoArvore(valor_real)

    lhs, rhs = producoes[index[0]]
    if lhs != simbolo_esperado:
        # Converte TEÓRICO → REAL para exibição
        valor_real = MAPEAMENTO_TOKENS.get(simbolo_esperado, simbolo_esperado)
        return NoArvore(valor_real)
    # ... continua
```

#### Exemplo:

**Derivação usa símbolos teóricos**:
```
ARITH_OP → soma
```

**Árvore ASCII exibe símbolos reais**:
```
ARITH_OP
└── +    ← Convertido de 'soma' para '+'
```

**Por quê?** Árvores com `+` são mais intuitivas que `soma` visualmente.

---

## 🔄 Parte 3: Fluxo Completo de Conversões

### 3.1 Exemplo: Processar `(5.5 A +)`

#### **Passo 1: Análise Léxica (RA1)**

```python
# Entrada: "5.5 A +"
# Saída (RA1):
tokens = [
    Token(Tipo_de_Token.ABRE_PARENTESES, '('),
    Token(Tipo_de_Token.NUMERO_REAL, '5.5'),
    Token(Tipo_de_Token.VARIAVEL, 'A'),
    Token(Tipo_de_Token.SOMA, '+'),
    Token(Tipo_de_Token.FECHA_PARENTESES, ')')
]
```

**Representação**: `Enum RA1` (Tipo_de_Token)

---

#### **Passo 2: Conversão RA1 → Parser (TIPO_PARA_SIMBOLO)**

```python
# parsear.py, linhas 52-60
entrada = []
for token in tokens:
    simbolo = TIPO_PARA_SIMBOLO.get(token.tipo)
    entrada.append(simbolo)

# Resultado:
entrada = ['(', 'number', 'identifier', '+', ')', '$']
```

**Representação**: `Símbolo Real` (string)

---

#### **Passo 3: Parsing LL(1) (Usa Símbolos Reais)**

```python
# Parser consulta tabela LL(1) com símbolos reais
pilha = ['$', 'PROGRAM']
indice = 0

# Exemplo de consulta:
topo = 'ARITH_OP'
simbolo_entrada = '+'  # ← Símbolo REAL
producao = tabela_ll1[topo][simbolo_entrada]  # M[ARITH_OP, +] = ['+']
```

**Tabela LL(1) usa símbolos REAIS**:
```python
M[ARITH_OP, +] = ['+']
M[ARITH_OP, -] = ['-']
M[OPERANDO, number] = ['number', 'OPERANDO_OPCIONAL']
```

---

#### **Passo 4: Geração de Derivação (Real → Teórico)**

```python
# parsear.py, linhas 102-113
# Produção da tabela (real):
producao = ['+']

# Conversão para exibição (teórico):
for teorico, real in MAPEAMENTO_TOKENS.items():
    if real == '+':
        simbolo_teorico = 'soma'
        break

# Derivação adicionada:
derivacao.append("ARITH_OP → soma")
```

**Representação**: `Símbolo Teórico` (string descritiva)

---

#### **Passo 5: Visualização da Árvore (Teórico → Real)**

```python
# gerarArvore.py, linha 40
# Derivação usa teórico:
derivacao = ["ARITH_OP → soma"]

# Ao construir nó da árvore:
simbolo_esperado = 'soma'
valor_real = MAPEAMENTO_TOKENS.get('soma', 'soma')  # → '+'

# Árvore exibida:
ARITH_OP
└── +    ← Convertido de volta para REAL
```

**Representação**: `Símbolo Real` (string concisa)

---

### 3.2 Diagrama de Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUXO DE CONVERSÕES                          │
└─────────────────────────────────────────────────────────────────┘

[1] CÓDIGO FONTE
    "(5.5 A +)"
        │
        ▼
[2] ANÁLISE LÉXICA (RA1)
    Token(Tipo_de_Token.SOMA, '+')  ← ENUM
        │
        │ TIPO_PARA_SIMBOLO
        ▼
[3] ENTRADA DO PARSER
    entrada = ['+']  ← SÍMBOLO REAL
        │
        ▼
[4] TABELA LL(1)
    M[ARITH_OP, +] = ['+']  ← SÍMBOLOS REAIS
        │
        │ MAPEAMENTO_TOKENS (reverso)
        ▼
[5] DERIVAÇÃO (para exibição)
    "ARITH_OP → soma"  ← SÍMBOLO TEÓRICO
        │
        │ MAPEAMENTO_TOKENS (direto)
        ▼
[6] ÁRVORE ASCII
    ARITH_OP
    └── +  ← SÍMBOLO REAL
```

---

## 📊 Parte 4: Por que 3 Representações?

### 4.1 Justificativa Técnica

| Representação | Vantagem | Uso |
|---------------|----------|-----|
| **Enum RA1** | Type-safety, evita strings mágicas | Analisador léxico, validação |
| **Símbolo Real** | Conciso, próximo do código-fonte | Tabela LL(1), parsing eficiente |
| **Símbolo Teórico** | Legível, auto-documentado | Gramática formal, derivações |

---

### 4.2 Exemplo: Operador de Divisão Real

```python
# Enum RA1:
Tipo_de_Token.DIVISAO_REAL
✅ Autocompletar do IDE
✅ Impossível digitar errado

# Símbolo Real:
'|'
✅ Tabela LL(1) compacta
⚠️ Pode confundir com OR lógico

# Símbolo Teórico:
'divisao_real'
✅ Documentação clara
✅ Sem ambiguidade
⚠️ Verboso para tabela LL(1)
```

**Solução**: Usar cada representação no contexto apropriado!

---

### 4.3 Sem Conversões (Problema Hipotético)

#### Opção 1: Usar apenas enums

```python
# Tabela LL(1) com enums:
M[ARITH_OP, Tipo_de_Token.SOMA] = [Tipo_de_Token.SOMA]
❌ Verboso
❌ Mistura conceitos (léxico + sintático)
```

#### Opção 2: Usar apenas símbolos reais

```python
# Derivação:
"ARITH_OP → |"  # Divisão real
❌ Pouco legível
❌ Confuso: | pode ser OR ou divisão

# Parser recebe strings:
entrada = ['+', '-', '|']
❌ Sem type-safety
❌ Erros em tempo de execução
```

#### Opção 3: Usar apenas símbolos teóricos

```python
# Tabela LL(1):
M[ARITH_OP, 'soma'] = ['soma']
M[ARITH_OP, 'subtracao'] = ['subtracao']
M[ARITH_OP, 'multiplicacao'] = ['multiplicacao']
M[ARITH_OP, 'divisao_inteira'] = ['divisao_inteira']
M[ARITH_OP, 'divisao_real'] = ['divisao_real']
❌ Tabela enorme e verbosa
❌ Parsing mais lento (strings longas)
```

**✅ Solução adotada**: Usar cada representação onde faz sentido + conversões automáticas.

---

## 🔧 Parte 5: Implementação das Conversões

### 5.1 Conversão Enum → Real (Usada no Parser)

```python
# src/RA2/functions/python/parsear.py

# Dicionário de mapeamento (linhas 17-42)
TIPO_PARA_SIMBOLO = {
    Tipo_de_Token.NUMERO_REAL: 'number',
    Tipo_de_Token.SOMA: '+',
    # ... 27 mapeamentos
}

# Uso (linhas 52-60)
def parsear(tabela_ll1, tokens_linha):
    entrada = []
    for token in tokens_linha:
        simbolo = TIPO_PARA_SIMBOLO.get(token.tipo)  # ← Conversão direta
        if simbolo:
            entrada.append(simbolo)
    entrada.append('$')
    # ... continua parsing
```

**Complexidade**: O(1) - Lookup em dicionário

---

### 5.2 Conversão Teórico → Real (Construção da Gramática)

```python
# src/RA2/functions/python/configuracaoGramatica.py

def mapear_gramatica_para_tokens_reais(gramatica_teorica):
    """Converte gramática com tokens teóricos para tokens reais"""
    gramatica_real = {}

    for nt, producoes in gramatica_teorica.items():
        gramatica_real[nt] = []
        for producao in producoes:
            producao_real = []
            for simbolo in producao:
                if simbolo in MAPEAMENTO_TOKENS:
                    producao_real.append(MAPEAMENTO_TOKENS[simbolo])  # ← Conversão
                else:
                    producao_real.append(simbolo)
            gramatica_real[nt].append(producao_real)

    return gramatica_real

# Uso:
gramatica_real = mapear_gramatica_para_tokens_reais(GRAMATICA_RPN)
```

**Complexidade**: O(n) - Percorre toda a gramática uma vez

---

### 5.3 Conversão Real → Teórico (Busca Reversa)

```python
# src/RA2/functions/python/parsear.py (linhas 102-113)

# Ao gerar derivação:
producao_teorica = []
for simbolo in producao:
    simbolo_teorico = None

    # Busca reversa no MAPEAMENTO_TOKENS
    for teorico, real in MAPEAMENTO_TOKENS.items():
        if real == simbolo:  # ← Comparação linear
            simbolo_teorico = teorico
            break

    producao_teorica.append(simbolo_teorico if simbolo_teorico else simbolo)

derivacao.append(f"{topo} → {' '.join(producao_teorica)}")
```

**Complexidade**: O(n) - Busca linear no dicionário (poderia ser otimizada)

---

### 5.4 Otimização Possível (Mapeamento Inverso)

```python
# src/RA2/functions/python/configuracaoGramatica.py (linha 96)

def mapear_tokens_reais_para_teoricos(conjunto_ou_dict):
    """Converte tokens reais de volta para tokens teóricos"""
    # Cria mapeamento inverso (uma vez)
    mapeamento_inverso = {v: k for k, v in MAPEAMENTO_TOKENS.items()}

    # Agora conversões são O(1)
    return {mapeamento_inverso.get(token, token) for token in conjunto_ou_dict}
```

**Nota**: Essa função existe mas não é usada no parser atual (linhas 107-110). Poderia otimizar a busca reversa!

---

## 📋 Parte 6: Resumo Executivo

### Fluxo Completo:

```
RA1 (Enum)
    ↓ TIPO_PARA_SIMBOLO
Parser (Real)
    ↓ MAPEAMENTO_TOKENS (reverso)
Derivação (Teórico)
    ↓ MAPEAMENTO_TOKENS (direto)
Árvore (Real)
```

### Tabela de Conversões:

| De → Para | Mapeamento Usado | Função | Arquivo |
|-----------|------------------|--------|---------|
| Enum → Real | `TIPO_PARA_SIMBOLO` | `parsear()` | parsear.py |
| Teórico → Real | `MAPEAMENTO_TOKENS` | `mapear_gramatica_para_tokens_reais()` | configuracaoGramatica.py |
| Real → Teórico | `MAPEAMENTO_TOKENS` (reverso) | Loop manual | parsear.py |
| Teórico → Real | `MAPEAMENTO_TOKENS` | `construir_no()` | gerarArvore.py |

### Por que Usar Conversões?

✅ **Separação de conceitos**: Léxico (enum) ≠ Sintático (real) ≠ Formal (teórico)
✅ **Legibilidade**: Cada contexto usa representação mais apropriada
✅ **Manutenibilidade**: Mudar mapeamento não quebra código
✅ **Performance**: Tabela LL(1) compacta com símbolos reais
✅ **Documentação**: Derivações e gramática com símbolos teóricos descritivos

---

## 🔗 Referências

### Arquivos do Projeto

- **TIPO_PARA_SIMBOLO**: `src/RA2/functions/python/parsear.py` (linhas 17-42)
- **MAPEAMENTO_TOKENS**: `src/RA2/functions/python/configuracaoGramatica.py` (linhas 43-68)
- **Conversões na gramática**: `src/RA2/functions/python/configuracaoGramatica.py` (linhas 75-91)
- **Conversões na árvore**: `src/RA2/functions/python/gerarArvore.py` (linhas 40, 46)
- **Tokens RA1**: `src/RA1/functions/python/tokens.py`

### Documentos Relacionados

- **Atribuição Simples e Epsilon**: `docs/RA3/documents/Atribuicao_Simples_Epsilon.md`
- **Gramática LL(1)**: Documentado em `CLAUDE.md` (linhas 97-123)

---

**Fim do Documento**

---

**Criado por**: Claude (Anthropic) - Sonnet 4.5
**Data**: 2025-10-22
**Versão**: 1.0
**Projeto**: Compilador RA3_1
