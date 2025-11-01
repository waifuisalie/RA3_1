# GitHub Issues Documentation for RA3

This directory contains all the detailed documentation for creating GitHub issues for the RA3 Semantic Analyzer project.

## Quick Start

1. **Read:** `issues_overview.md` - Start here for workflow and dependencies
2. **Create:** GitHub labels using `github_labels.md`
3. **Create:** GitHub issues using individual issue files
4. **Follow:** Recommended workflow from overview

## Files in This Directory

### Overview & Planning

- **`issues_overview.md`** - Complete project overview with:
  - All 7 issues summary table
  - Dependency graph
  - Recommended workflow (2-week plan)
  - Deliverables checklist
  - Grading criteria mapping
  - Team coordination guidelines
  - Testing strategy
  - Prova de autoria preparation

### Labels

- **`github_labels.md`** - All GitHub labels to create:
  - 11 labels with colors and descriptions
  - Usage guidelines
  - Example combinations

### Individual Issues (Ready to Copy to GitHub)

1. **`issue_01_grammar_symbol_table.md`** - Aluno 1
   - Attribute grammar definition
   - Symbol table implementation
   - Grammar documentation

2. **`issue_02_type_checking.md`** - Aluno 2
   - Type verification rules
   - Type coercion
   - Error reporting

3. **`issue_03_memory_control.md`** - Aluno 3
   - Memory validation
   - Control flow validation
   - Scope management

4. **`issue_04_ast_integration.md`** - Aluno 4
   - Attributed AST generation
   - Main integration
   - Report generation

5. **`issue_05_test_files.md`** - All Team
   - 3 test files creation
   - Unit testing requirements
   - Test documentation

6. **`issue_06_documentation.md`** - All Team
   - README updates
   - CONTRIBUTING guide
   - Architecture docs

7. **`issue_07_output_generators.md`** - Aluno 4
   - Output directory structure
   - 5 file generators
   - Helper utilities

## How to Use These Files

### Step 1: Create Labels in GitHub

1. Go to your repository → Issues → Labels
2. Open `github_labels.md`
3. Click "New label" for each of the 11 labels
4. Copy name, color, and description exactly

### Step 2: Create Issues in GitHub

For each issue file:

1. Go to repository → Issues → New issue
2. **Title:** Copy from issue markdown (e.g., "Implement Attribute Grammar and Symbol Table")
3. **Description:** You can either:
   - Copy entire issue markdown content, OR
   - Write brief description and link to the markdown file
4. **Labels:** Add labels as specified in each issue
5. **Assignee:** Assign to team member
6. **Milestone:** Create "RA3 Semantic Analyzer" milestone if desired

### Step 3: Follow Workflow

1. Start with issues that have no dependencies (Issues #1, #5)
2. Follow dependency graph from `issues_overview.md`
3. Use recommended 2-week timeline
4. Track progress in GitHub project board (optional)

## Issue Dependencies

```
Can Start Immediately:
├── Issue #5 (Test Files)
└── Issue #1 (Grammar & Symbol Table)
    └── Issue #2 (Type Checking)
        └── Issue #3 (Memory & Control)
            └── Issue #4 (Integration)
                └── Issue #6 (Documentation)

Can Work in Parallel:
├── Issue #7 (Output Generators) - works with #2, #3
└── Issue #5 (Test Files) - anytime
```

## Grading Impact Summary

| Issue | Grading Category | Impact |
|-------|------------------|--------|
| #1 | Functionality (70%) | -20% if incomplete |
| #2 | Functionality (70%) | -30% + -10% per rule |
| #3 | Functionality (70%) | -40% combined |
| #4 | Functionality (70%) | -45% combined |
| #5 | Robustness (15%) | -15% if incomplete |
| #6 | Organization (15%) | -15% if incomplete |
| #7 | Robustness (15%) | Part of deliverables |

## Quick Reference

### All Deliverables

**Code Files (9):**
- Grammar & Symbol Table (Issue #1): 3 files
- Type Checking (Issue #2): 3 files
- Memory & Control (Issue #3): 3 files
- Integration (Issue #4): Updates to `compilar.py`

**Test Files (3+):**
- `teste1_valido.txt`
- `teste2_erros_tipos.txt`
- `teste3_erros_memoria.txt`
- Unit tests for all modules

**Output Files (5):** Generated automatically
- `gramatica_atributos.md`
- `arvore_atribuida.md`
- `arvore_atribuida.json`
- `julgamento_tipos.md`
- `erros_semanticos.md`

**Documentation (6+):**
- README.md (updated)
- CONTRIBUTING.md (new)
- CLAUDE.md (updated)
- Architecture docs
- Type system docs
- Testing guide

### Team Assignments

Assign based on team discussion:
- **Issue #1** → Aluno 1 (Grammar expert)
- **Issue #2** → Aluno 2 (Type system expert)
- **Issue #3** → Aluno 3 (Validation expert)
- **Issue #4** → Aluno 4 (Integration lead)
- **Issues #5, #6, #7** → Collaborative

### Timeline Summary

**Week 1:**
- Days 1-2: Setup + Issue #5 (Tests) + Start #1
- Days 3-5: Complete #1, Start #2, #7
- Days 6-7: Complete #2, Start #3

**Week 2:**
- Days 1-3: Complete #3, #7, Start #4, #6
- Days 4-5: Complete #4, #6
- Days 6-7: Testing, bug fixes, prova prep

## Additional Notes

- **All team members must understand all code** (prova de autoria requirement)
- Each developer creates unit tests for their module
- Use pull requests for all changes
- Follow PEP 8 style guide
- Keep commits clear and descriptive
- Update issues as work progresses

## Questions?

- Check `issues_overview.md` for workflow details
- Check individual issue files for specific requirements
- Refer to main requirements: `docs/RA3/documents/RA3_Phase3_Requirements.md`
- Consult `CLAUDE.md` for project architecture

---

**Created:** 2025-10-21
**Purpose:** GitHub issues planning for RA3 Semantic Analyzer
**Status:** Ready to create issues in GitHub
