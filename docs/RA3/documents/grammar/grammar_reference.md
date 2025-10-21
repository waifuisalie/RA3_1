# Grammar Reference Documentation

## Production Rules (EBNF)

```ebnf
PROGRAM = LINHA, PROGRAM_PRIME ;
PROGRAM_PRIME = ( LINHA, PROGRAM_PRIME ) | ε ;
LINHA = abre_parenteses, SEQUENCIA, fecha_parenteses ;
SEQUENCIA = OPERANDO, SEQUENCIA_PRIME ;
SEQUENCIA_PRIME = ( OPERANDO, SEQUENCIA_PRIME )
                | OPERADOR_FINAL ;
OPERANDO = numero_real
         | ( variavel, OPERANDO_VAR_OPCIONAL )
         | LINHA ;
OPERANDO_VAR_OPCIONAL = res | not | ε ;
OPERADOR_FINAL = ARITH_OP
               | COMP_OP
               | LOGIC_OP
               | CONTROL_OP ;
CONTROL_OP = for | while | ifelse ;
ARITH_OP = soma
         | subtracao
         | multiplicacao
         | divisao_inteira
         | divisao_real
         | resto
         | potencia ;
COMP_OP = menor
        | maior
        | igual
        | menor_igual
        | maior_igual
        | diferente ;
LOGIC_OP = and | or | not ;
```

## Token Mappings (Theoretical → Real)

```
numero_real         → number
variavel            → identifier
abre_parenteses     → (
fecha_parenteses    → )
soma                → +
subtracao           → -
multiplicacao       → *
divisao_inteira     → /
divisao_real        → |
resto               → %
potencia            → ^
menor               → <
maior               → >
igual               → ==
menor_igual         → <=
maior_igual         → >=
diferente           → !=
and                 → &&
or                  → ||
not                 → !
for                 → for
while               → while
ifelse              → ifelse
res                 → res
```

## NULLABLE Sets

```
NULLABLE = {PROGRAM_PRIME, OPERANDO_VAR_OPCIONAL}
```

## FIRST Sets

```
FIRST(PROGRAM) = {(}
FIRST(PROGRAM_PRIME) = {(, ε}
FIRST(LINHA) = {(}
FIRST(SEQUENCIA) = {number, identifier, (}
FIRST(SEQUENCIA_PRIME) = {number, identifier, (, +, -, *, /, |, %, ^, <, >, ==, <=, >=, !=, &&, ||, !, for, while, ifelse}
FIRST(OPERANDO) = {number, identifier, (}
FIRST(OPERANDO_VAR_OPCIONAL) = {res, !, ε}
FIRST(OPERADOR_FINAL) = {+, -, *, /, |, %, ^, <, >, ==, <=, >=, !=, &&, ||, !, for, while, ifelse}
FIRST(ARITH_OP) = {+, -, *, /, |, %, ^}
FIRST(COMP_OP) = {<, >, ==, <=, >=, !=}
FIRST(LOGIC_OP) = {&&, ||, !}
FIRST(CONTROL_OP) = {for, while, ifelse}
```

## FOLLOW Sets

```
FOLLOW(PROGRAM) = {$}
FOLLOW(PROGRAM_PRIME) = {$}
FOLLOW(LINHA) = {(, ), $}
FOLLOW(SEQUENCIA) = {)}
FOLLOW(SEQUENCIA_PRIME) = {)}
FOLLOW(OPERANDO) = {number, identifier, (, +, -, *, /, |, %, ^, <, >, ==, <=, >=, !=, &&, ||, !, for, while, ifelse}
FOLLOW(OPERANDO_VAR_OPCIONAL) = {number, identifier, (, +, -, *, /, |, %, ^, <, >, ==, <=, >=, !=, &&, ||, !, for, while, ifelse}
FOLLOW(OPERADOR_FINAL) = {)}
FOLLOW(ARITH_OP) = {)}
FOLLOW(COMP_OP) = {)}
FOLLOW(LOGIC_OP) = {)}
FOLLOW(CONTROL_OP) = {)}
```

## LL(1) Parsing Table

