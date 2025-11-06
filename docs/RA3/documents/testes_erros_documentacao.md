# Documentação: Arquivos de Teste com Erros

## Visão Geral

Este documento descreve os três arquivos de teste que contêm casos de erro para validação do compilador nas fases RA1 (Análise Léxica), RA2 (Análise Sintática) e RA3 (Análise Semântica).

---

# TESTE4 - Erros de Tipos (RA3)

## Arquivo
`teste4_erros_tipos.txt`

## Objetivo
Validar a detecção de **erros semânticos de violação de tipos** na fase RA3.

---

## Seção 1: Erros de Divisão Inteira com Tipos Incompatíveis

### Linha 1: `(5.5 2 /)`
- **Erro Esperado:** Divisão inteira requer ambos operandos do tipo `int`
- **Descrição:** O operador `/` (divisão inteira) só aceita `int`. O operando `5.5` é `real`.
- **Regra Semântica:** `/ : int × int → int`

### Linha 2: `(3.5 2 /)`
- **Erro Esperado:** Divisão inteira com operando real
- **Descrição:** Primeiro operando é `real` quando deveria ser `int`.

### Linha 3: `(10.5 3 /)`
- **Erro Esperado:** Divisão inteira com operando real
- **Descrição:** Primeiro operando é `real`.

---

## Seção 2: Erros de Resto com Tipos Incompatíveis

### Linha 4: `(10.5 3 %)`
- **Erro Esperado:** Resto requer ambos operandos do tipo `int`
- **Descrição:** O operador `%` (módulo) só aceita `int`. O operando `10.5` é `real`.
- **Regra Semântica:** `% : int × int → int`

### Linha 5: `(100 50.5 %)`
- **Erro Esperado:** Resto com segundo operando real
- **Descrição:** Segundo operando é `real` quando deveria ser `int`.

### Linha 6: `(15.8 4.2 %)`
- **Erro Esperado:** Resto com ambos operandos reais
- **Descrição:** Ambos operandos são `real`.

---

## Seção 3: Erros de Potenciação com Expoente Incompatível

### Linha 7: `(2 3.5 ^)`
- **Erro Esperado:** Expoente deve ser do tipo `int`
- **Descrição:** O operador `^` requer expoente inteiro. O valor `3.5` é `real`.
- **Regra Semântica:** `^ : (int|real) × int → (int|real)`

### Linha 8: `(2 -3 ^)`
- **Erro Esperado:** Expoente deve ser não-negativo
- **Descrição:** O expoente `-3` é negativo. Requer `exp ≥ 0`.

### Linha 9: `(3 -2.5 ^)`
- **Erro Esperado:** Expoente inválido (real e negativo)
- **Descrição:** Viola duas restrições: não é inteiro E é negativo.

---

## Seção 4: Erros de Operações Aritméticas com Booleanos

### Linha 10: `((5 3 >) 2 +)`
- **Erro Esperado:** Operação aritmética não aceita tipo `boolean`
- **Descrição:** A comparação `(5 3 >)` retorna `boolean`, mas `+` requer numéricos.
- **Regra Semântica:** `+ : (int|real) × (int|real) → (int|real)`
- **Tipo inválido:** `boolean + int`

### Linha 11: `((2 3 <) 5 -)`
- **Erro Esperado:** Operação aritmética não aceita `boolean`
- **Descrição:** Comparação retorna `boolean`, não pode subtrair de inteiro.
- **Tipo inválido:** `boolean - int`

### Linha 12: `((5 3 >) ! 10 +)`
- **Erro Esperado:** Operação aritmética com resultado booleano
- **Descrição:** `!` negação de `boolean` resulta em `boolean`, não pode somar com `10`.
- **Tipo inválido:** `boolean + int`

---

## Seção 5: Erros de Operações Lógicas com Tipos Numéricos

### Linha 13: `(5 3 &&)`
- **Erro Esperado:** Operador lógico requer operandos `boolean`
- **Descrição:** O operador `&&` (AND) só aceita `boolean`. Os valores são `int`.
- **Regra Semântica:** `&& : boolean × boolean → boolean`

### Linha 14: `((5.5 2.0 >) (10 5 *) ||)`
- **Erro Esperado:** OR lógico com segundo operando não-booleano
- **Descrição:** Primeiro operando é `boolean`, mas segundo é `int`.
- **Tipo inválido:** `boolean || int`

---

## Seção 6: Erros em Estruturas de Controle

### Linha 15: `((10) (5 3 +) (2 1 -) IFELSE)`
- **Erro Esperado:** Condição de IFELSE deve ser `boolean`
- **Descrição:** O IFELSE requer condição booleana. O valor `10` é `int`.
- **Regra Semântica:** `IFELSE : boolean × T × T → T`

