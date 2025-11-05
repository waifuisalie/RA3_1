# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-04 21:19:03

## Resumo

- **Total de linhas:** 22
- **Linhas com tipo definido:** 22
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (+)
    LINHA [5] {numero_inteiro}
    LINHA [3] {numero_inteiro}
```

### Linha 2

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (*)
    LINHA [10.5] {numero_real}
    LINHA [2.0] {numero_real}
```

### Linha 3

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (>)
    LINHA [5.5] {numero_real}
    LINHA [3.2] {numero_real}
```

### Linha 4

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (&&)
    COMP_OP (>)
      LINHA [5] {numero_inteiro}
      LINHA [3] {numero_inteiro}
    COMP_OP (<)
      LINHA [2] {numero_inteiro}
      LINHA [1] {numero_inteiro}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [10] {numero_inteiro}
    LINHA [X] {variavel}
```

### Linha 6

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (+)
      LINHA [X] {variavel}
      LINHA [5] {numero_inteiro}
    LINHA [Y] {variavel}
```

### Linha 7

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (+)
    LINHA [100] {numero_inteiro}
    LINHA [50] {numero_inteiro}
```

### Linha 8

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [10] {numero_inteiro}
    LINHA [I] {variavel}
```

### Linha 9

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [1] {numero_inteiro_res}
```

### Linha 10

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [0] {numero_inteiro}
    LINHA [COUNTER] {variavel}
```

### Linha 11

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<)
      LINHA [COUNTER] {variavel}
      LINHA [5] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+)
          LINHA [COUNTER] {variavel}
          LINHA [1] {numero_inteiro}
        LINHA [COUNTER] {variavel}
```

### Linha 12

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (FOR)
    LINHA
      LINHA [1] {numero_inteiro}
    LINHA
      LINHA [10] {numero_inteiro}
    LINHA
      LINHA [1] {numero_inteiro}
    ARITH_OP (*)
      LINHA [I] {variavel}
      LINHA [2] {numero_inteiro}
```

### Linha 13

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (%)
    LINHA [23] {numero_inteiro}
    LINHA [6] {numero_inteiro}
```

### Linha 14

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (>)
      LINHA [X] {variavel}
      LINHA [15] {numero_inteiro}
    LINHA
      LINHA [100] {numero_inteiro}
    LINHA
      LINHA [200] {numero_inteiro}
```

### Linha 15

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (*)
    ARITH_OP (+)
      LINHA [5] {numero_inteiro}
      LINHA [3] {numero_inteiro}
    ARITH_OP (*)
      LINHA [2] {numero_inteiro}
      LINHA [4] {numero_inteiro}
```

### Linha 16

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [20] {numero_inteiro}
    LINHA [A] {variavel}
```

### Linha 17

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  CONTROL_OP (IFELSE)
    LOGIC_OP (&&)
      COMP_OP (>)
        LINHA [A] {variavel}
        LINHA [10] {numero_inteiro}
      COMP_OP (>)
        LINHA [Y] {variavel}
        LINHA [5] {numero_inteiro}
    LINHA
      ARITH_OP (|)
        ARITH_OP (+)
          LINHA [A] {variavel}
          LINHA [Y] {variavel}
        LINHA [2.0] {numero_real}
    LINHA
      ARITH_OP (*)
        LINHA [A] {variavel}
        LINHA [Y] {variavel}
```

### Linha 18

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (/)
    LINHA [15] {numero_inteiro}
    LINHA [7] {numero_inteiro}
```

### Linha 19

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (^)
    LINHA [2.5] {numero_real}
    LINHA [3.0] {numero_real}
```

### Linha 20

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [2] {numero_inteiro_res}
```

### Linha 21

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (-)
      LINHA [A] {variavel}
      LINHA [X] {variavel}
    LINHA [B] {variavel}
```

### Linha 22

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (>)
      LINHA [B] {variavel}
      LINHA [0] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (-)
          LINHA [B] {variavel}
          LINHA [1] {numero_inteiro}
        LINHA [B] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*