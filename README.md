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

Este projeto implementa um compilador para uma linguagem simplificada baseada em **Notação Polonesa Reversa (RPN)**. O compilador integra três fases de análise:

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
python3 compilar.py inputs/RA3/teste1.txt

# Usando caminho relativo ao diretório inputs/RA1
python3 compilar.py float/teste1.txt

# Usando caminho relativo ao diretório inputs/RA2
python3 compilar.py RA2/teste1.txt

# Usando caminho absoluto
python3 compilar.py /caminho/completo/para/arquivo.txt
```

### Arquivos de Saída

O compilador gera os seguintes arquivos de saída organizados por fase:

#### RA1 - Análise Léxica

- **`outputs/RA1/tokens/tokens_gerados.txt`**: Lista de tokens gerados pelo analisador léxico

#### RA2 - Análise Sintática

- **`outputs/RA2/arvore_sintatica.json`**: Árvore sintática em formato JSON (entrada para RA3)

#### RA3 - Análise Semântica

##### Diretório `relatorios/`

- **`relatorios/arvore_atribuida.md`**: Árvore sintática abstrata com atributos de tipo inferidos para cada nó
  - Mostra o tipo resultante de cada expressão
  - Apresenta a estrutura hierárquica da árvore com tipos anotados
  - Inclui resumo com total de linhas analisadas e contagem de tipos

- **`relatorios/erros_sematicos.md`**: Relatório detalhado de todos os erros semânticos encontrados
  - Lista cada erro com linha, descrição e contexto
  - Inclui resumo com total de erros e status da análise
  - Apresenta categorias de erros (tipos, memória, controle)

- **`relatorios/julgamento_tipos.md`**: Análise detalhada de inferência de tipos por expressão
  - Mostra o processo de julgamento de tipos linha por linha
  - Documenta regras de promoção de tipos aplicadas
  - Identifica expressões com tipos incompatíveis

- **`relatorios/tabela_simbolos.md`**: Tabela de símbolos com variáveis declaradas
  - Lista todas as variáveis com nome, tipo e escopo
  - Indica quais variáveis foram inicializadas
  - Mostra histórico de atribuições

- **`relatorios/gramatica_atributos.md`**: Gramática de atributos completa utilizada na análise
  - Define regras semânticas para cada produção
  - Especifica atributos sintetizados e herdados
  - Documenta as equações semânticas aplicadas

##### Diretório `outputs/RA3/`

- **`outputs/RA3/arvore_atribuida.json`**: Árvore sintática em formato JSON com atributos semânticos
  - Estrutura JSON com tipos inferidos para cada nó
  - Facilita processamento automatizado por outras ferramentas
  - Inclui metadados de linha e hierarquia de expressões

- **`outputs/RA3/gramatica_atributos.md`**: Cópia da gramática de atributos para referência

##### Console

- **Saída no console**: Relatório resumido de execução
  - Status de cada fase (RA1, RA2, RA3)
  - Resumo de erros encontrados (se houver)
  - Mensagens de sucesso ou falha da compilação

### Depuração

Para depurar o compilador, você pode:

1. **Verificar tokens gerados**: Examine `outputs/RA1/tokens/tokens_gerados.txt`
2. **Verificar árvore sintática**: Examine `outputs/RA2/arvore_sintatica.json`
3. **Verificar análise semântica**: Consulte os relatórios em `relatorios/`
4. **Adicionar prints de debug**: Adicione prints nos módulos Python relevantes
5. **Executar testes unitários**: `python3 -m pytest tests/`

### Entendendo os Arquivos de Saída

#### 1. Árvore Atribuída (`arvore_atribuida.md` e `arvore_atribuida.json`)

Estes arquivos contêm a **árvore sintática abstrata com atributos semânticos**. Cada nó da árvore inclui:

- **`tipo_vertice`**: Nome do símbolo não-terminal da gramática
- **`tipo_inferido`**: Tipo semântico inferido (`int`, `real`, `boolean`, ou `None`)
- **`numero_linha`**: Número da linha no código-fonte
- **`filhos`**: Lista de sub-expressões aninhadas

**Formato Markdown** (`arvore_atribuida.md`):
```markdown
### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

LINHA
└── SEQUENCIA
    ├── OPERANDO: 5 (int)
    ├── OPERANDO: 3 (int)
    └── OPERADOR_FINAL: + (int)
