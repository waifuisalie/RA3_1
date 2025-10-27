# Compilador RPN - Analisador Léxico, Sintático e Semântico

## Informações Institucionais

**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
**Disciplina:** Linguagens Formais e Compiladores
**Professor:** Frank Alcantara
**Ano:** 2025

### Integrantes do Grupo

- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

**Nome do grupo no Canvas:** RA3_1

---

## Descrição do Projeto

Este projeto implementa um **compilador completo** para uma linguagem simplificada baseada em **Notação Polonesa Reversa (RPN)**. O compilador integra três fases de análise:

1. **RA1 - Análise Léxica**: Tokenização de expressões RPN
2. **RA2 - Análise Sintática**: Parser LL(1) com geração de árvore sintática
3. **RA3 - Análise Semântica**: Verificação de tipos, memória e estruturas de controle

### Características Principais

- **Linguagem**: Notação Polonesa Reversa (RPN) no formato `(A B operador)`
- **Tipos de dados**: `int`, `real` (float), `boolean`
- **Operadores aritméticos**: `+`, `-`, `*`, `/`, `|`, `%`, `^`
- **Operadores relacionais**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Operadores lógicos**: `&&`, `||`, `!`
- **Estruturas de controle**: `IFELSE`, `WHILE`, `FOR`
- **Comandos especiais**: `RES` (referência a resultados anteriores), `MEM` (variáveis)
- **Análise semântica completa**: verificação de tipos, inicialização de variáveis, validação de estruturas de controle

---

## Compilação e Execução

### Requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa (usa apenas biblioteca padrão)

### Execução

Para executar o compilador, use o seguinte comando:

```bash
python3 compilar.py <arquivo_de_teste>
```

**Exemplos:**

```bash
# Usando caminho relativo ao diretório raiz
python3 compilar.py inputs/RA3/teste1_valido.txt

# Usando caminho relativo ao diretório inputs/RA1
python3 compilar.py float/teste1.txt

# Usando caminho relativo ao diretório inputs/RA2
python3 compilar.py RA2/teste1.txt

# Usando arquivo na raiz (arquivos de teste legados)
python3 compilar.py teste1_valido.txt

# Usando caminho absoluto
python3 compilar.py /caminho/completo/para/arquivo.txt
```

### Arquivos de Saída

O compilador gera os seguintes arquivos de saída:

- **`outputs/RA1/tokens/tokens_gerados.txt`**: Tokens gerados pelo analisador léxico
- **`outputs/RA2/arvore_sintatica.json`**: Árvore sintática em formato JSON (entrada para RA3)
- **Saída no console**: Relatório completo de execução com erros (se houver)

### Depuração

Para depurar o compilador, você pode:

1. **Verificar tokens gerados**: Examine `outputs/RA1/tokens/tokens_gerados.txt`
2. **Verificar árvore sintática**: Examine `outputs/RA2/arvore_sintatica.json`
3. **Adicionar prints de debug**: Adicione prints nos módulos Python relevantes
4. **Executar testes unitários**: `python3 -m pytest tests/`

---

## Estrutura do Projeto

