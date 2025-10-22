# Teoria Completa: Gramáticas de Atributos (Com Explicações Literais)

**Curso:** Linguagens Formais e Autômatos
**Fase:** RA3 - Análise Semântica
**Grupo:** RA3_1
**Objetivo:** Entender CADA PASSO de uma derivação semântica

---

## 📚 Parte 1: Fundamentos (O Que São Esses Símbolos?)

### 1.1 O Que É Uma Gramática de Atributos?

**Definição Simples:**
Uma gramática de atributos é uma gramática livre de contexto (que você já conhece do RA2) **MAIS** regras que calculam **atributos** (propriedades) de cada símbolo.

**Analogia:**
- **Gramática livre de contexto (RA2):** Verifica se a **FORMA** está correta (sintaxe)
  - Exemplo: `(5 3 +)` tem parênteses balanceados? ✓
- **Gramática de atributos (RA3):** Verifica se o **SIGNIFICADO** faz sentido (semântica)
  - Exemplo: `(5 3 +)` → podemos somar int com int? ✓ Qual o tipo? int

**Definição Formal:**
```
AG = (G, A, R)
```

Onde:
- **G** = gramática livre de contexto que você já conhece
- **A** = conjunto de **atributos** (ex: tipo, valor)
- **R** = **regras semânticas** (como calcular os atributos)

---

### 1.2 Tipos de Atributos (Por Que Existem Dois Tipos?)

#### Atributo Sintetizado (⬆️ Sobe na Árvore)

**O QUE É:**
Um atributo cujo valor é calculado a partir dos **filhos** na árvore sintática.

**POR QUE EXISTE:**
Porque às vezes o tipo de uma expressão depende das partes que a compõem.

**EXEMPLO LITERAL:**
```
Expressão: (5 3 +)

Árvore:
        +
       / \
      5   3

Para saber o tipo de (+):
  1. Olho para baixo (filhos)
  2. Filho esquerdo: 5 → tipo int
  3. Filho direito: 3 → tipo int
  4. Conclusão: + tem tipo int (porque int + int = int)

FLUXO: Filhos → Pai (⬆️ sobe)
ATRIBUTO: tipo (sintetizado)
```

#### Atributo Herdado (⬇️ Desce na Árvore)

**O QUE É:**
Um atributo cujo valor vem do **pai** ou **irmãos** na árvore.

**POR QUE EXISTE:**
Porque às vezes precisamos de contexto externo (ex: em qual escopo estamos?).

**EXEMPLO LITERAL:**
```
Programa:
  Linha 1: (5 X MEM)    ← escopo = 0
  Linha 2: (X 3 +)      ← escopo = 0

Para saber em qual escopo X está:
  1. Olho para cima (contexto do programa)
  2. Programa diz: "estamos no escopo 0"
  3. Conclusão: X tem escopo 0

FLUXO: Pai → Filhos (⬇️ desce)
ATRIBUTO: escopo (herdado)
```

---

### 1.3 A Notação Γ ⊢ (Leia com Atenção!)

#### O Símbolo Γ (Gamma)

**O QUE É:**
Γ é uma **tabela** que mapeia nomes de variáveis para seus tipos.

**PENSE COMO:**
Um dicionário em Python:
```python
Γ = {
    'X': 'int',
    'Y': 'real',
    'FLAG': 'boolean'
}
```

**ESCREVEMOS:**
```
Γ = { X: int, Y: real, FLAG: boolean }
```

**POR QUE EXISTE:**
Porque precisamos lembrar qual tipo cada variável tem. Quando vemos `X` no código, precisamos consultar Γ para saber que `X` é `int`.

---

#### O Símbolo ⊢ (Turnstile)

**LÊ-SE:** "julga" ou "deriva" ou "prova"

**SIGNIFICADO:**
```
Γ ⊢ e : T
```
Lê-se: "No ambiente Γ, a expressão e tem tipo T"

**EXEMPLO LITERAL:**
```
Γ = { X: int }
Γ ⊢ X : int
```
Lê-se: "No ambiente onde X é int, a expressão X tem tipo int"

**POR QUE USAMOS:**
Porque precisamos deixar claro **em qual contexto** estamos fazendo a afirmação. O tipo de X depende do que está em Γ!

---

#### Regras de Inferência (Como Provar Algo)

**FORMATO GERAL:**
```
Premissa 1    Premissa 2    ...    Premissa N
───────────────────────────────────────────────── (Nome da Regra)
                  Conclusão
```

**LEIA COMO:**
"**SE** todas as premissas (coisas acima da linha) são verdadeiras,
 **ENTÃO** a conclusão (coisa abaixo da linha) é verdadeira"

**EXEMPLO CONCRETO:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
──────────────────────────── (ADD)
   Γ ⊢ (5 3 +) : int
