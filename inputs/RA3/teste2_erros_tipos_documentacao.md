# Documentação: teste2_erros_tipos.txt

## Objetivo
Arquivo de teste contendo **erros semânticos de violação de tipos** para validação da fase RA3 (Análise Semântica).

---

## Expressões e Erros Esperados

### **Linha 1: Real em Divisão Inteira**
```
(5.5 2 /)
```
- **Erro Esperado:** `Divisão inteira requer operandos inteiros`
- **Descrição:** O operador `/` (divisão inteira) só aceita operandos do tipo `int`. O operando `5.5` é `real`.
- **Regra Semântica:** `/ : int × int → int`

---

### **Linha 2: Real em Módulo**
```
(10.5 3 %)
```
- **Erro Esperado:** `Resto requer operandos inteiros`
- **Descrição:** O operador `%` (módulo/resto) só aceita operandos do tipo `int`. O operando `10.5` é `real`.
- **Regra Semântica:** `% : int × int → int`

---

### **Linha 3: Expoente Real**
```
(2 3.5 ^)
```
- **Erro Esperado:** `Expoente deve ser inteiro`
- **Descrição:** O operador `^` (potência) requer que o expoente seja inteiro, mesmo que a base possa ser real. O expoente `3.5` é `real`.
- **Regra Semântica:** `^ : (int|real) × int → (int|real)`

---

### **Linha 4: Expoente Negativo**
```
(2 -3 ^)
```
- **Erro Esperado:** `Expoente deve ser positivo`
- **Descrição:** O operador `^` requer expoente não-negativo (≥ 0). O valor `-3` é negativo.
- **Regra Semântica:** `^ : base × exp → result onde exp ≥ 0`

---

### **Linha 5: Boolean em Aritmética**
```
((5 3 >) 2 +)
```
- **Erro Esperado:** `Operação aritmética não aceita tipo boolean`
- **Descrição:** A comparação `(5 3 >)` retorna `boolean`, mas o operador `+` requer operandos numéricos (`int` ou `real`).
- **Regra Semântica:** `+ : (int|real) × (int|real) → (int|real)`
- **Tipo inválido:** `boolean + int`

---

### **Linha 6: Inteiros em Operador Lógico AND**
```
(5 3 &&)
```
- **Erro Esperado:** `Operador lógico requer operandos booleanos`
- **Descrição:** O operador `&&` (AND lógico) só aceita operandos `boolean`. Os valores `5` e `3` são `int`.
- **Regra Semântica:** `&& : boolean × boolean → boolean`

---

### **Linha 7: Boolean Negado em Aritmética**
```
((5 3 >) ! 10 +)
```
- **Erro Esperado:** `Operação aritmética não aceita tipo boolean`
- **Descrição:** A expressão `(5 3 >)` retorna `boolean`, negada por `!` continua `boolean`, que não pode ser usada em `+`.
- **Tipo inválido:** `boolean + int`

---

### **Linha 8: Condição Não-Booleana em IFELSE**
```
((10) (5 3 +) (2 1 -) IFELSE)
```
- **Erro Esperado:** `Condição de controle deve ser booleana`
- **Descrição:** O `IFELSE` requer que a condição (primeiro operando) seja `boolean`. O valor `10` é `int`.
- **Regra Semântica:** `IFELSE : boolean × T × T → T`

---

### **Linha 9: Resultado de Divisão Real em Soma com Inteiro**
```
((3.5 2 /) 5 +)
```
- **Erro Esperado:** `Divisão inteira requer operandos inteiros` (ou erro de tipo misto)
- **Descrição:** O operador `/` (divisão inteira) recebe `3.5` (real), violando a restrição de tipos inteiros.
- **Nota:** Mesmo com promoção de tipo, a divisão inteira não aceita reais.

---

### **Linha 10: Real no Segundo Operando de Módulo**
```
(100 50.5 %)
```
- **Erro Esperado:** `Resto requer operandos inteiros`
- **Descrição:** O operador `%` só aceita inteiros em ambos operandos. O valor `50.5` é `real`.
- **Regra Semântica:** `% : int × int → int`

---

### **Linha 11: Inteiro em OR Lógico**
```
((5.5 2.0 >) (10 5 *) ||)
```
- **Erro Esperado:** `Operador lógico requer operandos booleanos`
- **Descrição:** O primeiro operando `(5.5 2.0 >)` é `boolean`, mas o segundo `(10 5 *)` é `int`. O operador `||` requer ambos `boolean`.
- **Regra Semântica:** `|| : boolean × boolean → boolean`
- **Tipo inválido:** `boolean || int`

---

### **Linha 12: Ambos Operandos Reais em Módulo**
```
(15.8 4.2 %)
```
- **Erro Esperado:** `Resto requer operandos inteiros`
- **Descrição:** Ambos operandos são `real`, mas `%` requer `int`.
- **Regra Semântica:** `% : int × int → int`

---

### **Linha 13: Boolean em Subtração**
```
((2 3 <) 5 -)
```
- **Erro Esperado:** `Operação aritmética não aceita tipo boolean`
- **Descrição:** A comparação `(2 3 <)` retorna `boolean`, que não pode ser usado no operador `-`.
- **Regra Semântica:** `- : (int|real) × (int|real) → (int|real)`
- **Tipo inválido:** `boolean - int`

---

### **Linha 14: Expoente Real Negativo**
```
(3 -2.5 ^)
```
- **Erro Esperado:** `Expoente deve ser inteiro` e/ou `Expoente deve ser positivo`
- **Descrição:** O expoente `-2.5` viola duas restrições: não é inteiro E é negativo.
- **Regra Semântica:** `^ : base × int(≥0) → result`

---

### **Linha 15: Boolean em Multiplicação (Atribuição Aninhada)**
```
((10 X) ((5 3 >) 2 *) Y)
```
- **Erro Esperado:** `Operação aritmética não aceita tipo boolean`
- **Descrição:** A segunda atribuição `((5 3 >) 2 *) Y` tenta multiplicar `boolean` por `int`.
- **Tipo inválido:** `boolean * int`
- **Nota:** A primeira atribuição `(10 X)` é válida, mas a segunda contém o erro.

---

## Regras Semânticas de Tipos (Resumo)

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
- `IFELSE` : `boolean × T × T → T`

### Promoção de Tipo
- **Permitida:** `int → real` em operações aritméticas (`+, -, *, |, ^`) e comparações
- **Não permitida:** `int → boolean`, `boolean → int`, `boolean → real`

---

## Uso no RA3

Este arquivo deve ser usado para validar que o analisador semântico:

1. ✅ Detecta violações de tipo em operadores aritméticos
2. ✅ Valida restrições de operadores especiais (`/`, `%`, `^`)
3. ✅ Verifica tipos booleanos em operadores lógicos
4. ✅ Valida condições booleanas em estruturas de controle
5. ✅ Impede uso de booleanos em contextos numéricos
6. ✅ Valida restrições de expoentes (inteiro e não-negativo)

**Cada linha deve gerar um erro semântico claro e informativo.**

---

## Notas de Implementação

- O analisador deve reportar o **primeiro erro** encontrado em cada linha
- Mensagens de erro devem incluir:
  - Número da linha
  - Tipo esperado vs tipo encontrado
  - Operador/contexto onde ocorreu o erro
- Algumas linhas podem ter **múltiplos erros** (ex: linha 14), mas apenas o primeiro deve ser reportado

---

**Arquivo criado em:** `inputs/RA3/teste2_erros_tipos.txt`
**Última atualização:** 2025-10-22