```
RA3_1/
├── compilar.py                         # Programa principal - integra RA1 + RA2 + RA3
├── teste1_valido.txt                   # Arquivo de teste válido (raiz)
├── teste2_erros_tipos.txt              # Arquivo de teste com erros de tipos (raiz)
├── teste3_erros_memoria.txt            # Arquivo de teste com erros de memória (raiz)
├── LICENSE                             # Licença do projeto
├── README.md                           # Este arquivo
│
├── src/                                # Código-fonte
│   ├── RA1/                           # Fase 1 - Analisador Léxico
│   │   └── functions/
│   │       ├── python/                # Funções Python do analisador léxico
│   │       │   ├── __init__.py
│   │       │   ├── analisador_lexico.py    # Tokenização e análise léxica
│   │       │   ├── tokens.py               # Definições de tipos de tokens
│   │       │   ├── io_utils.py             # Utilitários de I/O
│   │       │   ├── rpn_calc.py             # Calculadora RPN
│   │       │   └── exibirResultados.py     # Exibição de resultados
│   │       └── assembly/              # Geração de código Assembly RISC-V (legado RA1)
│   │           ├── __init__.py
│   │           ├── builder.py
│   │           ├── header.py
│   │           ├── footer.py
│   │           ├── data_section.py
│   │           ├── code_section.py
│   │           ├── operations.py
│   │           ├── registers.py
│   │           ├── routines.py
│   │           └── io.py
│   │
│   ├── RA2/                           # Fase 2 - Analisador Sintático LL(1)
│   │   └── functions/
│   │       └── python/                # Funções do parser LL(1)
│   │           ├── __init__.py
│   │           ├── lerTokens.py            # Leitura e processamento de tokens
│   │           ├── construirGramatica.py   # Construção da gramática LL(1)
│   │           ├── parsear.py              # Parser descendente recursivo
│   │           ├── gerarArvore.py          # Geração de árvore sintática
│   │           ├── configuracaoGramatica.py # Configuração da gramática
│   │           ├── calcularFirst.py        # Cálculo dos conjuntos FIRST
│   │           ├── calcularFollow.py       # Cálculo dos conjuntos FOLLOW
│   │           └── construirTabelaLL1.py   # Construção da tabela LL(1)
│   │
│   └── RA3/                           # Fase 3 - Analisador Semântico
│       └── functions/
│           └── python/                # Funções do analisador semântico
│               ├── __init__.py
│               ├── analisador_semantico.py      # Função principal de análise semântica
│               ├── analisador_tipos.py          # Análise de tipos e verificação
│               ├── analisador_memoria_controle.py # Análise de memória e controle
│               ├── gramatica_atributos.py       # Gramática de atributos completa
│               ├── tabela_simbolos.py           # Tabela de símbolos
│               └── tipos.py                     # Sistema de tipos
│
├── inputs/                             # Arquivos de entrada para testes
│   ├── RA1/                           # Entradas da Fase 1
│   │   ├── float/                     # Testes com ponto flutuante
│   │   │   ├── teste1.txt
│   │   │   ├── teste2.txt
│   │   │   ├── teste3.txt
│   │   │   └── teste_parenteses_completo.txt
│   │   └── int/                       # Testes para assembly (inteiros)
│   │       ├── teste1_assembly.txt
│   │       ├── teste2_assembly.txt
│   │       ├── teste3_assembly.txt
│   │       └── teste_parenteses_completo.txt
│   ├── RA2/                           # Entradas da Fase 2
│   │   ├── teste1.txt                      # Operações básicas
│   │   ├── teste2.txt                      # Estruturas de controle
│   │   ├── teste3.txt                      # Casos complexos
│   │   └── teste4_incorreto.txt            # Casos com erros
│   └── RA3/                           # Entradas da Fase 3
│       ├── teste1_valido.txt               # Teste válido completo
│       ├── teste2_erros_tipos.txt          # Erros de verificação de tipos
│       ├── teste3_erros_memoria.txt        # Erros de memória não inicializada
│       └── teste_*.txt                     # Outros arquivos de teste
│
├── outputs/                            # Arquivos de saída gerados
│   ├── RA1/                           # Saídas do analisador léxico
│   │   ├── tokens/
│   │   │   └── tokens_gerados.txt          # Tokens gerados
│   │   └── assembly/
│   │       ├── programa_completo.S         # Código assembly RISC-V
│   │       └── registers.inc               # Include de registradores
│   ├── RA2/                           # Saídas do analisador sintático
│   │   └── arvore_sintatica.json           # Árvore sintática gerada
│   └── RA3/                           # Saídas do analisador semântico
│       └── gramatica_atributos.md          # Gramática de atributos
│
├── docs/                               # Documentação completa
│   ├── RA1/                           # Documentação da Fase 1
│   │   └── Github/
│   │       └── README.md                   # README original do RA1
│   ├── RA2/                           # Documentação da Fase 2
│   │   ├── Github/
│   │   │   └── README.md                   # README específico do RA2
│   │   └── documents/                 # Documentação técnica detalhada
│   │       ├── 01_Grammar_Fundamentals.md
│   │       ├── 02_LL1_Parsing_and_Syntax_Analysis.md
│   │       ├── 03_FIRST_FOLLOW_Sets_Calculation.md
│   │       ├── 04_LL1_Table_Construction_and_Conflict_Resolution.md
│   │       ├── 05_Control_Structure_Syntax_Design.md
│   │       ├── 06_Complete_FIRST_FOLLOW_Calculation.md
│   │       ├── 07_LL1_Table_and_Conflict_Resolution.md
│   │       ├── 08_Grammar_Validation_and_Final_Specification.md
│   │       ├── grammar_analysis.md         # Análise completa da gramática
│   │       └── grammar_calculations.md     # Cálculos matemáticos detalhados
│   └── RA3/                           # Documentação da Fase 3
│       ├── documents/                 # Documentação técnica
│       │   ├── Atribuicao_Simples_Epsilon.md
│       │   ├── Conversoes_Tokens_Parser.md
│       │   ├── Correcao_Bug_RES.md
│       │   └── RA3_Fase3_Doc/
│       │       ├── README_EXTRACTION.md
│       │       └── text/
│       │           └── RA3_Fase3_Analisador_Semantico.txt
│       ├── github_issues/             # Issues do GitHub
│       ├── theory/                    # Documentação teórica
│       │   ├── 01_attribute_grammars_theory.md
│       │   ├── 02_symbol_table_theory.md
│       │   ├── 03_type_system_theory.md
│       │   └── 04_advanced_exercises.md
│       └── IMPLEMENTATION_GUIDE.md    # Guia de implementação
│
├── flowcharts/                         # Diagramas e fluxogramas
│   ├── RA1/                           # Diagramas da Fase 1
│   │   ├── Divisao_Inteira_e_Modulo.jpeg
│   │   ├── Divisao_Real.jpeg
│   │   ├── Multiplicacao_Inteira.jpeg
│   │   ├── Multiplicacao_Real.jpeg
│   │   ├── Potenciacao_Inteira_e_Real.jpeg
│   │   ├── Soma_Inteira.jpeg
│   │   ├── Soma_Real.jpeg
│   │   ├── Subtracao_Inteira.jpeg
│   │   └── Subtracao_Real.jpeg
│   └── RA2/                           # Diagramas da Fase 2
│       ├── RA2_Architecture_Overview.md    # Visão geral da arquitetura
│       └── RA2_Function_Interfaces.md      # Interfaces entre funções
│
└── tests/                              # Testes unitários
    └── RA3/
        ├── test_analisar_semantica.py
        ├── test_tabela_simbolos.py
        └── test_tipos.py
```