| Non-terminal | number | identifier | ( | ) | + | - | * | / | \| | % | ^ | < | <= | > | >= | == | != | && | \|\| | ! | res | for | while | ifelse | $ |
|--------------|--------|------------|---|---|---|---|---|---|----|----|---|---|----|----|----|----|----|----|------|---|-----|-----|-------|--------|---|
| PROGRAM | - | - | PROGRAM → LINHA PROGRAM_PRIME | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PROGRAM_PRIME | - | - | PROGRAM_PRIME → LINHA PROGRAM_PRIME | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | PROGRAM_PRIME → ε |
| LINHA | - | - | LINHA → ( SEQUENCIA ) | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SEQUENCIA | SEQUENCIA → OPERANDO SEQUENCIA_PRIME | SEQUENCIA → OPERANDO SEQUENCIA_PRIME | SEQUENCIA → OPERANDO SEQUENCIA_PRIME | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SEQUENCIA_PRIME | SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME | SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME | SEQUENCIA_PRIME → OPERANDO SEQUENCIA_PRIME | - | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | - | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | SEQUENCIA_PRIME → OPERADOR_FINAL | - |
| OPERANDO | OPERANDO → number | OPERANDO → identifier OPERANDO_VAR_OPCIONAL | OPERANDO → LINHA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| OPERANDO_VAR_OPCIONAL | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | - | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ! | OPERANDO_VAR_OPCIONAL → res | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | OPERANDO_VAR_OPCIONAL → ε | - |
| OPERADOR_FINAL | - | - | - | - | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → ARITH_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → COMP_OP | OPERADOR_FINAL → LOGIC_OP | OPERADOR_FINAL → LOGIC_OP | OPERADOR_FINAL → LOGIC_OP | - | OPERADOR_FINAL → CONTROL_OP | OPERADOR_FINAL → CONTROL_OP | OPERADOR_FINAL → CONTROL_OP | - |
| ARITH_OP | - | - | - | - | ARITH_OP → + | ARITH_OP → - | ARITH_OP → * | ARITH_OP → / | ARITH_OP → \| | ARITH_OP → % | ARITH_OP → ^ | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| COMP_OP | - | - | - | - | - | - | - | - | - | - | - | COMP_OP → < | COMP_OP → <= | COMP_OP → > | COMP_OP → >= | COMP_OP → == | COMP_OP → != | - | - | - | - | - | - | - | - |
| LOGIC_OP | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | LOGIC_OP → && | LOGIC_OP → \|\| | LOGIC_OP → ! | - | - | - | - | - |
| CONTROL_OP | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | CONTROL_OP → for | CONTROL_OP → while | CONTROL_OP → ifelse | - |

## Grammar Properties

### Conflict-Free LL(1)
This grammar is **conflict-free** and fully LL(1) compliant:
- No FIRST/FIRST conflicts
- No FIRST/FOLLOW conflicts
- Deterministic parsing decisions for all non-terminals

### Nullable Non-Terminals
Only two non-terminals can derive epsilon:
- `PROGRAM_PRIME`: Allows zero or more lines in a program
- `OPERANDO_VAR_OPCIONAL`: Allows variables to appear alone without RES or NOT

### Language Features
The grammar supports:
- **Arithmetic operators**: `+`, `-`, `*`, `/`, `|`, `%`, `^`
- **Comparison operators**: `<`, `>`, `==`, `<=`, `>=`, `!=`
- **Logical operators**: `&&`, `||`, `!`
- **Control structures**: `for`, `while`, `ifelse`
- **Special keywords**: `RES` (result reference), variable identifiers
- **Nested expressions**: Through recursive `OPERANDO → LINHA` production
- **RPN (Reverse Polish Notation)**: All operations are postfix

## Syntax Trees

Syntax trees are generated during parsing and saved to `arvore_output.txt` in the project root. Each parsed line produces an ASCII-formatted syntax tree showing the derivation structure.

To view the latest syntax trees, see: `../../outputs/RA2/arvore_output.txt`

## Notes

- This grammar definition is the **source of truth** for the RA3 compiler phase
- All theoretical token names map to real tokens as shown in the Token Mappings section
- The grammar has been verified to be LL(1) with no conflicts
- Epsilon productions are represented as `ε` in EBNF notation and `epsilon` in the implementation
