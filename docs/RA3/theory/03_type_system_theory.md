# Teoria Completa: Sistema de Tipos (Com Explicações Literais)

**Curso:** Linguagens Formais e Autômatos
**Fase:** RA3 - Análise Semântica
**Grupo:** RA3_1
**Objetivo:** Entender O QUE são tipos, POR QUE existem, e COMO funcionam

---

## 📚 Parte 1: O Que São Tipos?

### 1.1 Definição Intuitiva

**PERGUNTA:** O que é um "tipo"?

**RESPOSTA SIMPLES:**
Um tipo é uma **categoria** que diz:
1. Que **valores** são permitidos
2. Que **operações** podemos fazer

**ANALOGIAS:**

**Analogia 1: Tipos de Carros**
- Tipo "Carro": pode andar na rua, precisa gasolina
- Tipo "Barco": pode navegar, precisa água
- ERRO: Usar barco na rua ✗

**Analogia 2: Tipos de Dados**
- Tipo `int`: valores = {..., -1, 0, 1, 2, ...}, operações = {+, -, *, /}
- Tipo `string`: valores = {"hello", "world"}, operações = {concatenar}
- ERRO: somar int + string ✗

---

### 1.2 Os Três Tipos da Nossa Linguagem

#### Tipo 1: int (Inteiros)

**DEFINIÇÃO FORMAL:**
```
int = ℤ = {..., -2, -1, 0, 1, 2, ...}
```

**VALORES PERMITIDOS:**
- 5, -3, 0, 42, -100, ...
- NÃO permitido: 3.5, 2.7, "hello"

**OPERAÇÕES:**
- Aritméticas: `+`, `-`, `*`, `/`, `%`, `^`
- Comparação: `>`, `<`, `>=`, `<=`, `==`, `!=`

**REPRESENTAÇÃO:**
- 32 bits (em computadores modernos)
- Faixa: -2,147,483,648 a 2,147,483,647

---

#### Tipo 2: real (Reais / Ponto Flutuante)

**DEFINIÇÃO FORMAL:**
```
real ⊂ ℝ (subconjunto dos reais - precisão limitada)
```

**VALORES PERMITIDOS:**
- 3.14, -2.5, 0.0, 1.414, ...
- TAMBÉM: 5.0 (mesmo sendo "inteiro", o `.0` faz ser real)

**OPERAÇÕES:**
- Mesmas de int: `+`, `-`, `*`, `|` (divisão real), `^`
- Comparação: `>`, `<`, `>=`, `<=`, `==`, `!=`

**REPRESENTAÇÃO:**
- IEEE 754 (padrão internacional)
- No Arduino: 16 bits (float reduzido)
- Precisão: ~3 casas decimais

**IMPORTANTE:**
```
3.0 ≠ 3 (em termos de TIPO!)

3.0 é real
3 é int

Valores iguais, TIPOS diferentes!
```

---

#### Tipo 3: boolean (Booleanos)

**DEFINIÇÃO FORMAL:**
```
boolean = {true, false}
```

**VALORES PERMITIDOS:**
- Somente: `true` ou `false`
- Nada mais!

**OPERAÇÕES:**
- Lógicas: `&&` (AND), `||` (OR), `!` (NOT)

**COMO SURGE:**
- Resultado de comparações: `(5 3 >)` → `true`
- Operações lógicas: `(true false &&)` → `false`

**RESTRIÇÃO IMPORTANTE:**
```
Boolean NÃO pode ser armazenado em MEM!

(5 3 >) → tipo boolean
((5 3 >) X MEM) → ERRO! ✗
```

**POR QUÊ:**
Nossa linguagem só permite armazenar números (int, real).

---

### 1.3 Hierarquia de Tipos

**CONCEITO:**
Alguns tipos são "maiores" (mais gerais) que outros.

**HIERARQUIA:**
```
       real (maior)
         ↑
        int (menor)
```

**O QUE SIGNIFICA:**
- **int < real:** Todo int pode ser visto como real
  - 5 (int) → 5.0 (real) ✓