---

## Sintaxe da Linguagem

### Notação Polonesa Reversa (RPN)

A linguagem utiliza Notação Polonesa Reversa, onde operadores aparecem após os operandos:

```
(operando1 operando2 operador)
```

### Tipos de Dados

- **`int`**: Números inteiros (ex: `5`, `-3`, `100`)
- **`real`** (ou `float`): Números de ponto flutuante (ex: `3.14`, `-2.5`, `10.0`)
- **`boolean`**: Resultado de operações relacionais e lógicas (usado internamente)

**Observação**: O tipo `boolean` não pode ser armazenado em memória (`MEM`), sendo usado apenas como resultado de expressões relacionais e lógicas em estruturas de controle.

### Operadores Suportados

#### Operadores Aritméticos

| Operador | Descrição | Exemplo | Requisitos |
|----------|-----------|---------|------------|
| `+` | Adição | `(5 3 +)` → `8` | Operandos numéricos (int ou real) |
| `-` | Subtração | `(10 3 -)` → `7` | Operandos numéricos (int ou real) |
| `*` | Multiplicação | `(4 5 *)` → `20` | Operandos numéricos (int ou real) |
| `/` | Divisão inteira | `(10 3 /)` → `3` | **AMBOS operandos devem ser int** |
| `\|` | Divisão real | `(10 3 \|)` → `3.333...` | Operandos numéricos, **resultado sempre real** |
| `%` | Resto (módulo) | `(10 3 %)` → `1` | **AMBOS operandos devem ser int** |
| `^` | Potenciação | `(2 3 ^)` → `8` | Base int/real, **expoente deve ser int positivo** |

