# Documentação: teste3_erros_memoria.txt

## Objetivo
Arquivo de teste contendo **erros semânticos de memória e controle** para validação da fase RA3 (Análise Semântica).

---

## Expressões e Erros Esperados

### **Linha 1: Leitura de Variável Não Inicializada**
```
(Y)
```
- **Erro Esperado:** `Variável 'Y' utilizada sem inicialização`
- **Descrição:** A variável `Y` é referenciada sem ter sido previamente atribuída/inicializada.
- **Regra Semântica:** Toda variável deve ser inicializada antes do uso.
- **Contexto:** Primeira linha do arquivo - nenhuma variável foi definida ainda.

---

### **Linha 2: Inicialização Válida (Referência para erros futuros)**
```
(10 X)
```
- **Erro Esperado:** ❌ **NENHUM** - Esta linha é válida
- **Descrição:** Inicializa a variável `X` com o valor `10`.
- **Nota:** Esta linha serve como referência para detectar que `X` está inicializada, mas outras variáveis não.

---

### **Linha 3: Referência RES Negativa**
```
(-1 RES)
```
- **Erro Esperado:** `Referência RES deve ter índice não-negativo`
- **Descrição:** O operador `RES` requer um índice `N ≥ 1` indicando quantas linhas voltar. O valor `-1` é inválido.
- **Regra Semântica:** `RES : int(N ≥ 1) → tipo_da_linha_N_anterior`

---

### **Linha 4: Referência RES Além do Limite**
```
(100 RES)
```
- **Erro Esperado:** `Referência RES aponta para linha inexistente`
- **Descrição:** Na linha 4, não existem 100 linhas anteriores. O índice `100` excede o número de linhas processadas.
- **Regra Semântica:** `(N RES)` na linha `L` requer que `N < L`
- **Contexto:** Linha atual = 4, linhas disponíveis = 3 (linhas 1, 2, 3)

---

### **Linha 5: Armazenamento de Boolean em Memória**
```
((5 3 >) BOOL)
```
- **Erro Esperado:** `Tipo 'boolean' não pode ser armazenado em memória`
- **Descrição:** A comparação `(5 3 >)` retorna `boolean`, que não pode ser armazenado em variáveis. Apenas `int` e `real` são permitidos.
- **Regra Semântica:** `(valor variavel)` onde `valor : int | real`
- **Tipo inválido:** Tentativa de `(boolean BOOL)`

---

### **Linha 6: Uso de Variável com Boolean**
```
(BOOL)
```
- **Erro Esperado:** `Variável 'BOOL' utilizada sem inicialização`
- **Descrição:** A variável `BOOL` não foi inicializada (linha 5 falhou). Mesmo que a linha 5 fosse válida, `BOOL` não pode armazenar boolean.
- **Nota:** Este erro depende da implementação - pode ser reportado como não inicializada OU como tentativa de uso de boolean.

---

### **Linha 7: Condição Não-Booleana em WHILE**
```
((10) (5 3 +) WHILE)
```
- **Erro Esperado:** `Condição de controle deve ser booleana`
- **Descrição:** O `WHILE` requer condição `boolean`, mas recebe `(10)` que é `int`.
- **Regra Semântica:** `(condição corpo WHILE)` onde `condição : boolean`
- **Tipo inválido:** `int` usado como condição

---

### **Linha 8: Condição Não-Booleana em IFELSE**
```
((3.5) (10) (20) IFELSE)
```
- **Erro Esperado:** `Condição de controle deve ser booleana`
- **Descrição:** O `IFELSE` requer condição `boolean`, mas recebe `(3.5)` que é `real`.
- **Regra Semântica:** `(condição then else IFELSE)` onde `condição : boolean`
- **Tipo inválido:** `real` usado como condição

---

### **Linha 9: Uso de Variável Não Inicializada em Operação**
```
(Z 2 +)
```
- **Erro Esperado:** `Variável 'Z' utilizada sem inicialização`
- **Descrição:** A variável `Z` nunca foi inicializada, mas é usada na soma.
- **Regra Semântica:** Todas as variáveis em expressões devem estar no escopo de memória.

---

### **Linha 10: Comparação com Variável Não Inicializada**
```
((X Y >) TEST)
```
- **Erro Esperado:** `Variável 'Y' utilizada sem inicialização`
- **Descrição:** `X` foi inicializada na linha 2, mas `Y` nunca foi. A comparação `(X Y >)` é inválida.
- **Nota:** Mesmo que a comparação fosse válida (retornaria boolean), armazená-la em `TEST` também seria erro.
- **Erros múltiplos:**
  1. `Y` não inicializada
  2. Tentativa de armazenar boolean em `TEST`

---

### **Linha 11: Multiplicação com Variável Não Inicializada**
```
(W 5 *)
```
- **Erro Esperado:** `Variável 'W' utilizada sem inicialização`
- **Descrição:** A variável `W` nunca foi definida.
- **Regra Semântica:** Operandos em operações aritméticas devem estar inicializados.

---

### **Linha 12: Referência RES para Linha Atual (Índice 0)**
```
(0 RES)
```
- **Erro Esperado:** `Referência RES deve ter índice não-negativo` ou `Referência RES inválida (índice zero)`
- **Descrição:** `RES` com índice `0` não faz sentido (não há "linha 0 anterior").
- **Regra Semântica:** `N RES` requer `N ≥ 1`

