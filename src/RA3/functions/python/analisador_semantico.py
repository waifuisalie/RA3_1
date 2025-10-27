#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1

from typing import Dict, Any, Optional, List, Tuple
from src.RA3.functions.python.analisador_tipos import analisarSemantica as analisarSemanticaTipos, ErroSemantico
from src.RA3.functions.python.analisador_memoria_controle import analisarSemanticaMemoria, analisarSemanticaControle
from src.RA3.functions.python.tabela_simbolos import TabelaSimbolos


def _converter_arvore_json_para_analisador(arvore_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte a árvore sintática JSON exportada pelo parser RA2
    para o formato esperado pelo analisador semântico.
    
    Formato JSON (RA2):
    {
      "linhas": [
        {
          "numero_linha": 1,
          "arvore": {...},
          "tokens": [...]
        }
      ]
    }
    
    Formato esperado pelo analisador:
    {
      "linhas": [
        {
          "numero_linha": 1,
          "filhos": [
            {
              "elementos": [...],
              "operador": "..."
            }
          ]
        }
      ]
    }
    """
    linhas_convertidas = []
    
    for linha_json in arvore_json.get('linhas', []):
        numero_linha = linha_json.get('numero_linha')
        arvore = linha_json.get('arvore')
        tokens = linha_json.get('tokens', [])
        
        if arvore is None:
            continue  # Pular linhas com erro sintático
            
        # Extrair elementos e operador da árvore sintática usando tokens
        elementos, operador = _extrair_elementos_e_operador(arvore, tokens)
        
        linha_convertida = {
            'numero_linha': numero_linha,
            'filhos': [{
                'elementos': elementos,
                'operador': operador
            }]
        }
        linhas_convertidas.append(linha_convertida)
    
    return {'linhas': linhas_convertidas}


def _extrair_elementos_e_operador(arvore: Dict[str, Any], tokens: List[str]) -> Tuple[List[Dict[str, Any]], str]:
    """
    Extrai elementos (operandos) e operador de uma linha da árvore sintática.
    
    Args:
        arvore: Árvore sintática JSON
        tokens: Lista de tokens da linha (como strings)
        
    Returns:
        Tupla (elementos, operador) onde:
        - elementos: lista de dicionários com 'subtipo' e 'valor'
        - operador: string representando o operador ou '' se não houver
    """
    elementos = []
    operador = ""
    
    # Operadores conhecidos (aritméticos, comparação, lógicos, controle)
    operadores_conhecidos = [
        '+', '-', '*', '/', '%', '^', '|',  # aritméticos
        '>', '<', '>=', '<=', '==', '!=',   # comparação  
        '&&', '||', '!',                   # lógicos
        'IFELSE', 'WHILE', 'FOR',          # controle
        'RES'                              # especial
    ]
    
    # Filtrar tokens relevantes (remover parênteses)
    tokens_relevantes = [t for t in tokens if t not in ['(', ')']]
    
    # Percorrer tokens para identificar operadores e operandos
    for token in tokens_relevantes:
        if token in operadores_conhecidos:
            # É um operador
            if operador == "":
                operador = token
            # Se já havia operador, pode ser erro, mas vamos aceitar o primeiro
        else:
            # É um operando - tentar identificar tipo
            try:
                # Tentar converter para número
                float(token)
                elementos.append({
                    'subtipo': 'numero_real',
                    'valor': token
                })
            except ValueError:
                # Não é número, deve ser variável
                elementos.append({
                    'subtipo': 'variavel', 
                    'valor': token
                })
    
    return elementos, operador


def _criar_seqs_map(arvore_convertida: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    """
    Cria o seqs_map necessário para as funções de análise de memória e controle.
    
    Args:
        arvore_convertida: Árvore no formato convertido pelo analisador
        
    Returns:
        Dicionário mapeando número da linha para {'operador': str, 'elementos': List[Dict]}
    """
    seqs_map = {}
    
    for linha in arvore_convertida.get('linhas', []):
        num_linha = linha.get('numero_linha')
        filhos = linha.get('filhos', [])
        
        if filhos:
            seq = filhos[0]  # Primeiro filho contém elementos e operador
            seqs_map[num_linha] = {
                'operador': seq.get('operador'),
                'elementos': seq.get('elementos', [])
            }
        else:
            seqs_map[num_linha] = {
                'operador': None,
                'elementos': []
            }
    
    return seqs_map


# Função principal delega para a implementação em analisador_tipos.py
# analisarSemantica está implementada em analisador_tipos.py


def analisarSemanticaDaJsonRA2(json_data: Dict[str, Any]) -> Optional[List[str]]:
    """
    Função principal que coordena a análise semântica completa:
    1. Análise de tipos (analisarSemantica)
    2. Análise de memória (analisarSemanticaMemoria)
    3. Análise de controle (analisarSemanticaControle)
    
    Retorna:
        None se não há erros, ou uma lista de strings de erro no formato esperado.
    """
    try:
        # Converter árvore JSON para formato esperado pelo analisador
        arvore_convertida = _converter_arvore_json_para_analisador(json_data)
        
        # Executar análise de tipos
        resultado_tipos = analisarSemanticaTipos(arvore_convertida)
        erros_formatados = []
        
        if isinstance(resultado_tipos, dict):
            if not resultado_tipos.get('sucesso', False):
                # Retornar lista de erros já formatados
                if resultado_tipos.get('erros'):
                    for erro in resultado_tipos['erros']:
                        if isinstance(erro, dict):
                            # O erro já vem formatado da função analisarSemantica
                            erros_formatados.append(erro.get('erro', str(erro)))
                        else:
                            erros_formatados.append(str(erro))
                return erros_formatados if erros_formatados else None
            # Usar a árvore anotada para as próximas análises
            arvore_anotada = resultado_tipos.get('arvore_anotada', arvore_convertida)
            tabela = resultado_tipos.get('tabela_simbolos')
        else:
            # Se retornou string, é um erro
            if resultado_tipos:
                return [resultado_tipos]
            arvore_anotada = arvore_convertida
            tabela = TabelaSimbolos()
        
        # Executar análise de memória
        erros_memoria = analisarSemanticaMemoria(arvore_anotada, _criar_seqs_map(arvore_convertida), tabela)
        if erros_memoria:
            erros_formatados.extend([erro['erro'] for erro in erros_memoria])
        
        # Executar análise de controle
        erros_controle = analisarSemanticaControle(arvore_anotada, _criar_seqs_map(arvore_convertida), tabela)
        if erros_controle:
            erros_formatados.extend([erro['erro'] for erro in erros_controle])
        
        # Se há erros de memória ou controle, retornar todos os erros
        if erros_formatados:
            return erros_formatados
        
        return None  # Sucesso
        
    except Exception as e:
        return [f"ERRO INTERNO: {str(e)}"]