- **real > int:** Nem todo real pode ser int
  - 3.5 (real) → ? (int) ✗ (perderia o .5)

**NOTAÇÃO:**
```
int ⊆ real  (int é subconjunto de real)
```

**CONSEQUÊNCIA:**
Quando misturamos int com real, convertemos int para real (promoção).

---

## 🔄 Parte 2: Promoção de Tipos (Type Promotion)

### 2.1 O Que É Promoção?

**DEFINIÇÃO:**
Promoção é converter temporariamente um tipo "menor" para tipo "maior" para realizar uma operação.

**FUNÇÃO FORMAL:**
```
promover_tipo : Tipo × Tipo → Tipo

promover_tipo(T₁, T₂) = {
    real,  se T₁ = real ∨ T₂ = real
    int,   caso contrário
}
```

**EM PORTUGUÊS:**
"Se QUALQUER dos tipos é real, resultado é real. Senão, resultado é int."

---

### 2.2 Por Que Precisamos de Promoção?

**PROBLEMA SEM PROMOÇÃO:**
```
5 (int) + 3.5 (real) = ?

Não podemos somar tipos diferentes diretamente!
```

**SOLUÇÃO COM PROMOÇÃO:**
```
PASSO 1: Promover 5 (int) para 5.0 (real)
PASSO 2: Agora: 5.0 (real) + 3.5 (real)
PASSO 3: Resultado: 8.5 (real)
```

**POR QUÊ REAL "VENCE":**
- Real pode representar QUALQUER int
  - 5 → 5.0 ✓ (sem perda)
- Int NÃO pode representar qualquer real
  - 3.5 → 3 ✗ (perde o .5)

**ANALOGIA:**
```
int = copo pequeno (250ml)
real = copo grande (500ml)

Misturar = precisamos de copo que caiba tudo
Logo, usamos copo grande (real)
```

---

### 2.3 Exemplos Detalhados de Promoção

**Exemplo 1: int + int (SEM promoção)**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 3 +)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos dos operandos
  - 5: int
  - 3: int

PASSO 2: Verificar se precisamos promover
  promover_tipo(int, int) = ?

  T₁ = int, é real? NÃO
  T₂ = int, é real? NÃO

  Nenhum é real → resultado = int

PASSO 3: Cálculo
  5 (int) + 3 (int) = 8 (int)

  SEM CONVERSÃO! Ambos já são int.

RESULTADO: 8 (tipo: int)
══════════════════════════════════════════════════════════════
```

**Exemplo 2: int + real (COM promoção)**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 3.5 +)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos dos operandos
  - 5: int
  - 3.5: real

PASSO 2: Aplicar promover_tipo
  promover_tipo(int, real) = ?

  T₁ = int, é real? NÃO
  T₂ = real, é real? SIM ✓

  Um dos tipos é real → resultado = real

PASSO 3: Conversão (o que acontece internamente)
  ────────────────────────────────────────────────
  ANTES DA OPERAÇÃO:
    Operando 1: 5 (int)
    Operando 2: 3.5 (real)

  CONVERSÃO AUTOMÁTICA:
    5 (int) → 5.0 (real)

    POR QUÊ: Para somar, precisamos mesmo tipo
    COMO: Adiciona ".0" → 5 vira 5.0

  DEPOIS DA CONVERSÃO:
    Operando 1: 5.0 (real)
    Operando 2: 3.5 (real)

PASSO 4: Operação
  5.0 (real) + 3.5 (real) = 8.5 (real)

RESULTADO: 8.5 (tipo: real)

POR QUE NÃO CONVERTEMOS 3.5 PARA INT:
  - 3.5 → 3 perderia informação (.5 sumiu)
  - 5 → 5.0 NÃO perde informação
  - Logo, promovemos int → real
══════════════════════════════════════════════════════════════
```

**Exemplo 3: real + int (ordem invertida)**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (3.5 5 +)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos
  - 3.5: real
  - 5: int