```

**TRADUÇÃO LITERAL:**
"**SE** 5 tem tipo int **E** 3 tem tipo int,
 **ENTÃO** (5 3 +) tem tipo int"

**POR QUE ESSA FORMA:**
Porque é uma maneira matemática rigorosa de dizer: "para concluir X, preciso primeiro provar A, B, C".

---

## 📖 Parte 2: As Regras Semânticas (Uma Por Uma)

### 2.1 Regra: INT-LITERAL

**REGRA FORMAL:**
```
─────────────────────────────
Γ ⊢ n : int    (se n ∈ ℤ)
```

**TRADUÇÃO LITERAL:**
"Se n é um número inteiro, então n tem tipo int (em qualquer ambiente Γ)"

**POR QUE NÃO HÁ PREMISSAS:**
Porque não precisamos provar nada antes! Um literal numérico inteiro **sempre** tem tipo int, independente de qualquer coisa.

**EXEMPLOS COM CADA PASSO:**

**Exemplo 1:** `5`
```
PASSO 1: Identificar o que temos
  - Temos: 5
  - É uma constante numérica

PASSO 2: Determinar se é inteiro
  - 5 tem ponto decimal? NÃO
  - 5 ∈ ℤ? SIM (5 é um número inteiro)

PASSO 3: Aplicar a regra INT-LITERAL
  - Premissas: (nenhuma)
  - Conclusão: Γ ⊢ 5 : int

RESULTADO: 5 tem tipo int
```

**Exemplo 2:** `-42`
```
PASSO 1: Identificar
  - Temos: -42
  - É uma constante numérica com sinal negativo

PASSO 2: Determinar se é inteiro
  - -42 tem ponto decimal? NÃO
  - -42 ∈ ℤ? SIM (números negativos são inteiros)

PASSO 3: Aplicar INT-LITERAL
  - Conclusão: Γ ⊢ -42 : int

RESULTADO: -42 tem tipo int
```

---

### 2.2 Regra: REAL-LITERAL

**REGRA FORMAL:**
```
─────────────────────────────────────
Γ ⊢ r : real    (se r ∈ ℝ, r ∉ ℤ)
```

**TRADUÇÃO LITERAL:**
"Se r é um número real (mas NÃO inteiro), então r tem tipo real"

**POR QUE "r ∉ ℤ":**
Porque se fosse inteiro, usaríamos INT-LITERAL! Esta regra é para números COM ponto decimal.

**EXEMPLO COM CADA PASSO:**

**Exemplo:** `3.14`
```
PASSO 1: Identificar
  - Temos: 3.14
  - É uma constante numérica

PASSO 2: Determinar se é real (não-inteiro)
  - 3.14 tem ponto decimal? SIM (.14)
  - 3.14 ∈ ℝ? SIM (é um número real)
  - 3.14 ∈ ℤ? NÃO (não é inteiro)

PASSO 3: Aplicar REAL-LITERAL
  - Conclusão: Γ ⊢ 3.14 : real

RESULTADO: 3.14 tem tipo real
```

---

### 2.3 Regra: VAR (Consulta de Variável)

**REGRA FORMAL:**
```
    x ∈ dom(Γ)    Γ(x) = T
─────────────────────────────
         Γ ⊢ x : T
```

**TRADUÇÃO LITERAL:**
"Se x existe no ambiente Γ e Γ diz que x tem tipo T, então x tem tipo T"

**O QUE SIGNIFICA CADA SÍMBOLO:**
- `x ∈ dom(Γ)` → "x está no domínio de Γ" → "x existe na tabela"
- `Γ(x) = T` → "Γ aplicado a x retorna T" → "o tipo de x em Γ é T"

**EXEMPLO COM CADA PASSO:**

**Setup:** `Γ = { CONTADOR: int, PI: real }`

**Exemplo 1:** Derivar tipo de `CONTADOR`
```
PASSO 1: Verificar se CONTADOR existe em Γ
  - Olho para Γ: { CONTADOR: int, PI: real }
  - CONTADOR está lá? SIM
  - Conclusão: CONTADOR ∈ dom(Γ) ✓

PASSO 2: Consultar o tipo de CONTADOR em Γ
  - Γ(CONTADOR) = ?
  - Olho na tabela: CONTADOR: int
  - Conclusão: Γ(CONTADOR) = int ✓

PASSO 3: Aplicar regra VAR
  - Premissa 1: CONTADOR ∈ dom(Γ) ✓
  - Premissa 2: Γ(CONTADOR) = int ✓
  - Conclusão: Γ ⊢ CONTADOR : int

RESULTADO: CONTADOR tem tipo int
```

**Exemplo 2:** Tentarive derivar tipo de `X` (não existe)
```
PASSO 1: Verificar se X existe em Γ
  - Olho para Γ: { CONTADOR: int, PI: real }
  - X está lá? NÃO
  - Conclusão: X ∉ dom(Γ) ✗

