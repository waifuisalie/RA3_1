#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import os
import json
from .configuracaoGramatica import MAPEAMENTO_TOKENS

class NoArvore:
    def __init__(self, label):
        self.label = label
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def desenhar_ascii(self, prefixo='', eh_ultimo=True):
        conector = '└── ' if eh_ultimo else '├── '
        resultado = prefixo + conector + self.label + '\n'
        prefixo_prox = prefixo + ('    ' if eh_ultimo else '│   ')
        for i, filho in enumerate(self.filhos):
            ultimo = i == len(self.filhos) - 1
            resultado += filho.desenhar_ascii(prefixo_prox, ultimo)
        return resultado

def no_para_dict(no: NoArvore) -> dict:
    """Converte NoArvore para dicionário (formato JSON) recursivamente"""
    return {
        "label": no.label,
        "filhos": [no_para_dict(filho) for filho in no.filhos]
    }

def gerarArvore(derivacao):
    producoes = [linha.split('→') for linha in derivacao]
    producoes = [(lhs.strip(), rhs.strip().split()) for lhs, rhs in producoes]

    index = [0]  # índice mutável

    def construir_no(simbolo_esperado):
        if index[0] >= len(producoes):
            # Converte nome do token para valor real se disponível
            valor_real = MAPEAMENTO_TOKENS.get(simbolo_esperado, simbolo_esperado)
            return NoArvore(valor_real)

        lhs, rhs = producoes[index[0]]
        if lhs != simbolo_esperado:
            # Converte nome do token para valor real se disponível
            valor_real = MAPEAMENTO_TOKENS.get(simbolo_esperado, simbolo_esperado)
            return NoArvore(valor_real)

        index[0] += 1
        no = NoArvore(lhs)
        for simbolo in rhs:
            if simbolo != 'ε':
                filho = construir_no(simbolo)
                no.adicionar_filho(filho)
            else:
                no.adicionar_filho(NoArvore('ε'))
        return no

    return construir_no('PROGRAM')

def exportar_arvore_ascii(arvore, nome_arquivo='arvore_output.txt'):
    conteudo = arvore.label + '\n'
    for i, filho in enumerate(arvore.filhos):
        eh_ultimo = i == len(arvore.filhos) - 1
        conteudo += filho.desenhar_ascii('', eh_ultimo)

    # Exportar para a raiz
    #with open(nome_arquivo, 'w', encoding='utf-8') as f:
    #    f.write(conteudo)

    # Exportar para /outputs/RA2/
    output_dir = os.path.join(os.getcwd(), 'outputs', 'RA2')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, nome_arquivo)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"Árvore exportada para: {nome_arquivo} e outputs/RA2/{nome_arquivo}")

def gerar_e_salvar_todas_arvores(derivacoes_por_linha, nome_arquivo='arvore_output.txt'):
    
    conteudo_completo = "=== ÁRVORES SINTÁTICAS GERADAS ===\n\n"
    
    arvores_geradas = 0
    
    for i, derivacao in enumerate(derivacoes_por_linha):
        conteudo_completo += f"LINHA {i+1}:\n"
        conteudo_completo += "=" * 50 + "\n"
        
        if derivacao and len(derivacao) > 0:
            try:
                # Gera a árvore para esta derivação
                arvore = gerarArvore(derivacao)
                
                # Adiciona representação ASCII da árvore
                conteudo_completo += arvore.label + '\n'
                for j, filho in enumerate(arvore.filhos):
                    eh_ultimo = j == len(arvore.filhos) - 1
                    conteudo_completo += filho.desenhar_ascii('', eh_ultimo)
                
                arvores_geradas += 1
            except Exception as e:
                conteudo_completo += f"ERRO ao gerar árvore: {e}\n"
        else:
            conteudo_completo += "ERRO SINTÁTICO - Árvore não gerada\n"
        
        conteudo_completo += "\n" + "=" * 50 + "\n\n"
    
    # Salva na raiz
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo_completo)
        
        # Salva em outputs/RA2/
        output_dir = os.path.join(os.getcwd(), 'outputs', 'RA2')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, nome_arquivo)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(conteudo_completo)
        
        print(f"  {arvores_geradas} árvore(s) sintática(s) salva(s) em:")
        print(f"   - {nome_arquivo}")
        print(f"   - outputs/RA2/{nome_arquivo}")
        
        return True
        
    except Exception as e:
        print(f"  Erro ao salvar árvores: {e}")
        return False

def exportar_arvores_json(derivacoes_por_linha, tokens_por_linha, linhas_originais, nome_arquivo='arvore_sintatica.json'):
    """
    Exporta árvores sintáticas para JSON (formato navegável para RA3)

    Args:
        derivacoes_por_linha: Lista de derivações (uma por linha)
        tokens_por_linha: Lista de tokens (uma por linha)
        linhas_originais: Linhas de código originais
        nome_arquivo: Nome do arquivo JSON (padrão: 'arvore_sintatica.json')

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        estrutura_json = {
            "tipo": "PROGRAM",
            "linhas": []
        }

        for i, derivacao in enumerate(derivacoes_por_linha):
            numero_linha = i + 1

            if derivacao and len(derivacao) > 0:
                # Gera árvore para esta linha
                arvore = gerarArvore(derivacao)
                arvore_dict = no_para_dict(arvore)

                linha_json = {
                    "numero_linha": numero_linha,
                    "expressao_original": linhas_originais[i] if i < len(linhas_originais) else "",
                    "tokens": tokens_por_linha[i] if i < len(tokens_por_linha) else [],
                    "arvore": arvore_dict,
                    "derivacao_passos": len(derivacao),
                    "sucesso": True
                }
            else:
                # Linha com erro sintático
                linha_json = {
                    "numero_linha": numero_linha,
                    "expressao_original": linhas_originais[i] if i < len(linhas_originais) else "",
                    "tokens": tokens_por_linha[i] if i < len(tokens_por_linha) else [],
                    "arvore": None,
                    "erro": "Erro sintático - parsing falhou",
                    "sucesso": False
                }

            estrutura_json["linhas"].append(linha_json)

        # Adiciona estatísticas
        linhas_validas = sum(1 for linha in estrutura_json["linhas"] if linha["sucesso"])
        estrutura_json["estatisticas"] = {
            "total_linhas": len(derivacoes_por_linha),
            "linhas_validas": linhas_validas,
            "linhas_com_erro": len(derivacoes_por_linha) - linhas_validas
        }

        # Salvar JSON em outputs/RA2/
        output_dir = os.path.join(os.getcwd(), 'outputs', 'RA2')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, nome_arquivo)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(estrutura_json, f, indent=2, ensure_ascii=False)

        print(f"\n--- EXPORTAÇÃO JSON ---")
        print(f"  Árvore JSON salva: outputs/RA2/{nome_arquivo}")
        print(f"  - Linhas válidas: {linhas_validas}")
        print(f"  - Linhas com erro: {len(derivacoes_por_linha) - linhas_validas}")

        return True

    except Exception as e:
        print(f"  Erro ao exportar JSON: {e}")
        return False
