#!/usr/bin/env python3
"""
Script temporário para executar testes unitários individualmente
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# Importar unittest
import unittest

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python executar_teste_individual.py <caminho_do_teste>")
        sys.exit(1)

    test_path = sys.argv[1]

    # Carregar o módulo de teste
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(test_path), pattern=os.path.basename(test_path))

    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Retornar código de saída baseado em sucesso
    sys.exit(0 if result.wasSuccessful() else 1)