PASSO 2: Posso aplicar a regra VAR?
  - Premissa 1 falhou (X não existe)
  - NÃO posso aplicar a regra

RESULTADO: ERRO! "Variável X não declarada"
```

---

### 2.4 Regra: ADD (Adição - Mesmo Tipo)

**REGRA FORMAL:**
```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : T    T ∈ {int, real}
──────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ +) : T
```

**TRADUÇÃO LITERAL:**
"Se e₁ tem tipo T E e₂ tem tipo T E T é numérico (int ou real), então (e₁ e₂ +) tem tipo T"

**POR QUE TRÊS PREMISSAS:**
1. Primeira premissa: Precisamos saber o tipo de e₁
2. Segunda premissa: Precisamos saber o tipo de e₂
3. Terceira premissa: Precisamos garantir que T é um tipo numérico (não boolean!)

**EXEMPLO COMPLETO COM CADA PASSO:**

**Expressão:** `(5 3 +)`

```
══════════════════════════════════════════════════════════════
OBJETIVO: Provar que Γ ⊢ (5 3 +) : int
══════════════════════════════════════════════════════════════

PASSO 1: Analisar o operando esquerdo (e₁ = 5)
──────────────────────────────────────────────────
SUB-OBJETIVO: Provar que Γ ⊢ 5 : int

  1.1: Identificar que 5 é literal inteiro
       - 5 não tem ponto decimal
       - 5 ∈ ℤ (5 é número inteiro)

  1.2: Aplicar regra INT-LITERAL
       ───────────────────── (INT-LITERAL)
           Γ ⊢ 5 : int

  CONCLUSÃO DO PASSO 1: Γ ⊢ 5 : int ✓


PASSO 2: Analisar o operando direito (e₂ = 3)
──────────────────────────────────────────────────
SUB-OBJETIVO: Provar que Γ ⊢ 3 : int

  2.1: Identificar que 3 é literal inteiro
       - 3 não tem ponto decimal
       - 3 ∈ ℤ

  2.2: Aplicar regra INT-LITERAL
       ───────────────────── (INT-LITERAL)
           Γ ⊢ 3 : int

  CONCLUSÃO DO PASSO 2: Γ ⊢ 3 : int ✓


PASSO 3: Verificar se os tipos são iguais
──────────────────────────────────────────────────
  - Tipo de e₁: int (do PASSO 1)
  - Tipo de e₂: int (do PASSO 2)
  - São iguais? SIM (int = int) ✓
  - T = int


PASSO 4: Verificar se T é tipo numérico
──────────────────────────────────────────────────
  - T = int
  - int ∈ {int, real}? SIM ✓
  - Podemos somar? SIM


PASSO 5: Aplicar regra ADD
──────────────────────────────────────────────────
  Verificar todas as premissas:
    ✓ Γ ⊢ 5 : int       (PASSO 1)
    ✓ Γ ⊢ 3 : int       (PASSO 2)
    ✓ int ∈ {int, real} (PASSO 4)

  Escrever derivação formal:

      Γ ⊢ 5 : int    Γ ⊢ 3 : int    int ∈ {int, real}
      ─────────────────────────────────────────────── (ADD)
                  Γ ⊢ (5 3 +) : int


══════════════════════════════════════════════════════════════
RESULTADO FINAL: (5 3 +) tem tipo int
══════════════════════════════════════════════════════════════
```

---

### 2.5 Regra: ADD-PROMOTE (Adição com Promoção)

**REGRA FORMAL:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
──────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : real
```

**TRADUÇÃO LITERAL:**
"Se e₁ é int E e₂ é real, então (e₁ e₂ +) tem tipo real"

**POR QUE O RESULTADO É REAL:**
Porque quando misturamos int com real, o int é "promovido" para real. É como misturar água (real) com gelo (int) → você fica com água.

**O QUE É "PROMOÇÃO":**
Converter temporariamente um tipo "menor" (int) para um tipo "maior" (real) para fazer a operação.

**EXEMPLO COMPLETO:**

**Expressão:** `(5 3.5 +)`

