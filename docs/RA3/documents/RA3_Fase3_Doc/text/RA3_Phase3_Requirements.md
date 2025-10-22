# RA3 - Fase 3: Analisador Semântico

**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
**Disciplina:** Linguagens Formais e Autômatos
**Professor:** Frank Alcantara
**Ano:** 2025

## Grupo RA3_1

### Integrantes (ordem alfabética)
- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

---

## 1. Objetivo

Desenvolver um **analisador semântico** sobre um parser LL(1) para a linguagem RPN simplificada, complementando as Fases 1 (Analisador Léxico) e 2 (Analisador Sintático).

### Objetivo Específico
Utilizar a **árvore sintática abstrata** gerada na Fase 2 como entrada e criar uma **árvore sintática abstrata atribuída** através da aplicação de uma **Gramática de Atributos**.

---

## 2. Descrição do Trabalho

O programa deve ser capaz de:

1. **Ler arquivo de teste** (.txt) em formato ASCII com código-fonte RPN (uma expressão por linha)
2. **Utilizar a AST da Fase 2** como entrada
3. **Criar Gramática de Atributos** da linguagem
4. **Implementar analisador semântico** para criar AST atribuída
5. **Gerar documento de análise semântica** (julgamento de tipos, verificações semânticas)
6. **Detectar e reportar erros** léxicos, sintáticos e **semânticos**

### ⚠️ OBSERVAÇÃO CRÍTICA

**A partir desta fase, todos os três analisadores serão utilizados em conjunto:**

```
Arquivo de teste → Analisador Léxico (Fase 1) → Analisador Sintático (Fase 2) → Analisador Semântico (Fase 3)
```

- **OBRIGATÓRIO:** Mesmo formato de tokens da Fase 1
- **OBRIGATÓRIO:** Mesma gramática da Fase 2
- Divergências = erros de integração = perda de pontos

**Nesta fase NÃO será necessário gerar código Assembly.**

---

## 3. Características da Linguagem

### 3.1 Notação RPN

Formato: `(A B op)` onde A e B são operandos e op é um operador

### 3.2 Operadores Suportados

**Aritméticos:**
- `+` Adição: `(A B +)`
- `-` Subtração: `(A B -)`
- `*` Multiplicação: `(A B *)`
- `|` Divisão Real: `(A B |)`
- `/` Divisão Inteira: `(A B /)` (apenas inteiros)
- `%` Resto: `(A B %)` (apenas inteiros)
- `^` Potenciação: `(A B ^)` (B deve ser inteiro positivo)

**Relacionais (retornam tipo booleano):**
- `>` Maior que
- `<` Menor que
- `>=` Maior ou igual
- `<=` Menor ou igual
- `==` Igual
- `!=` Diferente

Todos aceitam operandos `int` ou `real` e retornam `booleano`.

**Lógicos (retornam tipo booleano):**
- `&&` E lógico (AND): `(A B &&)`
- `||` OU lógico (OR): `(A B ||)`
- `!` Negação lógica (NOT): `(A !)` (unário postfix)

**Modo Permissivo (Truthiness):**
Os operadores lógicos aceitam operandos `int`, `real` ou `boolean`:
- Valores numéricos são convertidos via truthiness: `0` e `0.0` = false, outros valores = true
- Operandos boolean são usados diretamente
- Resultado SEMPRE é boolean

**Exemplos:**
- `(5 3 &&)` → `true && true` = `true`
- `(0 5 ||)` → `false || true` = `true`
- `((x 0 >) !)` → negação de comparação

### 3.3 Tipos de Dados

A linguagem suporta três tipos:

1. **int:** Números inteiros
2. **real (float):** Números de ponto flutuante
3. **booleano:** Resultado de operações relacionais (usado internamente)

**⚠️ IMPORTANTE:** O tipo booleano NÃO pode ser armazenado em memórias (MEM), apenas usado como resultado de expressões relacionais em estruturas de controle.

