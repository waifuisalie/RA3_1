# Teoria Completa: Tabela de Símbolos (Com Explicações Literais)

**Curso:** Linguagens Formais e Autômatos
**Fase:** RA3 - Análise Semântica
**Grupo:** RA3_1
**Objetivo:** Entender O QUE é uma tabela de símbolos e POR QUE precisamos dela

---

## 📚 Parte 1: O Que É Uma Tabela de Símbolos?

### 1.1 Definição Simples

**ANALOGIA 1:**
Uma tabela de símbolos é como uma **agenda telefônica**:
- **Nome** → **Número** (na agenda)
- **Variável** → **Tipo** (na tabela de símbolos)

**ANALOGIA 2:**
É como um **dicionário em Python**:
```python
tabela = {
    'CONTADOR': 'int',
    'PI': 'real',
    'FLAG': 'boolean'
}
```

**DEFINIÇÃO FORMAL:**
```
Γ : Identificador → (Tipo × Estado × Escopo × ...)
```
Lê-se: "Γ mapeia cada identificador para suas propriedades (tipo, estado, escopo, etc.)"

---

### 1.2 Por Que Precisamos Dela?

**PROBLEMA SEM TABELA:**
```
Linha 1: (5 X MEM)    ← X é int
Linha 2: (X 3.5 +)    ← Qual é o tipo de X? 🤔
```

Se não guardarmos que X é int (linha 1), como saberemos na linha 2?

**SOLUÇÃO COM TABELA:**
```
Linha 1: (5 X MEM)
  Ação: Adicionar X à tabela
  Γ = { X: int }

Linha 2: (X 3.5 +)
  Ação: Consultar X na tabela
  Γ(X) = int ✓
  Logo: int + real = real
```

**TRÊS FUNÇÕES PRINCIPAIS:**

1. **LEMBRAR** tipos de variáveis
2. **RASTREAR** se variável foi inicializada
3. **GERENCIAR** escopos (quais variáveis são visíveis)

---

## 📖 Parte 2: Estrutura da Tabela

### 2.1 O Que Guardamos Para Cada Variável?

Para cada símbolo (variável), guardamos:

| Campo | Tipo | Significado | Exemplo |
|-------|------|-------------|---------|
| `nome` | string | Identificador da variável | `"CONTADOR"` |
| `tipo` | string | Tipo do valor | `"int"` ou `"real"` |
| `inicializada` | boolean | Foi atribuído valor? | `true` ou `false` |
| `escopo` | int | Nível de escopo | `0` (global) |
| `linha_declaracao` | int | Onde foi criada | `5` |
| `linha_ultimo_uso` | int | Última referência | `12` |

**EXEMPLO VISUAL:**

```
Tabela de Símbolos Γ:
┌────────────┬──────┬──────────────┬────────┬─────────────────┬──────────────────┐
│ Nome       │ Tipo │ Inicializada │ Escopo │ Linha Decl.     │ Linha Último Uso │
├────────────┼──────┼──────────────┼────────┼─────────────────┼──────────────────┤
│ CONTADOR   │ int  │ true         │ 0      │ 5               │ 12               │
│ PI         │ real │ true         │ 0      │ 8               │ 8                │
│ TEMP       │ int  │ false        │ 0      │ 10              │ -                │
└────────────┴──────┴──────────────┴────────┴─────────────────┴──────────────────┘
```

---

### 2.2 Notação Matemática vs Implementação

**NOTAÇÃO MATEMÁTICA (em provas):**
```
Γ = { X: int, Y: real }
```

**IMPLEMENTAÇÃO (em Python):**
```python
class TabelaSimbolos:
    def __init__(self):
        self._simbolos = {
            'X': SimboloInfo(nome='X', tipo='int', inicializada=True, ...),
            'Y': SimboloInfo(nome='Y', tipo='real', inicializada=True, ...)
        }
```

**SÃO A MESMA COISA!** Notação matemática é mais compacta, implementação tem mais detalhes.

---

## 🔧 Parte 3: Operações na Tabela

### 3.1 Operação: ADICIONAR (Declaração de Variável)

**O QUE FAZ:**
Adiciona uma nova variável à tabela (ou atualiza se já existe).

