#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from .configuracaoGramatica import (
    GRAMATICA_TEORICA_ORIGINAL, # Assumed to be the original, raw grammar
    SIMBOLO_INICIAL_ORIGINAL,   # Assumed to be the original start symbol
    EPSILON,                    # Constant for the epsilon symbol (e.g., 'EPSILON')
    is_non_terminal,            # Helper to check if a symbol is a non-terminal (by casing)
    is_terminal,                # Helper to check if a symbol is a terminal (by casing)
)
from .calcularFirst import calcularFirst
from .calcularFollow import calcularFollow
from .construirTabelaLL1 import construirTabelaLL1, ConflictError

def get_canonical_grammar():
    """
    Constructs the canonical grammar from the original definition.

    In the canonical representation, all non-terminals are converted to uppercase
    and all terminals to lowercase. This ensures a consistent internal representation
    for all subsequent grammar processing algorithms.

    Returns:
        tuple[dict, str]: A tuple containing:
            - The canonical grammar as a dictionary (non-terminal -> list of productions).
            - The canonical start symbol (uppercase).
    """
    canonical_grammar = {}
    original_grammar = GRAMATICA_TEORICA_ORIGINAL
    
    # Non-terminals in the original grammar are identified by being keys in the grammar dict.
    # This set is used to correctly classify symbols during canonicalization.
    original_non_terminals = set(original_grammar.keys())
    
    canonical_start_symbol = SIMBOLO_INICIAL_ORIGINAL.upper()

    # Process each rule from the original grammar definition
    for nt_original, productions_original in original_grammar.items():
        nt_canonical = nt_original.upper()
        canonical_grammar[nt_canonical] = []

        # Process each production for the current non-terminal
        for production_original in productions_original:
            production_canonical = []
            # Process each symbol within the production
            for symbol_original in production_original:
                if symbol_original == 'EPSILON':
                    production_canonical.append(EPSILON)
                elif symbol_original in original_non_terminals:
                    # Symbol is a non-terminal, convert to uppercase
                    production_canonical.append(symbol_original.upper())
                else:
                    # Symbol is a terminal, convert to lowercase
                    production_canonical.append(symbol_original.lower())
            canonical_grammar[nt_canonical].append(production_canonical)
            
    return canonical_grammar, canonical_start_symbol

def imprimir_gramatica_completa():
    """
    Constructs and displays the complete grammar analysis, including production rules,
    FIRST/FOLLOW sets, and the LL(1) parsing table.
    
    All internal processing is performed on the canonical grammar representation,
    ensuring adherence to the uppercase non-terminal, lowercase terminal convention.
    """
    # 1. Build the canonical grammar from the original source
    gramatica_canonizada, simbolo_inicial_canonizado = get_canonical_grammar()
    
    # 2. Extract non-terminals and terminals from the CANONICAL grammar.
    nao_terminais = set(gramatica_canonizada.keys())
    
    terminais = set()
    for producoes in gramatica_canonizada.values():
        for producao in producoes:
            for simbolo in producao:
                if is_terminal(simbolo):
                    terminais.add(simbolo)
    
    # 3. Calculate FIRST/FOLLOW sets and construct LL(1) table using the canonical grammar.
    # These functions are assumed to be adapted to accept the grammar as a parameter.
    conjuntos_first = calcularFirst(gramatica_canonizada)
    conjuntos_follow = calcularFollow(gramatica_canonizada, simbolo_inicial_canonizado)
    
    tabela_ll1 = None
    conflitos = []
    
    try:
        tabela_ll1 = construirTabelaLL1(gramatica_canonizada, simbolo_inicial_canonizado)
    except ConflictError as e:
        conflitos = [str(e)]
    
    # 4. Prepare productions for display, handling the epsilon character 'ε'
    producoes_lista = []
    for nt, producoes in gramatica_canonizada.items():
        for producao in producoes:
            if producao == [EPSILON]:
                producoes_lista.append(f"{nt} -> ε")
            else:
                producoes_lista.append(f"{nt} -> {' '.join(producao)}")
    
    # 5. Print all results using canonical symbols and user-friendly display formats
    print(f"\n---- Estrutura da Gramática ----")
    print(f"\n- Símbolo Inicial: \n  {simbolo_inicial_canonizado}")
    
    print(f"\n- Símbolos Não-Terminais:")
    non_terminals_sorted = sorted(list(nao_terminais))
    print(f"  {{{', '.join(non_terminals_sorted)}}}")
    
    print(f"\n- Símbolos Terminais:")
    display_terminais = sorted([t for t in terminais if t != EPSILON])
    print(f"  {{{', '.join(display_terminais)}}}")
    
    print(f"\n- Regras de Produção:")
    for i, producao in enumerate(producoes_lista, 1):
        print(f"{i:2}. {producao}")
    
    print(f"\n- Conjuntos First:")
    for nt in sorted(conjuntos_first.keys()):
        first_set = conjuntos_first[nt]
        display_first = ['ε' if s == EPSILON else s for s in sorted(list(first_set))]
        symbols_str = ', '.join(display_first) if display_first else '∅'
        print(f"FIRST({nt}) = {{{symbols_str}}}")
    
    print(f"\n- Conjuntos Follow:")
    for nt in sorted(conjuntos_follow.keys()):
        follow_set = conjuntos_follow[nt]
        display_follow = ['ε' if s == EPSILON else s for s in sorted(list(follow_set))]
        symbols_str = ', '.join(display_follow) if display_follow else '∅'
        print(f"FOLLOW({nt}) = {{{symbols_str}}}")
    
    print(f"\n- Tabela LL(1):")
    if tabela_ll1:
        table = tabela_ll1
        total_entries = 0
        
        for nt in sorted(table.keys()):
            for terminal in sorted(table[nt].keys()):
                production_entry = table[nt].get(terminal)
                if production_entry is not None:
                    display_production = ['ε' if s == EPSILON else s for s in production_entry]
                    production_str = ' '.join(display_production)
                    print(f"M[{nt}, {terminal}] = {nt} → {production_str}")
                    total_entries += 1
        
        print(f"\nTotal de entradas na tabela: {total_entries}")
    else:
        print("Erro na construção da Tabela LL(1).")
    
    if conflitos:
        print(f"\nCONFLITOS LL(1) DETECTADOS:")
        for i, conflito in enumerate(conflitos, 1):
            print(f"{i}. {conflito}")