**Tipos Válidos para Armazenamento:**
- MEM aceita: `int`, `real`
- MEM rejeita: `boolean`
- RES aceita: `int`, `real`, `boolean` (diferente de MEM!)

**⚠️ NOTA:** O sistema utiliza **exatamente 3 tipos**. Não há tipo `void` ou outros tipos auxiliares.

### 3.4 Precisão Numérica

Baseada na arquitetura do Arduino:

| Arquitetura | Precisão |
|-------------|----------|
| 8 bits | Meia precisão (16 bits, IEEE 754) |
| 16 bits | Precisão simples (32 bits, IEEE 754) |
| 32 bits | Precisão dupla (64 bits, IEEE 754) |
| 64 bits | Precisão quádrupla (128 bits, IEEE 754) |

**Para esta avaliação:** Considerar arquitetura Arduino Uno R3 / Mega (8 bits)

### 3.5 Expressões Aninhadas

Sem limite de aninhamento:

```
(A (C D *) +)              # Soma A ao produto de C e D
((A B %) (D E *) /)        # Divide resto de A por B pelo produto de D e E
((A B +) (C D *) |)        # Divisão real da soma de A e B pelo produto de C e D
```

A, B, C, D, E podem ser literais ou referências a memórias.

---

## 4. Comandos Especiais

### 4.1 Comandos de Memória

- `(N RES)` - Retorna resultado da expressão N linhas anteriores (N ≥ 0)
- `(V MEM)` - Armazena valor V em memória MEM
- `(MEM)` - Retorna valor armazenado em MEM

**⚠️ MUDANÇA IMPORTANTE DA FASE 2:**
- `(MEM)` agora retorna **erro semântico** se não foi inicializada
- Verificação deve ser feita no analisador semântico

### 4.2 Regras de Escopo

**Escopo Global (Arquivo):**
- Cada arquivo de texto representa um escopo de memória independente
- Variáveis não compartilham estado entre arquivos

**Escopo de Estruturas de Controle:**
- Variáveis dentro de estruturas de controle aninhadas (FOR, WHILE, IFELSE) devem ter escopo validado
- O atributo `escopo` deve rastrear o nível de aninhamento
- Cada estrutura de controle pode criar um novo nível de escopo

**Nomenclatura:**
- MEM pode ser qualquer conjunto de letras maiúsculas: `MEM`, `VAR`, `X`, `CONTADOR`
- `RES` é uma keyword reservada da linguagem
- Nomes de variáveis são case-insensitive (convertidos para UPPERCASE internamente)

---

## 5. Estruturas de Controle

Devem ser incluídas na gramática em notação pós-fixada (RPN).

**Tokens necessários:** (definir sintaxe específica para `FOR`, `WHILE`, `IFELSE`)

---

## 6. Analisador Semântico - Especificação

### 6.1 Verificações Semânticas Obrigatórias

1. **Julgamento de Tipos:**
   - Verificar compatibilidade entre operandos
   - Ex: potência `^` deve ter expoente inteiro

2. **Verificação de Memória:**
   - Garantir inicialização antes do uso

3. **Verificação de Comandos Especiais:**
   - Validar uso correto de `(N RES)`, `(V MEM)`, `(MEM)`

4. **Verificação de Estruturas de Controle:**
   - Formação correta das estruturas (IFELSE, WHILE, FOR)
   - Condições devem resultar em valor booleano **ou equivalente**
   - **"Equivalente"** significa: int/real podem ser usados via truthiness (0 = false, não-zero = true)
   - IFELSE: Ambos os ramos devem ter o **mesmo tipo**
   - WHILE/FOR: Retornam o tipo da última expressão do corpo
   - FOR: Parâmetros inicio, fim e passo DEVEM ser int

5. **Detecção de Erros Semânticos:**
   - Mensagens claras
   - Indicação de linha e natureza do erro