PASSO 2: Aplicar promover_tipo
  promover_tipo(real, int) = ?

  T₁ = real, é real? SIM ✓

  Um é real → resultado = real

PASSO 3: Conversão
  Operando 1: 3.5 (real) → sem mudança
  Operando 2: 5 (int) → 5.0 (real)

PASSO 4: Operação
  3.5 (real) + 5.0 (real) = 8.5 (real)

RESULTADO: 8.5 (tipo: real)

OBSERVAÇÃO: Ordem NÃO importa!
  (5 3.5 +) = (3.5 5 +) = real
══════════════════════════════════════════════════════════════
```

**Exemplo 4: real + real (já são iguais)**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (3.5 2.1 +)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos
  - 3.5: real
  - 2.1: real

PASSO 2: Aplicar promover_tipo
  promover_tipo(real, real) = ?

  T₁ = real, é real? SIM
  T₂ = real, é real? SIM

  Pelo menos um é real → resultado = real

PASSO 3: Conversão
  SEM CONVERSÃO! Ambos já são real.

PASSO 4: Operação
  3.5 (real) + 2.1 (real) = 5.6 (real)

RESULTADO: 5.6 (tipo: real)
══════════════════════════════════════════════════════════════
```

---

### 2.4 Tabela de Promoção

**REFERÊNCIA RÁPIDA:**

| T₁ (esquerda) | T₂ (direita) | promover_tipo(T₁, T₂) | Por quê? |
|---------------|--------------|----------------------|----------|
| int | int | **int** | Ambos int → sem mudança |
| int | real | **real** | real "vence" → promove int |
| real | int | **real** | real "vence" → promove int |
| real | real | **real** | Ambos real → sem mudança |

**REGRA SIMPLES:**
Se há **QUALQUER** real → resultado é **real**

---

## ⚖️ Parte 3: Compatibilidade de Tipos

### 3.1 O Que É Compatibilidade?

**DEFINIÇÃO:**
Compatibilidade determina se podemos usar certos tipos com certos operadores.

**TRÊS NÍVEIS:**

1. **Compatível e Igual:** Tipos iguais, sem conversão
   - `int + int` → OK, resultado int

2. **Compatível com Promoção:** Tipos diferentes, com conversão
   - `int + real` → OK após promover int, resultado real

3. **Incompatível:** Não permitido de jeito nenhum
   - `int / real` → ERRO! Divisão inteira requer ambos int

---

### 3.2 Operadores Permissivos (Aceitam Promoção)

**OPERADORES:** `+`, `-`, `*`, `|` (divisão real)

**REGRA:**
```
tipos_compativeis_aritmetica(T₁, T₂) = T₁ ∈ {int, real} ∧ T₂ ∈ {int, real}
```

**TRADUÇÃO:**
"Ambos devem ser numéricos (int ou real), mas NÃO precisam ser iguais"

**EXEMPLO DETALHADO:**

```
══════════════════════════════════════════════════════════════
VERIFICAR: (5 3.5 +) é válido?
══════════════════════════════════════════════════════════════

PASSO 1: Operador é +
  + está em {+, -, *, |}? SIM
  Logo: usa regra PERMISSIVA

PASSO 2: Verificar compatibilidade
  tipos_compativeis_aritmetica(int, real) = ?

  int ∈ {int, real}? SIM ✓
  real ∈ {int, real}? SIM ✓

  Ambas condições OK → COMPATÍVEL

PASSO 3: Tipo resultado
  promover_tipo(int, real) = real

CONCLUSÃO: (5 3.5 +) é VÁLIDO, tipo real
══════════════════════════════════════════════════════════════
```

---

### 3.3 Operadores Restritos (SÓ aceitam int)

**OPERADORES:** `/` (div inteira), `%` (módulo)

**REGRA:**
```
tipos_compativeis_divisao_inteira(T₁, T₂) = T₁ = int ∧ T₂ = int
```