**Regras de promoção de tipos**: Se um operando é `real` e outro é `int`, o resultado é promovido para `real`.

#### Operadores Relacionais

Retornam **sempre** tipo `boolean`.

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `>` | Maior que | `(5 3 >)` → `boolean` |
| `<` | Menor que | `(3 5 <)` → `boolean` |
| `>=` | Maior ou igual | `(5 5 >=)` → `boolean` |
| `<=` | Menor ou igual | `(3 5 <=)` → `boolean` |
| `==` | Igual | `(5 5 ==)` → `boolean` |
| `!=` | Diferente | `(5 3 !=)` → `boolean` |

#### Operadores Lógicos

Retornam **sempre** tipo `boolean`. Modo permissivo: aceitam valores numéricos via "truthiness" (0 = false, ≠0 = true).

| Operador | Descrição | Exemplo | Aridade |
|----------|-----------|---------|---------|
| `&&` | E lógico (AND) | `((5 3 >) (2 1 <) &&)` → `boolean` | Binário |
| `\|\|` | OU lógico (OR) | `((5 3 <) (2 1 >) \|\|)` → `boolean` | Binário |
| `!` | NÃO lógico (NOT) | `((5 3 >) !)` → `boolean` | Unário |

### Estruturas de Controle

#### IFELSE - Estrutura Condicional

**Sintaxe**: `(condição blocoTrue blocoFalse IFELSE)`

- **condição**: Expressão convertível para boolean
- **blocoTrue**: Expressão executada se condição for verdadeira
- **blocoFalse**: Expressão executada se condição for falsa
- **Requisito**: Ambos os blocos devem ter o **mesmo tipo**

**Exemplo**:
```
((X 15 >) (100) (200) IFELSE)
# Se X > 15, retorna 100, senão retorna 200
```

#### WHILE - Laço de Repetição

**Sintaxe**: `(condição corpo WHILE)`

- **condição**: Expressão convertível para boolean
- **corpo**: Expressão executada enquanto condição for verdadeira
- **Retorna**: Tipo da última expressão do corpo

**Exemplo**:
```
((COUNTER 5 <) (((COUNTER 1 +) COUNTER)) WHILE)
# Enquanto COUNTER < 5, incrementa COUNTER
```

#### FOR - Laço com Contador

**Sintaxe**: `(inicio fim passo corpo FOR)`

- **inicio**: Valor inicial do contador (**deve ser int**)
- **fim**: Valor final do contador (**deve ser int**)
- **passo**: Incremento do contador (**deve ser int**)
- **corpo**: Expressão executada a cada iteração
- **Retorna**: Tipo da última expressão do corpo

**Exemplo**:
```
((1) (10) (1) (I 2 *) FOR)
# Para I de 1 até 10, incrementando de 1, calcula I * 2
```

### Comandos Especiais

#### MEM - Armazenamento e Recuperação de Variáveis

**Armazenar**: `(valor VARIAVEL)`
- Armazena `valor` em `VARIAVEL`
- Valor deve ser `int` ou `real` (boolean **não** pode ser armazenado)
- Marca a variável como inicializada

**Recuperar**: `(VARIAVEL)`
- Retorna o valor armazenado em `VARIAVEL`
- **Erro semântico** se a variável não foi inicializada

**Exemplos**:
```
(10 X)        # Armazena 10 em X
(X)           # Recupera o valor de X (retorna 10)
((X 5 +) Y)   # Armazena X + 5 em Y
```

#### RES - Referência a Resultados Anteriores

