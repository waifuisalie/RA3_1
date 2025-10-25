# Getting Started with RA3 GitHub Issues

## 📋 What You Have

All GitHub issue documentation has been created in this directory:

```
docs/RA3/github_issues/
├── README.md                               # Directory guide
├── GETTING_STARTED.md                      # This file
├── issues_overview.md                      # Complete workflow & planning
├── github_labels.md                        # 11 labels to create
├── issue_01_grammar_symbol_table.md        # Issue #1 (Aluno 1)
├── issue_02_type_checking.md               # Issue #2 (Aluno 2)
├── issue_03_memory_control.md              # Issue #3 (Aluno 3)
├── issue_04_ast_integration.md             # Issue #4 (Aluno 4)
├── issue_05_test_files.md                  # Issue #5 (All team)
├── issue_06_documentation.md               # Issue #6 (All team)
└── issue_07_output_generators.md           # Issue #7 (Aluno 4)
```

## 🚀 Quick Start (5 Steps)

### Step 1: Read the Overview (5 minutes)

```bash
# Open and read
cat docs/RA3/github_issues/issues_overview.md
```

This gives you:
- All 7 issues at a glance
- Dependency graph
- 2-week timeline
- Grading impact
- Team coordination guidelines

### Step 2: Create Labels (5 minutes)

1. Go to: `https://github.com/your-username/RA3_1/issues/labels`
2. Open: `github_labels.md`
3. For each of the 11 labels, click "New label" and copy:
   - Name (e.g., `phase-3-semantic`)
   - Color (e.g., `#0E8A16`)
   - Description

### Step 3: Create Issues (20 minutes)

For each of the 7 issue files:

1. Go to: `https://github.com/your-username/RA3_1/issues/new`
2. **Title:** Copy from markdown (first heading)
3. **Description:** Either:
   - Copy entire markdown content, OR
   - Write: "See full details in `docs/RA3/github_issues/issue_0X_title.md`"
4. **Labels:** Add the labels listed in each issue
5. **Assignee:** Assign team member
6. **Submit**

### Step 4: Assign Team Members

Discuss with your team and assign:
- **Issue #1** → One person (responsible for grammar & symbol table)
- **Issue #2** → One person (responsible for type checking)
- **Issue #3** → One person (responsible for memory/control validation)
- **Issue #4** → One person (responsible for integration)
- **Issues #5, #6, #7** → Everyone collaborates

### Step 5: Start Working!

Follow the recommended workflow from `issues_overview.md`:

**Week 1, Days 1-2:**
```bash
# Everyone can start these
- Create test files (Issue #5)
- Start grammar & symbol table (Issue #1 assignee)
```

## 📊 Issue Summary

| # | Title | Assignee | Can Start? | Blocks |
|---|-------|----------|------------|--------|
| 1 | Grammar & Symbol Table | Aluno 1 | ✅ Yes | #2 |
| 2 | Type Checking | Aluno 2 | ⏸️ Needs #1 | #3 |
| 3 | Memory & Control | Aluno 3 | ⏸️ Needs #1,#2 | #4 |
| 4 | Integration | Aluno 4 | ⏸️ Needs #1,#2,#3 | #6 |
| 5 | Test Files | All | ✅ Yes | - |
| 6 | Documentation | All | ⏸️ Needs #1-4 | - |
| 7 | Output Generators | Aluno 4 | ⏸️ Needs #1-3 | #4 |

## 📝 What Each Issue Contains

Each issue markdown file has:

✅ **Clear description** of what needs to be done
✅ **Specific tasks** with checkboxes for tracking
✅ **Acceptance criteria** with unit testing requirements
✅ **Interface specifications** (inputs/outputs)
✅ **Grading impact** (how it affects your grade)
✅ **Dependencies** (what it needs, what it blocks)
✅ **Files to create** (exact file structure)
✅ **Implementation tips** (code examples)
✅ **References** to documentation

