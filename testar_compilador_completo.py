#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o compilador completo (compilar.py) com vários arquivos
"""

import sys
import io
import subprocess
from pathlib import Path

# UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent
COMPILAR = ROOT_DIR / "compilar.py"

def executar_teste(arquivo_teste, descricao):
    """Executa um teste e captura resultado"""
    print(f"\n{'='*80}")
    print(f"TESTE: {descricao}")
    print(f"Arquivo: {arquivo_teste}")
    print(f"{'='*80}\n")

    cmd = [sys.executable, str(COMPILAR), str(arquivo_teste)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )

        # Filtrar saída para mostrar apenas o relevante
        linhas = result.stdout.split('\n')

        # Mostrar tokenização
        print("TOKENIZAÇÃO:")
        for linha in linhas:
            if 'tokenizada' in linha.lower() or 'tokens salvos' in linha.lower():
                print(f"  {linha.strip()}")

        # Mostrar análise sintática resumida
        print("\nANÁLISE SINTÁTICA:")
        for linha in linhas:
            if 'Analisando' in linha or 'linhas' in linha.lower():
                print(f"  {linha.strip()}")
                break

        # Mostrar análise semântica
        print("\nANÁLISE SEMÂNTICA:")
        capturar = False
        for linha in linhas:
            if '--- RA3: ANÁLISE SEMÂNTICA ---' in linha:
                capturar = True
            if capturar:
                if linha.strip():
                    print(f"  {linha.strip()}")
                if '---' in linha and 'ÁRVORE' in linha:
                    break

        # Mostrar geração de árvore
        print("\nGERAÇÃO DE ÁRVORE:")
        capturar = False
        for linha in linhas:
            if 'ÁRVORE ATRIBUÍDA' in linha:
                capturar = True
            if capturar and linha.strip():
                print(f"  {linha.strip()}")

        # Mostrar erros se houver
        if 'ERRO' in result.stdout or 'Erro' in result.stdout:
            print("\nERROS DETECTADOS:")
            for linha in linhas:
                if 'ERRO' in linha or 'Erro' in linha:
                    print(f"  {linha.strip()}")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("ERRO: Timeout na execução")
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def main():
    print("="*80)
    print("TESTES DO COMPILADOR COMPLETO (compilar.py)")
    print("="*80)

    testes = [
        ("inputs/RA3/teste1_valido.txt", "Teste 1: Casos Válidos (22 linhas)"),
        ("inputs/RA3/teste2_erros_tipos.txt", "Teste 2: Erros de Tipo (15 linhas)"),
        ("inputs/RA3/teste3_erros_memoria.txt", "Teste 3: Erros de Memória (15 linhas)"),
    ]

    resultados = []

    for arquivo, descricao in testes:
        caminho = ROOT_DIR / arquivo
        if not caminho.exists():
            print(f"\n[AVISO] Arquivo não encontrado: {arquivo}")
            continue

        sucesso = executar_teste(caminho, descricao)
        resultados.append((descricao, sucesso))

    # Resumo
    print(f"\n{'='*80}")
    print("RESUMO DOS TESTES")
    print(f"{'='*80}\n")

    for desc, sucesso in resultados:
        status = "[OK]" if sucesso else "[FALHOU]"
        print(f"{status} {desc}")

    print(f"\nTotal: {len(resultados)} testes")
    print(f"Sucessos: {sum(1 for _, s in resultados if s)}")
    print(f"Falhas: {sum(1 for _, s in resultados if not s)}")

if __name__ == "__main__":
    main()