```

**Formato JSON** (`arvore_atribuida.json`):
```json
{
  "tipo_vertice": "LINHA",
  "tipo_inferido": "int",
  "numero_linha": 5,
  "filhos": [...]
}
```

**Uso**: Depurar inferência de tipos e visualizar a estrutura hierárquica das expressões.

---

#### 2. Erros Semânticos (`erros_sematicos.md`)

Lista **todos os erros semânticos** detectados durante a análise:

```markdown
### Erro 1
ERRO SEMÂNTICO [Linha 10]: Operador '/' requer operandos inteiros. Recebido: real, int
Contexto: (5.5 / 2)
```

**Categorias de erros**:
- **Erros de tipos**: Incompatibilidade de tipos em operações
- **Erros de memória**: Variáveis não inicializadas ou não declaradas
- **Erros de controle**: Condições inválidas, ramos inconsistentes

**Uso**: Identificar e corrigir problemas semânticos no código-fonte.

---

#### 3. Julgamento de Tipos (`julgamento_tipos.md`)

Documenta o **processo de inferência de tipos** para cada expressão:

```markdown
## Linha 5: (5 3 +)

### Análise de Tipos:
- Operando esquerdo: 5 (int)
- Operando direito: 3 (int)
- Operador: + (requer numéricos)
- Regra aplicada: int + int = int

### Tipo Resultante: `int`
```

**Informações incluídas**:
- Tipos dos operandos
- Regras de promoção de tipos aplicadas (ex: `int` + `real` = `real`)
- Restrições de operadores (ex: `/` requer ambos `int`)
- Expressões de identidade (epsilon) para linhas vazias

**Uso**: Entender como o compilador inferiu cada tipo e diagnosticar erros sutis de tipos.

---

#### 4. Tabela de Símbolos (`tabela_simbolos.md`)

Lista **todas as variáveis declaradas** no programa:

```markdown
| Nome | Tipo | Inicializada | Escopo | Linha Declaração |
|------|------|--------------|--------|------------------|
| X    | int  | Sim          | global | 2                |
| Y    | real | Sim          | global | 5                |
| COUNTER | int | Sim       | global | 8                |
```

**Informações por variável**:
- **Nome**: Identificador da variável
- **Tipo**: `int` ou `real` (boolean não pode ser armazenado)
- **Inicializada**: Se a variável recebeu valor antes de ser usada
- **Escopo**: Contexto da variável (global para este compilador)
- **Linha Declaração**: Linha onde a variável foi inicializada pela primeira vez

**Uso**: Verificar quais variáveis existem e se foram inicializadas corretamente.

---

#### 5. Gramática de Atributos (`gramatica_atributos.md`)

Documenta a **gramática de atributos completa** usada na análise semântica:

```markdown
### Produção: SEQUENCIA → OPERANDO OPERANDO OPERADOR_FINAL

#### Atributos Sintetizados:
- SEQUENCIA.tipo = tipo_resultado_operacao(OPERANDO₁.tipo, OPERANDO₂.tipo, OPERADOR_FINAL.simbolo)

#### Regras Semânticas:
1. Verificar compatibilidade de tipos dos operandos
2. Aplicar promoção de tipos se necessário (int → real)
3. Validar restrições do operador (ex: '/' requer int)
4. Calcular tipo resultante
```

**Conteúdo**:
- Produções da gramática com atributos
- Atributos sintetizados (propagados de baixo para cima)
- Atributos herdados (propagados de cima para baixo)
- Equações semânticas para cada produção
- Regras de verificação de tipos

**Uso**: Referência técnica para entender as regras semânticas implementadas.

---

### Localização dos Arquivos

Os relatórios são gerados em **duas localizações**:

1. **`relatorios/`** (raiz do projeto): Cópias para acesso rápido após cada execução
2. **`outputs/RA3/relatorios/`**: Estrutura organizada para arquivamento

Ambos os locais contêm os mesmos arquivos, permitindo que você escolha a localização mais conveniente para consulta.

---

## Estrutura do Projeto

```
RA3_1/
├── compilar.py                         # Programa principal - integra RA1 + RA2 + RA3
├── LICENSE                             # Licença do projeto
├── README.md                           # Este arquivo
├── CLAUDE.md                           # Instruções para Claude Code (IA)
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
│       ├── teste1.txt                       # Teste válido completo (casos básicos)
│       ├── teste2.txt                       # Teste válido abrangente
│       ├── teste3.txt                       # Teste válido complementar
│       ├── teste4_erros_tipos.txt           # Erros de verificação de tipos
│       ├── teste5_erros_memoria.txt         # Erros de memória não inicializada
│       ├── teste6_erros_compilador.txt      # Erros abrangentes (RA1+RA2+RA3)
│       └── extra/                           # Casos de teste adicionais
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
│       ├── arvore_atribuida.json           # Árvore com atributos semânticos (JSON)
│       ├── gramatica_atributos.md          # Gramática de atributos
│       └── relatorios/                     # Relatórios detalhados
│           ├── arvore_atribuida.md         # Árvore atribuída (markdown)
│           ├── erros_sematicos.md          # Relatório de erros semânticos
│           ├── julgamento_tipos.md         # Análise de inferência de tipos
│           ├── tabela_simbolos.md          # Tabela de símbolos
│           └── gramatica_atributos.md      # Gramática de atributos (cópia)
│
├── relatorios/                         # Relatórios da última execução (raiz)
│   ├── arvore_atribuida.md                 # Cópia para acesso rápido
│   ├── erros_sematicos.md                  # Cópia para acesso rápido
│   ├── julgamento_tipos.md                 # Cópia para acesso rápido
│   ├── tabela_simbolos.md                  # Cópia para acesso rápido
│   └── gramatica_atributos.md              # Cópia para acesso rápido
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