**TRADUÇÃO:**
"AMBOS devem ser EXATAMENTE int (sem exceção!)"

**POR QUE TÃO RESTRITO:**
- `/` é divisão INTEIRA (trunca resultado)
- `%` é resto da divisão (só faz sentido com inteiros)

**EXEMPLO: VÁLIDO**

```
══════════════════════════════════════════════════════════════
VERIFICAR: (10 3 /) é válido?
══════════════════════════════════════════════════════════════

PASSO 1: Operador é /
  / é divisão inteira
  Regra: AMBOS devem ser int

PASSO 2: Verificar tipos
  tipos_compativeis_divisao_inteira(int, int) = ?

  10 é int? SIM ✓
  3 é int? SIM ✓
  int = int? SIM ✓

PASSO 3: Cálculo
  10 / 3 = 3 (trunca, não arredonda)
  Tipo: int

CONCLUSÃO: VÁLIDO, resultado 3 (int)
══════════════════════════════════════════════════════════════
```

**EXEMPLO: INVÁLIDO**

```
══════════════════════════════════════════════════════════════
VERIFICAR: (10 3.0 /) é válido?
══════════════════════════════════════════════════════════════

PASSO 1: Operador é /
  Regra: AMBOS devem ser int

PASSO 2: Verificar tipos
  tipos_compativeis_divisao_inteira(int, real) = ?

  10 é int? SIM ✓
  3.0 é real? SIM (tem .0)
  int = int? NÃO! (segundo é real) ✗

  FALHA! Segundo operando não é int

PASSO 3: Por que não promover?
  ────────────────────────────────────────
  SE promovêssemos 10 para 10.0:
    10.0 / 3.0 = 3.333... (real)

  MAS: / deve retornar INT!

  CONFLITO: Operação real, resultado int?

  DECISÃO: Proibir!

CONCLUSÃO: INVÁLIDO! Erro semântico
MENSAGEM: "Divisão inteira requer ambos int"
SOLUÇÃO: Use | em vez de /
══════════════════════════════════════════════════════════════
```

---

### 3.4 Caso Especial: Potência (^)

**REGRA ÚNICA:**
```
tipos_compativeis_potencia(T_base, T_expoente) =
    T_base ∈ {int, real} ∧ T_expoente = int
```

**TRADUÇÃO:**
"Base pode ser int OU real, mas expoente DEVE ser int"

**POR QUÊ:**
- Base: faz sentido elevar inteiro ou real
  - 2^3 = 8 ✓
  - 2.5^2 = 6.25 ✓
- Expoente: deve ser inteiro para ter significado claro
  - 2^3 significa "2 × 2 × 2" (3 vezes)
  - 2^3.5 significa... ? (ambíguo!)

**TIPO RESULTADO:**
```
tipo_resultado_potencia(T_base) = T_base
```
"Resultado tem o MESMO tipo da base"

**EXEMPLOS:**

