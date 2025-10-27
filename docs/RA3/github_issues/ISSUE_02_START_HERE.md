# 🎯 Issue #2 Start Here

You asked for comprehensive documentation to implement Issue #2. **I've created everything you need.**

---

## 📦 What You Got

**4 Complete Documentation Files** (~2,800 lines total):

### 1. **README_ISSUE_02.md** ← Start here first!
- Navigation guide for all documents
- Quick summary of each file
- Answer to "which document should I read?"
- Time estimates and pro tips

### 2. **ISSUE_02_IMPLEMENTATION_GUIDE.md** ← Main technical reference
- What Issue #1 already provided (use these!)
- Complete specification for 3 modules
- 11 verification functions with full specs
- Detailed algorithm explanations
- Code examples and templates
- Edge cases and critical considerations
- Troubleshooting guide

### 3. **ISSUE_02_QUICK_REFERENCE.md** ← Keep open while coding
- File structure to create
- Code templates
- Type rules cheat sheet (9 tables!)
- Common mistakes (❌ vs ✅)
- Integration checklist
- Quick debug commands

### 4. **ISSUE_02_VISUAL_GUIDE.md** ← Understand the flow
- Pipeline diagram
- Module interaction flowchart
- Type inference decision tree
- Type rule matrices for each operator
- Testing hierarchy
- Debugging flowchart

---

## 🚀 Getting Started (30 minutes)

### Step 1: Understand the Task (15 min)
```
Read in order:
1. README_ISSUE_02.md → Get oriented
2. ISSUE_02_QUICK_REFERENCE.md → High-level overview
3. ISSUE_02_IMPLEMENTATION_GUIDE.md sections 1-4 → What you're building
```

### Step 2: See the Big Picture (10 min)
```
Look at diagrams:
- VISUAL_GUIDE.md → "Overall Pipeline"
- VISUAL_GUIDE.md → "Module Interaction Diagram"
```

### Step 3: Choose Your Path (5 min)
```
Pick one:
- Want complete details? → IMPLEMENTATION_GUIDE.md
- Want quick reference? → QUICK_REFERENCE.md
- Want to see examples? → VISUAL_GUIDE.md
- Want to get unstuck? → README_ISSUE_02.md "Questions" section
```

---

## 📚 File Guide

| File | Size | Purpose | Read When |
|------|------|---------|-----------|
| README_ISSUE_02.md | ~200 lines | Navigation guide | First (30 min) |
| ISSUE_02_IMPLEMENTATION_GUIDE.md | 1,711 lines | Complete technical spec | Implementing each module |
| ISSUE_02_QUICK_REFERENCE.md | 418 lines | Quick lookup | Coding & debugging |
| ISSUE_02_VISUAL_GUIDE.md | 682 lines | Diagrams & examples | Understanding concepts |

---

## 🎯 The Three Modules You'll Create

```python
# 1. gerador_erros.py (~100 lines)
# Purpose: Error handling
# Time: 30-60 minutes
class ErroSemantico(Exception):
    def __init__(self, linha, descricao, contexto, categoria):
        ...

# 2. verificador_tipos.py (~300 lines)
# Purpose: Type validation
# Time: 2-4 hours
def verificar_aritmetica(tipo1, tipo2, op, linha, contexto):
    # Validate +, -, *, |
    
def verificar_divisao_inteira(tipo1, tipo2, op, linha, contexto):
    # Validate /, % (STRICT - no mixing!)
    
def verificar_potencia(tipo_base, tipo_exp, linha, contexto):
    # Validate ^ (exponent MUST be int)
    
def verificar_comparacao(tipo1, tipo2, op, linha, contexto):
    # Validate >, <, >=, <=, ==, != (returns boolean)
    
def verificar_logico_binario(tipo1, tipo2, op, linha, contexto):
    # Validate &&, || (permissive mode)
    
def verificar_logico_unario(tipo, linha, contexto):
    # Validate ! (permissive mode)
    
def verificar_controle_for(init, end, step, body, linha, contexto):
    # Validate FOR (all must be int)
    
def verificar_controle_while(cond, body, linha, contexto):
    # Validate WHILE (condition permissive)
    
def verificar_controle_ifelse(cond, true_br, false_br, linha, contexto):
    # Validate IFELSE (CRITICAL: branches MUST match!)

# 3. analisador_semantico.py (~350 lines)
# Purpose: AST traversal and type annotation
# Time: 4-6 hours
def analisarSemantica(arvore_sintatica, tabela_simbolos):
    # Main entry point
    # Returns: (arvore_anotada, lista_erros)
```

---

## 🔑 Key Concepts

### 1. Post-Order Traversal
Children analyzed before parent. **Critical for correctness!**

```
        (+)
       /   \
      5     3
      
Process:
1. Analyze (5) → type = int
2. Analyze (3) → type = int
3. NOW analyze (+) using child types
```

### 2. Type Promotion (Some Operators)
```
+, -, *, | :  int + real = real ✓
/, % :        real / int = ERROR ✗ (STRICT!)
```

### 3. Permissive Mode (Logical Operators)
```
(5 3 &&) → true && true = true
(0.0 5 ||) → false || true = true
```

