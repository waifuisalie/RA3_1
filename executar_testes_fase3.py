#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar testes da Fase 3 e capturar resultados
Resolve problemas de encoding no Windows
"""

import sys
import io
import subprocess
from pathlib import Path
import json

# Define encoding UTF-8 para saída
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent
INPUTS_RA3 = ROOT_DIR / "inputs" / "RA3"
OUTPUTS_RA3 = ROOT_DIR / "outputs" / "RA3"

def executar_compilador(arquivo_teste):
    """Executa o compilador com um arquivo de teste"""
    print(f"\n{'='*80}")
    print(f"TESTANDO: {arquivo_teste.name}")
    print(f"{'='*80}\n")

    cmd = [sys.executable, str(ROOT_DIR / "compilar.py"), str(arquivo_teste)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)

        print(f"\nCódigo de retorno: {result.returncode}")

        return {
            'arquivo': arquivo_teste.name,
            'sucesso': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        }

    except subprocess.TimeoutExpired:
        print("ERRO: Timeout na execução")
        return {
            'arquivo': arquivo_teste.name,
            'sucesso': False,
            'erro': 'Timeout'
        }
    except Exception as e:
        print(f"ERRO: {e}")
        return {
            'arquivo': arquivo_teste.name,
            'sucesso': False,
            'erro': str(e)
        }

def verificar_outputs():
    """Verifica se os arquivos de saída foram gerados"""
    print(f"\n{'='*80}")
    print("VERIFICANDO ARQUIVOS DE SAÍDA")
    print(f"{'='*80}\n")

    arquivos_esperados = [
        OUTPUTS_RA3 / "arvore_atribuida.json",
        OUTPUTS_RA3 / "relatorios" / "arvore_atribuida.md",
        OUTPUTS_RA3 / "relatorios" / "julgamento_tipos.md",
        OUTPUTS_RA3 / "relatorios" / "erros_sematicos.md",
        OUTPUTS_RA3 / "relatorios" / "tabela_simbolos.md"
    ]

    for arquivo in arquivos_esperados:
        if arquivo.exists():
            print(f"[OK] {arquivo.relative_to(ROOT_DIR)}")

            # Se for JSON, validar
            if arquivo.suffix == '.json':
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"     JSON válido com {len(str(data))} caracteres")
                except Exception as e:
                    print(f"     ERRO ao validar JSON: {e}")

            # Se for markdown, mostrar tamanho
            elif arquivo.suffix == '.md':
                tamanho = arquivo.stat().st_size
                print(f"     Markdown com {tamanho} bytes")
        else:
            print(f"[FALTA] {arquivo.relative_to(ROOT_DIR)}")

def main():
    print("=" * 80)
    print("EXECUÇÃO DE TESTES - FASE 3: ANÁLISE SEMÂNTICA")
    print("=" * 80)

    # Lista de arquivos de teste
    testes = [
        "teste1_valido.txt",
        "teste2_erros_tipos.txt",
        "teste3_erros_memoria.txt",
        "teste_fase3_completo.txt",
        "teste_erros_fase3.txt"
    ]

    resultados = []

    for teste in testes:
        arquivo_teste = INPUTS_RA3 / teste

        if not arquivo_teste.exists():
            print(f"\n[AVISO] Arquivo não encontrado: {teste}")
            continue

        resultado = executar_compilador(arquivo_teste)
        resultados.append(resultado)

    # Verificar outputs do último teste
    verificar_outputs()

    # Resumo
    print(f"\n{'='*80}")
    print("RESUMO DOS TESTES")
    print(f"{'='*80}\n")

    sucessos = sum(1 for r in resultados if r.get('sucesso', False))
    total = len(resultados)

    print(f"Total de testes: {total}")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas: {total - sucessos}")

    for resultado in resultados:
        status = "[OK]" if resultado.get('sucesso', False) else "[FALHOU]"
        print(f"{status} {resultado['arquivo']}")

    return 0 if sucessos == total else 1

if __name__ == "__main__":
    sys.exit(main())