```
══════════════════════════════════════════════════════════════
OBJETIVO: Provar que Γ ⊢ (5 3.5 +) : real
══════════════════════════════════════════════════════════════

PASSO 1: Analisar operando esquerdo (e₁ = 5)
──────────────────────────────────────────────────
  - 5 não tem ponto decimal
  - 5 ∈ ℤ
  - Aplicar INT-LITERAL

  CONCLUSÃO: Γ ⊢ 5 : int ✓


PASSO 2: Analisar operando direito (e₂ = 3.5)
──────────────────────────────────────────────────
  - 3.5 TEM ponto decimal (.5)
  - 3.5 ∈ ℝ mas 3.5 ∉ ℤ
  - Aplicar REAL-LITERAL

  CONCLUSÃO: Γ ⊢ 3.5 : real ✓


PASSO 3: Os tipos são iguais?
──────────────────────────────────────────────────
  - Tipo de e₁: int
  - Tipo de e₂: real
  - int = real? NÃO ✗

  PERGUNTA: Posso usar a regra ADD normal?
  RESPOSTA: NÃO! ADD requer mesmos tipos.

  PRÓXIMO PASSO: Tentar ADD-PROMOTE


PASSO 4: Verificar se ADD-PROMOTE se aplica
──────────────────────────────────────────────────
  Verificar premissas de ADD-PROMOTE:
    ✓ Γ ⊢ 5 : int   (PASSO 1)
    ✓ Γ ⊢ 3.5 : real (PASSO 2)

  Ambas premissas OK! Posso aplicar ADD-PROMOTE.


PASSO 5: Entender O QUE acontece (Promoção)
──────────────────────────────────────────────────
  ANTES da soma:
    - e₁ = 5 (int)
    - e₂ = 3.5 (real)

  O COMPILADOR FAZ (internamente):
    - Promove 5 (int) para 5.0 (real)
    - Agora: 5.0 (real) + 3.5 (real)
    - Resultado: 8.5 (real)

  POR QUE PROMOVER PARA REAL:
    - real é "maior" que int
    - real pode representar qualquer int
    - int NÃO pode representar qualquer real (ex: 3.5)


PASSO 6: Aplicar ADD-PROMOTE
──────────────────────────────────────────────────
      Γ ⊢ 5 : int    Γ ⊢ 3.5 : real
      ────────────────────────────── (ADD-PROMOTE)
           Γ ⊢ (5 3.5 +) : real


══════════════════════════════════════════════════════════════
RESULTADO FINAL: (5 3.5 +) tem tipo real
POR QUÊ: Quando misturamos int com real, sempre resulta em real
══════════════════════════════════════════════════════════════
```

---

### 2.6 Regra: DIV-INT (Divisão Inteira)

**REGRA FORMAL:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
────────────────────────────────
    Γ ⊢ (e₁ e₂ /) : int
```

**TRADUÇÃO LITERAL:**
"Se AMBOS operandos são int, então divisão inteira (/) resulta em int"

**POR QUE AMBOS DEVEM SER INT:**
Porque `/` é DIVISÃO INTEIRA, não divisão real. Ela trunca o resultado.
- Exemplo: 7 / 2 = 3 (não 3.5)
- Se permitíssemos real, o significado de "/" mudaria!

**EXEMPLO: Derivação Válida**

**Expressão:** `(10 3 /)`

```
══════════════════════════════════════════════════════════════
OBJETIVO: Provar que Γ ⊢ (10 3 /) : int
══════════════════════════════════════════════════════════════

PASSO 1: Verificar e₁ = 10
  - 10 não tem ponto decimal
  - 10 ∈ ℤ
  - Γ ⊢ 10 : int ✓

PASSO 2: Verificar e₂ = 3
  - 3 não tem ponto decimal
  - 3 ∈ ℤ
  - Γ ⊢ 3 : int ✓

PASSO 3: Verificar regra DIV-INT
  - Premissa 1: Γ ⊢ 10 : int ✓
  - Premissa 2: Γ ⊢ 3 : int ✓
  - AMBOS são int? SIM ✓

PASSO 4: Aplicar DIV-INT
      Γ ⊢ 10 : int    Γ ⊢ 3 : int
      ────────────────────────────── (DIV-INT)
           Γ ⊢ (10 3 /) : int

PASSO 5: O que acontece em tempo de execução?
  - 10 / 3 = 3.333...
  - MAS: divisão inteira TRUNCA
  - Resultado: 3 (int)

══════════════════════════════════════════════════════════════
RESULTADO FINAL: (10 3 /) tem tipo int, valor 3
══════════════════════════════════════════════════════════════
```

**EXEMPLO: Derivação INVÁLIDA (Erro Semântico)**

**Expressão:** `(10.5 3 /)`

```
══════════════════════════════════════════════════════════════
OBJETIVO: Tentar provar que Γ ⊢ (10.5 3 /) : ???
══════════════════════════════════════════════════════════════

PASSO 1: Verificar e₁ = 10.5
  - 10.5 TEM ponto decimal
  - 10.5 ∈ ℝ mas 10.5 ∉ ℤ
  - Γ ⊢ 10.5 : real ✓

  ATENÇÃO: Tipo é REAL, não INT!

PASSO 2: Verificar e₂ = 3
  - 3 não tem ponto decimal
  - Γ ⊢ 3 : int ✓

PASSO 3: Tentar aplicar DIV-INT
  - Regra DIV-INT requer: Γ ⊢ e₁ : int
  - Temos: Γ ⊢ e₁ : real
  - real = int? NÃO ✗

  CONCLUSÃO: Premissa 1 FALHA!