6. **Geração de Relatório:**
   - Documento de análise semântica
   - Erros encontrados
   - Árvore sintática abstrata atribuída

### 6.2 Gramática de Atributos

Deve ser definida e documentada em arquivo markdown.

#### Tipos de Atributos

**Atributos Sintetizados:**
- Calculados a partir dos filhos
- Propagam informação de baixo para cima

**Atributos Herdados:**
- Calculados a partir do pai ou irmãos
- Propagam informação de cima para baixo

#### Atributos Principais

Para cada não-terminal e terminal:

- `tipo`: Tipo da expressão (inteiro, real, booleano)
- `valor`: Valor calculado (quando aplicável)
- `inicializada`: Para memórias, indica se foram inicializadas
- `escopo`: Nível de escopo da variável

### 6.3 Exemplos de Regras de Produção

#### 1. Adição de Inteiros
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
      Γ ⊢ e₁ + e₂ : int
```

#### 2. Adição com Promoção de Tipo
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : float
───────────────────────────────
     Γ ⊢ e₁ + e₂ : float
```

Ou usando função `promover_tipo`:
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂
──────────────────────────────────────
Γ ⊢ e₁ + e₂ : promover_tipo(T₁, T₂)
```

#### 3. Estrutura Condicional
```
Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : T    Γ ⊢ e₃ : T
─────────────────────────────────────────────
      Γ ⊢ if e₁ then e₂ else e₃ : T
```

#### 4. Declaração de Variável
```
Γ ⊢ e : T'    T' ≤ T    Γ[x ↦ T] ⊢ ecorpo : Tcorpo
──────────────────────────────────────────────────
         Γ ⊢ (x : T ← e; ecorpo) : Tcorpo
```

#### 5. Chamada de Função
```
tabela(f) = (T₁, …, Tₙ) → Tret    Γ ⊢ eᵢ : T'ᵢ    T'ᵢ ≤ Tᵢ para i = 1..n
────────────────────────────────────────────────────────────────────────
                    Γ ⊢ f(e₁, …, eₙ) : Tret
```

#### Observações sobre as Regras

- Exemplos usam notação **infixa** para clareza
- Na implementação, adaptar para **notação RPN**
- Exemplo:
  - Infixa (regras): `if e₁ then e₂ else e₃`
  - RPN (código): `(e₁ e₂ e₃ IF)`
- Semântica de tipagem permanece a mesma

#### 6. Estruturas de Controle e Tipos de Retorno

**IFELSE:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ etrue : T    Γ ⊢ efalse : T
────────────────────────────────────────────────────────────────────
              Γ ⊢ (cond etrue efalse IFELSE) : T
```
- Condição: Qualquer tipo convertível para boolean
- **Restrição:** Ambos os ramos DEVEM ter o mesmo tipo T
- Resultado: tipo T (tipo dos ramos)

**WHILE:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```
- Resultado: tipo da última expressão do corpo

**FOR:**
```
Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T
────────────────────────────────────────────────────────────────────
              Γ ⊢ (init end step corpo FOR) : T