### 4. IFELSE Type Matching (MOST IMPORTANT!)
```
(true 5 10 IFELSE) → both int ✓
(true 5 2.5 IFELSE) → int vs real ✗ ERROR!
```

---

## ✅ Success Criteria

When all of these are true, you're done:

- [ ] `gerador_erros.py` created and tested
- [ ] `verificador_tipos.py` with 11 functions working
- [ ] `analisador_semantico.py` handles all node types
- [ ] Post-order traversal correct (children before parent)
- [ ] Error messages match format exactly
- [ ] 20+ unit tests passing
- [ ] Integrated with `compilar.py`
- [ ] Output files generated (`arvore_anotada.json`, `erros_semanticos.md`)
- [ ] No crashes on test inputs

---

## ⏱️ Time Investment

```
Reading & Understanding:        1-2 hours
  └─ QUICK_REFERENCE + sections of IMPLEMENTATION_GUIDE

gerador_erros.py:              1 hour
  └─ Simple error class

verificador_tipos.py:          4-5 hours
  └─ 11 functions, test each

analisador_semantico.py:       5-6 hours
  └─ Complex recursive algorithm

Testing & Integration:         3-4 hours
  └─ 20+ tests + compilar.py integration

Debugging & Polish:            2-3 hours
  └─ Edge cases and refinement

TOTAL: 16-21 hours
      (2-3 days of focused work)
```

---

## 🆘 Getting Unstuck

### Problem: "I don't know where to start"
→ Open **README_ISSUE_02.md** → "How to Use These Documents"

### Problem: "I don't understand [X concept]"
→ Open **README_ISSUE_02.md** → "Questions? Check Here First"

### Problem: "My implementation has a bug"
→ Open **ISSUE_02_QUICK_REFERENCE.md** → "Common Mistakes"

### Problem: "I need to see an example"
→ Open **ISSUE_02_VISUAL_GUIDE.md** (has 9 examples!)

### Problem: "I need complete technical details"
→ Open **ISSUE_02_IMPLEMENTATION_GUIDE.md** (850 lines of spec!)

---

## 📋 Document Checklist

All files created and ready:

- ✅ README_ISSUE_02.md - Navigation guide
- ✅ ISSUE_02_IMPLEMENTATION_GUIDE.md - Complete technical spec
- ✅ ISSUE_02_QUICK_REFERENCE.md - Cheat sheet
- ✅ ISSUE_02_VISUAL_GUIDE.md - Diagrams & flowcharts
- ✅ ISSUE_02_START_HERE.md - This file!

**Total: ~2,800 lines of documentation covering every aspect**

---

## 🎓 Learning Path

```
Complete Beginner Path:
1. ISSUE_02_START_HERE.md (this file) - 10 min
2. README_ISSUE_02.md - 20 min
3. ISSUE_02_QUICK_REFERENCE.md (sections 1-2) - 15 min
4. ISSUE_02_IMPLEMENTATION_GUIDE.md (sections 1-5) - 30 min
5. ISSUE_02_VISUAL_GUIDE.md (first 3 diagrams) - 20 min
   ↓
Ready to code!

During Implementation:
- Keep QUICK_REFERENCE.md open
- Refer to IMPLEMENTATION_GUIDE.md for function specs
- Check VISUAL_GUIDE.md when confused

When Stuck:
- Check README_ISSUE_02.md "Questions" section
- Search IMPLEMENTATION_GUIDE.md for the concept
- Look for similar examples in VISUAL_GUIDE.md
```

---

## 💡 Pro Tips

1. **Read these documents, don't skim them!**
   - They're comprehensive for a reason
   - Every detail matters

2. **Test as you go, don't wait until the end**
   - Test gerador_erros.py immediately
   - Test each verificador function as you write it
   - Test analisador_semantico.py with simple examples first

3. **Keep QUICK_REFERENCE.md visible while coding**
   - Type rules table
   - Common mistakes
   - Operator matrices

4. **Debug with print statements**
   - What types do children have?
   - What type is the operator returning?
   - Are errors being raised correctly?

5. **Refer to Issue #1 implementations**
   - tipos.py - use these utilities!
   - tabela_simbolos.py - it's already done
   - gramatica_atributos.py - all rules defined

---

## 📖 Next Steps

1. **Right now:** Read README_ISSUE_02.md (5-10 min)
2. **Next 20 min:** Skim QUICK_REFERENCE.md
3. **Next 30 min:** Read IMPLEMENTATION_GUIDE.md sections 1-4
4. **Then:** Pick a module and start coding!

---

## 🎯 Your Mission

Implement three Python modules that:
- ✅ Validate type rules for all RPN operators
- ✅ Traverse the syntax tree and add type information
- ✅ Collect and report semantic errors
- ✅ Output a type-annotated AST

**You have complete specifications for every function. No guessing required!**

---

## 📞 Questions?

Check the README_ISSUE_02.md file in the "Questions? Check Here First" table.

If it's not there, it's definitely in one of the other three documents.

---

**You've got this! Start with README_ISSUE_02.md and follow the path. 🚀**