### Linha 16: `((10 X) ((5 3 >) 2 *) Y)`
- **Erro Esperado:** Multiplicação de `boolean` com `int`
- **Descrição:** Atribuição aninhada tenta multiplicar resultado de comparação.
- **Tipo inválido:** `boolean * int`

---

# TESTE5 - Erros de Memória e Inicialização (RA3)

## Arquivo
`teste5_erros_memoria.txt`

## Objetivo
Validar a detecção de **erros de memória, variáveis não inicializadas e uso incorreto de RES**.

---

## Seção 1: Variáveis Não Inicializadas

### Linha 1: `(Y)`
- **Erro Esperado:** Variável `Y` utilizada sem inicialização
- **Descrição:** Tentativa de acessar variável que nunca foi declarada.

### Linha 2: `(Z 2 +)`
- **Erro Esperado:** Variável `Z` não inicializada
- **Descrição:** Uso de `Z` em operação aritmética sem declaração prévia.

### Linha 3: `(W 5 *)`
- **Erro Esperado:** Variável `W` não inicializada
- **Descrição:** Multiplicação com variável não declarada.

### Linha 4: `((A B +) C)`
- **Erro Esperado:** Variáveis `A` e `B` não inicializadas
- **Descrição:** Soma de duas variáveis não declaradas e atribuição ao resultado.

---

## Seção 2: Uso de Variáveis Após Declaração

### Linha 5: `(10 X)`
- **Operação Válida:** Declaração de `X` com valor `10`
- **Nota:** Esta linha é válida, mas as próximas dependem dela.

### Linha 6: `((X Y >) TEST)`
- **Erro Esperado:** Variável `Y` não inicializada
- **Descrição:** Comparação usa `X` (válida) mas `Y` não foi declarada.

### Linha 7: `(BOOL)`
- **Erro Esperado:** Variável `BOOL` não inicializada
- **Descrição:** Acesso a variável nunca declarada.

---

## Seção 3: Uso Incorreto de RES

### Linha 8: `(-1 RES)`
- **Erro Esperado:** RES com valor negativo (possivelmente inválido)
- **Descrição:** Uso de RES com número negativo.

### Linha 9: `(100 RES)`
- **Possível Erro:** Uso de RES fora de contexto válido
- **Descrição:** Dependendo da implementação, pode gerar erro.

### Linha 10: `(0 RES)`
- **Possível Erro:** Uso de RES
- **Descrição:** RES com zero.

### Linha 11: `(-5 RES)`
- **Erro Esperado:** RES com valor negativo
- **Descrição:** Número negativo com RES.

### Linha 12: `((50 RES) D)`
- **Erro Esperado:** Uso incorreto de RES em expressão
- **Descrição:** RES dentro de expressão sendo atribuído a variável.

---

## Seção 4: Armazenamento de Booleanos

### Linha 13: `((5 3 >) BOOL)`
- **Erro Esperado:** Tipo `boolean` não pode ser armazenado em variável
- **Descrição:** Tentativa de atribuir resultado de comparação a variável.
- **Regra Semântica:** Variáveis só aceitam tipos `int` e `real`.

---

## Seção 5: Estruturas de Controle com Erros

### Linha 14: `((10) (5 3 +) WHILE)`
- **Erro Esperado:** Condição de WHILE deve ser `boolean`
- **Descrição:** WHILE requer condição booleana, mas recebe `int`.
- **Regra Semântica:** `WHILE : boolean × body → void`

### Linha 15: `((3.5) (10) (20) IFELSE)`
- **Erro Esperado:** Condição de IFELSE deve ser `boolean`
- **Descrição:** IFELSE recebe `real` como condição.
- **Regra Semântica:** `IFELSE : boolean × T × T → T`

---

# TESTE6 - Erros Abrangentes do Compilador (RA1, RA2, RA3)

## Arquivo
`teste6_erros_compilador.txt`

## Objetivo
Validar a detecção de erros em **todas as fases do compilador** de forma balanceada: 10 casos para RA1, 10 para RA2 e 10 para RA3.

---

## PARTE 1: Erros Léxicos (RA1) - 10 Casos

### Caso 1: `(5 @ 3)`
- **Erro Esperado:** Caractere inválido `@`
- **Fase:** RA1 - Análise Léxica
- **Descrição:** O caractere `@` não pertence ao alfabeto da linguagem.

### Caso 2: `(10 # 5)`
- **Erro Esperado:** Caractere inválido `#`
- **Fase:** RA1
- **Descrição:** Símbolo `#` não reconhecido pelo analisador léxico.