```
══════════════════════════════════════════════════════════════
CASO 1: Base int, expoente int
══════════════════════════════════════════════════════════════
(2 3 ^)

Base: 2 (int)
Expoente: 3 (int)

Verificar: tipos_compativeis_potencia(int, int) = ?
  Base int? SIM ✓
  Expoente int? SIM ✓

Cálculo: 2³ = 8
Tipo: int (mesmo da base)

VÁLIDO: 8 (int)


══════════════════════════════════════════════════════════════
CASO 2: Base real, expoente int
══════════════════════════════════════════════════════════════
(2.5 2 ^)

Base: 2.5 (real)
Expoente: 2 (int)

Verificar: tipos_compativeis_potencia(real, int) = ?
  Base real? SIM ✓
  Expoente int? SIM ✓

Cálculo: 2.5² = 6.25
Tipo: real (mesmo da base)

VÁLIDO: 6.25 (real)


══════════════════════════════════════════════════════════════
CASO 3: Base int, expoente real → ERRO
══════════════════════════════════════════════════════════════
(2 3.5 ^)

Base: 2 (int)
Expoente: 3.5 (real)

Verificar: tipos_compativeis_potencia(int, real) = ?
  Base int? SIM ✓
  Expoente int? NÃO! (é real) ✗

POR QUE ERRO:
  - 2^3.5 = 2^(7/2) = √(2^7) = √128 ≈ 11.31
  - Definição matemática complexa
  - Resultado sempre real (mesmo base int)
  - Nossa linguagem NÃO suporta

INVÁLIDO! Erro semântico


══════════════════════════════════════════════════════════════
CASO 4: Expoente negativo → ERRO (mesmo sendo int!)
══════════════════════════════════════════════════════════════
(2 -3 ^)

Base: 2 (int)
Expoente: -3 (int)

Verificar tipo: tipos_compativeis_potencia(int, int) = ?
  Base int? SIM ✓
  Expoente int? SIM ✓

  TIPO OK!

Verificar VALOR: expoente > 0?
  -3 > 0? NÃO ✗

POR QUE ERRO:
  - 2^(-3) = 1/(2^3) = 1/8 = 0.125
  - Resultado é REAL (não int)
  - Mas base é int, deveria retornar int
  - INCONSISTÊNCIA!

INVÁLIDO! Erro semântico

OBSERVAÇÃO: Isso é verificação de VALOR, não tipo!
══════════════════════════════════════════════════════════════
```

---

## 🔀 Parte 4: Truthiness (Modo Permissivo)

### 4.1 O Que É Truthiness?

**DEFINIÇÃO:**
Truthiness é a capacidade de interpretar valores não-booleanos como booleanos.

**FUNÇÃO:**
```
truthy : Valor × Tipo → boolean

truthy(v, T) = {
    v,           se T = boolean
    v ≠ 0,       se T = int
    v ≠ 0.0,     se T = real
}
```

**EXEMPLOS:**
```
truthy(true, boolean) = true
truthy(false, boolean) = false
truthy(5, int) = true (5 ≠ 0)
truthy(0, int) = false (0 = 0)
truthy(3.14, real) = true (3.14 ≠ 0.0)
truthy(0.0, real) = false (0.0 = 0.0)
```

---

### 4.2 Por Que Truthiness?

**PROBLEMA:**
```
(5 3 &&)  ← int && int, mas && espera boolean!
```

**SOLUÇÃO 1: Modo Estrito (proibir)**
```
Erro: && requer boolean, encontrado int
```

**SOLUÇÃO 2: Modo Permissivo (truthy)**
```
Converter: truthy(5) = true, truthy(3) = true
Resultado: true && true = true
```

**NOSSA ESCOLHA:** Modo Permissivo
- Mais flexível
- Comum em linguagens (Python, JavaScript)
- Sem perda de segurança de tipos

---

### 4.3 Exemplos Detalhados

**Exemplo 1: int && int**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 0 &&)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos
  - 5: int
  - 0: int

PASSO 2: Operador && (AND lógico)
  Regra estrita: AMBOS devem ser boolean
  Temos: int e int

  Modo estrito: ERRO ✗
  Modo permissivo: Tentar truthy ✓

PASSO 3: Aplicar truthiness
  truthy(5, int) = ?
    5 ≠ 0? SIM
    Resultado: true

  truthy(0, int) = ?
    0 ≠ 0? NÃO
    Resultado: false

PASSO 4: Operação lógica
  true && false = false

RESULTADO: false (tipo: boolean)

INTERPRETAÇÃO:
  "5 é verdadeiro" AND "0 é falso" = falso
══════════════════════════════════════════════════════════════
```

**Exemplo 2: real || real**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (3.14 0.0 ||)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos
  - 3.14: real
  - 0.0: real

PASSO 2: Aplicar truthiness
  truthy(3.14, real) = ?
    3.14 ≠ 0.0? SIM
    Resultado: true

  truthy(0.0, real) = ?
    0.0 ≠ 0.0? NÃO
    Resultado: false

PASSO 3: Operação lógica (OR)
  true || false = true

RESULTADO: true (tipo: boolean)
══════════════════════════════════════════════════════════════
```

