#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from typing import Union, Set, Dict, Any

# ============================================================================
# CONSTANTES DE CONFIGURAÇÃO DA GRAMÁTICA E SÍMBOLOS CANÔNICOS
# ============================================================================

# Símbolo inicial da gramática
SIMBOLO_INICIAL = 'PROGRAM'

# Símbolo canônico para Epsilon (produção vazia), em minúsculas como um terminal
EPSILON_SYMBOL = 'epsilon'

# Mapeamento dos tokens teóricos (agora em lowercase) para tokens reais do projeto.
# Estes são os terminais que o lexer/scanner reconhece.
MAPEAMENTO_TOKENS = {
    'numero_real': 'NUMBER',
    'variavel': 'IDENTIFIER',
    'abre_parenteses': '(',
    'fecha_parenteses': ')',
    'soma': '+',
    'subtracao': '-',
    'multiplicacao': '*',
    'divisao_inteira': '/',
    'divisao_real': '|',
    'resto': '%',
    'potencia': '^',
    'menor': '<',
    'maior': '>',
    'igual': '==',
    'menor_igual': '<=',
    'maior_igual': '>=',
    'diferente': '!=',
    'and': '&&',
    'or': '||',
    'not': '!',
    'for': 'FOR',
    'while': 'WHILE',
    'ifelse': 'IFELSE',
    'res': 'RES',
    EPSILON_SYMBOL: '' # Epsilon é mapeado para uma string vazia
}

# Definição da gramática.
# Não-Terminais são em MAIÚSCULAS.
# Terminais teóricos são em minúsculas.
GRAMATICA_RPN = {
    # Programa principal
    'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
    'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], [EPSILON_SYMBOL]],
    
    # Estrutura de linha
    'LINHA': [['abre_parenteses', 'CONTENT', 'fecha_parenteses']],
    
    # Conteúdo principal - diferenciado deterministicamente
    'CONTENT': [
        ['numero_real', 'AFTER_NUM'],
        ['variavel', 'AFTER_VAR'],
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'AFTER_EXPR'],
        ['for', 'FOR_STRUCT'],
        ['while', 'WHILE_STRUCT'],
        ['ifelse', 'IFELSE_STRUCT']
    ],
    
    # AFTER_NUM - processar após número inicial
    'AFTER_NUM': [
        ['numero_real', 'OPERATOR'],
        ['variavel', 'AFTER_VAR_OP'],
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'OPERATOR'],
        ['not'],
        ['res'],
        [EPSILON_SYMBOL]
    ],
    
    'AFTER_VAR_OP': [['OPERATOR'], [EPSILON_SYMBOL]],
    
    # AFTER_VAR - processar após variável inicial  
    'AFTER_VAR': [
        ['numero_real', 'OPERATOR'],
        ['variavel', 'AFTER_VAR_OP'],
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'OPERATOR'],
        ['not'],
        [EPSILON_SYMBOL]
    ],
    
    # AFTER_EXPR - processar após expressão em parênteses
    'AFTER_EXPR': [
        ['numero_real', 'OPERATOR'],
        ['variavel', 'AFTER_VAR_OP'],
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'AFTER_EXPR'],
        ['OPERATOR', 'EXPR_CHAIN'],
        [EPSILON_SYMBOL]
    ],
    
    # EXPR_CHAIN - para operadores entre expressões
    'EXPR_CHAIN': [
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'AFTER_EXPR'],
        [EPSILON_SYMBOL]
    ],
    
    # EXPR - expressões internas
    'EXPR': [
        ['numero_real', 'AFTER_NUM'],
        ['variavel', 'AFTER_VAR'],
        ['abre_parenteses', 'EXPR', 'fecha_parenteses', 'AFTER_EXPR'],
        ['ifelse', 'IFELSE_STRUCT']
    ],
    
    # Hierarquia de operadores
    'OPERATOR': [['ARITH_OP'], ['COMP_OP'], ['LOGIC_OP']],
    'ARITH_OP': [['soma'], ['subtracao'], ['multiplicacao'], ['divisao_inteira'], ['divisao_real'], ['resto'], ['potencia']],
    'COMP_OP': [['menor'], ['maior'], ['igual'], ['menor_igual'], ['maior_igual'], ['diferente']],
    'LOGIC_OP': [['and'], ['or'], ['not']],
    
    # Estruturas de controle
    'FOR_STRUCT': [['abre_parenteses', 'numero_real', 'fecha_parenteses', 
                   'abre_parenteses', 'numero_real', 'fecha_parenteses', 
                   'abre_parenteses', 'numero_real', 'fecha_parenteses', 'LINHA']],
    'WHILE_STRUCT': [['abre_parenteses', 'EXPR', 'fecha_parenteses', 'LINHA']],
    'IFELSE_STRUCT': [['abre_parenteses', 'EXPR', 'fecha_parenteses', 'LINHA', 'LINHA']]
}