```
- **Restrição:** init, end, step DEVEM ser int
- Resultado: tipo da última expressão do corpo

### 6.4 Exemplo de Aplicação em RPN

**Expressão:** `(5 3 +)`

Aplicação:
1. `Γ ⊢ 5 : int` (literal inteiro)
2. `Γ ⊢ 3 : int` (literal inteiro)
3. Pela regra de adição: `Γ ⊢ 5 + 3 : int`

**Expressão:** `(5.0 3 +)`

Aplicação:
1. `Γ ⊢ 5.0 : float` (literal real)
2. `Γ ⊢ 3 : int` (literal inteiro)
3. Pela regra de promoção: `Γ ⊢ 5.0 + 3 : float`

---

## 7. Divisão de Tarefas (até 4 alunos)

### 7.1 Aluno 1: Gramática de Atributos e Tabela de Símbolos

#### Responsabilidades
- Implementar `definirGramaticaAtributos()`
- Definir atributos (sintetizados e herdados) para cada símbolo
- Documentar gramática completa em EBNF
- Criar estrutura da Tabela de Símbolos

#### Tarefas Específicas
- Regras de verificação de tipos para operadores aritméticos
- Regras para validação de escopo e uso de memórias (MEM)
- Ações semânticas para estruturas de controle
- Implementar conversão de truthiness para operadores lógicos e condições
- Funções auxiliares: `inicializarTabelaSimbolos()`, `adicionarSimbolo()`, `buscarSimbolo()`

#### Interface
- **Entrada:** Nenhuma (gramática fixa)
- **Saída:** Gramática de atributos + Tabela de Símbolos inicializada
- **Fornece para:** `analisarSemantica()`

### 7.2 Aluno 2: Análise Semântica e Verificação de Tipos

#### Responsabilidades
- Implementar `analisarSemantica(arvoreSintatica, gramaticaAtributos, tabelaSimbolos)`
- Percorrer AST
- Aplicar regras semânticas
- Detectar erros de tipo
- Implementar coerção de tipos (int → real)

#### Formato de Mensagens de Erro
```
ERRO SEMÂNTICO [Linha X]: <descrição>
Contexto: <trecho relevante do código>
```

Exemplo:
```
ERRO SEMÂNTICO [Linha 5]: Memória 'CONTADOR' utilizada sem inicialização
Contexto: (CONTADOR)
```

#### Tarefas Específicas
- Algoritmo de percurso da árvore (pós-ordem)
- Validar compatibilidade de tipos
- Verificar expoente da potenciação é inteiro
- Garantir operandos de `/` e `%` são inteiros
- Criar funções de teste de tipos

#### Interface
- **Entrada:** AST (Fase 2) + gramática de atributos + Tabela de Símbolos
- **Saída:** AST com anotações de tipo OU erro semântico
- **Fornece para:** `gerarArvoreAtribuida()`

### 7.3 Aluno 3: Análise de Memória e Estruturas de Controle

#### Responsabilidades
- Implementar `analisarSemanticaMemoria(arvoreSintatica, tabelaSimbolos)`
- Implementar `analisarSemanticaControle(arvoreSintatica, tabelaSimbolos)`
- Validar uso de memórias
- Validar estruturas de controle
- Lógica de escopo

#### Tarefas Específicas
- Popular Tabela de Símbolos com informações de inicialização
- Verificar `(MEM)` não usado antes de `(V MEM)`
- Validar N em `(N RES)` é inteiro não negativo e aponta para expressão válida
- Verificar condições em estruturas são expressões válidas
- Validar escopo em estruturas aninhadas
- Criar testes com erros semânticos de memória e controle

#### Interface
- **Entrada:** AST + Tabela de Símbolos
- **Saída:** Lista de erros semânticos + Tabela atualizada
- **Chamada:** Sequencial após `analisarSemantica()` do Aluno 2
- **Colaboração:** Recebe árvore anotada com tipos, complementa com validações

### 7.4 Aluno 4: Geração de AST Atribuída e Integração

#### Responsabilidades
- Implementar `gerarArvoreAtribuida(arvoreAnotada)`
- Implementar `main()` gerenciando execução sequencial
- Gerar relatórios em markdown
- Coordenar integração de todos os módulos

#### Tarefas Específicas
- Transformar árvore anotada em estrutura final (atribuída)
- Impressão da árvore (texto/JSON)
- Salvar árvore e relatórios
- Implementar `main()` chamando Fases 1, 2, 3 em sequência
- Testar sistema completo

#### Interface
- **Entrada:** AST anotada pela análise semântica
- **Saída:** AST atribuída + arquivos de relatório
- **Gerencia:** Execução completa via linha de comando

---

## 8. Passos de Integração

1. Utilizar sistema integrado Fases 1 e 2 como base
2. Inserir `definirGramaticaAtributos()` + Tabela de Símbolos (Aluno 1)
3. Integrar `analisarSemantica()` (Alunos 2 e 3)
4. Integrar `gerarArvoreAtribuida()` + atualizar `main()` (Aluno 4)
5. Realizar testes completos

**Interfaces:** Concordar formatos de dados (AST, Tabela de Símbolos, árvore atribuída)
**Depuração:** Testar cada módulo isoladamente antes da integração

---

## 9. Arquivos de Teste

### Requisitos Mínimos

**Quantidade:** Mínimo 3 arquivos, cada um com ≥10 linhas

**Cada arquivo deve incluir:**
- ✅ Todas as operações: `+`, `-`, `*`, `|`, `/`, `%`, `^`
- ✅ Comandos especiais: `(N RES)`, `(V MEM)`, `(MEM)`
- ✅ Pelo menos 1 laço de repetição
- ✅ Pelo menos 1 tomada de decisão
- ✅ Literais inteiros, reais e uso de memórias
- ✅ Casos com erros semânticos (para validar tratamento)

**Localização:** Mesmo diretório do código-fonte
**Execução:** `./compilar teste1.txt`

**⚠️ NÃO é preciso criar testes automatizados**, mas incluir no README as rotinas de teste usadas.

---

## 10. Repositório GitHub

### Estrutura Obrigatória

```
RA3_1/
├── compilar.py (ou .c, .cpp)              # Código-fonte principal
├── src/                                    # Módulos
│   ├── RA1/                               # Fase 1 (reuso)
│   ├── RA2/                               # Fase 2 (reuso)
│   └── RA3/                               # Fase 3 (novo)
├── inputs/                                 # Arquivos de teste
│   ├── teste1.txt
│   ├── teste2.txt
│   └── teste3.txt
├── outputs/                                # Arquivos gerados
│   ├── gramatica_atributos.md
│   ├── arvore_atribuida.md (ou .json)
│   ├── julgamento_tipos.md
│   └── erros_semanticos.md
├── docs/                                   # Documentação
└── README.md                               # Documentação principal
```

### Requisitos do Repositório

- ✅ Nome: `RA3_1` (conforme Canvas)
- ✅ Visibilidade: **Público**
- ✅ Commits claros
- ✅ Contribuições via pull requests
- ✅ Issues encorajadas
- ❌ Usuários FIXOS (sem mudança durante desenvolvimento)
- ❌ NÃO alterar para privado

### Cabeçalho Obrigatório do Código

```python
# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1
```

---

## 11. Entregáveis

### 11.1 Código-Fonte
- ✅ Programa completo (Python, C ou C++)
- ✅ Todas as funções especificadas implementadas

### 11.2 Arquivos de Teste
- ✅ Mínimo 3 arquivos, ≥10 linhas cada
- ✅ Casos válidos e inválidos (léxico, sintático, semântico)
- ✅ Estruturas de controle

### 11.3 Documentação (README.md)
- ✅ Informações institucionais
- ✅ Integrantes em ordem alfabética
- ✅ Instruções de compilação/execução/depuração
- ✅ Sintaxe das estruturas de controle
- ✅ Exemplos de uso

### 11.4 Arquivos Markdown Gerados

**Gerados automaticamente pela execução:**

1. **gramatica_atributos.md** - Gramática de atributos da linguagem
2. **julgamento_tipos.md** - Relatório de julgamento de tipos
3. **erros_semanticos.md** - Relatório de erros semânticos
4. **arvore_atribuida.md** (ou JSON) - AST atribuída de um arquivo de teste

**⚠️ IMPORTANTE:** A AST atribuída deve ser salva em JSON para interoperabilidade com próxima fase.

**Formato JSON mínimo:**
- Tipo do vértice
- Tipo inferido
- Filhos
- Número da linha

### 11.5 Formato de Execução

```bash
./compilar teste1.txt
```

---

## 12. Critérios de Avaliação

### 12.1 Funcionalidades do Analisador (70%)

| Critério | Penalidade |
|----------|------------|
| Implementação correta da verificação de tipos | Base da nota |
| Falha na verificação de inicialização de memória | -20% |
| Falha na validação das estruturas de controle | -20% |
| Cada regra de tipo não verificada (ex: expoente inteiro) | -10% |
| Falha na geração da AST atribuída | -30% |
| Gramática de atributos incompleta/mal documentada | -20% |

### 12.2 Organização e Legibilidade (15%)

- ✅ Código claro, comentado e bem estruturado
- ✅ Comentários seguindo Google C++ Style Guide ou PEP 8
- ✅ README completo com todas as informações
- ✅ Repositório organizado com commits claros e PRs

**⚠️ AVISO:** Participação desequilibrada entre membros = redução da nota (avaliação automática)

### 12.3 Robustez (15%)

- ✅ Tratamento de erros semânticos com mensagens claras (linha + tipo)
- ✅ Testes cobrindo todos os casos (válidos e inválidos)
- ✅ Geração correta de todos os arquivos markdown

---

## 13. Prova de Autoria

### Procedimento

1. **Sorteio:** Um aluno será sorteado via https://frankalcantara.com/sorteio.html
2. **Explicação:** Aluno explica o projeto e responde dúvidas do professor
3. **Pergunta:** Aluno escolhe número de 1 a 10 → pergunta sobre o projeto

### Penalidade

**Falha na resposta ou explicação:** -35% da nota provisória **para todo o grupo**

### ⚠️ IMPORTANTE

**Todos os alunos devem entender o funcionamento completo do projeto.**

O aluno sorteado deve ser capaz de responder **qualquer pergunta sobre qualquer parte do projeto**, mesmo que não tenha implementado aquela parte específica.

---

## 14. Uso de Inteligência Artificial

### ✅ Permitido

- Gerar código repetitivo (boilerplate) e configurações
- Explicar conceitos complexos e documentação
- Depurar mensagens de erro e sugerir correções
- Escrever testes unitários e documentação
- Otimizar e refatorar código existente
- Brainstorming de ideias e arquitetura

### ❌ Proibido

- **Envio às Cegas:** Submeter código IA sem revisão/compreensão → **ANULAÇÃO DO TRABALHO**
- **Contornar Aprendizado:** Pedir IA para construir componente inteiro que você deve aprender
- **Violação de Licenças:** Código que viole políticas acadêmicas

### Princípio Fundamental

> **Você é o arquiteto e o engenheiro; a IA é sua assistente. Você mantém total responsabilidade pelo código que envia.**

Você deve ser capaz de explicar qualquer código do projeto, **linha por linha**.

---

## 15. Avisos Críticos

- ❌ **Plágio resultará na anulação do trabalho**
- ❌ **Trabalhos identificados como cópias terão nota zerada**
- ❌ **Grupos com mais de 4 membros terão trabalho anulado**
- ❌ **Aluno não pode trocar usuário GitHub durante desenvolvimento**
- ❌ **Repositório não pode ser alterado para privado**

---

## 16. Avaliação Automatizada por IA

- Todos os trabalhos serão **pré-avaliados automaticamente** por ferramenta de IA
- Verificação de **originalidade do texto e autoria do código**
- Cumprimento de **todas as regras de entrega e desenvolvimento**
- Resultado = **nota base do trabalho**
- Nota pode ser alterada na **prova de autoria**

---

## Referências

- **Documento original:** [https://frankalcantara.com/lf/fase3.html](https://frankalcantara.com/lf/fase3.html)
- **Texto extraído:** `RA3_Fase3_Analisador_Semantico.txt`
- **Data de extração:** 2025-10-20

---

**Copyright © 2025 Frank de Alcantara**