**REGRA FORMAL:**
```
    Γ ⊢ e : T    x ∉ dom(Γ)
────────────────────────────────
   Γ, x: T ⊢ (e x MEM) : T
```

**TRADUÇÃO:**
"Se e tem tipo T e x NÃO existe em Γ, então após (e x MEM), Γ agora contém x com tipo T"

**EXEMPLO PASSO-A-PASSO:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 CONTADOR MEM)
ESTADO INICIAL: Γ₀ = {} (tabela vazia)
══════════════════════════════════════════════════════════════

PASSO 1: O que estamos tentando fazer?
──────────────────────────────────────────────────
  Sintaxe RPN: (valor variável MEM)
  - valor = 5
  - variável = CONTADOR
  - comando = MEM (armazenar em memória)

  OBJETIVO: Armazenar 5 em CONTADOR


PASSO 2: Determinar tipo do valor
──────────────────────────────────────────────────
  Valor: 5
  Tem ponto decimal? NÃO
  Tipo: int

  DERIVAÇÃO:
  ───────────────────── (INT-LITERAL)
      Γ₀ ⊢ 5 : int


PASSO 3: Verificar se CONTADOR já existe
──────────────────────────────────────────────────
  Pergunta: CONTADOR ∈ dom(Γ₀)?
  Γ₀ = {} (vazia)
  CONTADOR está em {}? NÃO

  Conclusão: CONTADOR NÃO existe (vamos CRIAR)


PASSO 4: Aplicar regra MEM-STORE
──────────────────────────────────────────────────
  Regra:
      Γ ⊢ e : T    x ∉ dom(Γ)
  ────────────────────────────────
     Γ, x: T ⊢ (e x MEM) : T

  Verificar premissas:
    ✓ Γ₀ ⊢ 5 : int (PASSO 2)
    ✓ CONTADOR ∉ dom(Γ₀) (PASSO 3)

  Conclusão: Podemos aplicar MEM-STORE!


PASSO 5: Atualizar o ambiente
──────────────────────────────────────────────────
  ANTES: Γ₀ = {}

  OPERAÇÃO: Adicionar CONTADOR com tipo int

  DEPOIS: Γ₁ = { CONTADOR: int, inicializada: true }


PASSO 6: Estado completo após operação
──────────────────────────────────────────────────
  Tabela de Símbolos Γ₁:
  ┌────────────┬──────┬──────────────┬────────┐
  │ Nome       │ Tipo │ Inicializada │ Escopo │
  ├────────────┼──────┼──────────────┼────────┤
  │ CONTADOR   │ int  │ true         │ 0      │
  └────────────┴──────┴──────────────┴────────┘


══════════════════════════════════════════════════════════════
RESULTADO: Γ₁ = { CONTADOR: int }
TIPO DA EXPRESSÃO: int
══════════════════════════════════════════════════════════════
```

---

### 3.2 Operação: BUSCAR (Recuperação de Variável)

**O QUE FAZ:**
Consulta o tipo de uma variável na tabela.

**REGRA FORMAL:**
```
    x ∈ dom(Γ)    Γ(x) = T
─────────────────────────────
         Γ ⊢ x : T