### Caso 3: `(7 $ 2)`
- **Erro Esperado:** Caractere inválido `$`
- **Fase:** RA1
- **Descrição:** Caractere especial `$` não é válido.

### Caso 4: `(3.14.15 X)`
- **Erro Esperado:** Número malformado com múltiplos pontos
- **Fase:** RA1
- **Descrição:** Token numérico com dois pontos decimais.

### Caso 5: `(..5 Y)`
- **Erro Esperado:** Número começando com ponto duplo
- **Fase:** RA1
- **Descrição:** Formato numérico inválido `..5`.

### Caso 6: `(10. A)`
- **Erro Esperado:** Número terminando com ponto
- **Fase:** RA1
- **Descrição:** Número sem dígitos após o ponto decimal.

### Caso 7: `(20 & 15)`
- **Erro Esperado:** Caractere inválido `&` (único)
- **Fase:** RA1
- **Descrição:** Operador `&&` existe, mas `&` sozinho não é válido.

### Caso 8: `(8 %% 3)`
- **Erro Esperado:** Operador duplicado incorreto `%%`
- **Fase:** RA1
- **Descrição:** Operador `%` duplicado não é reconhecido.

### Caso 9: `(5 . 5 X)`
- **Erro Esperado:** Número malformado com espaços
- **Fase:** RA1
- **Descrição:** Espaços dentro de número `5 . 5` não são permitidos.

### Caso 10: `(@ # $ %)`
- **Erro Esperado:** Múltiplos caracteres inválidos
- **Fase:** RA1
- **Descrição:** Sequência de caracteres não reconhecidos.

---

## PARTE 2: Erros Sintáticos (RA2) - 10 Casos

### Caso 11: `5 3 +)`
- **Erro Esperado:** Parêntese de abertura faltando
- **Fase:** RA2 - Análise Sintática
- **Descrição:** Expressão sem `(` inicial.

### Caso 12: `((5 3 +)`
- **Erro Esperado:** Parêntese de fechamento faltando
- **Fase:** RA2
- **Descrição:** Parênteses desbalanceados.

### Caso 13: `(+)`
- **Erro Esperado:** Operador sem operandos suficientes
- **Fase:** RA2
- **Descrição:** Operador `+` sem operandos.

### Caso 14: `(*)`
- **Erro Esperado:** Operador multiplicação sem operandos
- **Fase:** RA2
- **Descrição:** Multiplicação sem valores.

### Caso 15: `(5 + 3)`
- **Erro Esperado:** Notação infixa incorreta
- **Fase:** RA2
- **Descrição:** Linguagem usa RPN (notação posfixa), não infixa.

### Caso 16: `(10 - 5)`
- **Erro Esperado:** Notação infixa com subtração
- **Fase:** RA2
- **Descrição:** Operador entre operandos não é válido em RPN.

### Caso 17: `5 3 +`
- **Erro Esperado:** Falta de parênteses obrigatórios
- **Fase:** RA2
- **Descrição:** Expressão sem delimitadores.

### Caso 18: `(+ 5 3)`
- **Erro Esperado:** Operador no início (ordem incorreta)
- **Fase:** RA2
- **Descrição:** RPN requer operandos antes do operador.

### Caso 19: `(5 3 + -)`
- **Erro Esperado:** Múltiplos operadores seguidos
- **Fase:** RA2
- **Descrição:** Dois operadores sem operandos suficientes.

### Caso 20: `()`
- **Erro Esperado:** Estrutura vazia
- **Fase:** RA2
- **Descrição:** Parênteses sem conteúdo.

---

## PARTE 3: Erros Semânticos (RA3) - 10 Casos

### Caso 21: `(5.5 2 /)`
- **Erro Esperado:** Divisão inteira com operando real
- **Fase:** RA3 - Análise Semântica
- **Descrição:** Operador `/` requer ambos operandos `int`.
- **Regra Semântica:** `/ : int × int → int`

### Caso 22: `(10.5 3 %)`
- **Erro Esperado:** Resto com operando real
- **Fase:** RA3
- **Descrição:** Operador `%` só aceita `int`.
- **Regra Semântica:** `% : int × int → int`

### Caso 23: `(2 3.5 ^)`
- **Erro Esperado:** Potenciação com expoente real
- **Fase:** RA3
- **Descrição:** Expoente deve ser `int`.
- **Regra Semântica:** `^ : (int|real) × int → (int|real)`

### Caso 24: `(UNDEFINED_VAR)`
- **Erro Esperado:** Variável não inicializada
- **Fase:** RA3
- **Descrição:** Uso de variável nunca declarada.