## 🎯 Key Deliverables

You need to deliver:

### Code (9 Python modules)
- 3 files for Issue #1 (grammar, symbol table, types)
- 3 files for Issue #2 (analyzer, type checker, error generator)
- 3 files for Issue #3 (memory validator, control validator, scope manager)
- Plus: Update to `compilar.py` (Issue #4)

### Tests (3+ files)
- `inputs/RA3/teste1_valido.txt`
- `inputs/RA3/teste2_erros_tipos.txt`
- `inputs/RA3/teste3_erros_memoria.txt`
- Unit tests for all modules

### Generated Outputs (5 files)
These are created automatically when you run the compiler:
- `outputs/RA3/gramatica_atributos.md`
- `outputs/RA3/arvore_atribuida.md`
- `outputs/RA3/arvore_atribuida.json`
- `outputs/RA3/julgamento_tipos.md`
- `outputs/RA3/erros_semanticos.md`

### Documentation (Updates + New)
- Update: `README.md`
- Update: `CLAUDE.md`
- Create: `CONTRIBUTING.md`
- Create: Architecture docs

## ⚠️ Important Reminders

### For Grading
- **Functionality = 70%** (Issues #1-4 are critical!)
- **Organization = 15%** (Issue #6 - documentation)
- **Robustness = 15%** (Issue #5 - tests)

### For Prova de Autoria
- ❗ **Everyone must understand ALL code**
- One random team member will be selected
- They must explain the entire project
- Failure = -35% for the whole team
- See "Prova de Autoria Preparation" in `issues_overview.md`

### For Repository
- ✅ All issues tracked in GitHub
- ✅ All changes via pull requests
- ✅ Clear commit messages
- ✅ Balanced participation (automatic evaluation)

## 🔗 Useful Links

- **Main Requirements:** `docs/RA3/documents/RA3_Phase3_Requirements.md`
- **Current Grammar:** `src/RA2/functions/python/configuracaoGramatica.py`
- **Project Instructions:** `CLAUDE.md`
- **Professor's Page:** https://frankalcantara.com/lf/fase3.html

## 💡 Tips for Success

1. **Start Early**
   - Issues #1 and #5 can start immediately
   - Don't wait for everything to be perfect

2. **Communicate Often**
   - Use GitHub issues for discussions
   - Comment on pull requests
   - Help each other understand code

3. **Test Continuously**
   ```bash
   # Run tests frequently
   python3 -m pytest tests/RA3/
   ```

4. **Document As You Go**
   - Write docstrings for every function
   - Comment complex logic
   - Update README when adding features

5. **Review Together**
   - Schedule team code reviews
   - Explain your code to teammates
   - Ask questions about others' code

6. **Practice for Prova**
   - Everyone should be able to explain:
     - How the grammar works
     - How types are checked
     - How memory is validated
     - How everything integrates

## 📅 Suggested Timeline

### Week 1
- **Mon-Tue:** Labels + Issues + Tests (#5) + Start #1
- **Wed-Fri:** Complete #1, Start #2 & #7
- **Sat-Sun:** Complete #2, Start #3

### Week 2
- **Mon-Wed:** Complete #3 & #7, Start #4 & #6
- **Thu-Fri:** Complete #4 & #6
- **Sat-Sun:** Final testing, bug fixes, prova prep

## 🆘 Need Help?

1. **For issue details:** Read the specific issue markdown file
2. **For workflow:** Check `issues_overview.md`
3. **For project context:** Read `CLAUDE.md`
4. **For requirements:** See `docs/RA3/documents/RA3_Phase3_Requirements.md`

## ✨ You're Ready!

You have everything you need:
- ✅ All issues documented
- ✅ Labels defined
- ✅ Workflow planned
- ✅ Grading criteria clear
- ✅ Timeline suggested
- ✅ Code examples provided

**Next step:** Create the labels and issues in GitHub, then start coding! 🚀

---

**Good luck with RA3!** 🎓