**Exemplo 3: Misturando tipos**

```
══════════════════════════════════════════════════════════════
EXPRESSÃO: (5 3.14 &&)
══════════════════════════════════════════════════════════════

PASSO 1: Tipos
  - 5: int
  - 3.14: real

PASSO 2: Aplicar truthiness
  truthy(5, int) = true (5 ≠ 0)
  truthy(3.14, real) = true (3.14 ≠ 0.0)

PASSO 3: Operação
  true && true = true

RESULTADO: true (tipo: boolean)

OBSERVAÇÃO: Podemos misturar int e real em lógica!
══════════════════════════════════════════════════════════════
```

---

## 📝 Parte 5: Exercícios com Soluções Completas

### Exercício 5.1: Promoção Básica

**Questão:** Para cada expressão, determine o tipo resultado e justifique.

a) `(7 2 +)`
b) `(7.0 2.0 +)`
c) `(7 2.0 +)`
d) `(7.0 2 +)`

**Soluções:**

```
══════════════════════════════════════════════════════════════
a) (7 2 +)
══════════════════════════════════════════════════════════════

Tipos: int + int
Promover_tipo(int, int) = int
  POR QUÊ: Nenhum é real

RESULTADO: 9 (int)
JUSTIFICATIVA: Ambos int, sem promoção necessária


══════════════════════════════════════════════════════════════
b) (7.0 2.0 +)
══════════════════════════════════════════════════════════════

Tipos: real + real
Promover_tipo(real, real) = real
  POR QUÊ: Pelo menos um é real (ambos são)

RESULTADO: 9.0 (real)
JUSTIFICATIVA: Ambos real, resultado real


══════════════════════════════════════════════════════════════
c) (7 2.0 +)
══════════════════════════════════════════════════════════════

Tipos: int + real
Promover_tipo(int, real) = real
  POR QUÊ: Segundo operando é real

Conversão: 7 (int) → 7.0 (real)
Operação: 7.0 + 2.0 = 9.0

RESULTADO: 9.0 (real)
JUSTIFICATIVA: Promoção de int para real


══════════════════════════════════════════════════════════════
d) (7.0 2 +)
══════════════════════════════════════════════════════════════

Tipos: real + int
Promover_tipo(real, int) = real
  POR QUÊ: Primeiro operando é real

Conversão: 2 (int) → 2.0 (real)
Operação: 7.0 + 2.0 = 9.0

RESULTADO: 9.0 (real)
JUSTIFICATIVA: Promoção de int para real

OBSERVAÇÃO: c) e d) têm o MESMO resultado
            (ordem não importa para promoção)
══════════════════════════════════════════════════════════════
```

---

### Exercício 5.2: Compatibilidade

**Questão:** Para cada expressão, diga se é VÁLIDA ou ERRO. Se erro, por quê?

a) `(10 2 /)`
b) `(10.0 2 /)`
c) `(10 2.0 |)`
d) `(2 3.5 ^)`

**Soluções:**

