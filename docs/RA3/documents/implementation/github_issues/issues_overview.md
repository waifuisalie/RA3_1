# RA3 GitHub Issues Overview

## Project: Semantic Analyzer for RPN Compiler

**Group:** RA3_1
**Phase:** 3 - Semantic Analysis
**Total Issues:** 7

---

## Quick Summary

| Issue # | Title | Assignee | Priority | Labels | Status |
|---------|-------|----------|----------|--------|--------|
| #1 | Grammar & Symbol Table | Aluno 1 | High | `phase-3-semantic`, `symbol-table`, `type-checking`, `deliverable` | Not Started |
| #2 | Type Checking | Aluno 2 | High | `phase-3-semantic`, `type-checking` | Not Started |
| #3 | Memory & Control Validation | Aluno 3 | High | `phase-3-semantic`, `memory-validation`, `control-flow` | Not Started |
| #4 | AST Generation & Integration | Aluno 4 | High | `phase-3-semantic`, `integration`, `deliverable` | Not Started |
| #5 | Test Files | All | High | `phase-3-semantic`, `testing`, `deliverable` | Not Started |
| #6 | Documentation | All | Medium | `phase-3-semantic`, `documentation`, `deliverable` | Not Started |
| #7 | Output Generators | Aluno 4 | Medium | `phase-3-semantic`, `deliverable`, `documentation` | Not Started |

---

## Dependency Graph

```
Issue #5 (Tests) ─┐
                  │
Issue #1 ─────────┼─────> Issue #2 ─────> Issue #3 ─────> Issue #4
(Grammar)         │       (Types)         (Memory)        (Integration)
                  │                                            │
Issue #7 ─────────┘                                            │
(Generators)                                                   │
                                                               │
Issue #6 <─────────────────────────────────────────────────────┘
(Docs)
```

### Dependency Details

**Can Start Immediately:**
- Issue #5 (Test Files) - No dependencies
- Issue #1 (Grammar & Symbol Table) - No dependencies

**Blocked By:**
- Issue #2 requires Issue #1
- Issue #3 requires Issues #1, #2
- Issue #4 requires Issues #1, #2, #3, #7
- Issue #6 requires Issues #1-4 (to document them)
- Issue #7 requires Issues #1, #2, #3 (for data to output)

**Parallel Work Possible:**
- Issue #5 can be done anytime
- Issue #7 can work in parallel with Issues #2-3
- Issue #6 can start documentation while implementation ongoing

---

## Recommended Workflow

### Week 1: Foundation

**Days 1-2:**
- [ ] Create all GitHub issues from templates
- [ ] Create GitHub labels
- [ ] **Issue #5:** Create test files (all team)
- [ ] **Issue #1:** Start grammar & symbol table (Aluno 1)

**Days 3-5:**
- [ ] **Issue #1:** Complete grammar & symbol table (Aluno 1)
- [ ] **Issue #7:** Start output generators (Aluno 4)
- [ ] **Issue #2:** Start type checking (Aluno 2)

**Days 6-7:**
- [ ] **Issue #2:** Complete type checking (Aluno 2)
- [ ] **Issue #3:** Start memory/control validation (Aluno 3)
- [ ] **Issue #7:** Complete output generators (Aluno 4)

### Week 2: Integration

**Days 1-3:**
- [ ] **Issue #3:** Complete memory/control validation (Aluno 3)
- [ ] **Issue #4:** Start integration (Aluno 4)
- [ ] **Issue #6:** Start documentation updates (All)

**Days 4-5:**
- [ ] **Issue #4:** Complete integration (Aluno 4)
- [ ] **Issue #6:** Complete documentation (All)
- [ ] **All:** Test complete system with test files

**Days 6-7:**
- [ ] **All:** Bug fixes and refinements
- [ ] **All:** Final testing and validation
- [ ] **All:** Prepare for prova de autoria (everyone understands all code)

---

## Deliverables Checklist

### Code Deliverables

