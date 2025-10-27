# Issue #2: Type Checking and Semantic Analysis

## 📋 Documentation Files Created

I've created **comprehensive documentation** to help you implement Issue #2. All files are in `docs/RA3/github_issues/`:

### 1. **ISSUE_02_IMPLEMENTATION_GUIDE.md** (Main Reference)
**~850 lines, COMPLETE SPECIFICATION**

Contains:
- ✅ Quick summary of what you're building
- ✅ What Issue #1 already provided (use these!)
- ✅ Detailed specifications for all 3 modules:
  - `gerador_erros.py` - Error handling
  - `verificador_tipos.py` - Type validation (11 functions)
  - `analisador_semantico.py` - AST traversal
- ✅ Function-by-function specifications with:
  - Purpose and algorithm
  - Type rules explained
  - Code examples
  - Expected behavior
- ✅ Complete test requirements
- ✅ Integration instructions
- ✅ Critical considerations (permissive mode, IFELSE rules, etc.)
- ✅ Troubleshooting guide

**Use this when:** You need the complete technical details for any function.

---

### 2. **ISSUE_02_QUICK_REFERENCE.md** (Cheat Sheet)
**~300 lines, QUICK LOOKUP**

Contains:
- ✅ File structure you need to create
- ✅ Quick template for each module
- ✅ 9-row operator type matrix (what types are allowed?)
- ✅ Type inference rules (int/real from literals)
- ✅ Common mistakes (❌ WRONG vs ✅ CORRECT)
- ✅ Integration checklist
- ✅ Output files expected
- ✅ Time estimates per module
- ✅ Quick debug commands

**Use this when:** You need a quick reminder or are stuck on a specific issue.

---

### 3. **ISSUE_02_VISUAL_GUIDE.md** (Diagrams)
**~400 lines, VISUAL REFERENCE**

Contains:
- ✅ Overall compiler pipeline diagram
- ✅ Module interaction flowchart
- ✅ Detailed type inference decision tree
- ✅ Type annotation step-by-step example
- ✅ Error detection flowchart with example
- ✅ Type rule matrices for each operator (9 tables!)
- ✅ Testing hierarchy and test flow
- ✅ Debugging decision tree
- ✅ Time breakdown by component

**Use this when:** You want to visualize how things work together.

---

## 🚀 How to Use These Documents

### First Time Reading (Understanding the Task)
1. Start with **QUICK_REFERENCE.md** - Get oriented (15 min read)
2. Read **IMPLEMENTATION_GUIDE.md** sections 1-4 - Understand what you're building (30 min)
3. Skim **VISUAL_GUIDE.md** - See how it all connects (20 min)

**Total time: ~1 hour to fully understand the task**

### When Implementing Each Module

#### For gerador_erros.py:
- Section: IMPLEMENTATION_GUIDE.md → "Module 1: gerador_erros.py"
- Reference: QUICK_REFERENCE.md → "Step 1"
- Diagram: VISUAL_GUIDE.md → "Module 1: gerador_erros.py"

#### For verificador_tipos.py:
- Section: IMPLEMENTATION_GUIDE.md → "Module 2: verificador_tipos.py"
- Reference: QUICK_REFERENCE.md → "Step 2" + "Type Rules Cheat Sheet"
- Diagram: VISUAL_GUIDE.md → "Module 2" + "Type Rule Matrix"
- When stuck: VISUAL_GUIDE.md → "Debugging Flowchart"

#### For analisador_semantico.py:
- Section: IMPLEMENTATION_GUIDE.md → "Module 3: analisador_semantico.py"
- Reference: QUICK_REFERENCE.md → "Step 3"
- Diagram: VISUAL_GUIDE.md → "Module 3" + "Type Inference Flow"
- When stuck: VISUAL_GUIDE.md → "Debugging Flowchart"

#### For Testing:
- Section: IMPLEMENTATION_GUIDE.md → "Test Requirements"
- Reference: QUICK_REFERENCE.md → "Testing Pyramid"
- Diagram: VISUAL_GUIDE.md → "Testing Flow"

### When You Get Stuck

**"My error messages don't match the spec"**
→ QUICK_REFERENCE.md → "Common Mistakes"

**"I don't understand permissive mode"**
→ IMPLEMENTATION_GUIDE.md → "Critical Considerations #3"

**"What types can I mix in division?"**
→ QUICK_REFERENCE.md → "Type Rules Cheat Sheet"

**"How does post-order traversal work?"**
→ VISUAL_GUIDE.md → "Module 3: analisador_semantico.py"

**"Why is IFELSE different from other operators?"**
→ IMPLEMENTATION_GUIDE.md → "Critical Considerations #4"

**"Is my integration correct?"**
→ IMPLEMENTATION_GUIDE.md → "Integration Points"

---

## 📊 Document Statistics