```
══════════════════════════════════════════════════════════════
a) (10 2 /)
══════════════════════════════════════════════════════════════

Operador: / (divisão inteira)
Tipos: int / int

Verificar: tipos_compativeis_divisao_inteira(int, int)
  10 é int? SIM ✓
  2 é int? SIM ✓

VÁLIDO ✓
Resultado: 5 (int)
Cálculo: 10 / 2 = 5


══════════════════════════════════════════════════════════════
b) (10.0 2 /)
══════════════════════════════════════════════════════════════

Operador: / (divisão inteira)
Tipos: real / int

Verificar: tipos_compativeis_divisao_inteira(real, int)
  10.0 é int? NÃO! (é real) ✗

INVÁLIDO ✗

POR QUÊ:
  - / requer AMBOS int
  - 10.0 é real (tem .0)
  - Mesmo sendo "10", o .0 faz ser real

ERRO: "Divisão inteira requer ambos int, encontrado real e int"
SOLUÇÃO: Use | (divisão real) ou remova .0


══════════════════════════════════════════════════════════════
c) (10 2.0 |)
══════════════════════════════════════════════════════════════

Operador: | (divisão real)
Tipos: int | real

Verificar: tipos_compativeis_aritmetica(int, real)
  10 é numérico? SIM ✓
  2.0 é numérico? SIM ✓

VÁLIDO ✓
Tipo resultado: real (SEMPRE real para |)
Cálculo: 10.0 / 2.0 = 5.0

OBSERVAÇÃO: Resultado é 5.0 (real), não 5 (int)


══════════════════════════════════════════════════════════════
d) (2 3.5 ^)
══════════════════════════════════════════════════════════════

Operador: ^ (potência)
Tipos: int ^ real

Base: 2 (int)
Expoente: 3.5 (real)

Verificar: tipos_compativeis_potencia(int, real)
  Base numérica? SIM ✓
  Expoente int? NÃO! (é real) ✗

INVÁLIDO ✗

POR QUÊ:
  - Expoente DEVE ser int
  - 3.5 é real
  - Definição de 2^3.5 é complexa (raízes)
  - Nossa linguagem não suporta

ERRO: "Expoente de potência deve ser int, encontrado real"
SOLUÇÃO: Use expoente inteiro: (2 3 ^)
══════════════════════════════════════════════════════════════
```

---

### Exercício 5.3: Truthiness

**Questão:** Qual o resultado de cada expressão em modo permissivo?

a) `(5 3 &&)`
b) `(0 10 ||)`
c) `(0.0 0 &&)`

**Soluções:**

```
══════════════════════════════════════════════════════════════
a) (5 3 &&)
══════════════════════════════════════════════════════════════

Tipos: int && int

PASSO 1: Converter para boolean
  truthy(5, int) = (5 ≠ 0) = true
  truthy(3, int) = (3 ≠ 0) = true

PASSO 2: Operação lógica
  true && true = true

RESULTADO: true (boolean)

INTERPRETAÇÃO:
  "5 é verdadeiro" E "3 é verdadeiro" = verdadeiro


══════════════════════════════════════════════════════════════
b) (0 10 ||)
══════════════════════════════════════════════════════════════

Tipos: int || int

PASSO 1: Converter
  truthy(0, int) = (0 ≠ 0) = false
  truthy(10, int) = (10 ≠ 0) = true

PASSO 2: Operação
  false || true = true

RESULTADO: true (boolean)

INTERPRETAÇÃO:
  "0 é falso" OU "10 é verdadeiro" = verdadeiro
  (basta um ser verdadeiro em OR)


══════════════════════════════════════════════════════════════
c) (0.0 0 &&)
══════════════════════════════════════════════════════════════

Tipos: real && int

PASSO 1: Converter
  truthy(0.0, real) = (0.0 ≠ 0.0) = false
  truthy(0, int) = (0 ≠ 0) = false

PASSO 2: Operação
  false && false = false

RESULTADO: false (boolean)

INTERPRETAÇÃO:
  "0.0 é falso" E "0 é falso" = falso
  (ambos precisam ser verdadeiros em AND)
══════════════════════════════════════════════════════════════
```

---

## 🎯 Resumo Final

### Promoção de Tipos:
- **int + int → int** (sem promoção)
- **int + real → real** (promove int)
- **real + int → real** (promove int)
- **real + real → real** (sem promoção)

### Compatibilidade:
- **Permissiva:** `+`, `-`, `*`, `|` (aceita int+real)
- **Restrita:** `/`, `%` (SÓ int+int)
- **Especial:** `^` (base qualquer, expoente int)

### Truthiness:
- **0, 0.0** → false
- **≠ 0** → true
- Permite lógica com números

---

**Próximo:** `04_advanced_exercises.md` - Exercícios complexos

**Desenvolvido por:** Grupo RA3_1 - PUCPR
**Data:** 2025-01-19