```

**EXEMPLO PASSO-A-PASSO:**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (CONTADOR 1 +)
ESTADO: Γ = { CONTADOR: int, inicializada: true }
══════════════════════════════════════════════════════════════

PASSO 1: O que precisamos saber?
──────────────────────────────────────────────────
  Expressão: (CONTADOR 1 +)
  Para aplicar regra ADD, precisamos:
    - Tipo de CONTADOR
    - Tipo de 1

  FOCO: Tipo de CONTADOR


PASSO 2: Verificar se CONTADOR existe
──────────────────────────────────────────────────
  Pergunta: CONTADOR ∈ dom(Γ)?
  Γ = { CONTADOR: int }
  CONTADOR está em Γ? SIM ✓

  POR QUE VERIFICAR:
    - Se não existir, é erro!
    - Não podemos usar variável não declarada


PASSO 3: Consultar tipo em Γ
──────────────────────────────────────────────────
  Operação: Γ(CONTADOR)

  Como funciona:
    - Olho na tabela Γ
    - Procuro linha com nome = CONTADOR
    - Leio o campo tipo

  Resultado: Γ(CONTADOR) = int ✓


PASSO 4: Aplicar regra VAR
──────────────────────────────────────────────────
      CONTADOR ∈ dom(Γ)    Γ(CONTADOR) = int
  ──────────────────────────────────────────────── (VAR)
             Γ ⊢ CONTADOR : int


PASSO 5: Verificar inicialização (IMPORTANTE!)
──────────────────────────────────────────────────
  Γ.inicializada(CONTADOR) = ?

  Tabela:
  ┌────────────┬──────┬──────────────┐
  │ CONTADOR   │ int  │ true         │
  └────────────┴──────┴──────────────┘

  Resultado: true ✓

  POR QUE ISSO IMPORTA:
    - Se fosse false, seria ERRO SEMÂNTICO!
    - "Uso de variável não inicializada"


PASSO 6: Completar derivação de (CONTADOR 1 +)
──────────────────────────────────────────────────
      Γ ⊢ CONTADOR : int    Γ ⊢ 1 : int
  ─────────────────────────────────────── (ADD)
          Γ ⊢ (CONTADOR 1 +) : int


══════════════════════════════════════════════════════════════
RESULTADO: (CONTADOR 1 +) tem tipo int
POR QUÊ: Γ nos disse que CONTADOR é int
══════════════════════════════════════════════════════════════
```

---

### 3.3 Operação: VERIFICAR INICIALIZAÇÃO

**POR QUE EXISTE:**
Impedir uso de variáveis antes de atribuir valor!

**ERRO COMUM:**
```c
int x;           // declarada mas NÃO inicializada
int y = x + 5;   // ERRO! x não tem valor ainda
```

**REGRA FORMAL:**
```
x ∈ dom(Γ)    Γ(x) = T    inicializada(Γ, x) = true
────────────────────────────────────────────────────
              Γ ⊢ (x) : T
```

**EXEMPLO: ERRO DE VARIÁVEL NÃO INICIALIZADA**

```
══════════════════════════════════════════════════════════════
CENÁRIO:
  Linha 1: Criamos VAR mas NÃO inicializamos
  Linha 2: Tentamos usar VAR
══════════════════════════════════════════════════════════════

LINHA 1: Declaração sem inicialização
──────────────────────────────────────────────────
  (Imagine que temos uma forma de declarar sem valor)

  Estado: Γ₁ = { VAR: int, inicializada: false }

  Tabela:
  ┌──────┬──────┬──────────────┐
  │ VAR  │ int  │ FALSE        │ ← ATENÇÃO!
  └──────┴──────┴──────────────┘


LINHA 2: (VAR 5 +)
──────────────────────────────────────────────────

PASSO 1: Tentar derivar tipo de VAR
  ──────────────────────────────────────
  Verificar premissas de VAR:
    ✓ VAR ∈ dom(Γ₁) (VAR existe)
    ✓ Γ₁(VAR) = int (VAR tem tipo int)

  Até aqui OK! MAS...


PASSO 2: Verificar inicialização
  ──────────────────────────────────────
  Premissa adicional (MEM-LOAD):
    inicializada(Γ₁, VAR) = true

  Temos:
    inicializada(Γ₁, VAR) = false ✗✗✗

  FALHA! Premissa não satisfeita!


PASSO 3: Resultado
  ──────────────────────────────────────
  NÃO podemos aplicar regra VAR/MEM-LOAD

  ERRO SEMÂNTICO:
    "Variável VAR utilizada sem inicialização"


══════════════════════════════════════════════════════════════
POR QUE ISSO É IMPORTANTE?
══════════════════════════════════════════════════════════════

RAZÃO 1: Segurança
  - Variável não inicializada tem LIXO em memória
  - Resultado da operação seria imprevisível

RAZÃO 2: Clareza
  - Força programador a pensar: "qual valor inicial?"
  - Evita bugs difíceis de encontrar

RAZÃO 3: Boa prática
  - Linguagens modernas (Java, Rust) exigem isso
  - É padrão da indústria

ANALOGIA:
  - É como tentar usar caixa vazia
  - Primeiro coloque algo (inicialize)
  - Depois pegue (use)
══════════════════════════════════════════════════════════════
```

---

## 📝 Parte 4: Evolução do Ambiente (Γ)

