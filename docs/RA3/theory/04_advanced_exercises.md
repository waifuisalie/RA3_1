# Exercícios Avançados de Análise Semântica

## Objetivo

Este documento apresenta **exercícios complexos** que combinam todos os conceitos aprendidos:
- Gramáticas de atributos
- Tabela de símbolos
- Sistema de tipos
- Promoção de tipos
- Estruturas de controle

**IMPORTANTE:** Todos os exercícios são explicados **passo a passo** com **justificativas detalhadas** do POR QUÊ de cada decisão.

---

## Índice

1. [Expressões Aritméticas Aninhadas](#1-expressões-aritméticas-aninhadas)
2. [Expressões Lógicas Complexas](#2-expressões-lógicas-complexas)
3. [Estruturas de Controle IFELSE](#3-estruturas-de-controle-ifelse)
4. [Estruturas de Controle WHILE](#4-estruturas-de-controle-while)
5. [Estruturas de Controle FOR](#5-estruturas-de-controle-for)
6. [Comando RES com Rastreamento](#6-comando-res-com-rastreamento)
7. [Detecção de Erros Semânticos](#7-detecção-de-erros-semânticos)
8. [Exercícios Integradores](#8-exercícios-integradores)

---

## 1. Expressões Aritméticas Aninhadas

### Exercício 1.1: Três Níveis de Aninhamento

**Expressão RPN:**
```
((5 3 +) (2.5 4 *) /)
```

**Objetivo:** Derivar completamente com árvore de derivação e evolução de tipos.

---

#### PASSO A PASSO DA DERIVAÇÃO

**NÍVEL 1: Avaliar a subexpressão mais interna esquerda**

```
Expressão: (5 3 +)
```

**PASSO 1.1:** Avaliar o primeiro operando
```
O QUE TEMOS: 5
É LITERAL? SIM (constante numérica)
TEM PONTO DECIMAL? NÃO
5 ∈ ℤ? SIM

REGRA APLICADA: INT-LITERAL
Γ ⊢ 5 : int

POR QUÊ: 5 é um número inteiro sem ponto decimal
```

**PASSO 1.2:** Avaliar o segundo operando
```
O QUE TEMOS: 3
É LITERAL? SIM
TEM PONTO DECIMAL? NÃO
3 ∈ ℤ? SIM

REGRA APLICADA: INT-LITERAL
Γ ⊢ 3 : int

POR QUÊ: 3 é um número inteiro sem ponto decimal
```

**PASSO 1.3:** Verificar compatibilidade dos operandos
```
OPERADOR: +
TIPO ESQUERDA: int
TIPO DIREITA: int

VERIFICAÇÃO: tipos_compativeis_aritmetica(int, int)
RESULTADO: TRUE

POR QUÊ: O operador + é PERMISSIVO, aceita int+int
```

**PASSO 1.4:** Determinar tipo do resultado
```
FUNÇÃO: tipo_resultado_aritmetica(int, int, '+')

LÓGICA:
  - Se operador é '|': retorna real (SEMPRE)
  - Senão: promover_tipo(int, int)

CÁLCULO:
  promover_tipo(int, int):
    - max(int, int) = int
    - Retorna: int

RESULTADO: int

POR QUÊ: int + int = int (sem promoção necessária)
```

**PASSO 1.5:** Aplicar regra semântica
```
REGRA APLICADA: ARITH-OP

Premissas:
  1. Γ ⊢ 5 : int         ✓
  2. Γ ⊢ 3 : int         ✓
  3. tipos_compativeis_aritmetica(int, int) ✓
  4. tipo = promover_tipo(int, int) = int ✓

Conclusão:
  Γ ⊢ (5 3 +) : int

POR QUÊ: Todas as premissas satisfeitas
```

---

**NÍVEL 2: Avaliar a subexpressão mais interna direita**

```
Expressão: (2.5 4 *)
```

**PASSO 2.1:** Avaliar o primeiro operando
```
O QUE TEMOS: 2.5
É LITERAL? SIM
TEM PONTO DECIMAL? SIM (tem ".5")
2.5 ∈ ℝ? SIM

REGRA APLICADA: REAL-LITERAL
Γ ⊢ 2.5 : real

POR QUÊ: 2.5 tem ponto decimal, logo é real
```

**PASSO 2.2:** Avaliar o segundo operando
```
O QUE TEMOS: 4
É LITERAL? SIM
TEM PONTO DECIMAL? NÃO
4 ∈ ℤ? SIM

REGRA APLICADA: INT-LITERAL
Γ ⊢ 4 : int

POR QUÊ: 4 é inteiro (sem ponto decimal)
```

**PASSO 2.3:** Verificar compatibilidade
```
OPERADOR: *
TIPO ESQUERDA: real
TIPO DIREITA: int

VERIFICAÇÃO: tipos_compativeis_aritmetica(real, int)
RESULTADO: TRUE

POR QUÊ: O operador * é PERMISSIVO, aceita real*int
```

**PASSO 2.4:** Determinar tipo do resultado
```
FUNÇÃO: tipo_resultado_aritmetica(real, int, '*')

LÓGICA:
  - Operador é '|'? NÃO
  - Então: promover_tipo(real, int)

CÁLCULO:
  promover_tipo(real, int):
    Hierarquia: int < real
    max(real, int) = real
    Retorna: real

RESULTADO: real

POR QUÊ: real * int → precisamos promover int para real
         4 vira 4.0, então 2.5 * 4.0 = real
```

**PASSO 2.5:** Aplicar regra semântica
```
REGRA APLICADA: ARITH-OP

Premissas:
  1. Γ ⊢ 2.5 : real      ✓
  2. Γ ⊢ 4 : int         ✓
  3. tipos_compativeis_aritmetica(real, int) ✓
  4. tipo = promover_tipo(real, int) = real ✓

Conclusão:
  Γ ⊢ (2.5 4 *) : real

POR QUÊ: Multiplicação promove para real
```

---

**NÍVEL 3: Avaliar a expressão completa**

```
Expressão: ((5 3 +) (2.5 4 *) /)
```

**PASSO 3.1:** Identificar operandos e operador
```
OPERANDO ESQUERDO: (5 3 +)
TIPO: int (do NÍVEL 1)

OPERANDO DIREITO: (2.5 4 *)
TIPO: real (do NÍVEL 2)

OPERADOR: / (divisão inteira)
```

**PASSO 3.2:** Verificar compatibilidade para divisão inteira
```
OPERADOR: /
TIPO ESQUERDA: int
TIPO DIREITA: real

VERIFICAÇÃO: tipos_compativeis_divisao_inteira(int, real)

LÓGICA DA FUNÇÃO:
  def tipos_compativeis_divisao_inteira(t1, t2):
      return t1 == TYPE_INT and t2 == TYPE_INT

CÁLCULO:
  t1 == TYPE_INT? SIM (int == int)
  t2 == TYPE_INT? NÃO (real != int)

  AND das condições: TRUE and FALSE = FALSE

RESULTADO: FALSE

POR QUÊ: A divisão inteira (/) REQUER int/int
         Temos int/real, o que é INCOMPATÍVEL
```

**PASSO 3.3:** Conclusão
```
ERRO SEMÂNTICO DETECTADO!

Mensagem: "Operador '/' requer operandos int+int, mas recebeu int e real"

POR QUÊ:
  - O operador / é RESTRITIVO (diferente de +, -, *, que são permissivos)
  - Divisão inteira só faz sentido com dois inteiros
  - 8 / 2 = 4 (int)
  - 8 / 2.5 → não tem sentido para divisão inteira
  - Para dividir por real, use | (divisão real)

CORREÇÃO SUGERIDA:
  Use: ((5 3 +) (2.5 4 *) |)
  Isso retornará real
```

---

#### ÁRVORE DE DERIVAÇÃO COMPLETA

```
                        ❌ ERRO
                           |
                   ((5 3 +) (2.5 4 *) /)
                   /                    \
              (5 3 +)                (2.5 4 *)
              tipo: int              tipo: real
              /    |    \            /    |     \
             5     3     +         2.5    4      *
          int   int   arith      real   int   arith
                                          ↓
                                      promove
                                       4→4.0

ERRO: Operador / requer int/int, mas tem int/real
```

**POR QUÊ A ÁRVORE TEM ERRO:**
- Subárvore esquerda está correta: (5 3 +) : int ✓
- Subárvore direita está correta: (2.5 4 *) : real ✓
- Raiz está ERRADA: / não aceita int/real ❌

---

### Exercício 1.2: Versão Corrigida com Divisão Real

**Expressão RPN:**
```
((5 3 +) (2.5 4 *) |)
```

**DERIVAÇÃO COMPLETA:**

**PASSO 1:** Subexpressão esquerda (REUTILIZAMOS DO EXERCÍCIO 1.1)
```
(5 3 +) : int
```

**PASSO 2:** Subexpressão direita (REUTILIZAMOS DO EXERCÍCIO 1.1)
```
(2.5 4 *) : real
```

**PASSO 3:** Avaliar divisão real
```
OPERADOR: | (divisão real)
TIPO ESQUERDA: int
TIPO DIREITA: real

VERIFICAÇÃO: tipos_compativeis_aritmetica(int, real)
RESULTADO: TRUE

POR QUÊ: O operador | é PERMISSIVO (aceita qualquer combinação numérica)
```

**PASSO 4:** Determinar tipo do resultado
```
FUNÇÃO: tipo_resultado_aritmetica(int, real, '|')

LÓGICA:
  - Se operador é '|': retorna real (SEMPRE!)

RESULTADO: real

POR QUÊ:
  - Divisão real SEMPRE retorna real
  - Mesmo int/int com | retorna real
  - Exemplo: (6 2 |) = 3.0 (não 3)
```

**PASSO 5:** Aplicar regra semântica
```
REGRA APLICADA: ARITH-OP

Premissas:
  1. Γ ⊢ (5 3 +) : int           ✓
  2. Γ ⊢ (2.5 4 *) : real         ✓
  3. tipos_compativeis_aritmetica(int, real) ✓
  4. operador == '|' → tipo = real ✓

Conclusão:
  Γ ⊢ ((5 3 +) (2.5 4 *) |) : real

POR QUÊ: Divisão real sempre retorna real
```

#### ÁRVORE DE DERIVAÇÃO

```
                        ✓ CORRETO
                           |
                   ((5 3 +) (2.5 4 *) |) : real
                   /                    \
              (5 3 +)                (2.5 4 *)
              tipo: int              tipo: real
              /    |    \            /    |     \
             5     3     +         2.5    4      *
          int   int   arith      real   int   arith

RESULTADO: real (divisão real sempre retorna real)
```

---

## 2. Expressões Lógicas Complexas

### Exercício 2.1: Lógica com Truthiness

**Expressão RPN:**
```
(5 0 &&)
```

**Objetivo:** Demonstrar conversão de truthiness para booleano.

---

#### DERIVAÇÃO COMPLETA

**PASSO 1:** Avaliar primeiro operando
```
O QUE TEMOS: 5
TIPO: int (literal inteiro)

REGRA APLICADA: INT-LITERAL
Γ ⊢ 5 : int
```

**PASSO 2:** Avaliar segundo operando
```
O QUE TEMOS: 0
TIPO: int (literal inteiro)

REGRA APLICADA: INT-LITERAL
Γ ⊢ 0 : int
```

**PASSO 3:** Verificar compatibilidade para operador lógico
```
OPERADOR: && (AND lógico)
TIPO ESQUERDA: int
TIPO DIREITA: int

VERIFICAÇÃO: tipos_compativeis_logica(int, int)

LÓGICA DA FUNÇÃO:
  def tipos_compativeis_logica(t1, t2):
      # Modo PERMISSIVO: aceita int, real, boolean
      return t1 in [TYPE_INT, TYPE_REAL, TYPE_BOOLEAN] and \
             t2 in [TYPE_INT, TYPE_REAL, TYPE_BOOLEAN]

CÁLCULO:
  int ∈ {int, real, boolean}? SIM
  int ∈ {int, real, boolean}? SIM

RESULTADO: TRUE

POR QUÊ: Modo permissivo aceita int através de truthiness
```

**PASSO 4:** Aplicar conversão de truthiness
```
FUNÇÃO: para_booleano(valor, tipo)

PARA OPERANDO ESQUERDO (5):
  valor = 5
  tipo = int

  LÓGICA:
    Se tipo == boolean: retorna valor (já é boolean)
    Senão: retorna (valor != 0)

  CÁLCULO:
    5 != 0? SIM
    Retorna: true

  POR QUÊ: Qualquer número diferente de zero é "truthy"

PARA OPERANDO DIREITO (0):
  valor = 0
  tipo = int

  LÓGICA:
    Se tipo == boolean: retorna valor
    Senão: retorna (valor != 0)

  CÁLCULO:
    0 != 0? NÃO
    Retorna: false

  POR QUÊ: Zero é "falsy" (representa falso)
```

**PASSO 5:** Aplicar operação lógica
```
OPERAÇÃO: truthy(5) && truthy(0)
        = true && false
        = false

TIPO DO RESULTADO: boolean

POR QUÊ: Operadores lógicos SEMPRE retornam boolean
```

**PASSO 6:** Aplicar regra semântica
```
REGRA APLICADA: LOGIC-AND

Premissas:
  1. Γ ⊢ 5 : int                        ✓
  2. Γ ⊢ 0 : int                        ✓
  3. tipos_compativeis_logica(int, int) ✓
  4. esq_bool = truthy(5) = true        ✓
  5. dir_bool = truthy(0) = false       ✓
  6. resultado = true && false = false  ✓
  7. tipo_resultado = boolean           ✓

Conclusão:
  Γ ⊢ (5 0 &&) : boolean

POR QUÊ: Conversão de truthiness permite int em operador lógico
```

---

### Exercício 2.2: Lógica Aninhada com Comparação

**Expressão RPN:**
```
((5 3 >) (2 0 !=) &&)
```

**DERIVAÇÃO COMPLETA:**

**NÍVEL 1: Subexpressão esquerda**
```
Expressão: (5 3 >)
```

**PASSO 1.1:** Avaliar operandos
```
Γ ⊢ 5 : int
Γ ⊢ 3 : int
```

**PASSO 1.2:** Verificar compatibilidade para comparação
```
OPERADOR: >
TIPO ESQUERDA: int
TIPO DIREITA: int

VERIFICAÇÃO: tipos_compativeis_comparacao(int, int)

LÓGICA:
  - Aceita: int, real (qualquer combinação)

RESULTADO: TRUE

POR QUÊ: Comparação numérica aceita int/int
```

**PASSO 1.3:** Aplicar comparação
```
OPERAÇÃO: 5 > 3
RESULTADO VALOR: true
TIPO RESULTADO: boolean

POR QUÊ: Comparações SEMPRE retornam boolean
```

**PASSO 1.4:** Aplicar regra
```
REGRA APLICADA: COMP-OP

Conclusão:
  Γ ⊢ (5 3 >) : boolean
```

---

**NÍVEL 2: Subexpressão direita**
```
Expressão: (2 0 !=)
```

**PASSO 2.1:** Avaliar operandos
```
Γ ⊢ 2 : int
Γ ⊢ 0 : int
```

**PASSO 2.2:** Verificar compatibilidade
```
VERIFICAÇÃO: tipos_compativeis_comparacao(int, int)
RESULTADO: TRUE
```

**PASSO 2.3:** Aplicar comparação
```
OPERAÇÃO: 2 != 0
RESULTADO VALOR: true (2 é diferente de 0)
TIPO RESULTADO: boolean
```

**PASSO 2.4:** Aplicar regra
```
REGRA APLICADA: COMP-OP

Conclusão:
  Γ ⊢ (2 0 !=) : boolean
```

---

**NÍVEL 3: Operação lógica completa**
```
Expressão: ((5 3 >) (2 0 !=) &&)
```

**PASSO 3.1:** Identificar operandos
```
OPERANDO ESQUERDO: (5 3 >) : boolean
OPERANDO DIREITO: (2 0 !=) : boolean
OPERADOR: &&
```

**PASSO 3.2:** Verificar compatibilidade
```
VERIFICAÇÃO: tipos_compativeis_logica(boolean, boolean)

LÓGICA:
  boolean ∈ {int, real, boolean}? SIM
  boolean ∈ {int, real, boolean}? SIM

RESULTADO: TRUE

POR QUÊ: boolean é diretamente compatível (sem conversão)
```

**PASSO 3.3:** Aplicar operação lógica
```
OPERAÇÃO: true && true = true

POR QUÊ:
  - (5 3 >) = true (5 é maior que 3)
  - (2 0 !=) = true (2 é diferente de 0)
  - true && true = true
```

**PASSO 3.4:** Aplicar regra
```
REGRA APLICADA: LOGIC-AND

Premissas:
  1. Γ ⊢ (5 3 >) : boolean      ✓
  2. Γ ⊢ (2 0 !=) : boolean     ✓
  3. tipos_compativeis_logica(boolean, boolean) ✓
  4. esq_bool = true            ✓
  5. dir_bool = true            ✓
  6. resultado = true && true = true ✓
  7. tipo = boolean             ✓

Conclusão:
  Γ ⊢ ((5 3 >) (2 0 !=) &&) : boolean
```

#### ÁRVORE DE DERIVAÇÃO

```
                    ((5 3 >) (2 0 !=) &&) : boolean
                    /                     \
              (5 3 >) : boolean      (2 0 !=) : boolean
              /   |    \             /   |     \
             5    3     >           2    0      !=
           int  int   comp        int  int    comp

           true                   true
                    \            /
                     true && true = true
```

---

## 3. Estruturas de Controle IFELSE

### Exercício 3.1: IFELSE com Branches Compatíveis

**Expressão RPN:**
```
((5 3 >) (10 2 +) (8 4 +) IFELSE)
```

**Objetivo:** Demonstrar verificação de compatibilidade de branches.

---

#### DERIVAÇÃO COMPLETA

**PASSO 1: Avaliar condição**
```
Expressão: (5 3 >)

DERIVAÇÃO (resumida, já vimos antes):
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  tipos_compativeis_comparacao(int, int) ✓
  5 > 3 = true

CONCLUSÃO:
  Γ ⊢ (5 3 >) : boolean
```

**PASSO 2: Avaliar branch verdadeiro (then)**
```
Expressão: (10 2 +)

DERIVAÇÃO:
  Γ ⊢ 10 : int
  Γ ⊢ 2 : int
  tipos_compativeis_aritmetica(int, int) ✓
  tipo = promover_tipo(int, int) = int

CONCLUSÃO:
  Γ ⊢ (10 2 +) : int
```

**PASSO 3: Avaliar branch falso (else)**
```
Expressão: (8 4 +)

DERIVAÇÃO:
  Γ ⊢ 8 : int
  Γ ⊢ 4 : int
  tipos_compativeis_aritmetica(int, int) ✓
  tipo = promover_tipo(int, int) = int

CONCLUSÃO:
  Γ ⊢ (8 4 +) : int
```

**PASSO 4: Verificar compatibilidade dos branches**
```
TIPO BRANCH THEN: int
TIPO BRANCH ELSE: int

VERIFICAÇÃO: branches_compativeis(int, int)

LÓGICA DA FUNÇÃO:
  def branches_compativeis(tipo_then, tipo_else):
      return promover_tipo(tipo_then, tipo_else) is not None

CÁLCULO:
  promover_tipo(int, int) = int (não é None)

RESULTADO: TRUE

POR QUÊ: Ambos branches têm o mesmo tipo, então são compatíveis
```

**PASSO 5: Determinar tipo do resultado**
```
TIPO RESULTADO = promover_tipo(tipo_then, tipo_else)
                = promover_tipo(int, int)
                = int

POR QUÊ: O resultado de IFELSE é o tipo comum dos branches
```

**PASSO 6: Aplicar regra semântica**
```
REGRA APLICADA: IFELSE-CTRL

Premissas:
  1. Γ ⊢ (5 3 >) : boolean              ✓
  2. Γ ⊢ (10 2 +) : int                 ✓
  3. Γ ⊢ (8 4 +) : int                  ✓
  4. branches_compativeis(int, int)     ✓
  5. tipo = promover_tipo(int, int) = int ✓

Conclusão:
  Γ ⊢ ((5 3 >) (10 2 +) (8 4 +) IFELSE) : int

POR QUÊ: Todos os requisitos de IFELSE foram satisfeitos
```

#### ÁRVORE DE DERIVAÇÃO

```
        ((5 3 >) (10 2 +) (8 4 +) IFELSE) : int
        /           |           |          \
   (5 3 >)      (10 2 +)    (8 4 +)      IFELSE
   boolean        int          int        ctrl

   true           12           12
                   \           /
                  tipos compatíveis: int
                  resultado: int
```

---

### Exercício 3.2: IFELSE com Promoção de Tipos

**Expressão RPN:**
```
((10 5 >) (3.5 2.0 +) (7 1 -) IFELSE)
```

**DERIVAÇÃO COMPLETA:**

**PASSO 1: Condição**
```
(10 5 >) : boolean
```

**PASSO 2: Branch then**
```
Expressão: (3.5 2.0 +)

DERIVAÇÃO:
  Γ ⊢ 3.5 : real (tem ponto decimal)
  Γ ⊢ 2.0 : real (tem ponto decimal)
  tipos_compativeis_aritmetica(real, real) ✓
  tipo = promover_tipo(real, real) = real

CONCLUSÃO:
  Γ ⊢ (3.5 2.0 +) : real
```

**PASSO 3: Branch else**
```
Expressão: (7 1 -)

DERIVAÇÃO:
  Γ ⊢ 7 : int
  Γ ⊢ 1 : int
  tipos_compativeis_aritmetica(int, int) ✓
  tipo = promover_tipo(int, int) = int

CONCLUSÃO:
  Γ ⊢ (7 1 -) : int
```

**PASSO 4: Verificar compatibilidade dos branches**
```
TIPO BRANCH THEN: real
TIPO BRANCH ELSE: int

VERIFICAÇÃO: branches_compativeis(real, int)

CÁLCULO:
  promover_tipo(real, int) = real (não é None)

RESULTADO: TRUE

POR QUÊ: int pode ser promovido para real
```

**PASSO 5: Determinar tipo do resultado**
```
TIPO RESULTADO = promover_tipo(real, int)
                = real

POR QUÊ:
  - Branch then retorna real
  - Branch else retorna int
  - Precisamos de tipo comum
  - int é promovido para real
  - Resultado final: real
```

**PASSO 6: Aplicar regra**
```
REGRA APLICADA: IFELSE-CTRL

Premissas:
  1. Γ ⊢ (10 5 >) : boolean             ✓
  2. Γ ⊢ (3.5 2.0 +) : real             ✓
  3. Γ ⊢ (7 1 -) : int                  ✓
  4. branches_compativeis(real, int)    ✓
  5. tipo = promover_tipo(real, int) = real ✓

Conclusão:
  Γ ⊢ ((10 5 >) (3.5 2.0 +) (7 1 -) IFELSE) : real

POR QUÊ: Promoção de tipos permitiu compatibilidade
```

---

### Exercício 3.3: IFELSE com ERRO - Branches Incompatíveis

**Expressão RPN:**
```
((1 0 >) (5 3 +) (10 5 >) IFELSE)
```

**DERIVAÇÃO COMPLETA:**

**PASSO 1: Condição**
```
(1 0 >) : boolean ✓
```

**PASSO 2: Branch then**
```
Expressão: (5 3 +)

DERIVAÇÃO:
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  tipo = int

CONCLUSÃO:
  Γ ⊢ (5 3 +) : int
```

**PASSO 3: Branch else**
```
Expressão: (10 5 >)

DERIVAÇÃO:
  Γ ⊢ 10 : int
  Γ ⊢ 5 : int
  tipos_compativeis_comparacao(int, int) ✓
  10 > 5 = true
  tipo = boolean

CONCLUSÃO:
  Γ ⊢ (10 5 >) : boolean
```

**PASSO 4: Verificar compatibilidade**
```
TIPO BRANCH THEN: int
TIPO BRANCH ELSE: boolean

VERIFICAÇÃO: branches_compativeis(int, boolean)

LÓGICA:
  promover_tipo(int, boolean):
    Hierarquia: int < real
    boolean NÃO está na hierarquia
    Retorna: None

RESULTADO: FALSE (promover_tipo retornou None)

POR QUÊ: int e boolean são tipos INCOMPATÍVEIS
```

**PASSO 5: Conclusão**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "Branches de IFELSE têm tipos incompatíveis: int e boolean"

POR QUÊ:
  - IFELSE precisa retornar UM único tipo
  - Branch then retorna int
  - Branch else retorna boolean
  - Não existe conversão int ↔ boolean
  - Logo, IMPOSSÍVEL determinar tipo de retorno

CORREÇÃO:
  Certifique-se de que ambos branches retornem tipos compatíveis:
  - int/int ✓
  - int/real ✓ (promove para real)
  - real/real ✓
  - boolean/boolean ✓
  - int/boolean ❌
  - real/boolean ❌
```

---

## 4. Estruturas de Controle WHILE

### Exercício 4.1: WHILE Básico

**Expressão RPN:**
```
((COUNTER 10 <) (COUNTER 1 +) WHILE)
```

**Contexto:**
```
Ambiente inicial:
Γ₀ = {COUNTER: int, inicializada: true}
```

**DERIVAÇÃO COMPLETA:**

**PASSO 1: Avaliar condição**
```
Expressão: (COUNTER 10 <)
```

**PASSO 1.1: Avaliar COUNTER**
```
O QUE TEMOS: COUNTER
É VARIÁVEL? SIM

BUSCAR NA TABELA:
  nome = "COUNTER"
  COUNTER ∈ dom(Γ₀)? SIM

INFORMAÇÕES:
  tipo = int
  inicializada = true

VERIFICAÇÃO: inicializada == true? SIM ✓

REGRA APLICADA: VAR-USE

Conclusão:
  Γ₀ ⊢ COUNTER : int

POR QUÊ: Variável existe, está inicializada, tipo é int
```

**PASSO 1.2: Avaliar 10**
```
Γ₀ ⊢ 10 : int
```

**PASSO 1.3: Aplicar comparação**
```
OPERADOR: <
TIPO ESQUERDA: int
TIPO DIREITA: int

tipos_compativeis_comparacao(int, int) ✓

RESULTADO OPERAÇÃO: COUNTER < 10 (valor depende de runtime)
TIPO RESULTADO: boolean

REGRA APLICADA: COMP-OP

Conclusão:
  Γ₀ ⊢ (COUNTER 10 <) : boolean
```

**PASSO 2: Avaliar corpo do WHILE**
```
Expressão: (COUNTER 1 +)
```

**PASSO 2.1: Avaliar operandos**
```
Γ₀ ⊢ COUNTER : int (já derivado)
Γ₀ ⊢ 1 : int
```

**PASSO 2.2: Aplicar adição**
```
OPERADOR: +
TIPO ESQUERDA: int
TIPO DIREITA: int

tipos_compativeis_aritmetica(int, int) ✓
tipo = promover_tipo(int, int) = int

REGRA APLICADA: ARITH-OP

Conclusão:
  Γ₀ ⊢ (COUNTER 1 +) : int
```

**PASSO 3: Aplicar regra WHILE**
```
REGRA APLICADA: WHILE-CTRL

Premissas:
  1. Γ₀ ⊢ (COUNTER 10 <) : boolean     ✓
  2. Γ₀ ⊢ (COUNTER 1 +) : int          ✓
  3. tipo_resultado = tipo_corpo = int ✓

Conclusão:
  Γ₀ ⊢ ((COUNTER 10 <) (COUNTER 1 +) WHILE) : int

POR QUÊ: WHILE retorna o tipo da última expressão do corpo
```

#### OBSERVAÇÃO IMPORTANTE

```
SEMÂNTICA RUNTIME vs SEMÂNTICA ESTÁTICA:

ANÁLISE SEMÂNTICA (compile-time):
  - Verifica TIPOS
  - Condição é boolean? ✓
  - Corpo tem tipo consistente? ✓
  - NÃO verifica se loop termina

EXECUÇÃO (runtime):
  - Avalia condição: COUNTER < 10
  - Se true: executa corpo, repete
  - Se false: termina

POR QUÊ: Análise semântica garante type safety, não comportamento runtime
```

---

## 5. Estruturas de Controle FOR

### Exercício 5.1: FOR com Parâmetros Válidos

**Expressão RPN:**
```
((1 10 2 FOR) (I 2 *) FOR)
```

**Objetivo:** Demonstrar validação de parâmetros do FOR e corpo.

---

#### DERIVAÇÃO COMPLETA

**PASSO 1: Avaliar parâmetros do FOR**

**PASSO 1.1: Avaliar init (início)**
```
Expressão: 1

Γ ⊢ 1 : int

POR QUÊ: 1 é literal inteiro
```

**PASSO 1.2: Avaliar end (fim)**
```
Expressão: 10

Γ ⊢ 10 : int

POR QUÊ: 10 é literal inteiro
```

**PASSO 1.3: Avaliar step (passo)**
```
Expressão: 2

Γ ⊢ 2 : int

POR QUÊ: 2 é literal inteiro
```

**PASSO 1.4: Verificar compatibilidade dos parâmetros**
```
VERIFICAÇÃO: parametros_for_validos(int, int, int)

LÓGICA DA FUNÇÃO:
  def parametros_for_validos(tipo_init, tipo_end, tipo_step):
      return (tipo_init == TYPE_INT and
              tipo_end == TYPE_INT and
              tipo_step == TYPE_INT)

CÁLCULO:
  tipo_init == TYPE_INT? SIM (int == int)
  tipo_end == TYPE_INT? SIM (int == int)
  tipo_step == TYPE_INT? SIM (int == int)

  AND: TRUE and TRUE and TRUE = TRUE

RESULTADO: TRUE

POR QUÊ: FOR requer que todos os parâmetros sejam int
         (início, fim, passo DEVEM ser inteiros)
```

**PASSO 2: Avaliar corpo do FOR**
```
Expressão: (I 2 *)
```

**OBSERVAÇÃO SOBRE VARIÁVEL I:**
```
CONTEXTO: Dentro do FOR, a variável I é implicitamente declarada

AMBIENTE ESTENDIDO:
  Γ_for = Γ ∪ {I: int, inicializada: true}

POR QUÊ:
  - FOR cria automaticamente variável de controle I
  - Tipo de I é sempre int
  - I está sempre inicializada (começa com valor init)
```

**PASSO 2.1: Avaliar I**
```
Γ_for ⊢ I : int

POR QUÊ: I foi implicitamente declarada pelo FOR
```

**PASSO 2.2: Avaliar 2**
```
Γ_for ⊢ 2 : int
```

**PASSO 2.3: Aplicar multiplicação**
```
OPERADOR: *
TIPO ESQUERDA: int
TIPO DIREITA: int

tipos_compativeis_aritmetica(int, int) ✓
tipo = promover_tipo(int, int) = int

REGRA APLICADA: ARITH-OP

Conclusão:
  Γ_for ⊢ (I 2 *) : int
```

**PASSO 3: Aplicar regra FOR**
```
REGRA APLICADA: FOR-CTRL

Premissas:
  1. Γ ⊢ 1 : int                                    ✓
  2. Γ ⊢ 10 : int                                   ✓
  3. Γ ⊢ 2 : int                                    ✓
  4. parametros_for_validos(int, int, int)          ✓
  5. Γ_for = Γ ∪ {I: int, inicializada: true}       ✓
  6. Γ_for ⊢ (I 2 *) : int                          ✓
  7. tipo_resultado = tipo_corpo = int              ✓

Conclusão:
  Γ ⊢ ((1 10 2 FOR) (I 2 *) FOR) : int

POR QUÊ:
  - Parâmetros são int ✓
  - Corpo é avaliado em ambiente estendido ✓
  - Resultado é tipo do corpo ✓
```

#### SEMÂNTICA RUNTIME DO FOR

```
EXECUÇÃO (para entendimento):

Iteração 1: I = 1  → corpo avalia (1 2 *) = 2
Iteração 2: I = 3  → corpo avalia (3 2 *) = 6
Iteração 3: I = 5  → corpo avalia (5 2 *) = 10
Iteração 4: I = 7  → corpo avalia (7 2 *) = 14
Iteração 5: I = 9  → corpo avalia (9 2 *) = 18
Iteração 6: I = 11 → PARA (I > end)

RESULTADO: 18 (último valor calculado)
TIPO: int

POR QUÊ: FOR retorna último valor do corpo
```

---

### Exercício 5.2: FOR com ERRO - Parâmetro Real

**Expressão RPN:**
```
((1 10.5 1 FOR) (I) FOR)
```

**DERIVAÇÃO:**

**PASSO 1: Avaliar parâmetros**
```
Γ ⊢ 1 : int
Γ ⊢ 10.5 : real  ← PROBLEMA AQUI
Γ ⊢ 1 : int
```

**PASSO 2: Verificar parâmetros**
```
VERIFICAÇÃO: parametros_for_validos(int, real, int)

LÓGICA:
  tipo_init == TYPE_INT? SIM (int == int)
  tipo_end == TYPE_INT? NÃO (real != int)
  tipo_step == TYPE_INT? SIM (int == int)

  AND: TRUE and FALSE and TRUE = FALSE

RESULTADO: FALSE

POR QUÊ: Segundo parâmetro (end) é real, mas deve ser int
```

**PASSO 3: Conclusão**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "FOR requer parâmetros int, mas recebeu (int, real, int)"

POR QUÊ:
  - FOR itera sobre valores INTEIROS
  - init = 1, end = 10.5, step = 1
  - Como iterar até 10.5 com passo 1?
  - I teria valores: 1, 2, 3, ..., 10, 11 (pula 10.5!)
  - AMBÍGUO e INCONSISTENTE

CORREÇÃO:
  Use: ((1 10 1 FOR) (I) FOR)
  Ou: converta 10.5 para 11 manualmente
```

---

## 6. Comando RES com Rastreamento

### Exercício 6.1: RES Básico

**Programa RPN:**
```
Linha 1: (5 3 +)
Linha 2: (1 RES 2 *)
```

**Objetivo:** Demonstrar referência a resultados anteriores.

---

#### DERIVAÇÃO COMPLETA

**ANÁLISE DA LINHA 1:**
```
Expressão: (5 3 +)

DERIVAÇÃO:
  Γ ⊢ 5 : int
  Γ ⊢ 3 : int
  tipos_compativeis_aritmetica(int, int) ✓
  tipo = int

CONCLUSÃO:
  Γ ⊢ (5 3 +) : int

RESULTADO RUNTIME: 8
TIPO: int
```

**TABELA DE RESULTADOS APÓS LINHA 1:**
```
Linha | Resultado | Tipo
------|-----------|-----
  1   |     8     | int
```

---

**ANÁLISE DA LINHA 2:**
```
Expressão: (1 RES 2 *)
```

**PASSO 1: Avaliar primeiro operando**
```
Γ ⊢ 1 : int
```

**PASSO 2: Avaliar RES**
```
Expressão: RES
N = 1 (número antes de RES)
```

**PASSO 2.1: Verificar referência**
```
LINHA ATUAL: 2
VOLTAR N LINHAS: 1
LINHA REFERENCIADA: 2 - 1 = 1

VERIFICAÇÃO: linha 1 existe? SIM ✓
VERIFICAÇÃO: 1 <= linha_atual - 1? SIM (1 <= 1) ✓
```

**PASSO 2.2: Buscar tipo da linha referenciada**
```
TABELA DE RESULTADOS:
  Linha 1: tipo = int

TIPO DO RES: int

POR QUÊ: RES herda o tipo da linha que referencia
```

**PASSO 2.3: Aplicar regra RES**
```
REGRA APLICADA: RES-REF

Premissas:
  1. Γ ⊢ 1 : int                                ✓
  2. n = 1                                      ✓
  3. linha_ref = linha_atual - n = 2 - 1 = 1    ✓
  4. 1 <= linha_atual - 1 = 1                   ✓
  5. tipo(linha 1) = int                        ✓

Conclusão:
  Γ ⊢ (1 RES) : int

POR QUÊ: RES referencia linha 1 que tem tipo int
```

**PASSO 3: Avaliar terceiro operando**
```
Γ ⊢ 2 : int
```

**PASSO 4: Aplicar multiplicação**
```
OPERADOR: *
TIPO ESQUERDA: int (de 1 RES)
TIPO DIREITA: int (de 2)

tipos_compativeis_aritmetica(int, int) ✓
tipo = promover_tipo(int, int) = int

REGRA APLICADA: ARITH-OP

Conclusão:
  Γ ⊢ (1 RES 2 *) : int

POR QUÊ: int * int = int
```

**RESULTADO RUNTIME:**
```
1 RES → valor da linha 1 → 8
(8 2 *) → 16

TABELA ATUALIZADA:
Linha | Resultado | Tipo
------|-----------|-----
  1   |     8     | int
  2   |    16     | int
```

---

### Exercício 6.2: RES com Múltiplas Referências

**Programa RPN:**
```
Linha 1: (10 5 -)
Linha 2: (3 2 +)
Linha 3: (2 RES 1 RES *)
```

**ANÁLISE DA LINHA 1:**
```
Γ ⊢ (10 5 -) : int
Resultado runtime: 5
```

**ANÁLISE DA LINHA 2:**
```
Γ ⊢ (3 2 +) : int
Resultado runtime: 5
```

**TABELA APÓS LINHA 2:**
```
Linha | Resultado | Tipo
------|-----------|-----
  1   |     5     | int
  2   |     5     | int
```

---

**ANÁLISE DA LINHA 3:**
```
Expressão: (2 RES 1 RES *)
```

**PASSO 1: Avaliar primeiro operando (2 RES)**
```
N = 2
Linha referenciada = 3 - 2 = 1

VERIFICAÇÃO:
  Linha 1 existe? SIM ✓
  2 <= (3 - 1) = 2? SIM ✓

TIPO: int (da linha 1)

Γ ⊢ (2 RES) : int

POR QUÊ: Referencia linha 1 que retornou int
```

**PASSO 2: Avaliar segundo operando (1 RES)**
```
N = 1
Linha referenciada = 3 - 1 = 2

VERIFICAÇÃO:
  Linha 2 existe? SIM ✓
  1 <= (3 - 1) = 2? SIM ✓

TIPO: int (da linha 2)

Γ ⊢ (1 RES) : int

POR QUÊ: Referencia linha 2 que retornou int
```

**PASSO 3: Aplicar multiplicação**
```
OPERADOR: *
TIPO ESQUERDA: int (de 2 RES)
TIPO DIREITA: int (de 1 RES)

tipos_compativeis_aritmetica(int, int) ✓
tipo = promover_tipo(int, int) = int

Conclusão:
  Γ ⊢ (2 RES 1 RES *) : int
```

**RESULTADO RUNTIME:**
```
2 RES → linha 1 → 5
1 RES → linha 2 → 5
(5 5 *) → 25

TABELA ATUALIZADA:
Linha | Resultado | Tipo
------|-----------|-----
  1   |     5     | int
  2   |     5     | int
  3   |    25     | int
```

---

### Exercício 6.3: RES com ERRO - Referência Inválida

**Programa RPN:**
```
Linha 1: (5 3 +)
Linha 2: (3 RES)
```

**ANÁLISE DA LINHA 1:**
```
Γ ⊢ (5 3 +) : int ✓
```

**ANÁLISE DA LINHA 2:**
```
Expressão: (3 RES)

N = 3
Linha referenciada = 2 - 3 = -1
```

**VERIFICAÇÃO:**
```
LINHA REFERENCIADA: -1
VERIFICAÇÃO: linha -1 existe? NÃO ❌

OUTRA VERIFICAÇÃO: 3 <= (linha_atual - 1)?
  3 <= (2 - 1) = 1?
  3 <= 1? NÃO ❌

RESULTADO: ERRO
```

**CONCLUSÃO:**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "RES referencia linha inválida: tentou voltar 3 linhas, mas estamos na linha 2"

POR QUÊ:
  - Estamos na linha 2
  - RES pede para voltar 3 linhas
  - Linha 2 - 3 = -1 (NÃO EXISTE)
  - Só podemos referenciar linhas anteriores existentes

CORREÇÃO:
  Use: (1 RES) para referenciar linha 1
  Regra: N <= linha_atual - 1
```

---

## 7. Detecção de Erros Semânticos

### Exercício 7.1: Variável Não Inicializada

**Programa RPN:**
```
Linha 1: (X 5 +)
```

**Ambiente:**
```
Γ₀ = {X: int, inicializada: false}
```

**DERIVAÇÃO:**

**PASSO 1: Tentar avaliar X**
```
O QUE TEMOS: X
É VARIÁVEL? SIM

BUSCAR NA TABELA:
  nome = "X"
  X ∈ dom(Γ₀)? SIM

INFORMAÇÕES ENCONTRADAS:
  tipo = int
  inicializada = false  ← PROBLEMA!
```

**PASSO 2: Verificar inicialização**
```
VERIFICAÇÃO: inicializada == true?
  false == true? NÃO ❌

RESULTADO: ERRO
```

**CONCLUSÃO:**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "Variável 'X' usada antes de ser inicializada"

POR QUÊ:
  - X foi declarada (existe na tabela)
  - Mas não tem valor ainda (inicializada = false)
  - Usar X agora leria "lixo de memória"
  - Análise semântica PREVINE este erro

CORREÇÃO:
  Linha 1: (5 X)      # Armazena 5 em X
  Linha 2: (X 5 +)    # Agora pode usar X

POR QUÊ DA CORREÇÃO:
  - (5 X) executa MEM_STORE
  - Marca X como inicializada
  - Linha 2 pode usar X com segurança
```

---

### Exercício 7.2: Tipo Incompatível para Armazenamento

**Expressão RPN:**
```
((5 3 >) VAR)
```

**Ambiente:**
```
Γ₀ = {VAR: int, inicializada: false}
```

**DERIVAÇÃO:**

**PASSO 1: Avaliar expressão a armazenar**
```
Expressão: (5 3 >)

DERIVAÇÃO:
  Γ₀ ⊢ 5 : int
  Γ₀ ⊢ 3 : int
  tipos_compativeis_comparacao(int, int) ✓
  5 > 3 = true
  tipo = boolean

CONCLUSÃO:
  Γ₀ ⊢ (5 3 >) : boolean
```

**PASSO 2: Tentar armazenar em VAR**
```
OPERAÇÃO: MEM_STORE
VALOR: resultado de (5 3 >)
TIPO DO VALOR: boolean
VARIÁVEL: VAR
```

**PASSO 3: Verificar compatibilidade de armazenamento**
```
VERIFICAÇÃO: tipo_compativel_armazenamento(boolean)

LÓGICA DA FUNÇÃO:
  def tipo_compativel_armazenamento(tipo):
      # MEM só pode armazenar int e real
      # BOOLEAN NÃO PODE SER ARMAZENADO
      return tipo in [TYPE_INT, TYPE_REAL]

CÁLCULO:
  boolean ∈ {int, real}? NÃO ❌

RESULTADO: FALSE
```

**CONCLUSÃO:**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "MEM não pode armazenar tipo boolean (apenas int ou real)"

POR QUÊ:
  - Requisito explícito: "boolean não pode ser armazenado em MEM"
  - Razão: MEM é para valores numéricos
  - (5 3 >) retorna boolean
  - Logo, não pode armazenar

CORREÇÃO:
  Linha 1: ((5 3 >) (1) (0) IFELSE VAR)

  POR QUÊ DA CORREÇÃO:
    - IFELSE retorna 1 se true, 0 se false
    - 1 e 0 são int
    - int PODE ser armazenado
    - Converte boolean → int
```

---

### Exercício 7.3: Potência com Expoente Negativo

**Expressão RPN:**
```
(2 -3 ^)
```

**OBSERVAÇÃO INICIAL:**
```
RPN NÃO TEM UNARY MINUS!

Como representar -3?
  Resposta: (0 3 -)

Expressão correta seria:
  (2 (0 3 -) ^)
```

**VAMOS ASSUMIR QUE -3 CHEGOU COMO RESULTADO:**

**Programa RPN:**
```
Linha 1: (0 3 -)
Linha 2: (2 1 RES ^)
```

**ANÁLISE DA LINHA 1:**
```
Γ ⊢ (0 3 -) : int
Resultado runtime: -3
```

**ANÁLISE DA LINHA 2:**
```
Expressão: (2 1 RES ^)
```

**PASSO 1: Avaliar base**
```
Γ ⊢ 2 : int
```

**PASSO 2: Avaliar expoente (1 RES)**
```
1 RES → linha 1 → tipo: int
Γ ⊢ (1 RES) : int
```

**PASSO 3: Verificar compatibilidade para potência**
```
OPERADOR: ^
TIPO BASE: int
TIPO EXPOENTE: int

VERIFICAÇÃO: tipos_compativeis_potencia(int, int, valor_expoente)

LÓGICA DA FUNÇÃO:
  def tipos_compativeis_potencia(tipo_base, tipo_exp, valor_exp):
      # Base pode ser int ou real
      # Expoente DEVE ser int
      # Expoente DEVE ser >= 0 (não negativo!)
      return (tipo_base in [TYPE_INT, TYPE_REAL] and
              tipo_exp == TYPE_INT and
              valor_exp >= 0)

CÁLCULO:
  tipo_base ∈ {int, real}? SIM (int ∈ {int, real})
  tipo_exp == TYPE_INT? SIM (int == int)
  valor_exp >= 0? NÃO (-3 < 0) ❌

  AND: TRUE and TRUE and FALSE = FALSE

RESULTADO: FALSE
```

**CONCLUSÃO:**
```
❌ ERRO SEMÂNTICO DETECTADO!

Mensagem: "Operador '^' requer expoente positivo, mas recebeu -3"

POR QUÊ:
  - Requisito: expoente deve ser inteiro E positivo
  - Temos: 2^(-3)
  - Resultado seria: 1/(2^3) = 0.125
  - Mas nossa linguagem não suporta expoentes negativos

POR QUÊ NÃO SUPORTAMOS:
  - Expoente negativo retorna real
  - Base int, expoente negativo → real
  - Mais complexo para implementar
  - Requisito restringe para positivos apenas

CORREÇÃO:
  Use: (2 3 ^) → 2^3 = 8 ✓
```

---

## 8. Exercícios Integradores

### Exercício 8.1: Programa Completo com Múltiplas Estruturas

**Programa RPN:**
```
Linha 1: (10 X)
Linha 2: (X 5 >)
Linha 3: ((2 RES) ((X 2 *)) ((X 2 |)) IFELSE)
Linha 4: (3 RES Y)
```

**Ambiente Inicial:**
```
Γ₀ = {X: int, inicializada: false,
      Y: real, inicializada: false}
```

---

#### ANÁLISE LINHA POR LINHA

**LINHA 1: (10 X)**

```
Operação: MEM_STORE
```

**PASSO 1.1: Avaliar valor**
```
Γ₀ ⊢ 10 : int
```

**PASSO 1.2: Verificar armazenamento**
```
tipo_compativel_armazenamento(int)
  int ∈ {int, real}? SIM ✓

RESULTADO: TRUE
```

**PASSO 1.3: Atualizar tabela**
```
ANTES: Γ₀ = {X: int, inicializada: false, ...}

OPERAÇÃO: marcar_inicializada('X', linha=1)

DEPOIS: Γ₁ = {X: int, inicializada: true, ...}

POR QUÊ: MEM_STORE inicializa a variável
```

**PASSO 1.4: Conclusão**
```
Γ₀ ⊢ (10 X) : int

RESULTADO RUNTIME: 10 (valor armazenado)
TIPO: int
```

**TABELA DE RESULTADOS:**
```
Linha | Resultado | Tipo | Ambiente
------|-----------|------|----------
  1   |    10     | int  | Γ₁: X inicializada
```

---

**LINHA 2: (X 5 >)**

```
Ambiente: Γ₁ (X está inicializada)
```

**PASSO 2.1: Avaliar X**
```
X ∈ dom(Γ₁)? SIM
inicializada(X)? TRUE ✓
tipo(X) = int

Γ₁ ⊢ X : int
```

**PASSO 2.2: Avaliar 5**
```
Γ₁ ⊢ 5 : int
```

**PASSO 2.3: Aplicar comparação**
```
OPERADOR: >
tipos_compativeis_comparacao(int, int) ✓
tipo = boolean

Γ₁ ⊢ (X 5 >) : boolean
```

**RESULTADO RUNTIME:**
```
X = 10
10 > 5 = true
```

**TABELA ATUALIZADA:**
```
Linha | Resultado | Tipo    | Ambiente
------|-----------|---------|----------
  1   |    10     | int     | Γ₁
  2   |   true    | boolean | Γ₁
```

---

**LINHA 3: ((2 RES) ((X 2 *)) ((X 2 |)) IFELSE)**

```
Ambiente: Γ₁
```

**PASSO 3.1: Avaliar condição (2 RES)**
```
N = 2
Linha referenciada = 3 - 2 = 1

Linha 1: tipo = int

PROBLEMA: Esperamos boolean para condição!

SOLUÇÃO: Usar truthiness
  linha 1 retornou: 10
  truthy(10) = (10 != 0) = true

Γ₁ ⊢ (2 RES) : int → boolean (via truthiness)

POR QUÊ: Condições aceitam int via conversão truthy
```

**PASSO 3.2: Avaliar branch then ((X 2 *))**
```
Expressão: (X 2 *)

DERIVAÇÃO:
  Γ₁ ⊢ X : int (X está inicializada)
  Γ₁ ⊢ 2 : int
  tipos_compativeis_aritmetica(int, int) ✓
  tipo = int

Γ₁ ⊢ (X 2 *) : int
```

**PASSO 3.3: Avaliar branch else ((X 2 |))**
```
Expressão: (X 2 |)

DERIVAÇÃO:
  Γ₁ ⊢ X : int
  Γ₁ ⊢ 2 : int
  tipos_compativeis_aritmetica(int, int) ✓
  operador == '|' → tipo = real

Γ₁ ⊢ (X 2 |) : real
```

**PASSO 3.4: Verificar compatibilidade dos branches**
```
TIPO BRANCH THEN: int
TIPO BRANCH ELSE: real

branches_compativeis(int, real)
  promover_tipo(int, real) = real (não é None)

RESULTADO: TRUE ✓

POR QUÊ: int pode ser promovido para real
```

**PASSO 3.5: Determinar tipo do resultado**
```
tipo_resultado = promover_tipo(int, real) = real

POR QUÊ: Tipo comum dos branches é real
```

**PASSO 3.6: Aplicar regra IFELSE**
```
Γ₁ ⊢ ((2 RES) ((X 2 *)) ((X 2 |)) IFELSE) : real
```

**RESULTADO RUNTIME:**
```
Condição: truthy(10) = true
Branch executado: then
Cálculo: X * 2 = 10 * 2 = 20
Tipo: int → promovido para real → 20.0
```

**TABELA ATUALIZADA:**
```
Linha | Resultado | Tipo    | Ambiente
------|-----------|---------|----------
  1   |    10     | int     | Γ₁
  2   |   true    | boolean | Γ₁
  3   |   20.0    | real    | Γ₁
```

---

**LINHA 4: (3 RES Y)**

```
Operação: MEM_STORE
Ambiente: Γ₁
```

**PASSO 4.1: Avaliar valor (3 RES)**
```
N = 3
Linha referenciada = 4 - 3 = 1

Linha 1: tipo = int

Γ₁ ⊢ (3 RES) : int

POR QUÊ: Referencia linha 1 que é int
```

**PASSO 4.2: Verificar armazenamento**
```
VARIÁVEL: Y
TIPO DO VALOR: int (de 3 RES)
TIPO DA VARIÁVEL: real

VERIFICAÇÃO DE ATRIBUIÇÃO:
  Podemos armazenar int em variável real? SIM
  Conversão: int → real (promoção automática)
```

**PASSO 4.3: Atualizar tabela**
```
ANTES: Γ₁ = {..., Y: real, inicializada: false}

OPERAÇÃO:
  marcar_inicializada('Y', linha=4)
  valor = 10 (de linha 1)
  tipo armazenado = real (promovido de int)

DEPOIS: Γ₂ = {..., Y: real, inicializada: true}
```

**PASSO 4.4: Conclusão**
```
Γ₁ ⊢ (3 RES Y) : int

EFEITO COLATERAL: Y agora contém 10.0 (promovido de int)
```

**TABELA FINAL:**
```
Linha | Resultado | Tipo    | Ambiente
------|-----------|---------|----------
  1   |    10     | int     | Γ₁: X=10
  2   |   true    | boolean | Γ₁
  3   |   20.0    | real    | Γ₁
  4   |    10     | int     | Γ₂: X=10, Y=10.0
```

**ESTADO FINAL DA MEMÓRIA:**
```
Γ₂ = {
  X: {tipo: int, valor: 10, inicializada: true},
  Y: {tipo: real, valor: 10.0, inicializada: true}
}
```

---

### Exercício 8.2: Programa com WHILE e FOR

**Programa RPN:**
```
Linha 1: (0 SUM)
Linha 2: (0 I)
Linha 3: ((I 10 <) ((SUM I +) SUM) WHILE)
Linha 4: ((1 5 1 FOR) (I 2 ^) FOR)
```

**Ambiente:**
```
Γ₀ = {
  SUM: int, inicializada: false,
  I: int, inicializada: false
}
```

---

**LINHA 1: (0 SUM)**
```
Γ₀ ⊢ 0 : int
tipo_compativel_armazenamento(int) ✓

Γ₁ = Γ₀ ∪ {SUM: int, inicializada: true}

Γ₀ ⊢ (0 SUM) : int

Resultado: SUM = 0
```

---

**LINHA 2: (0 I)**
```
Γ₁ ⊢ 0 : int
tipo_compativel_armazenamento(int) ✓

Γ₂ = Γ₁ ∪ {I: int, inicializada: true}

Γ₁ ⊢ (0 I) : int

Resultado: I = 0
```

---

**LINHA 3: ((I 10 <) ((SUM I +) SUM) WHILE)**

**PASSO 3.1: Condição**
```
Γ₂ ⊢ I : int (inicializada ✓)
Γ₂ ⊢ 10 : int
tipos_compativeis_comparacao(int, int) ✓

Γ₂ ⊢ (I 10 <) : boolean
```

**PASSO 3.2: Corpo do WHILE**
```
Expressão: ((SUM I +) SUM)
```

**PASSO 3.2.1: Subexpressão (SUM I +)**
```
Γ₂ ⊢ SUM : int (inicializada ✓)
Γ₂ ⊢ I : int (inicializada ✓)
tipos_compativeis_aritmetica(int, int) ✓
tipo = int

Γ₂ ⊢ (SUM I +) : int
```

**PASSO 3.2.2: Armazenamento em SUM**
```
Valor: resultado de (SUM I +) : int
Variável: SUM : int

tipo_compativel_armazenamento(int) ✓
SUM já está inicializada, atualização permitida ✓

Γ₂ ⊢ ((SUM I +) SUM) : int
```

**PASSO 3.3: Aplicar WHILE**
```
Γ₂ ⊢ ((I 10 <) ((SUM I +) SUM) WHILE) : int

POR QUÊ: WHILE retorna tipo do corpo (int)
```

**SEMÂNTICA RUNTIME (ilustrativa):**
```
Iteração 1: I=0, SUM=0 → SUM = SUM + I = 0
Iteração 2: I=1, SUM=0 → SUM = 0 + 1 = 1
Iteração 3: I=2, SUM=1 → SUM = 1 + 2 = 3
...
(Mas CUIDADO: I nunca é incrementado! Loop infinito!)

PROBLEMA: Este código tem erro lógico (não semântico)
  - Semanticamente correto ✓
  - Logicamente: loop infinito ❌

POR QUÊ: Análise semântica não detecta loops infinitos
```

---

**LINHA 4: ((1 5 1 FOR) (I 2 ^) FOR)**

**PASSO 4.1: Parâmetros do FOR**
```
Γ₂ ⊢ 1 : int
Γ₂ ⊢ 5 : int
Γ₂ ⊢ 1 : int

parametros_for_validos(int, int, int) ✓
```

**PASSO 4.2: Corpo do FOR**
```
Ambiente estendido: Γ_for = Γ₂ ∪ {I: int, inicializada: true}

ATENÇÃO: I do FOR shadowing I externa!

Expressão: (I 2 ^)
```

**PASSO 4.2.1: Avaliar I**
```
Γ_for ⊢ I : int (I do FOR, não I externa)
```

**PASSO 4.2.2: Avaliar 2**
```
Γ_for ⊢ 2 : int
```

**PASSO 4.2.3: Verificar potência**
```
OPERADOR: ^
TIPO BASE: int
TIPO EXPOENTE: int

tipos_compativeis_potencia(int, int, valor_exp=2)
  tipo_base ∈ {int, real}? SIM
  tipo_exp == int? SIM
  valor_exp >= 0? SIM (2 >= 0)

RESULTADO: TRUE ✓

tipo_resultado = tipo_base = int

POR QUÊ: Base int, expoente int positivo → resultado int
```

**PASSO 4.3: Aplicar FOR**
```
Γ₂ ⊢ ((1 5 1 FOR) (I 2 ^) FOR) : int
```

**RESULTADO RUNTIME:**
```
Iteração 1: I=1 → 1^2 = 1
Iteração 2: I=2 → 2^2 = 4
Iteração 3: I=3 → 3^2 = 9
Iteração 4: I=4 → 4^2 = 16
Iteração 5: I=5 → 5^2 = 25

Resultado: 25 (último valor)
Tipo: int
```

---

## 📚 Resumo dos Conceitos

### 1. Derivação de Tipos
- Sempre começar pelos literais
- Aplicar regras recursivamente para subexpressões
- Verificar compatibilidade antes de aplicar operadores
- Propagar tipos para cima na árvore

### 2. Tabela de Símbolos
- Rastrear inicialização é CRÍTICO
- Ambiente evolui: Γ₀ → Γ₁ → Γ₂ ...
- MEM_STORE atualiza ambiente
- Uso de variável requer inicialização

### 3. Estruturas de Controle
- IFELSE: branches devem ser compatíveis
- WHILE: corpo determina tipo do resultado
- FOR: parâmetros DEVEM ser int

### 4. RES (Referências)
- Só referencia linhas anteriores
- Herda tipo da linha referenciada
- N <= linha_atual - 1

### 5. Erros Semânticos Comuns
- Variável não inicializada
- Tipos incompatíveis
- Boolean em MEM
- Expoente negativo
- RES para linha inválida

---

## 🎯 Estratégia Para Resolver Exercícios

### Passo 1: Identifique os Componentes
- Quais são os operandos?
- Qual é o operador?
- Há subexpressões?

### Passo 2: Derive de Dentro Para Fora
- Resolva subexpressões mais internas primeiro
- Construa árvore de derivação
- Anote tipo de cada nó

### Passo 3: Verifique Compatibilidade
- Operador aceita esses tipos?
- Precisa de promoção?
- Há restrições (como /, %, ^)?

### Passo 4: Determine Tipo do Resultado
- Aplique função de promoção
- Verifique regras especiais (| sempre real)
- Propague para cima

### Passo 5: Atualize Ambiente (se aplicável)
- MEM_STORE marca inicialização
- Rastreie evolução: Γ₀ → Γ₁ → ...

---

**FIM DOS EXERCÍCIOS AVANÇADOS**

Estes exercícios cobrem TODO o sistema semântico implementado, desde conceitos básicos até cenários complexos com múltiplas estruturas aninhadas.

**Lembre-se:** A chave é sempre explicar o POR QUÊ de cada passo!