PASSO 4: Por que não posso aplicar a regra?
  - DIV-INT exige AMBOS int
  - Temos: real e int
  - real ≠ int

  ANALOGIA: É como tentar encaixar peça redonda em buraco quadrado

PASSO 5: Há outra regra que funcione?
  - ADD-PROMOTE? NÃO (isso é para adição)
  - DIV-REAL (operador |)? SIM! Mas não é isso que temos

  CONCLUSÃO: NÃO HÁ REGRA QUE SE APLIQUE

══════════════════════════════════════════════════════════════
RESULTADO FINAL: ERRO SEMÂNTICO!
MENSAGEM: "Divisão inteira (/) requer ambos operandos int,
           mas encontrado real e int"
SOLUÇÃO: Use | para divisão real: (10.5 3 |) : real
══════════════════════════════════════════════════════════════
```

---

## 📝 Parte 3: Exercícios Com Soluções MUITO Detalhadas

### Exercício 3.1: Derivação Básica

**Questão:** Derive o tipo de `(7 2 +)`

**Solução Passo-a-Passo:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (7 2 +)
AMBIENTE: Γ = {} (vazio - não há variáveis)
══════════════════════════════════════════════════════════════

ETAPA 1: Decompor a expressão
──────────────────────────────────────────────────
  Formato RPN: (operando1 operando2 operador)
  - operando1 (e₁) = 7
  - operando2 (e₂) = 2
  - operador = +


ETAPA 2: Derivar tipo de e₁ (7)
──────────────────────────────────────────────────
  2.1: O que é 7?
       - É um literal numérico
       - Não tem ponto decimal
       - 7 ∈ ℤ (sim, 7 é inteiro)

  2.2: Qual regra usar?
       - É literal? SIM
       - É inteiro? SIM
       - REGRA: INT-LITERAL

  2.3: Aplicar INT-LITERAL
       ───────────────────── (INT-LITERAL)
           Γ ⊢ 7 : int

  CONCLUSÃO ETAPA 2: Γ ⊢ 7 : int ✓


ETAPA 3: Derivar tipo de e₂ (2)
──────────────────────────────────────────────────
  3.1: O que é 2?
       - É um literal numérico
       - Não tem ponto decimal
       - 2 ∈ ℤ

  3.2: Qual regra usar?
       - INT-LITERAL (mesmo raciocínio da etapa 2)

  3.3: Aplicar INT-LITERAL
       ───────────────────── (INT-LITERAL)
           Γ ⊢ 2 : int

  CONCLUSÃO ETAPA 3: Γ ⊢ 2 : int ✓


ETAPA 4: Escolher regra para combinação
──────────────────────────────────────────────────
  4.1: O que temos?
       - e₁ : int (etapa 2)
       - e₂ : int (etapa 3)
       - Operador: +

  4.2: Tipos são iguais?
       - int = int? SIM

  4.3: Qual regra usar?
       - Opção 1: ADD (para tipos iguais)
       - Opção 2: ADD-PROMOTE (para int + real)
       - Escolhemos: ADD (porque ambos são int)


ETAPA 5: Verificar premissas de ADD
──────────────────────────────────────────────────
  Regra ADD:
      Γ ⊢ e₁ : T    Γ ⊢ e₂ : T    T ∈ {int, real}
      ──────────────────────────────────────────────
                 Γ ⊢ (e₁ e₂ +) : T

  Verificar cada premissa:
    Premissa 1: Γ ⊢ 7 : int
                Temos isso? SIM (etapa 2) ✓
                T = int

    Premissa 2: Γ ⊢ 2 : int
                Temos isso? SIM (etapa 3) ✓
                T = int (mesmo da premissa 1!)

    Premissa 3: int ∈ {int, real}
                int está no conjunto {int, real}? SIM ✓


ETAPA 6: Aplicar ADD
──────────────────────────────────────────────────
  Todas as premissas OK, posso concluir:

      Γ ⊢ 7 : int    Γ ⊢ 2 : int    int ∈ {int, real}
      ─────────────────────────────────────────────── (ADD)
                  Γ ⊢ (7 2 +) : int


ETAPA 7: Árvore de Derivação Completa
──────────────────────────────────────────────────
                  ───────────────────── (INT)    ───────────────────── (INT)
                      Γ ⊢ 7 : int                    Γ ⊢ 2 : int
                  ─────────────────────────────────────────────────────────
                               Γ ⊢ (7 2 +) : int (ADD)


══════════════════════════════════════════════════════════════
RESPOSTA FINAL: (7 2 +) tem tipo int
══════════════════════════════════════════════════════════════
```

---

### Exercício 3.2: Derivação com Promoção

**Questão:** Derive o tipo de `(5 3.5 +)`. Por que o resultado não é int?

**Solução Completa:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 3.5 +)
OBJETIVO: Derivar tipo E explicar por que não é int
══════════════════════════════════════════════════════════════