---

### **Linha 13: Soma com Variáveis Não Inicializadas**
```
((A B +) C)
```
- **Erro Esperado:** `Variável 'A' utilizada sem inicialização` (ou `'B'`, dependendo da ordem de análise)
- **Descrição:** Nem `A` nem `B` foram inicializadas.
- **Erros múltiplos:** Duas variáveis não inicializadas na mesma expressão.

---

### **Linha 14: Referência RES com Índice Negativo (Variação)**
```
(-5 RES)
```
- **Erro Esperado:** `Referência RES deve ter índice não-negativo`
- **Descrição:** Outro caso de índice negativo para `RES`.
- **Regra Semântica:** `N ≥ 1` para `(N RES)`

---

### **Linha 15: Referência RES Excedendo Limite do Arquivo**
```
((50 RES) D)
```
- **Erro Esperado:** `Referência RES aponta para linha inexistente`
- **Descrição:** Na linha 15, não existem 50 linhas anteriores (apenas 14).
- **Contexto:** Linha atual = 15, máximo `N` válido = 14

---

## Regras Semânticas de Memória e Controle (Resumo)

### Inicialização de Variáveis
- **Atribuição:** `(valor variavel)` onde `valor : int | real`
- **Restrição:** `valor` **NÃO** pode ser `boolean`
- **Escopo:** Variável permanece inicializada para todas as linhas seguintes

### Uso de Variáveis
- **Leitura:** `(variavel)` ou uso em expressões
- **Restrição:** Variável **DEVE** ter sido inicializada anteriormente
- **Erro:** Usar variável não inicializada gera erro semântico

### Operador RES (Result Reference)
- **Sintaxe:** `(N RES)` onde `N` é o número de linhas atrás
- **Restrições:**
  - `N ≥ 1` (não pode ser zero ou negativo)
  - `N < linha_atual` (não pode exceder linhas processadas)
  - Retorna o resultado (tipo e valor) da linha `linha_atual - N`

### Estruturas de Controle

#### WHILE
```
((condição) (corpo) WHILE)
```
- **condição:** Deve ser `boolean`
- **corpo:** Expressão executada repetidamente

#### FOR
```
((init) (limit) (step) (corpo) FOR)
```
- **init, limit, step:** Devem ser `int`
- **corpo:** Expressão executada a cada iteração

#### IFELSE
```
((condição) (then) (else) IFELSE)
```
- **condição:** Deve ser `boolean`
- **then, else:** Podem ser qualquer tipo, mas devem ser do mesmo tipo

---

## Categorias de Erros no Arquivo

### 🔴 **Variáveis Não Inicializadas (6 casos)**
- Linhas: 1, 6, 9, 11, 13, 10

### 🔴 **Referências RES Inválidas (5 casos)**
- **Índice negativo:** Linhas 3, 14
- **Índice zero:** Linha 12
- **Índice excede limite:** Linhas 4, 15

### 🔴 **Armazenamento de Boolean (2 casos)**
- Linhas: 5, 10 (segunda parte)

### 🔴 **Condições Não-Booleanas (2 casos)**
- **WHILE:** Linha 7
- **IFELSE:** Linha 8

---

## Uso no RA3

Este arquivo deve validar que o analisador semântico:

1. ✅ **Rastreia variáveis inicializadas** (tabela de símbolos)
2. ✅ **Detecta uso de variáveis não inicializadas**
3. ✅ **Valida índices de RES:**
   - Não negativos
   - Dentro do limite de linhas processadas
4. ✅ **Impede armazenamento de booleanos em variáveis**
5. ✅ **Valida tipos de condições em estruturas de controle**
6. ✅ **Gerencia estado de memória linha por linha**

---

## Notas de Implementação

### Tabela de Símbolos
- Deve armazenar: `nome_variavel → (tipo, inicializada)`
- Atualizada a cada atribuição `(valor variavel)`
- Consultada a cada uso de variável

### Histórico de Resultados
- Armazenar tipo de resultado de cada linha processada
- Indexar por número da linha para validar `RES`
- Permitir cálculo de `linha_atual - N`

### Validação de RES
```python
if N < 1:
    erro("Referência RES deve ter índice não-negativo")
elif N >= linha_atual:
    erro("Referência RES aponta para linha inexistente")
else:
    return resultado_linha[linha_atual - N]
```

### Validação de Atribuição
```python
if tipo_valor == 'boolean':
    erro("Tipo 'boolean' não pode ser armazenado em memória")
else:
    tabela_simbolos[variavel] = (tipo_valor, True)
```

---

## Ordem de Detecção de Erros

Quando **múltiplos erros** existem na mesma linha (ex: linha 10), reportar na seguinte ordem de prioridade:

1. **Variável não inicializada** (mais crítico)
2. **Tipo inválido em operação**
3. **Armazenamento de boolean**

**Exemplo (linha 10):**
```
((X Y >) TEST)
```
Reportar: `Variável 'Y' utilizada sem inicialização` (primeiro erro crítico)

---

**Arquivo criado em:** `inputs/RA3/teste3_erros_memoria.txt`
**Última atualização:** 2025-10-22
