#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA3_1


import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Caminhos de saída (relativos à raiz do projeto)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUT_ARVORE_ATRIBUIDA_JSON = OUTPUTS_DIR / "RA3" / "arvore_atribuida.json"
OUT_RELATORIOS_DIR = OUTPUTS_DIR / "RA3" / "relatorios"
ROOT_RELATORIOS_DIR = PROJECT_ROOT / "relatorios"

def gerarArvoreAtribuida(arvoreAnotada: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constrói a árvore sintática abstrata atribuída final a partir da árvore anotada.

    Args:
        arvoreAnotada: Árvore sintática anotada pela análise semântica

    Returns:
        Árvore sintática abstrata atribuída final
    """
    if not arvoreAnotada or 'linhas' not in arvoreAnotada:
        return {'arvore_atribuida': []}

    arvore_atribuida = []

    for linha in arvoreAnotada['linhas']:
        numero_linha = linha.get('numero_linha', 0)
        tipo = linha.get('tipo')

        # Construir a estrutura completa da árvore atribuída para esta linha
        raiz_linha = _construir_no_atribuido(linha, numero_linha)
        arvore_atribuida.append(raiz_linha)

    return {'arvore_atribuida': arvore_atribuida}


def _construir_no_atribuido(no: Dict[str, Any], numero_linha: int) -> Dict[str, Any]:
    """
    Constrói recursivamente um nó da árvore atribuída.

    Args:
        no: Nó da árvore anotada
        numero_linha: Número da linha para referência

    Returns:
        Nó da árvore atribuída com tipo, filhos, etc.
    """
    # Determinar tipo do vértice baseado na estrutura
    tipo_vertice = "LINHA"  # Padrão para nó raiz da linha

    # Se tem operador, é um nó operador
    operador = no.get('operador')
    if operador:
        if operador in ['+', '-', '*', '/', '%', '^', '|']:
            tipo_vertice = "ARITH_OP"
        elif operador in ['>', '<', '>=', '<=', '==', '!=']:
            tipo_vertice = "COMP_OP"
        elif operador in ['&&', '||', '!']:
            tipo_vertice = "LOGIC_OP"
        elif operador in ['IFELSE', 'WHILE', 'FOR']:
            tipo_vertice = "CONTROL_OP"
        elif operador == 'RES':
            tipo_vertice = "RES"
        else:
            tipo_vertice = "OPERADOR_FINAL"

    # Tipo inferido (do resultado da análise semântica)
    tipo_inferido = no.get('tipo')

    # Filhos
    filhos = []

    # Se tem filhos diretos (estrutura de árvore)
    if 'filhos' in no and no['filhos']:
        for filho in no['filhos']:
            filhos.append(_construir_no_atribuido(filho, numero_linha))
    # Se tem elementos (estrutura convertida)
    elif 'elementos' in no:
        for elemento in no['elementos']:
            # Cada elemento pode ser um operando simples ou uma subexpressão LINHA
            if isinstance(elemento, dict):
                if elemento.get('subtipo') == 'LINHA':
                    # É uma subexpressão - criar um nó recursivamente com sua estrutura
                    no_subexpressao = {
                        'numero_linha': numero_linha,
                        'elementos': elemento.get('elementos', []),
                        'operador': elemento.get('operador')
                    }
                    filhos.append(_construir_no_atribuido(no_subexpressao, numero_linha))
                else:
                    # Operando simples
                    no_elemento = {
                        'numero_linha': numero_linha,
                        'tipo': elemento.get('tipo'),
                        'subtipo': elemento.get('subtipo'),
                        'valor': elemento.get('valor')
                    }
                    filhos.append(_construir_no_atribuido(no_elemento, numero_linha))
            else:
                # Elemento não-dicionário (fallback)
                filhos.append(_construir_no_atribuido({'valor': str(elemento)}, numero_linha))

    # Valor se for terminal
    valor = no.get('valor')

    # Construir o nó atribuído
    no_atribuido = {
        'tipo_vertice': tipo_vertice,
        'tipo_inferido': tipo_inferido,
        'numero_linha': numero_linha,
        'filhos': filhos
    }

    if operador:
        no_atribuido['operador'] = operador

    if valor is not None:
        no_atribuido['valor'] = valor

    # Adicionar subtipo se existir (para operandos)
    subtipo = no.get('subtipo')
    if subtipo:
        no_atribuido['subtipo'] = subtipo

    return no_atribuido


def salvarArvoreAtribuida(arvoreAtribuida: Dict[str, Any]) -> None:
    """
    Salva a árvore atribuída em formato JSON.

    Args:
        arvoreAtribuida: Árvore sintática abstrata atribuída
    """
    OUT_ARVORE_ATRIBUIDA_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_ARVORE_ATRIBUIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(arvoreAtribuida, f, indent=2, ensure_ascii=False)


def gerarRelatoriosMarkdown(arvoreAtribuida: Dict[str, Any], errosSemanticos: Optional[List[str]],
                          tabelaSimbolos, caminhoSaida: Path) -> None:
    """
    Gera os relatórios em markdown: árvore atribuída, julgamento de tipos e erros semânticos.

    Args:
        arvoreAtribuida: Árvore sintática abstrata atribuída
        errosSemanticos: Lista de erros semânticos (ou None se não há erros)
        tabelaSimbolos: Tabela de símbolos da análise semântica
        caminhoSaida: Diretório onde salvar os relatórios
    """
    # Gerar relatórios no diretório especificado
    _gerar_relatorios_em_diretorio(arvoreAtribuida, errosSemanticos, tabelaSimbolos, caminhoSaida)

    # Também gerar na pasta raiz do projeto
    _gerar_relatorios_em_diretorio(arvoreAtribuida, errosSemanticos, tabelaSimbolos, ROOT_RELATORIOS_DIR)


def _gerar_relatorios_em_diretorio(arvoreAtribuida: Dict[str, Any], errosSemanticos: Optional[List[str]],
                                 tabelaSimbolos, caminhoSaida: Path) -> None:
    """
    Gera os relatórios em um diretório específico.
    """
    caminhoSaida.mkdir(parents=True, exist_ok=True)

    # 1. Relatório da Árvore Atribuída
    _gerar_relatorio_arvore_atribuida(arvoreAtribuida, caminhoSaida / "arvore_atribuida.md")

    # 2. Relatório de Julgamento de Tipos
    _gerar_relatorio_julgamento_tipos(arvoreAtribuida, caminhoSaida / "julgamento_tipos.md")

    # 3. Relatório de Erros Semânticos
    _gerar_relatorio_erros_sematicos(errosSemanticos, caminhoSaida / "erros_sematicos.md")

    # 4. Relatório da Tabela de Símbolos
    _gerar_relatorio_tabela_simbolos(tabelaSimbolos, caminhoSaida / "tabela_simbolos.md")


def _gerar_relatorio_arvore_atribuida(arvoreAtribuida: Dict[str, Any], caminhoArquivo: Path) -> None:
    """Gera relatório da árvore atribuída em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Árvore Sintática Abstrata Atribuída\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        arvore = arvoreAtribuida.get('arvore_atribuida', [])

        f.write("## Resumo\n\n")
        f.write(f"- **Total de linhas:** {len(arvore)}\n")
        f.write(f"- **Linhas com tipo definido:** {sum(1 for entrada in arvore if entrada.get('tipo_inferido') is not None)}\n")
        f.write(f"- **Linhas sem tipo definido:** {sum(1 for entrada in arvore if entrada.get('tipo_inferido') is None)}\n\n")

        # Detalhes da árvore por linha
        f.write("## Detalhes da Árvore Atribuída por Linha\n\n")

        for i, raiz_linha in enumerate(arvore, 1):
            f.write(f"### Linha {raiz_linha.get('numero_linha', i)}\n\n")
            f.write(f"**Tipo Resultado:** `{raiz_linha.get('tipo_inferido', 'N/A')}`\n\n")
            f.write("**Estrutura da Árvore:**\n\n")
            f.write("```\n")
            f.write(_formatar_arvore(raiz_linha, 0))
            f.write("```\n\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


def _formatar_arvore(no: Dict[str, Any], nivel: int) -> str:
    """Formata um nó da árvore para exibição textual."""
    indent = "  " * nivel
    tipo_vertice = no.get('tipo_vertice', 'UNKNOWN')
    tipo_inferido = no.get('tipo_inferido')
    operador = no.get('operador', '')
    valor = no.get('valor', '')
    subtipo = no.get('subtipo', '')

    linha = f"{indent}{tipo_vertice}"
    if operador:
        linha += f" ({operador})"
    if tipo_inferido:
        linha += f" : {tipo_inferido}"
    if valor:
        linha += f" [{valor}]"
    if subtipo:
        linha += f" {{{subtipo}}}"

    linha += "\n"

    for filho in no.get('filhos', []):
        linha += _formatar_arvore(filho, nivel + 1)

    return linha


def _gerar_relatorio_julgamento_tipos(arvoreAtribuida: Dict[str, Any], caminhoArquivo: Path) -> None:
    """Gera relatório de julgamento de tipos em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Julgamento de Tipos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        arvore = arvoreAtribuida.get('arvore_atribuida', [])

        f.write("## Análise de Tipos por Linha\n\n")
        f.write("| Linha | Tipo Inferido | Status |\n")
        f.write("|-------|---------------|--------|\n")

        for raiz_linha in arvore:
            linha = raiz_linha.get('numero_linha', '')
            tipo = raiz_linha.get('tipo_inferido')
            status = "  Tipo definido" if tipo is not None else "  Tipo indefinido"

            f.write(f"| {linha} | `{tipo if tipo else 'N/A'}` | {status} |\n")

        # Resumo de tipos
        tipos_encontrados = set()
        for raiz_linha in arvore:
            tipo = raiz_linha.get('tipo_inferido')
            if tipo:
                tipos_encontrados.add(str(tipo))

        f.write("\n## Resumo de Tipos\n\n")
        f.write("### Estatísticas\n")
        f.write(f"- **Total de expressões:** {len(arvore)}\n")
        f.write(f"- **Com tipo definido:** {sum(1 for raiz_linha in arvore if raiz_linha.get('tipo_inferido') is not None)}\n")
        f.write(f"- **Sem tipo definido:** {sum(1 for raiz_linha in arvore if raiz_linha.get('tipo_inferido') is None)}\n\n")

        if tipos_encontrados:
            f.write("### Tipos Utilizados\n")
            for tipo in sorted(tipos_encontrados):
                f.write(f"- `{tipo}`\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


def _gerar_relatorio_erros_sematicos(erros: Optional[List[str]], caminhoArquivo: Path) -> None:
    """Gera relatório de erros semânticos em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Erros Semânticos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not erros:
            f.write("##  Nenhum Erro Encontrado\n\n")
            f.write("A análise semântica foi concluída com sucesso sem nenhum erro detectado.\n")
        else:
            f.write(f"##  Erros Encontrados ({len(erros)})\n\n")

            for i, erro in enumerate(erros, 1):
                f.write(f"### Erro {i}\n")
                # Se erro é um dicionário, extrair a mensagem
                if isinstance(erro, dict):
                    mensagem_erro = erro.get('erro', str(erro))
                else:
                    mensagem_erro = str(erro)
                f.write(f"```\n{mensagem_erro}\n```\n\n")

            f.write("## Resumo\n\n")
            f.write(f"- **Total de erros:** {len(erros)}\n")
            f.write("- **Status:** Análise semântica falhou\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


def _gerar_relatorio_tabela_simbolos(tabela, caminhoArquivo: Path) -> None:
    """Gera relatório da tabela de símbolos em markdown."""
    with open(caminhoArquivo, 'w', encoding='utf-8') as f:
        f.write("# Tabela de Símbolos\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        try:
            simbolos = tabela.listar_simbolos() if hasattr(tabela, 'listar_simbolos') else []
        except:
            simbolos = []

        if not simbolos:
            f.write("##   Tabela Vazia\n\n")
            f.write("Nenhum símbolo foi registrado durante a análise.\n")
        else:
            f.write(f"## Símbolos Registrados ({len(simbolos)})\n\n")
            f.write("| Nome | Tipo | Inicializado | Linha | Usos |\n")
            f.write("|------|------|--------------|-------|------|\n")

            for simbolo in simbolos:
                nome = simbolo.nome
                tipo = simbolo.tipo
                inicializado = "  Sim" if simbolo.inicializada else "  Não"
                linha = simbolo.linha_declaracao if simbolo.linha_declaracao else 'N/A'
                usos = tabela.obter_numero_usos(nome) if hasattr(tabela, 'obter_numero_usos') else 0

                f.write(f"| `{nome}` | `{tipo}` | {inicializado} | {linha} | {usos} |\n")

        f.write("\n---\n*Relatório gerado automaticamente pelo Compilador RA3_1*")


# ============================================================================
# FUNÇÃO DE INTEGRAÇÃO - CHAMADA PELO COMPILAR.PY
# ============================================================================

def executar_geracao_arvore_atribuida(resultado_semantico: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal chamada pelo compilar.py para gerar a árvore atribuída.

    Args:
        resultado_semantico: Resultado da análise semântica completa

    Returns:
        Dicionário com árvore atribuída e informações dos relatórios gerados
    """
    try:
        # Extrair dados do resultado semântico
        arvore_anotada = resultado_semantico.get('arvore_anotada', {})
        erros_sematicos = resultado_semantico.get('erros', [])
        tabela_simbolos = resultado_semantico.get('tabela_simbolos')

        # Gerar árvore atribuída
        arvore_atribuida = gerarArvoreAtribuida(arvore_anotada)

        # Salvar árvore atribuída
        salvarArvoreAtribuida(arvore_atribuida)

        # Gerar relatórios
        gerarRelatoriosMarkdown(
            arvore_atribuida,
            erros_sematicos,
            tabela_simbolos,
            OUT_RELATORIOS_DIR
        )

        return {
            'sucesso': True,
            'arvore_atribuida': arvore_atribuida,
            'relatorios_gerados': [
                str(OUT_RELATORIOS_DIR / "arvore_atribuida.md"),
                str(OUT_RELATORIOS_DIR / "julgamento_tipos.md"),
                str(OUT_RELATORIOS_DIR / "erros_sematicos.md"),
                str(OUT_RELATORIOS_DIR / "tabela_simbolos.md"),
                str(ROOT_RELATORIOS_DIR / "arvore_atribuida.md"),
                str(ROOT_RELATORIOS_DIR / "julgamento_tipos.md"),
                str(ROOT_RELATORIOS_DIR / "erros_sematicos.md"),
                str(ROOT_RELATORIOS_DIR / "tabela_simbolos.md")
            ],
            'arquivo_arvore_json': str(OUT_ARVORE_ATRIBUIDA_JSON)
        }

    except Exception as e:
        return {
            'sucesso': False,
            'erro': f"Erro na geração da árvore atribuída: {str(e)}",
            'arvore_atribuida': None,
            'relatorios_gerados': []
        }