**Sintaxe**: `(N RES)`
- Retorna o resultado da expressão `N` linhas anteriores
- `N` deve ser um **inteiro não negativo** (literal ou variável)
- Se `N` for variável, ela deve estar inicializada
- Linha referenciada deve existir (linha_atual - N ≥ 1)
- **Diferente de MEM**: pode referenciar resultados `boolean`

**Exemplos**:
```
(5 3 +)       # Linha 1: resultado = 8
(2 RES)       # Linha 3: retorna resultado da linha 1 (8)
(1 I)         # Armazena 1 em I
(I RES)       # Usa I como offset (equivalente a (1 RES))
```

### Expressões Aninhadas

Expressões podem ser aninhadas sem limite definido:

```
((5 3 +) (2 4 *) *)
# Calcula (5 + 3) * (2 * 4) = 8 * 8 = 64

((A B +) (C D *) |)
# Divide (A + B) por (C * D) usando divisão real

(((COUNTER 1 +) COUNTER) (COUNTER 5 <) WHILE)
# Incrementa COUNTER enquanto COUNTER < 5
```

### Exemplos Completos

#### Exemplo 1: Operações Básicas
```
(5 3 +)                    # int + int = int (8)
(10.5 2.0 *)               # real * real = real (21.0)
(5 3.0 +)                  # int + real = real (8.0) - promoção de tipo
```

#### Exemplo 2: Estruturas de Controle
```
(10 X)                                    # Armazena 10 em X
((X 15 >) (100) (200) IFELSE)             # Se X > 15: 100, senão: 200
(0 COUNTER)                               # Inicializa COUNTER com 0
((COUNTER 5 <) (((COUNTER 1 +) COUNTER)) WHILE) # Loop enquanto COUNTER < 5
```

#### Exemplo 3: Uso de RES
```
(5 3 +)                    # Linha 1: resultado = 8
(2 4 *)                    # Linha 2: resultado = 8
(2 RES)                    # Linha 3: retorna resultado da linha 1 (8)
(1 RES)                    # Linha 4: retorna resultado da linha 3 (8)
```

---

## Análise Semântica (RA3)

### Gramática de Atributos

O analisador semântico implementa uma **gramática de atributos completa** para verificar a correção semântica do programa. A gramática define:

- **Atributos sintetizados**: Calculados a partir dos filhos (propagam informação de baixo para cima)
- **Atributos herdados**: Calculados a partir do pai ou irmãos (propagam informação de cima para baixo)

#### Atributos Principais

- `tipo`: Tipo da expressão (int, real, boolean)
- `valor`: Valor calculado (quando aplicável)
- `inicializada`: Para variáveis, indica se foram inicializadas
- `escopo`: Nível de escopo da variável

### Verificações Semânticas

O analisador realiza as seguintes verificações:

#### 1. Verificação de Tipos

- **Compatibilidade de tipos** em operações aritméticas
- **Promoção de tipos** (int → real) quando necessário
- **Restrições de tipos**:
  - `/` e `%`: ambos operandos devem ser `int`
  - `^`: expoente deve ser `int` positivo
  - `|`: operandos numéricos, resultado sempre `real`

#### 2. Verificação de Memória

- **Inicialização de variáveis**: Garante que variáveis são inicializadas antes de serem usadas
- **Tipos armazenáveis**: Apenas `int` e `real` podem ser armazenados em memória (boolean não)
- **Referências válidas**: Valida uso de `RES` com offsets válidos

#### 3. Verificação de Estruturas de Controle

- **Condições válidas**: Garante que condições são convertíveis para boolean
- **Tipos consistentes**: Em `IFELSE`, ambos os ramos devem ter o mesmo tipo
- **Contadores inteiros**: Em `FOR`, inicio, fim e passo devem ser inteiros

### Regras Semânticas (Exemplos)

#### Regra: Adição com Promoção de Tipo

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
```

**Exemplo**:
- `(5 3 +)`: int + int = int
- `(5.0 3 +)`: real + int = real (promoção)

#### Regra: Divisão Inteira

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────
    Γ ⊢ (e₁ e₂ /) : int
```