- [ ] `src/RA3/functions/python/gramatica_atributos.py` (Issue #1)
- [ ] `src/RA3/functions/python/tabela_simbolos.py` (Issue #1)
- [ ] `src/RA3/functions/python/tipos.py` (Issue #1)
- [ ] `src/RA3/functions/python/analisador_semantico.py` (Issue #2)
- [ ] `src/RA3/functions/python/verificador_tipos.py` (Issue #2)
- [ ] `src/RA3/functions/python/validador_memoria.py` (Issue #3)
- [ ] `src/RA3/functions/python/validador_controle.py` (Issue #3)
- [ ] `src/RA3/functions/python/gerador_arvore_atribuida.py` (Issue #4)
- [ ] `compilar.py` updated with RA3 integration (Issue #4)

### Test Deliverables

- [ ] `inputs/RA3/teste1_valido.txt` (Issue #5)
- [ ] `inputs/RA3/teste2_erros_tipos.txt` (Issue #5)
- [ ] `inputs/RA3/teste3_erros_memoria.txt` (Issue #5)
- [ ] Unit tests for all modules (Issues #1-4)

### Output Deliverables (Generated)

- [ ] `outputs/RA3/gramatica_atributos.md` (Issues #1, #7)
- [ ] `outputs/RA3/arvore_atribuida.md` (Issues #4, #7)
- [ ] `outputs/RA3/arvore_atribuida.json` (Issues #4, #7)
- [ ] `outputs/RA3/julgamento_tipos.md` (Issues #4, #7)
- [ ] `outputs/RA3/erros_semanticos.md` (Issues #2, #3, #7)

### Documentation Deliverables

- [ ] `README.md` updated with RA3 section (Issue #6)
- [ ] `CONTRIBUTING.md` created (Issue #6)
- [ ] `CLAUDE.md` updated (Issue #6)
- [ ] `docs/RA3/architecture.md` (Issue #6)
- [ ] `docs/RA3/type_system.md` (Issue #6)
- [ ] `docs/RA3/testing_guide.md` (Issue #6)

---

## Grading Criteria Mapping

### Functionality (70%)

| Criteria | Issue(s) | Penalty if Missing |
|----------|----------|--------------------|
| Type verification | #2 | Base grade |
| Memory initialization | #3 | -20% |
| Control structure validation | #3 | -20% |
| Type rules (e.g., int exponent) | #2 | -10% each |
| Attributed AST generation | #4 | -30% |
| Grammar documentation | #1 | -20% |

**Primary Issues:** #1, #2, #3, #4

### Organization (15%)

| Criteria | Issue(s) | Notes |
|----------|----------|-------|
| Code clarity & comments | All | PEP 8 compliance |
| README completeness | #6 | All required sections |
| Repository organization | All | Clear commits, PRs |
| Balanced participation | All | Automatic evaluation |

**Primary Issue:** #6

### Robustness (15%)

| Criteria | Issue(s) | Notes |
|----------|----------|-------|
| Error handling | #2, #3 | Clear messages with line numbers |
| Test coverage | #5 | All operators, commands, structures |
| Output file generation | #7 | All markdown files correct |

**Primary Issues:** #5, #7

---

## Issue Templates in GitHub

When creating issues in GitHub, use this format:

### Issue Title Format
```
[RA3-X] Short descriptive title
```

Examples:
- `[RA3-1] Implement Attribute Grammar and Symbol Table`
- `[RA3-2] Implement Type Checking and Semantic Analysis`

### Issue Description Template

```markdown
## Description
[Brief description from issue markdown file]

## Assignee
- [ ] @username

## Related Issues
- Requires: #X, #Y
- Blocks: #Z

## Acceptance Criteria
- [ ] Item 1
- [ ] Item 2
...

## Files to Create/Modify
- `path/to/file1.py`
- `path/to/file2.py`

## References
- Documentation: `docs/RA3/documents/RA3_Phase3_Requirements.md`
- Section X.Y

---
See full details in: `docs/RA3/github_issues/issue_0X_title.md`
```

---

## Team Coordination

### Communication Channels

- **GitHub Issues:** Task tracking and discussion
- **Pull Requests:** Code review and integration
- **GitHub Discussions:** General questions and planning

### Pull Request Guidelines

1. **Branch naming:** `issue-#-short-description`
   - Example: `issue-1-grammar-symbol-table`

2. **PR title:** `[RA3-#] Brief description`
   - Example: `[RA3-1] Add attribute grammar and symbol table`

3. **PR description must include:**
   - What was implemented
   - Testing performed
   - Related issue: `Closes #X`

4. **Review requirements:**
   - At least 1 approval from team member
   - All tests passing
   - PEP 8 compliance

### Code Review Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] Unit tests included
- [ ] Tests pass locally
- [ ] No merge conflicts
- [ ] Changes match issue acceptance criteria

---

## Testing Strategy

### Unit Testing (Each Developer)

Each developer writes unit tests for their own module:

- **Aluno 1:** `tests/RA3/test_tabela_simbolos.py`
- **Aluno 2:** `tests/RA3/test_verificador_tipos.py`
- **Aluno 3:** `tests/RA3/test_validador_memoria.py`, `test_validador_controle.py`
- **Aluno 4:** `tests/RA3/test_integracao.py`

### Integration Testing (All)

Use the three test files from Issue #5:
- `teste1_valido.txt` - Should pass all checks
- `teste2_erros_tipos.txt` - Should detect type errors
- `teste3_erros_memoria.txt` - Should detect memory errors

### Continuous Testing

```bash
# Run all tests
python3 -m pytest tests/RA3/

# Run specific module tests
python3 -m pytest tests/RA3/test_tabela_simbolos.py

# Run with coverage
python3 -m pytest --cov=src/RA3 tests/RA3/

# Run integration tests
python3 compilar.py inputs/RA3/teste1_valido.txt
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
```

---

## Prova de Autoria Preparation

### Important Reminders

- **All team members must understand ALL code** - even parts they didn't write
- One member will be randomly selected
- Selected member must explain entire project
- Failure = -35% for entire team

### Study Plan

**Week 1 End:** Each developer explains their module to team

**Week 2 Middle:** Team reviews all modules together

**Week 2 End:** Practice sessions:
- Random selection of team member
- Selected member explains entire architecture
- Other members ask questions

### Key Topics to Master

1. **Grammar & Type System** (Issue #1, #2)
   - All semantic rules
   - Type promotion logic
   - Attribute grammar structure

2. **Validation Logic** (Issue #3)
   - Memory initialization tracking
   - RES reference validation
   - Control structure validation

3. **Integration** (Issue #4)
   - Pipeline flow: RA1 → RA2 → RA3
   - Error handling strategy
   - Output generation

4. **Testing** (Issue #5)
   - Test coverage strategy
   - Why each test case exists
   - Expected behaviors

---

## Quick Reference Commands

### Setup
```bash
# Clone repository
git clone https://github.com/username/RA3_1.git
cd RA3_1

# Install dependencies
pip install -r requirements.txt
```

### Development
```bash
# Create branch for issue
git checkout -b issue-1-grammar-symbol-table

# Run tests while developing
python3 -m pytest tests/RA3/ -v

# Check code style
python3 -m flake8 src/RA3/
```

### Testing
```bash
# Run complete pipeline
python3 compilar.py inputs/RA3/teste1_valido.txt

# Check output files
ls -la outputs/RA3/
cat outputs/RA3/erros_semanticos.md
python3 -m json.tool outputs/RA3/arvore_atribuida.json
```

### Submission
```bash
# Verify all required files exist
ls src/RA3/functions/python/
ls inputs/RA3/
ls outputs/RA3/

# Final test before submission
python3 -m pytest tests/RA3/
python3 compilar.py inputs/RA3/teste1_valido.txt
python3 compilar.py inputs/RA3/teste2_erros_tipos.txt
python3 compilar.py inputs/RA3/teste3_erros_memoria.txt
```

---

## Contact Information

### Team Members

- **Breno Rossi Duarte** - @breno-rossi (Responsible for Issue TBD)
- **Francisco Bley Ruthes** - @fbleyruthes (Responsible for Issue TBD)
- **Rafael Olivare Piveta** - @RafaPiveta (Responsible for Issue TBD)
- **Stefan Benjamim Seixas Lourenco Rodrigues** - @waifuisalie (Responsible for Issue TBD)

### Issue Assignment

Assign issues based on team discussion:
- Issue #1 → Aluno 1
- Issue #2 → Aluno 2
- Issue #3 → Aluno 3
- Issue #4 → Aluno 4
- Issues #5, #6, #7 → Collaborative

---

## Additional Resources

- **Requirements Document:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
- **Original PDF:** `docs/RA3/documents/RA3_Fase3_Doc/text/Comandos_Fase3.pdf`
- **Current Grammar:** `src/RA2/functions/python/configuracaoGramatica.py`
- **Project Instructions:** `CLAUDE.md`

---

## Success Criteria

✅ All 7 issues completed
✅ All unit tests passing
✅ All 3 integration tests passing
✅ All 5 output files generated correctly
✅ README complete and accurate
✅ All team members understand all code
✅ Repository well-organized with clear commits
✅ Ready for prova de autoria

---

**Last Updated:** 2025-10-21
**Status:** Planning Phase - Ready to Create Issues