### 4.1 Como Γ Muda Ao Longo do Programa

**CONCEITO CHAVE:**
Γ não é estático! Ele **evolui** conforme executamos linha por linha.

**NOTAÇÃO:**
- Γ₀ = ambiente inicial (geralmente vazio)
- Γ₁ = ambiente após linha 1
- Γ₂ = ambiente após linha 2
- ...

**EXEMPLO COMPLETO:**

```
══════════════════════════════════════════════════════════════
PROGRAMA:
  Linha 1: (5 X MEM)
  Linha 2: (3.5 Y MEM)
  Linha 3: (X Y +)
  Linha 4: (3 RES RESULTADO MEM)
══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
LINHA 1: (5 X MEM)
═══════════════════════════════════════════════════════════════

ANTES: Γ₀ = {}
──────────────────────────────────────────────────

DERIVAÇÃO:
  PASSO 1: Tipo de 5
    ───────────────── (INT)
        Γ₀ ⊢ 5 : int

  PASSO 2: X existe em Γ₀?
    X ∈ dom(Γ₀)? NÃO (Γ₀ está vazia)

  PASSO 3: Aplicar MEM-STORE
        Γ₀ ⊢ 5 : int    X ∉ dom(Γ₀)
    ───────────────────────────────── (MEM-STORE)
       Γ₀, X: int ⊢ (5 X MEM) : int

DEPOIS: Γ₁ = { X: int, inicializada: true }
──────────────────────────────────────────────────

Tabela Γ₁:
┌──────┬──────┬──────────────┐
│ X    │ int  │ true         │
└──────┴──────┴──────────────┘


═══════════════════════════════════════════════════════════════
LINHA 2: (3.5 Y MEM)
═══════════════════════════════════════════════════════════════

ANTES: Γ₁ = { X: int }
──────────────────────────────────────────────────

DERIVAÇÃO:
  PASSO 1: Tipo de 3.5
    ───────────────── (REAL)
        Γ₁ ⊢ 3.5 : real

  PASSO 2: Y existe em Γ₁?
    Y ∈ dom(Γ₁)? NÃO (só temos X)

  PASSO 3: Aplicar MEM-STORE
        Γ₁ ⊢ 3.5 : real    Y ∉ dom(Γ₁)
    ────────────────────────────────────── (MEM-STORE)
       Γ₁, Y: real ⊢ (3.5 Y MEM) : real

DEPOIS: Γ₂ = { X: int, Y: real }
──────────────────────────────────────────────────

Tabela Γ₂:
┌──────┬──────┬──────────────┐
│ X    │ int  │ true         │
│ Y    │ real │ true         │
└──────┴──────┴──────────────┘


═══════════════════════════════════════════════════════════════
LINHA 3: (X Y +)
═══════════════════════════════════════════════════════════════

ESTADO: Γ₂ = { X: int, Y: real }
──────────────────────────────────────────────────

DERIVAÇÃO:
  PASSO 1: Tipo de X
    CONSULTAR Γ₂:
        X ∈ dom(Γ₂)    Γ₂(X) = int
    ────────────────────────────────── (VAR)
            Γ₂ ⊢ X : int

  PASSO 2: Tipo de Y
    CONSULTAR Γ₂:
        Y ∈ dom(Γ₂)    Γ₂(Y) = real
    ────────────────────────────────── (VAR)
            Γ₂ ⊢ Y : real

  PASSO 3: Combinar X + Y
        Γ₂ ⊢ X : int    Γ₂ ⊢ Y : real
    ────────────────────────────────── (ADD-PROMOTE)
           Γ₂ ⊢ (X Y +) : real

AMBIENTE PERMANECE: Γ₂ (não muda)
──────────────────────────────────────────────────
  POR QUÊ: Só lemos X e Y, não modificamos


═══════════════════════════════════════════════════════════════
LINHA 4: (3 RES RESULTADO MEM)
═══════════════════════════════════════════════════════════════

ANTES: Γ₂ = { X: int, Y: real }
──────────────────────────────────────────────────

DERIVAÇÃO:
  PASSO 1: Tipo de (3 RES)
    RES referencia linha (4 - 3) = linha 1
    Linha 1 retornou: int
    Logo: (3 RES) : int

  PASSO 2: Armazenar em RESULTADO
        Γ₂ ⊢ (3 RES) : int    RESULTADO ∉ dom(Γ₂)
    ──────────────────────────────────────────────── (MEM-STORE)
       Γ₂, RESULTADO: int ⊢ ... : int

DEPOIS: Γ₃ = { X: int, Y: real, RESULTADO: int }
──────────────────────────────────────────────────

Tabela Γ₃:
┌───────────┬──────┬──────────────┐
│ X         │ int  │ true         │
│ Y         │ real │ true         │
│ RESULTADO │ int  │ true         │
└───────────┴──────┴──────────────┘


══════════════════════════════════════════════════════════════
RESUMO DA EVOLUÇÃO:
══════════════════════════════════════════════════════════════

Γ₀ = {}                                    (início)
Γ₁ = { X: int }                            (após linha 1)
Γ₂ = { X: int, Y: real }                   (após linha 2)
Γ₂ (inalterado)                            (após linha 3)
Γ₃ = { X: int, Y: real, RESULTADO: int }   (após linha 4)

OBSERVAÇÃO:
  - Γ cresce conforme declaramos variáveis
  - Γ NÃO diminui (variáveis não são removidas)
  - Γ pode ser CONSULTADO a qualquer momento
══════════════════════════════════════════════════════════════
```