**Erro se**: Qualquer operando não for `int`.

#### Regra: Estrutura Condicional IFELSE

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

**Erro se**: Ramos `true` e `false` tiverem tipos diferentes.

### Mensagens de Erro

O analisador reporta erros no seguinte formato:

```
ERRO SEMÂNTICO [Linha X]: <descrição>
Contexto: <trecho relevante do código>
```

**Exemplo**:
```
ERRO SEMÂNTICO [Linha 5]: Variável 'CONTADOR' utilizada sem inicialização
Contexto: (CONTADOR)
```

---

## Arquivos de Teste

O projeto inclui arquivos de teste organizados por fase:

### RA3 - Testes de Análise Semântica

#### `inputs/RA3/teste1_valido.txt`
Arquivo de teste válido completo com:
- Todas as operações aritméticas
- Operadores relacionais e lógicos
- Estruturas de controle (IFELSE, WHILE, FOR)
- Comandos especiais (RES, MEM)
- Inicialização e uso correto de variáveis

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste1_valido.txt
# Deve executar sem erros semânticos
```

#### `inputs/RA3/teste2_erros_tipos.txt`
Arquivo com erros de verificação de tipos:
- Divisão inteira com operando real: `(5.5 2 /)`
- Módulo com operando real: `(10.5 3 %)`
- Potência com expoente real: `(2 3.5 ^)`
- Operações inválidas com boolean

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt
# Deve reportar erros semânticos de tipos
```

#### `inputs/RA3/teste3_erros_memoria.txt`
Arquivo com erros de memória não inicializada:
- Uso de variável antes de inicialização
- Referências RES inválidas

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
# Deve reportar erros de variável não inicializada
```

---

## Funções Principais


### RA3 - Análise Semântica

- **`definir_gramatica_atributos()`**: Define gramática de atributos completa
- **`criar_tabela_simbolos()`**: Cria estrutura de tabela de símbolos
- **`adicionar_simbolo(nome, tipo)`**: Adiciona símbolo à tabela
- **`buscar_simbolo(nome)`**: Busca símbolo na tabela

- **`analisarSemantica(arvore, gramatica, tabela)`**: Função principal de análise semântica
- **`verificar_tipos(expressao, tabela)`**: Verifica compatibilidade de tipos
- **`promover_tipo(tipo1, tipo2)`**: Realiza promoção de tipos quando necessário

- **`analisarSemanticaMemoria(arvore, tabela)`**: Valida uso de memórias
- **`analisarSemanticaControle(arvore, tabela)`**: Valida estruturas de controle
- **`verificar_inicializacao(variavel)`**: Verifica se variável foi inicializada

- **`gerarArvoreAtribuida(arvore)`**: Gera árvore sintática atribuída
- **`main()`**: Função principal que coordena execução
- **`gerar_relatorios()`**: Gera relatórios em markdown

---

## Tratamento de Erros

O compilador detecta e reporta três tipos de erros:

### Erros Léxicos (RA1)
- Tokens inválidos
- Caracteres não reconhecidos

### Erros Sintáticos (RA2)
- Estrutura RPN malformada
- Parênteses desbalanceados
- Tokens inesperados

### Erros Semânticos (RA3)
- **Erros de tipos**: Operações com tipos incompatíveis
- **Erros de memória**: Variáveis não inicializadas
- **Erros de controle**: Condições inválidas, ramos com tipos diferentes

**Exemplo de mensagem de erro**:
```
ERRO SEMÂNTICO [Linha 5]: Operador '/' requer ambos operandos do tipo 'int', mas recebeu 'real' e 'int'
Contexto: (5.5 2 /)
```

---

## Licença

Este projeto está licenciado sob a licença especificada no arquivo `LICENSE`.

---

## Referências

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
- Material de aula da disciplina Linguagens Formais e Compiladores - PUCPR
- Documentação do projeto disponível em `docs/`

---