PASSO 1: Derivar tipo de 5
  ───────────────────── (INT-LITERAL)
      Γ ⊢ 5 : int

PASSO 2: Derivar tipo de 3.5
  ───────────────────── (REAL-LITERAL)
      Γ ⊢ 3.5 : real

  POR QUE REAL: 3.5 tem ponto decimal (.5)

PASSO 3: Tentar aplicar ADD normal
  Regra ADD requer: Γ ⊢ e₁ : T  e  Γ ⊢ e₂ : T
  Temos: Γ ⊢ 5 : int  e  Γ ⊢ 3.5 : real

  int = real? NÃO! ✗

  CONCLUSÃO: NÃO podemos usar ADD

PASSO 4: Tentar ADD-PROMOTE
  Regra ADD-PROMOTE: Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
  Temos: Γ ⊢ 5 : int ✓  e  Γ ⊢ 3.5 : real ✓

  PERFEITO! Podemos usar ADD-PROMOTE

PASSO 5: Aplicar ADD-PROMOTE
      Γ ⊢ 5 : int    Γ ⊢ 3.5 : real
      ────────────────────────────── (ADD-PROMOTE)
           Γ ⊢ (5 3.5 +) : real

══════════════════════════════════════════════════════════════
RESPOSTA: (5 3.5 +) tem tipo real
══════════════════════════════════════════════════════════════

POR QUE NÃO É INT? (Explicação Detalhada)
──────────────────────────────────────────────────

RAZÃO 1: Matemática
  - 5 + 3.5 = 8.5
  - 8.5 NÃO É INTEIRO (tem parte decimal .5)
  - Se disséssemos que o tipo é int, estaríamos mentindo!

RAZÃO 2: Teoria dos Tipos
  - int pode representar: ..., -2, -1, 0, 1, 2, ...
  - real pode representar: ..., 2.5, 3.14, 8.5, ...
  - 8.5 ∈ real? SIM
  - 8.5 ∈ int? NÃO
  - Logo, tipo correto é real

RAZÃO 3: Hierarquia de Tipos
  - Temos: int < real (int é "menor" que real)
  - Quando misturamos, vamos para o tipo "maior"
  - É como: líquido + sólido = líquido
  - Ou: real + int = real

RAZÃO 4: Semântica da Operação
  - A adição PRESERVA a "realidade" dos valores
  - Se QUALQUER parte é real, resultado DEVE ser real
  - Caso contrário, perderíamos precisão!

ANALOGIA CONCRETA:
  - 5 metros (int) + 3.5 metros (real) = 8.5 metros (real)
  - Você não pode dizer "8 metros" (perderia os 0.5)
  - O tipo real PRESERVA toda a informação

══════════════════════════════════════════════════════════════
CONCLUSÃO: Resultado é real porque misturamos int com real,
           e real "vence" na hierarquia de tipos.
══════════════════════════════════════════════════════════════
```

---

### Exercício 3.3: Expressão Aninhada

**Questão:** Derive o tipo de `((5 3 +) 2 *)`

**Solução Ultra-Detalhada:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: ((5 3 +) 2 *)
ESTRUTURA: Há uma SUB-EXPRESSÃO (5 3 +) dentro
══════════════════════════════════════════════════════════════

ESTRATÉGIA: Derivar de DENTRO para FORA
──────────────────────────────────────────────────
  1. Primeiro: (5 3 +)    ← expressão interna
  2. Depois: (resultado 2 *) ← expressão externa


═══════════════════════════════════════════════════════════════
FASE 1: Derivar (5 3 +)
═══════════════════════════════════════════════════════════════

PASSO 1.1: Tipo de 5
  ───────────────────── (INT)
      Γ ⊢ 5 : int

PASSO 1.2: Tipo de 3
  ───────────────────── (INT)
      Γ ⊢ 3 : int

PASSO 1.3: Combinar com +
      Γ ⊢ 5 : int    Γ ⊢ 3 : int    int ∈ {int, real}
      ─────────────────────────────────────────────── (ADD)
                  Γ ⊢ (5 3 +) : int

CONCLUSÃO FASE 1: (5 3 +) tem tipo int ✓


═══════════════════════════════════════════════════════════════
FASE 2: Derivar a expressão completa ((5 3 +) 2 *)
═══════════════════════════════════════════════════════════════

PASSO 2.1: Operando esquerdo
  - Operando: (5 3 +)
  - Tipo: int (da FASE 1)
  - Conclusão: Γ ⊢ (5 3 +) : int ✓

PASSO 2.2: Operando direito
  - Operando: 2
  - É literal inteiro
  ───────────────────── (INT)
      Γ ⊢ 2 : int

PASSO 2.3: Combinar com *
  - e₁: (5 3 +), tipo int
  - e₂: 2, tipo int
  - Operador: *

  Aplicar regra MULT (similar a ADD):
      Γ ⊢ (5 3 +) : int    Γ ⊢ 2 : int    int ∈ {int, real}
      ───────────────────────────────────────────────────── (MULT)
                  Γ ⊢ ((5 3 +) 2 *) : int


═══════════════════════════════════════════════════════════════
ÁRVORE DE DERIVAÇÃO COMPLETA
═══════════════════════════════════════════════════════════════

                              ───── (INT)  ───── (INT)
                                Γ ⊢ 5:int   Γ ⊢ 3:int
                              ───────────────────────── (ADD)
                                 Γ ⊢ (5 3 +) : int
                                                         ───── (INT)
                                                         Γ ⊢ 2:int
        ────────────────────────────────────────────────────────────── (MULT)
                        Γ ⊢ ((5 3 +) 2 *) : int


═══════════════════════════════════════════════════════════════
CÁLCULO EM TEMPO DE EXECUÇÃO (para confirmar tipo)
═══════════════════════════════════════════════════════════════

  Passo 1: Calcular (5 3 +)
    - 5 + 3 = 8
    - Tipo: int

  Passo 2: Calcular (8 2 *)
    - 8 * 2 = 16
    - Tipo: int (int * int = int)


═══════════════════════════════════════════════════════════════
RESPOSTA FINAL: ((5 3 +) 2 *) tem tipo int
VALOR: 16
═══════════════════════════════════════════════════════════════
```