# ============================================================================
# FUNÇÕES DE IDENTIFICAÇÃO DE SÍMBOLOS
# ============================================================================

def is_non_terminal(symbol: str) -> bool:
    """
    Determines if a symbol is a non-terminal based on casing (ALL CAPS).

    Args:
        symbol: The grammar symbol string to check.

    Returns:
        True if the symbol is an uppercase string, False otherwise.
    """
    return isinstance(symbol, str) and symbol.isupper()

def is_terminal(symbol: str) -> bool:
    """
    Determines if a symbol is a terminal. A terminal is any symbol that is not
    a non-terminal (i.e., not an all-caps string).

    Args:
        symbol: The grammar symbol string to check.

    Returns:
        True if the symbol is a terminal, False otherwise.
    """
    return not is_non_terminal(symbol)


# ============================================================================
# FUNÇÕES DE MAPEAMENTO - Centralizadas para evitar duplicação
# ============================================================================

def mapear_gramatica_para_tokens_reais(gramatica_teorica: dict) -> dict:
    """
    Converte a gramática com símbolos teóricos para uma gramática com os
    tokens reais reconhecidos pelo lexer.

    Args:
        gramatica_teorica: Dicionário da gramática com terminais em minúsculas.

    Returns:
        Uma nova gramática com os terminais mapeados para suas representações reais.
    """
    gramatica_real = {}
    for nt, producoes in gramatica_teorica.items():
        gramatica_real[nt] = []
        for producao in producoes:
            producao_real = []
            for simbolo in producao:
                # Se o símbolo é um terminal teórico, mapeia para o real.
                if simbolo in MAPEAMENTO_TOKENS:
                    producao_real.append(MAPEAMENTO_TOKENS[simbolo])
                else:
                    # Senão, é um não-terminal (MAIÚSCULAS) e é mantido.
                    producao_real.append(simbolo)
            gramatica_real[nt].append(producao_real)
    return gramatica_real

def mapear_tokens_reais_para_teoricos(conjunto_ou_dict: Union[Set[str], Dict[str, Any]]) -> Union[Set[str], Dict[str, Any]]:
    """
    Converte tokens reais de volta para teóricos para exibição (e.g., FIRST/FOLLOW/Tabela).

    Args:
        conjunto_ou_dict: O conjunto de terminais ou o dicionário da tabela de parsing.

    Returns:
        Uma nova estrutura com os tokens convertidos para suas representações teóricas.
    """
    mapeamento_inverso = {v: k for k, v in MAPEAMENTO_TOKENS.items()}
    
    if isinstance(conjunto_ou_dict, set):
        return {mapeamento_inverso.get(token, token) for token in conjunto_ou_dict}
    
    if isinstance(conjunto_ou_dict, dict):
        resultado = {}
        for nt, terminais_dict in conjunto_ou_dict.items():
            resultado[nt] = {}
            for terminal, producao in terminais_dict.items():
                terminal_teorico = mapeamento_inverso.get(terminal, terminal)
                if producao is not None:
                    # Mapear símbolos na produção de volta para teóricos
                    producao_teorica = [mapeamento_inverso.get(s, s) for s in producao]
                    resultado[nt][terminal_teorico] = producao_teorica
                else:
                    resultado[nt][terminal_teorico] = None
        return resultado

    return conjunto_ou_dict