O projeto inclui 6 arquivos de teste organizados em `inputs/RA3/` para validação completa do compilador:

### Testes Válidos (Casos Corretos)

#### `teste1.txt`
**Casos básicos válidos** - 10 seções organizadas:
- Operações aritméticas básicas (`+`, `-`, `*`, `/`, `%`, `^`)
- Operações de comparação (`>`, `<`, `==`, `>=`, `<=`, `!=`)
- Operações lógicas (`&&`, `||`, `!`)
- Atribuições e uso de variáveis
- Operações com RES
- Estruturas WHILE, FOR e IFELSE
- Expressões complexas aninhadas

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste1.txt
# Deve executar sem erros
```

#### `teste2.txt`
**Casos abrangentes válidos** - Teste completo do analisador:
- Operações aritméticas válidas
- Declaração e uso de variáveis
- Promoção automática de tipos (`int` → `real`)
- Operações de comparação e lógica
- Estruturas de controle complexas
- Expressões aninhadas
- Loops com múltiplas operações

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste2.txt
# Deve executar sem erros semânticos
```

#### `teste3.txt`
**Casos complementares válidos** - 7 seções simplificadas:
- Declaração e operações básicas
- Promoção automática e comparações
- Operações lógicas e booleanas
- Atribuições e variáveis
- Estruturas IFELSE
- Estruturas WHILE
- Estruturas FOR

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste3.txt
# Deve executar sem erros
```

### Testes de Erro (Casos Inválidos)

#### `teste4_erros_tipos.txt`
**Erros de tipos (RA3)** - 6 seções de erros semânticos:
- Divisão inteira com tipos incompatíveis: `(5.5 2 /)`
- Resto com tipos incompatíveis: `(10.5 3 %)`
- Potenciação com expoente real: `(2 3.5 ^)`
- Operações aritméticas com booleanos: `((5 3 >) 2 +)`
- Operações lógicas com tipos numéricos: `(5 3 &&)`
- Estruturas de controle malformadas

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste4_erros_tipos.txt
# Deve reportar erros semânticos de tipos
```

#### `teste5_erros_memoria.txt`
**Erros de memória e inicialização (RA3)** - 5 seções:
- Variáveis não inicializadas: `(Y)`, `(Z 2 +)`
- Uso incorreto de RES: `(-1 RES)`
- Armazenamento de booleanos: `((5 3 >) BOOL)`
- Estruturas de controle com erros: `((10) (5 3 +) WHILE)`

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste5_erros_memoria.txt
# Deve reportar erros de variável não inicializada
```

#### `teste6_erros_compilador.txt`
**Erros abrangentes (RA1, RA2 e RA3)** - 30 casos balanceados:

**Parte 1 - Erros Léxicos (RA1) - 10 casos:**
- Caracteres inválidos: `(5 @ 3)`, `(10 # 5)`
- Números malformados: `(3.14.15 X)`, `(..5 Y)`

**Parte 2 - Erros Sintáticos (RA2) - 10 casos:**
- Parênteses desbalanceados: `((5 3 +)`
- Notação infixa incorreta: `(5 + 3)`
- Estruturas malformadas: `(+)`, `()`

**Parte 3 - Erros Semânticos (RA3) - 10 casos:**
- Tipos incompatíveis: `(5.5 2 /)`, `(10.5 3 %)`
- Variáveis não inicializadas: `(UNDEFINED_VAR)`
- Operações lógicas inválidas: `(5 3 &&)`
- Estruturas de controle com erros: `((5) (((X 1 +) X)) WHILE)`

**Exemplo de execução**:
```bash
python3 compilar.py inputs/RA3/teste6_erros_compilador.txt
# Deve reportar erros em todas as fases (RA1, RA2, RA3)
```

### Documentação dos Testes

Para documentação detalhada de todos os casos de erro, consulte:
- **`docs/RA3/documents/testes_erros_documentacao.md`** - Documentação completa dos 3 arquivos de teste com erros, incluindo regras semânticas e exemplos

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