---

### Exercício 3.4: Detectando Erro Semântico

**Questão:** Por que `(10 3.0 /)` é um erro? Explique CADA razão.

**Solução Com Análise Profunda:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (10 3.0 /)
PERGUNTA: Por que isso é ERRO?
══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
TENTATIVA DE DERIVAÇÃO (para ver onde falha)
═══════════════════════════════════════════════════════════════

PASSO 1: Tipo de 10
  - 10 não tem ponto decimal
  ───────────────────── (INT)
      Γ ⊢ 10 : int ✓

PASSO 2: Tipo de 3.0
  - 3.0 TEM ponto decimal (.0)
  - Mesmo sendo "3 ponto zero", ainda é REAL
  ───────────────────── (REAL)
      Γ ⊢ 3.0 : real ✓

PASSO 3: Tentar aplicar DIV-INT
  Regra DIV-INT:
      Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
      ────────────────────────────────
          Γ ⊢ (e₁ e₂ /) : int

  Verificar premissas:
    Premissa 1: Γ ⊢ 10 : int
                Temos: SIM ✓

    Premissa 2: Γ ⊢ 3.0 : int
                Temos: Γ ⊢ 3.0 : real
                real = int? NÃO ✗✗✗

  FALHA: Premissa 2 não é satisfeita!


═══════════════════════════════════════════════════════════════
POR QUE É ERRO? (5 Razões Fundamentais)
═══════════════════════════════════════════════════════════════

RAZÃO 1: Incompatibilidade de Tipos
────────────────────────────────────────────────
  - DIV-INT requer: int e int
  - Temos: int e real
  - real ≠ int (tipos diferentes)
  - NÃO HÁ REGRA que permita / com tipos mistos

RAZÃO 2: Semântica do Operador /
────────────────────────────────────────────────
  - / significa DIVISÃO INTEIRA
  - "Inteira" = trunca o resultado para inteiro
  - Exemplo: 10 / 3 = 3 (não 3.333...)

  SE permitíssemos (10 3.0 /):
    - 10 / 3.0 = 3.333... (matematicamente)
    - MAS / deve truncar para inteiro
    - Resultado seria: 3
    - PROBLEMA: Usamos operando real (3.0) mas resultado int (3)
    - Isso é INCONSISTENTE semanticamente!

RAZÃO 3: Sistema de Tipos Forte
────────────────────────────────────────────────
  - Nossa linguagem tem TIPAGEM FORTE
  - Isso significa: não permitimos mistura arbitrária de tipos
  - Cada operador tem regras ESTRITAS sobre tipos aceitos
  - / é PARTICULARMENTE estrito: SOMENTE int + int

RAZÃO 4: Existência de Operador Correto
────────────────────────────────────────────────
  - SOLUÇÃO: Use | em vez de /
  - | é divisão REAL (aceita int ou real, retorna real)
  - (10 3.0 |) : real ✓ (isso funciona!)

  Por que ter dois operadores?
    - / : divisão inteira (trunca)
    - | : divisão real (preserva decimais)

  Isso dá CLAREZA ao programador sobre a intenção

RAZÃO 5: Prevenção de Erros
────────────────────────────────────────────────
  SE permitíssemos (10 3.0 /):
    - Programador escreveu 3.0 (real)
    - Mas resultado seria truncado (int)
    - Provavelmente o programador QUERIA divisão real
    - Ao DAR ERRO, forçamos ele a usar | (correto)