---

## 🎓 Parte 5: Exercícios Detalhados

### Exercício 5.1: Evolução de Γ Simples

**Questão:**
Dado Γ₀ = {}, derive o ambiente final após:
```
Linha 1: (10 A MEM)
Linha 2: (20 B MEM)
```

**Solução Passo-a-Passo:**

```
══════════════════════════════════════════════════════════════
LINHA 1: (10 A MEM)
══════════════════════════════════════════════════════════════

Estado inicial: Γ₀ = {}

PASSO 1: Qual o tipo de 10?
  - 10 é literal inteiro
  - Tipo: int

PASSO 2: A existe em Γ₀?
  - Γ₀ está vazia
  - A ∉ dom(Γ₀)

PASSO 3: Adicionar A à tabela
  ANTES: Γ₀ = {}
  OPERAÇÃO: Adicionar A com tipo int
  DEPOIS: Γ₁ = { A: int, inicializada: true }

Tabela Γ₁:
┌──────┬──────┬──────────────┐
│ A    │ int  │ true         │
└──────┴──────┴──────────────┘


══════════════════════════════════════════════════════════════
LINHA 2: (20 B MEM)
══════════════════════════════════════════════════════════════

Estado atual: Γ₁ = { A: int }

PASSO 1: Qual o tipo de 20?
  - 20 é literal inteiro
  - Tipo: int

PASSO 2: B existe em Γ₁?
  - Γ₁ = { A: int }
  - B está em Γ₁? NÃO
  - B ∉ dom(Γ₁)

PASSO 3: Adicionar B à tabela
  ANTES: Γ₁ = { A: int }
  OPERAÇÃO: Adicionar B com tipo int
  DEPOIS: Γ₂ = { A: int, B: int }

Tabela Γ₂:
┌──────┬──────┬──────────────┐
│ A    │ int  │ true         │
│ B    │ int  │ true         │
└──────┴──────┴──────────────┘


══════════════════════════════════════════════════════════════
RESPOSTA FINAL:
══════════════════════════════════════════════════════════════

Γ_final = { A: int, B: int }

Ambas variáveis:
  - Tipo: int
  - Inicializadas: true
  - Escopo: 0
══════════════════════════════════════════════════════════════
```

---

### Exercício 5.2: Detectar Erro de Uso Antes de Inicialização

**Questão:**
Por que o seguinte programa tem erro?
```
Linha 1: (X 5 +)
```

(Assume Γ₀ = {})

**Solução Com Análise Profunda:**