### Caso 25: `(5 3 &&)`
- **Erro Esperado:** AND lógico com tipos numéricos
- **Fase:** RA3
- **Descrição:** Operador `&&` requer operandos `boolean`.
- **Regra Semântica:** `&& : boolean × boolean → boolean`

### Caso 26: `(10 20 ||)`
- **Erro Esperado:** OR lógico com tipos numéricos
- **Fase:** RA3
- **Descrição:** Operador `||` requer operandos `boolean`.
- **Regra Semântica:** `|| : boolean × boolean → boolean`

### Caso 27: `((5 3 >) (10) (5.5) IFELSE)`
- **Erro Esperado:** IFELSE com ramos de tipos diferentes
- **Fase:** RA3
- **Descrição:** Ramo verdadeiro é `int`, ramo falso é `real`.
- **Regra Semântica:** `IFELSE : boolean × T × T → T` (ambos ramos mesmo tipo)

### Caso 28: `((5) (((X 1 +) X)) WHILE)`
- **Erro Esperado:** WHILE com condição não-booleana
- **Fase:** RA3
- **Descrição:** Condição é `int`, deve ser `boolean`.
- **Regra Semântica:** `WHILE : boolean × body → void`

### Caso 29: `((1.5) (10) (1) (((I 1 +) I)) FOR)`
- **Erro Esperado:** FOR com início de tipo incompatível
- **Fase:** RA3
- **Descrição:** Parâmetro início é `real`, mas geralmente deve ser `int`.
- **Regra Semântica:** `FOR : int × int × int × body → void`

### Caso 30: `((5 3 >) X)`
- **Erro Esperado:** Tentativa de armazenar `boolean` em variável
- **Fase:** RA3
- **Descrição:** Variáveis só aceitam tipos `int` e `real`.
- **Regra:** Tipo `boolean` não pode ser armazenado em memória.

---

## Resumo das Regras Semânticas

### Operadores Aritméticos
- `+, -, *` : `(int|real) × (int|real) → (int|real)` com promoção `int → real`
- `/` : `int × int → int` (divisão inteira)
- `|` : `(int|real) × (int|real) → real` (divisão real)
- `%` : `int × int → int` (módulo)
- `^` : `(int|real) × int(≥0) → (int|real)` (potência)

### Operadores Relacionais
- `>, <, >=, <=, ==, !=` : `(int|real) × (int|real) → boolean`

### Operadores Lógicos
- `&&, ||` : `boolean × boolean → boolean`
- `!` : `boolean → boolean`

### Estruturas de Controle
- `WHILE` : `boolean × body → void`
- `FOR` : `int × int × int × body → void`
- `IFELSE` : `boolean × T × T → T` (ramos devem ter mesmo tipo)

### Restrições de Memória
- Variáveis aceitam apenas tipos `int` e `real`
- Tipo `boolean` não pode ser armazenado
- Variáveis devem ser inicializadas antes do uso

---

## Uso dos Arquivos de Teste

### Teste4 (Erros de Tipos)
```bash
python3 compilar.py teste4_erros_tipos.txt
```
- Valida regras de tipos em operadores
- Verifica restrições de tipos especiais
- Testa detecção de tipos incompatíveis

### Teste5 (Erros de Memória)
```bash
python3 compilar.py teste5_erros_memoria.txt
```
- Valida inicialização de variáveis
- Verifica uso de RES
- Testa armazenamento de tipos inválidos

### Teste6 (Erros Abrangentes)
```bash
python3 compilar.py teste6_erros_compilador.txt
```
- Valida todas as fases (RA1, RA2, RA3)
- Cobertura balanceada de 30 casos de erro
- Teste completo do compilador

---

## Notas de Implementação

1. **Ordem de Detecção:**
   - RA1 detecta erros léxicos primeiro
   - RA2 detecta erros sintáticos depois
   - RA3 detecta erros semânticos por último

2. **Mensagens de Erro:**
   - Devem incluir número da linha
   - Tipo esperado vs tipo encontrado
   - Contexto do erro

3. **Múltiplos Erros:**
   - Alguns casos podem ter múltiplos erros
   - Reportar o primeiro erro encontrado por linha

4. **Parada em Erro:**
   - Compilador pode parar na primeira fase com erro
   - Não processar RA2 se RA1 falhar
   - Não processar RA3 se RA2 falhar

---

**Arquivos localizados em:**
- `teste4_erros_tipos.txt`
- `teste5_erros_memoria.txt`
- `teste6_erros_compilador.txt`

**Última atualização:** 2025-11-05