═══════════════════════════════════════════════════════════════
ERRO EM FORMA DE REGRA
═══════════════════════════════════════════════════════════════

      Γ ⊢ 10 : int    Γ ⊢ 3.0 : real
      ────────────────────────────────── ✗ NÃO HÁ REGRA!
          Γ ⊢ (10 3.0 /) : ???

  Não existe nenhuma regra na gramática que derive isso!


═══════════════════════════════════════════════════════════════
COMPARAÇÃO: ERRO vs CORRETO
═══════════════════════════════════════════════════════════════

ERRADO:
  (10 3.0 /)
  └─ Tipo: int + real
  └─ Operador: / (requer int + int)
  └─ Resultado: ERRO SEMÂNTICO ✗

CORRETO (opção 1):
  (10 3 /)
  └─ Tipo: int + int
  └─ Operador: / (OK!)
  └─ Resultado: int (valor: 3) ✓

CORRETO (opção 2):
  (10 3.0 |)
  └─ Tipo: int + real
  └─ Operador: | (aceita mistura)
  └─ Resultado: real (valor: 3.333...) ✓


═══════════════════════════════════════════════════════════════
MENSAGEM DE ERRO (o que o compilador diria)
═══════════════════════════════════════════════════════════════

ERRO SEMÂNTICO [Expressão (10 3.0 /)]:
  Divisão inteira (/) requer ambos operandos do tipo int,
  mas encontrado:
    - Operando esquerdo: 10 (tipo: int) ✓
    - Operando direito: 3.0 (tipo: real) ✗

  Sugestão: Use o operador | para divisão real:
    (10 3.0 |) → tipo: real


═══════════════════════════════════════════════════════════════
RESPOSTA FINAL:
═══════════════════════════════════════════════════════════════
É erro porque:
  1. DIV-INT exige int + int (regra formal)
  2. Temos int + real (incompatível)
  3. Nenhuma regra se aplica
  4. Sistema de tipos REJEITA a expressão

Solução: Use | em vez de /
══════════════════════════════════════════════════════════════
```

---

## 🎓 Parte 4: Conceitos Importantes para Entender TUDO

### 4.1 Por Que Precisamos de Regras Formais?

**RESPOSTA LONGA:**

1. **Precisão:** Linguagem natural é ambígua
   - "Adicione dois números" - Quais tipos? Como?
   - Regra formal: EXATAMENTE quais tipos, EXATAMENTE qual resultado

2. **Completude:** Cobrimos TODOS os casos
   - Regras dizem o que fazer para QUALQUER expressão válida
   - Se não há regra, expressão é inválida

3. **Comunicação:** Equipe usa mesma definição
   - Você implementa em Python
   - Colega implementa em Java
   - Ambos seguem MESMAS regras formais = comportamento idêntico

4. **Prova de Corretude:**
   - Podemos PROVAR matematicamente que código está certo
   - Derivação formal = prova matemática

---

### 4.2 Como Ler Uma Regra de Inferência

**FORMATO:**
```
Premissa₁    Premissa₂    ...    PremissaN
─────────────────────────────────────────── (NOME)
            Conclusão
```

**PENSE COMO:**
```
SE todas premissas são verdadeiras
ENTÃO conclusão é verdadeira
```

**PENSE COMO CÓDIGO:**
```python
def NOME(premissa1, premissa2, ..., premissaN):
    if premissa1 and premissa2 and ... and premissaN:
        return conclusao
    else:
        raise ErroSemantico("Premissas não satisfeitas")
```

---

### 4.3 Diferença Entre Sintaxe e Semântica

**SINTAXE (RA2):**
- Pergunta: "Está escrito CORRETAMENTE?"
- Verifica: Parênteses, ordem dos símbolos
- Exemplo: `(5 3 +)` ✓ sintaxe OK

**SEMÂNTICA (RA3):**
- Pergunta: "Faz SENTIDO?"
- Verifica: Tipos compatíveis, variáveis existem
- Exemplo: `(5 3 +)` → int + int = int ✓ semântica OK

**ANALOGIA:**
- Sintaxe: "A frase está gramaticalmente correta?"
- Semântica: "A frase faz sentido?"
  - "O gato comeu o rato" ✓✓ (sintaxe OK, semântica OK)
  - "O rato comeu o gato" ✓✗ (sintaxe OK, semântica questionável)
  - "Comeu gato o rato" ✗✗ (sintaxe ruim, semântica irrelevante)

---

## 📚 Referências e Próximos Passos

### Para Aprofundar:

1. **Livro Dragon (Aho et al.)** - Capítulo 5 (Type Checking)
2. **Documentos relacionados:**
   - `02_symbol_table_theory.md` - Tabela de símbolos
   - `03_type_system_theory.md` - Sistema de tipos
   - `04_advanced_exercises.md` - Exercícios avançados

---

**Desenvolvido por:** Grupo RA3_1 - PUCPR
**Data:** 2025-01-19