```
══════════════════════════════════════════════════════════════
ANÁLISE: Por que (X 5 +) é ERRO?
══════════════════════════════════════════════════════════════

Estado: Γ₀ = {} (tabela vazia)
Expressão: (X 5 +)


TENTATIVA DE DERIVAÇÃO:
──────────────────────────────────────────────────

PASSO 1: Derivar tipo de X
  ────────────────────────────────────────
  Tentar aplicar regra VAR:
      X ∈ dom(Γ)    Γ(X) = T
  ─────────────────────────────────
           Γ ⊢ X : T

  Verificar premissa 1: X ∈ dom(Γ₀)?
    Γ₀ = {}
    X está em {}? NÃO ✗

  FALHA! Não podemos aplicar VAR!


POR QUE É ERRO? (5 Razões)
──────────────────────────────────────────────────

RAZÃO 1: X não foi declarado
  - Nunca fizemos (v X MEM)
  - X não existe na tabela
  - Não sabemos que tipo X deveria ter!

RAZÃO 2: Impossível determinar tipo
  - Para aplicar ADD, precisamos tipo de X
  - Tipo de X = Γ(X)
  - Mas X ∉ dom(Γ)!
  - Logo, Γ(X) = INDEFINIDO

RAZÃO 3: Falta de informação
  - Compilador pergunta: "Qual o tipo de X?"
  - Resposta: "Não sei, você não me disse!"
  - Não há como continuar

RAZÃO 4: Segurança de tipos
  - Se permitíssemos, poderia ser:
    - X é int? → (int 5 +) = int
    - X é real? → (real 5 +) = real
  - Resultado depende de tipo desconhecido!
  - Linguagem com tipagem forte NÃO permite isso

RAZÃO 5: Boa prática
  - "Use before declare" é erro em toda linguagem moderna
  - Java, C, C++, Rust: todos exigem declaração primeiro


COMO CORRIGIR:
──────────────────────────────────────────────────

CORRETO:
  Linha 1: (10 X MEM)  ← Declara X
  Linha 2: (X 5 +)     ← Agora OK!

DERIVAÇÃO CORRETA:
  Γ₀ = {}
  Linha 1: Γ₁ = { X: int }
  Linha 2:
    X ∈ dom(Γ₁)    Γ₁(X) = int
    ─────────────────────────────── (VAR)    ───── (INT)
        Γ₁ ⊢ X : int                         Γ₁ ⊢ 5 : int
    ──────────────────────────────────────────────────────── (ADD)
                   Γ₁ ⊢ (X 5 +) : int


══════════════════════════════════════════════════════════════
MENSAGEM DE ERRO (o que compilador diria):
══════════════════════════════════════════════════════════════

ERRO SEMÂNTICO [Linha 1]:
  Variável 'X' não foi declarada.

  Contexto: (X 5 +)
            ^
  Não é possível determinar o tipo de X.

  Sugestão: Declare X antes de usar:
    (valor X MEM)  ← declaração
    (X 5 +)        ← uso

══════════════════════════════════════════════════════════════
CONCLUSÃO:
══════════════════════════════════════════════════════════════
É erro porque X não existe em Γ₀.
Sem declaração prévia, não sabemos o tipo de X.
══════════════════════════════════════════════════════════════
```

---

### Exercício 5.3: Múltiplas Atualizações

**Questão:**
O que acontece se atribuímos a mesma variável duas vezes com tipos diferentes?
```
Linha 1: (5 X MEM)     ← X é int
Linha 2: (3.5 X MEM)   ← X é real agora?
```

Derive Γ após cada linha.

**Solução Completa:**

