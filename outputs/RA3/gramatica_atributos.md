# Gramática de Atributos - Linguagem RPN

**Projeto:** Analisador Semântico - Fase 3
**Grupo:** RA3_1
**Instituição:** PUCPR
**Data de Geração:** 2025-01-19

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Sistema de Tipos](#sistema-de-tipos)
3. [Operadores Aritméticos](#operadores-aritméticos)
4. [Operadores de Comparação](#operadores-de-comparação)
5. [Operadores Lógicos](#operadores-lógicos)
6. [Estruturas de Controle](#estruturas-de-controle)
7. [Comandos Especiais](#comandos-especiais)
8. [Exemplos Completos](#exemplos-completos)

---

## Visão Geral

Esta gramática de atributos define as regras semânticas para a linguagem RPN (Reverse Polish Notation) utilizada no projeto de compiladores. A gramática especifica:

- **Verificação de tipos** para todos os operadores
- **Inferência de tipos** para expressões compostas
- **Coerção automática** de tipos (int → real)
- **Validação de restrições** semânticas
- **Regras de escopo** e inicialização de variáveis

### Notação Utilizada

```
Γ ⊢ e : T
```

- **Γ** (Gamma): Contexto de tipagem (tabela de símbolos)
- **⊢** (turnstile): Relação de derivação semântica
- **e**: Expressão
- **T**: Tipo da expressão

### Tipos Primitivos

| Tipo | Descrição | Pode ser armazenado em MEM? |
|------|-----------|----------------------------|
| `int` | Números inteiros | ✅ Sim |
| `real` | Números de ponto flutuante | ✅ Sim |
| `boolean` | Valores booleanos | ❌ **Não** |

### Hierarquia de Tipos

```
int < real  (int pode ser promovido para real)
boolean     (separado, sem promoção)
```

---

## Sistema de Tipos

### Promoção de Tipos

**Função:** `promover_tipo(T₁, T₂) → T`

| T₁ | T₂ | Resultado |
|----|----|-----------|
| int | int | int |
| int | real | real |
| real | int | real |
| real | real | real |

### Conversão Truthiness (Modo Permissivo)

Para operadores lógicos e estruturas de controle:

| Tipo | Valor | Boolean Equivalente |
|------|-------|---------------------|
| int | 0 | false |
| int | ≠ 0 | true |
| real | 0.0 | false |
| real | ≠ 0.0 | true |
| boolean | valor | valor |

---

## Operadores Aritméticos

### 1. Adição (+)

**Sintaxe:** `(A B +)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
```

**Exemplos:**
```
(5 3 +) → tipo: int (5+3=8)
(5.0 3 +) → tipo: real (5.0+3.0=8.0)
(2 3.14 +) → tipo: real (2.0+3.14=5.14)
```

---

### 2. Subtração (-)

**Sintaxe:** `(A B -)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ -) : promover_tipo(T₁, T₂)
```

---

### 3. Multiplicação (*)

**Sintaxe:** `(A B *)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(T₁, T₂)
```

---

### 4. Divisão Real (|)

**Sintaxe:** `(A B |)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ |) : real
```

**⚠️ Importante:** Resultado é **SEMPRE real**, mesmo se ambos operandos são int.

**Exemplos:**
```
(6 2 |) → tipo: real (resultado: 3.0)
(5 2 |) → tipo: real (resultado: 2.5)
(5.0 2.0 |) → tipo: real (resultado: 2.5)
```

---

### 5. Divisão Inteira (/)

**Sintaxe:** `(A B /)`

**Regra Semântica:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ /) : int
```

**⚠️ Restrição Crítica:** AMBOS operandos DEVEM ser int.

**Exemplos Válidos:**
```
(7 2 /) → tipo: int (resultado: 3)
(10 3 /) → tipo: int (resultado: 3)
```

**Erros Semânticos:**
```
(7.0 2 /) → ERRO: operando 1 deve ser int
(7 2.0 /) → ERRO: operando 2 deve ser int
```

---

### 6. Resto da Divisão (%)

**Sintaxe:** `(A B %)`

**Regra Semântica:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ %) : int
```

**⚠️ Restrição Crítica:** AMBOS operandos DEVEM ser int.

**Exemplos:**
```
(7 3 %) → tipo: int (resultado: 1)
(10 3 %) → tipo: int (resultado: 1)
```

---

### 7. Potenciação (^)

**Sintaxe:** `(A B ^)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})
──────────────────────────────────────────────────────────
               Γ ⊢ (e₁ e₂ ^) : T
```

**Regras:**
- **Base (A):** Pode ser int ou real
- **Expoente (B):** DEVE ser int E positivo (> 0)
- **Resultado:** Mesmo tipo da base

**Exemplos Válidos:**
```
(2 3 ^) → tipo: int (2³ = 8)
(2.5 3 ^) → tipo: real (2.5³ = 15.625)
```

**Erros Semânticos:**
```
(2 3.5 ^) → ERRO: expoente deve ser int
(2 -1 ^) → ERRO: expoente deve ser positivo
(2 0 ^) → ERRO: expoente deve ser positivo
```

---

## Operadores de Comparação

**Operadores:** `>`, `<`, `>=`, `<=`, `==`, `!=`

### Regra Semântica Geral

**Sintaxe:** `(A B op)` onde op ∈ {>, <, >=, <=, ==, !=}

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ op) : boolean
```

**⚠️ Importante:** Resultado é **SEMPRE boolean**.

### Exemplos

| Expressão | Tipo Resultado | Semântica |
|-----------|---------------|-----------|
| `(5 3 >)` | boolean | 5 > 3 (true) |
| `(5.0 3 <)` | boolean | 5.0 < 3 (false) |
| `(2 2.0 ==)` | boolean | 2 == 2.0 (true) |
| `(x 0 >)` | boolean | x > 0 |

---

## Operadores Lógicos

### Modo Permissivo

Os operadores lógicos aceitam **int, real ou boolean** como operandos.
Valores numéricos são convertidos via **truthiness**.

### 1. AND (&&)

**Sintaxe:** `(A B &&)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ &&) : boolean
```

**Exemplos:**
```
((5 3 >) (x 0 >) &&) → boolean && boolean
(5 3 &&) → truthy(5) && truthy(3) = true && true = true
(0 5 &&) → truthy(0) && truthy(5) = false && true = false
```

---

### 2. OR (||)

**Sintaxe:** `(A B ||)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ ||) : boolean
```

**Exemplos:**
```
(0 5 ||) → false || true = true
(0 0 ||) → false || false = false
```

---

### 3. NOT (!)

**Sintaxe:** `(A !)` (unário postfix)

**Regra Semântica:**
```
Γ ⊢ e : T    (T ∈ {int, real, boolean})
───────────────────────────────────────
       Γ ⊢ (e !) : boolean
```

**Exemplos:**
```
((5 3 >) !) → !(true) = false
(5 !) → !(true) = false
(0 !) → !(false) = true
```

---

## Estruturas de Controle

### 1. IFELSE

**Sintaxe:** `(condição blocoTrue blocoFalse IFELSE)`

**Regra Semântica:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

**Regras:**
- Condição: Qualquer tipo conversível para boolean
- **Ambos os ramos devem ter o MESMO tipo T**
- Resultado: tipo T

**Exemplos Válidos:**
```
((x 0 >) (x 2 *) (x) IFELSE)
  cond: boolean
  true: int
  false: int
  resultado: int

((5) (3.14) (2.71) IFELSE)
  cond: int (truthy = true)
  true: real
  false: real
  resultado: real
```

**Erro Semântico:**
```
((x 0 >) (5) (3.14) IFELSE)
  ERRO: ramos devem ter o mesmo tipo (int vs real)
```

---

### 2. WHILE

**Sintaxe:** `(condição corpo WHILE)`

**Regra Semântica:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

**Regras:**
- Condição: Qualquer tipo conversível para boolean
- Corpo: Qualquer tipo T
- **Resultado: tipo da última expressão do corpo**

**Exemplo:**
```
((i 10 <) ((i 1 + i MEM)) WHILE)
  cond: boolean (i < 10)
  corpo: int (resultado do MEM)
  resultado: int
```

---

### 3. FOR

**Sintaxe:** `(inicio fim passo corpo FOR)`

**Regra Semântica:**
```
Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T
────────────────────────────────────────────────────────────────
              Γ ⊢ (init end step corpo FOR) : T
```

**Regras:**
- **Inicio, fim, passo: DEVEM ser int**
- Corpo: Qualquer tipo T
- **Resultado: tipo da última expressão do corpo**

**Exemplo:**
```
(0 10 1 ((i i +)) FOR)
  init: 0 (int)
  end: 10 (int)
  step: 1 (int)
  corpo: int
  resultado: int
```

**Erro Semântico:**
```
(0.0 10 1 (CORPO) FOR)
  ERRO: inicio deve ser int
```

---

## Comandos Especiais

### 1. Armazenamento em Memória (MEM)

**Sintaxe:** `(valor VARIAVEL)`

**Regra Semântica:**
```
Γ ⊢ e : T    T ∈ {int, real}    Γ[x ↦ (T, initialized)] ⊢ ...
───────────────────────────────────────────────────────────
            Γ ⊢ (e x) : T
```

**⚠️ Restrição Crítica:** Apenas `int` e `real` podem ser armazenados.
**Boolean NÃO pode ser armazenado!**

**Exemplos Válidos:**
```
(5 CONTADOR) → Armazena int 5 em CONTADOR
(3.14 PI) → Armazena real 3.14 em PI
```

**Erro Semântico:**
```
((5 3 >) RESULT) → ERRO: boolean não pode ser armazenado
```

---

### 2. Recuperação de Memória (MEM)

**Sintaxe:** `(VARIAVEL)`

**Regra Semântica:**
```
Γ(x) = (T, initialized)
───────────────────────
    Γ ⊢ (x) : T
```

**⚠️ Restrição Crítica:** Variável DEVE estar inicializada.

**Exemplo Válido:**
```
Linha 1: (5 VAR)     # Inicializa VAR com int 5
Linha 2: (VAR 3 +)   # OK: VAR é int, resultado int
```

**Erro Semântico:**
```
Linha 1: (MEM 3 +)   # ERRO: MEM não foi inicializada
```

---

### 3. Referência a Resultado (RES)

**Sintaxe:** `(N RES)` onde N = número de linhas atrás

**Regra Semântica:**
```
Γ ⊢ N : int    N ≥ 0    linha_atual - N ≥ 1    tipo_linha(atual - N) = T
──────────────────────────────────────────────────────────────────────────
                      Γ ⊢ (N RES) : T
```

**⚠️ Diferença de MEM:** RES **PODE** referenciar resultados boolean.

**Exemplos:**
```
Linha 1: (5 3 +)        # Resultado: int 8
Linha 2: (1 RES 2 *)    # OK: referencia int, resultado int 16

Linha 1: (5 3 >)        # Resultado: boolean true
Linha 2: (1 RES !)      # OK: referencia boolean, resultado boolean false
Linha 3: (2 RES 5 +)    # ERRO: boolean + int (incompatível)
```

---

## Exemplos Completos

### Exemplo 1: Cálculo com Promoção de Tipos

```
Linha 1: (5 3 +)           # int + int = int (8)
Linha 2: (1 RES 2.5 *)     # int * real = real (20.0)
Linha 3: (2 RES RESULTADO MEM)  # Armazena real 20.0
```

**Análise de Tipos:**
1. Linha 1: `int + int → int`
2. Linha 2: `int * real → real` (promoção)
3. Linha 3: `MEM(real)` ✅ válido

---

### Exemplo 2: Estrutura Condicional

```
Linha 1: (10 X MEM)             # Armazena 10 em X
Linha 2: ((X 0 >) (X 2 *) (X !) IFELSE)
```

**Análise:**
- Condição: `(X 0 >)` → boolean
- Ramo true: `(X 2 *)` → int (10 * 2 = 20)
- Ramo false: `(X !)` → boolean
- ❌ **ERRO:** ramos têm tipos diferentes (int vs boolean)

**Correção:**
```
((X 0 >) (X 2 *) (0) IFELSE)  # Ambos ramos são int
```

---

### Exemplo 3: Loop com Contador

```
Linha 1: (0 SOMA MEM)           # Inicializa SOMA = 0
Linha 2: (0 10 1 ((SOMA 1 RES + SOMA MEM)) FOR)
```

**Análise:**
- Linha 2:
  - Init: 0 (int) ✅
  - End: 10 (int) ✅
  - Step: 1 (int) ✅
  - Corpo: `(SOMA 1 RES + SOMA MEM)`
    - `SOMA + 1 RES` → int + int = int
    - Armazena em SOMA → tipo int
  - Resultado do FOR: int

---

### Exemplo 4: Erro - Boolean em MEM

```
Linha 1: (5 3 >)                # Resultado: boolean
Linha 2: (1 RES CONDICAO MEM)   # ❌ ERRO!
```

**Erro Semântico:**
```
ERRO SEMÂNTICO [Linha 2]: Tipo 'boolean' não pode ser armazenado em memória
Contexto: (1 RES CONDICAO MEM)
```

**Correção - Usar RES ao invés de MEM:**
```
Linha 1: (5 3 >)           # Resultado: boolean
Linha 2: (1 RES !)         # OK: referencia boolean via RES
```

---

## Sumário de Restrições Semânticas

| Operador/Comando | Restrição | Exemplo Inválido |
|------------------|-----------|------------------|
| `/`, `%` | Ambos operandos int | `(5.0 2 /)` |
| `^` | Expoente int > 0 | `(2 3.5 ^)`, `(2 -1 ^)` |
| IFELSE | Ramos mesmo tipo | `((c) (5) (3.14) IFELSE)` |
| FOR | Init/end/step int | `(0.5 10 1 corpo FOR)` |
| MEM Store | Apenas int/real | `((5 3 >) VAR)` |
| MEM Load | Deve estar inicializada | `(UNINIT 3 +)` |

---

## Estatísticas

- **Total de Regras Semânticas:** 22
- **Operadores Aritméticos:** 7
- **Operadores de Comparação:** 6
- **Operadores Lógicos:** 3
- **Estruturas de Controle:** 3
- **Comandos Especiais:** 3

---

**Documento gerado automaticamente a partir de:** `gramatica_atributos.py`
**Copyright © 2025 Grupo RA3_1 - PUCPR**