| Document | Pages | Length | Content |
|----------|-------|--------|---------|
| ISSUE_02_IMPLEMENTATION_GUIDE.md | ~15 | 850 lines | Complete technical specification |
| ISSUE_02_QUICK_REFERENCE.md | ~10 | 300 lines | Cheat sheet and quick lookup |
| ISSUE_02_VISUAL_GUIDE.md | ~12 | 400 lines | Diagrams and flowcharts |
| **Total** | **~37** | **1550+ lines** | Everything you need |

---

## ✅ What's Covered

### Understanding
- ✅ What you're building (type checking and AST annotation)
- ✅ Why it matters (foundation for Issues #3 and #4)
- ✅ How it fits in the pipeline (after RA2 parsing)

### Specification
- ✅ Three modules to create
- ✅ 11 type verification functions
- ✅ Complete algorithm for AST traversal
- ✅ Error handling and formatting

### Implementation
- ✅ Step-by-step implementation order
- ✅ Code templates and examples
- ✅ Function specifications with algorithms
- ✅ Edge cases and critical rules

### Testing
- ✅ Unit test requirements
- ✅ Integration test requirements
- ✅ Test organization and naming

### Debugging
- ✅ Common mistakes and solutions
- ✅ Debugging flowcharts
- ✅ Quick reference for specific problems
- ✅ Time estimates

---

## 🎯 Implementation Timeline

```
Day 1: Understanding & gerador_erros.py
├─ Read QUICK_REFERENCE + IMPLEMENTATION_GUIDE (1 hour)
├─ Create gerador_erros.py (1 hour)
└─ Test error formatting (30 min)
Total: ~2.5 hours

Day 2: verificador_tipos.py
├─ Create basic structure (15 min)
├─ Implement 11 functions (4 hours)
├─ Unit test each function (1 hour)
└─ Fix issues (30 min)
Total: ~6 hours

Day 3: analisador_semantico.py
├─ Create NoAnotado class & helpers (30 min)
├─ Implement core algorithm (2.5 hours)
├─ Handle all node types (1.5 hours)
├─ Integration testing (1 hour)
└─ Fix issues (30 min)
Total: ~6 hours

Day 4: Testing & Integration
├─ Create comprehensive test suite (1.5 hours)
├─ Integrate with compilar.py (1 hour)
├─ End-to-end testing (1.5 hours)
└─ Polish & documentation (30 min)
Total: ~4.5 hours

Grand Total: ~18.5 hours over 4 days (or adjust to your pace)
```

---

## 💡 Pro Tips

1. **Start with gerador_erros.py** - It's the simplest and builds confidence
2. **Test each verificador function** - Don't wait until all are done
3. **Use the Quick Reference while coding** - Keep it in another window
4. **Print debug info** - What types do children have? Print them!
5. **Review post-order example** - The most confusing concept, study it carefully
6. **Don't over-think IFELSE** - It's just "both branches same type"
7. **Use the visual guide** - Pictures > words for complex algorithms

---

## 📚 Related Documents

- **IMPLEMENTATION_GUIDE.md** - Read this first and refer to it constantly
- **QUICK_REFERENCE.md** - Keep this open while coding
- **VISUAL_GUIDE.md** - Refer to when confused about structure/flow
- Original requirements: **RA3_Phase3_Requirements.md** (section 7.2)
- Issue #1 docs: **issue_01_grammar_symbol_table.md**

---

## 🚦 Status

- ✅ All documentation created
- ✅ All code examples provided
- ✅ All edge cases documented
- ✅ All common mistakes noted
- ✅ All flowcharts drawn
- ✅ All time estimates calculated

**Ready to start implementing? You have everything you need!**

---

## Questions? Check Here First

| Question | Answer Location |
|----------|-----------------|
| What's the overall pipeline? | VISUAL_GUIDE.md → "Overall Pipeline" |
| How do I distinguish int from real? | IMPLEMENTATION_GUIDE.md → "inferir_tipo_literal()" |
| What are the type rules for each operator? | QUICK_REFERENCE.md → "Type Rules Cheat Sheet" |
| How does post-order traversal work? | VISUAL_GUIDE.md → "Module 3" |
| What's "permissive mode"? | IMPLEMENTATION_GUIDE.md → "Critical Considerations #3" |
| Why can't I mix types in division? | VISUAL_GUIDE.md → "Type Rule Matrix - /" |
| How do I test my functions? | IMPLEMENTATION_GUIDE.md → "Test Requirements" |
| Why is my IFELSE accepting different types? | QUICK_REFERENCE.md → "Common Mistakes" |
| What error format is required? | QUICK_REFERENCE.md → "Step 1" |
| How do I integrate with compilar.py? | IMPLEMENTATION_GUIDE.md → "Integration Points" |

**If you can't find the answer, re-read the IMPLEMENTATION_GUIDE.md section that covers that topic - it's in there!**