```
══════════════════════════════════════════════════════════════
ANÁLISE: Redeclaração com Tipo Diferente
══════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════
LINHA 1: (5 X MEM)
═══════════════════════════════════════════════════════════════

ANTES: Γ₀ = {}

DERIVAÇÃO:
  Γ₀ ⊢ 5 : int    X ∉ dom(Γ₀)
  ─────────────────────────────── (MEM-STORE)
     Γ₀, X: int ⊢ (5 X MEM) : int

DEPOIS: Γ₁ = { X: int, inicializada: true }

Tabela Γ₁:
┌──────┬──────┬──────────────┐
│ X    │ int  │ true         │  ← X é int
└──────┴──────┴──────────────┘


═══════════════════════════════════════════════════════════════
LINHA 2: (3.5 X MEM)
═══════════════════════════════════════════════════════════════

ANTES: Γ₁ = { X: int }

DERIVAÇÃO:
  PASSO 1: Tipo de 3.5
    ───────────────── (REAL)
        Γ₁ ⊢ 3.5 : real

  PASSO 2: X existe em Γ₁?
    X ∈ dom(Γ₁)? SIM! (X já foi declarado)

  PASSO 3: O que fazer?
    OPÇÃO A: Erro (não pode redeclarar)
    OPÇÃO B: Atualizar tipo de X

    NOSSA IMPLEMENTAÇÃO: OPÇÃO B
    (Permite mudança de tipo - redeclaração)

  PASSO 4: Atualizar X
    ANTES: X: int
    OPERAÇÃO: Mudar tipo para real
    DEPOIS: X: real

DEPOIS: Γ₂ = { X: real, inicializada: true }

Tabela Γ₂:
┌──────┬──────┬──────────────┐
│ X    │ real │ true         │  ← X AGORA é real!
└──────┴──────┴──────────────┘


══════════════════════════════════════════════════════════════
O QUE ACONTECEU:
══════════════════════════════════════════════════════════════

1. Γ₁: X tinha tipo int
2. Γ₂: X agora tem tipo real
3. O tipo MUDOU!

POR QUE PERMITIMOS:
  - Linha por linha, cada uma é independente
  - Γ₂ "esquece" que X era int
  - Γ₂ "lembra" apenas: X é real agora


IMPLICAÇÃO:
──────────────────────────────────────────────────

Se tivéssemos linha 3:
  Linha 3: (X 5 +)

  X ∈ dom(Γ₂)    Γ₂(X) = real
  ──────────────────────────────── (VAR)
       Γ₂ ⊢ X : real

  Logo:
      Γ₂ ⊢ X : real    Γ₂ ⊢ 5 : int
  ─────────────────────────────────── (ADD-PROMOTE)
         Γ₂ ⊢ (X 5 +) : real

  X é tratado como REAL (não int)!


══════════════════════════════════════════════════════════════
COMPARAÇÃO COM OUTRAS LINGUAGENS:
══════════════════════════════════════════════════════════════

PYTHON (permite):
  x = 5      # x é int
  x = 3.5    # x agora é float - OK!

C/JAVA (NÃO permite):
  int x = 5;
  float x = 3.5;  // ERRO! Já declarou como int

NOSSA LINGUAGEM RPN (permite):
  (5 X MEM)    // X é int
  (3.5 X MEM)  // X agora é real - OK!


══════════════════════════════════════════════════════════════
RESPOSTA FINAL:
══════════════════════════════════════════════════════════════

Γ₀ = {}                              (início)
Γ₁ = { X: int }                      (após linha 1)
Γ₂ = { X: real }                     (após linha 2)

X mudou de int para real!
══════════════════════════════════════════════════════════════
```

---

## 📚 Parte 6: Conceitos Avançados

### 6.1 Escopo (Por Que Precisamos?)

**PROBLEMA:**
```
Função A:
  int x = 5;

Função B:
  int x = 10;  ← É o mesmo X?
```

**SOLUÇÃO:** Escopos diferentes!

**COMO FUNCIONA:**
```
Γ_global = {}

Entrar em função A:
  Γ_A = { x: int, escopo: 1 }

Sair de função A:
  Γ = Γ_global (x some!)

Entrar em função B:
  Γ_B = { x: int, escopo: 1 }
```

**NO NOSSO CASO (RPN):**
- Cada arquivo = escopo independente
- Escopo sempre = 0 (global)
- Mas estrutura está pronta para estender!

---

## 🎯 Resumo Final

### O Que é Γ (Tabela de Símbolos):
- **Mapeamento:** Nome → Propriedades
- **Evolui:** Cresce ao longo do programa
- **Consultada:** Sempre que vemos variável

### Operações Principais:
1. **ADICIONAR:** Criar nova variável
2. **BUSCAR:** Consultar tipo
3. **VERIFICAR:** Checar inicialização

### Por Que Precisamos:
1. **Lembrar tipos:** int, real, boolean
2. **Rastrear inicialização:** Evitar uso antes de declarar
3. **Gerenciar escopo:** Quais variáveis existem

---

**Próximo:** `03_type_system_theory.md` - Sistema de tipos e promoção

**Desenvolvido por:** Grupo RA3_1 - PUCPR
**Data:** 2025-01-19
