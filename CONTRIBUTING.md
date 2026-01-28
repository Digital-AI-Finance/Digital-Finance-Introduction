# Contributing to Digital Finance: From FinTech to Crypto/Blockchain/DeFi

Thank you for your interest in contributing to this educational course! This document provides guidelines for reporting issues, suggesting improvements, and participating in the development of course materials.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Reporting Issues](#reporting-issues)
3. [Suggesting Content Improvements](#suggesting-content-improvements)
4. [Content Guidelines](#content-guidelines)
5. [Code and Notebook Standards](#code-and-notebook-standards)
6. [Pull Request Process](#pull-request-process)
7. [Commit Conventions](#commit-conventions)
8. [Local Development](#local-development)
9. [License](#license)

---

## Code of Conduct

We are committed to making this course welcoming and inclusive for educators and learners from all disciplinary backgrounds.

### Our Pledge

We pledge to:
- Treat all contributors with respect
- Welcome questions and diverse perspectives
- Provide constructive feedback
- Maintain a harassment-free environment
- Assume good intent but address impact

### Unacceptable Behavior

The following are not tolerated:
- Harassment, discrimination, or hostile language
- Unwelcome sexual attention or advances
- Deliberate misinformation in educational content
- Plagiarism or unattributed content
- Attempts to undermine academic integrity

For violations, contact the course maintainer at the GitHub repository.

---

## Reporting Issues

### When to Report an Issue

Report issues if you find:
- **Factual errors** in lecture slides or explanations (especially in financial concepts, cryptography, or blockchain mechanics)
- **Broken links** or missing resources
- **Notebook errors** (code that doesn't run, incorrect outputs, dependencies not installed)
- **Accessibility problems** (poor contrast, missing alt text, inaccessible formats)
- **Typos or grammatical errors** that affect clarity
- **Outdated information** (especially given rapid changes in crypto/DeFi landscape)
- **Ambiguous explanations** that confuse learners

### How to Report

1. **Check existing issues** first to avoid duplicates
2. **Use GitHub Issues** with a clear, descriptive title
3. **Include these details:**
   - What you expected to happen
   - What actually happened
   - Where the issue occurs (day, topic, or notebook number)
   - Steps to reproduce (if applicable)
   - Your environment (browser, Python version, OS)
   - Screenshots or code blocks (for visual or code issues)

### Issue Template

```markdown
## Issue Title
[Clear, concise description]

## Description
[Detailed explanation of the issue]

## Location
- Day: [Day 1-6]
- Topic: [e.g., 3.2]
- File: [e.g., Day-3-Slides/, NB06-Blockchain-Simulator.ipynb]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [...]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 12, Windows 11]
- Browser: [if applicable]
- Python Version: [if applicable]

## Screenshots or Code
[If helpful]
```

---

## Suggesting Content Improvements

### What We Welcome

We encourage suggestions for:
- **Clarifying explanations** (especially for complex concepts like blockchain consensus or smart contracts)
- **Additional analogies or metaphors** that improve accessibility
- **New hands-on notebook examples** (especially emerging topics like AI in finance)
- **Updated data** (crypto prices, regulatory developments, DeFi metrics)
- **Alternative teaching approaches** for challenging topics
- **New topics** that fit the course structure (only if they fit the five pillars and six-day structure)
- **Accessibility improvements** (captions, alt text, accessible formatting)
- **Connections to other fields** (how concepts relate to economics, law, computer science, etc.)

### What We Don't Accept

We don't modify core content for:
- **Controversial opinions** presented as fact (the course takes balanced, evidence-based stances)
- **Product endorsements** (the course is not marketing any company or product)
- **Politically partisan content** (we discuss regulation and policy neutrally)
- **Speculation without evidence** (especially in the volatile crypto space)
- **Out-of-scope topics** (the course focuses on digital finance, not general blockchain applications)

### How to Suggest Improvements

**Option 1: GitHub Discussions (preferred for ideas)**
- Start a discussion under the "Ideas" category
- Clearly state what you want to improve and why
- Link to specific materials (day/topic/notebook)
- Explain the benefit to learners

**Option 2: GitHub Issues (for specific problems)**
- Use the enhancement template below
- Be specific about the location and nature of the change
- Explain the impact on learner understanding

**Option 3: Pull Request (for minor improvements)**
- See [Pull Request Process](#pull-request-process) below
- For major changes, discuss first via Issues or Discussions

### Enhancement Suggestion Template

```markdown
## Title
[Clear, concise summary of the improvement]

## Location
- Day: [Day 1-6]
- Topic: [e.g., 2.3]
- Type: [Slide/Notebook/Documentation]

## Current State
[What's currently there and what's unclear or missing]

## Proposed Improvement
[Specific, actionable change]

## Rationale
[Why this improves the course]

## Example or Reference
[Links to similar content, research, or external resources]

## Impact on Learners
[How does this help students understand better?]
```

---

## Content Guidelines

### Educational Philosophy

This course is designed to:
- **Assume no prerequisites** — Every concept is explained from first principles
- **Build mental models** — Help students think critically, not memorize
- **Acknowledge tradeoffs** — Digital finance solutions involve design choices, not absolute truths
- **Balance perspectives** — Present both benefits and risks of FinTech and DeFi
- **Support diverse learning styles** — Mix lectures, visuals, hands-on work, and discussion

When contributing content, respect these principles.

### Accessibility Standards

All materials must be:

**1. Visually Accessible**
- Use sufficient contrast (WCAG AA minimum, AAA preferred)
- Provide alt text for all diagrams and images
- Avoid color alone to convey information
- Use readable font sizes (slides: 24pt minimum for body text)
- Test with accessibility tools (Axe, WAVE, or similar)

**2. Cognitively Accessible**
- Define financial and technical terms on first use
- Use short sentences and clear structure
- Break complex ideas into steps
- Provide worked examples for mathematical concepts
- Link new concepts to previously established ideas

**3. Technically Accessible**
- Provide captions for any videos
- Use semantic HTML in web materials
- Ensure all links are descriptive (not "click here")
- Provide transcripts for video content
- Test notebooks with screen readers where possible

### Language and Tone

Write for students from any disciplinary background:

- **Avoid jargon** without explanation (if you must use a term, define it)
- **Use concrete examples** over abstract descriptions
- **Acknowledge difficulty** — It's okay to say "this is tricky," but then explain why and break it down
- **Write actively** — "Banks verify transactions" not "Transactions are verified by banks"
- **Use consistent terminology** — If you call something "a smart contract" in Day 4, don't suddenly call it "blockchain code" in Day 5
- **Avoid loaded language** — Use neutral terms: "Cryptocurrency advocates argue..." not "Crypto fanatics insist..."
- **Be inclusive** — Use gender-neutral pronouns and diverse examples

### Technical Accuracy

Financial and cryptographic concepts must be accurate:

- **Verify claims against primary sources** (academic papers, white papers, official documentation)
- **Attribute ideas** — "Bitcoin's Nakamoto Consensus..." not just "blockchain consensus..."
- **Note when information might change** — Crypto/DeFi evolve rapidly; if something is time-sensitive, mention it
- **Distinguish between layers** — Be clear about what's Bitcoin vs. Ethereum vs. general blockchain concepts
- **Avoid overstating capability** — "Can potentially enable..." not "Will definitely enable..."
- **Address known limitations** — If you explain how something works, also explain what it can't do

### Keeping Content Current

Given the fast-moving nature of digital finance:

- **Flag outdated material** with issue reports
- **Suggest updates** for regulatory or market changes
- **Reference stable concepts** (how money works) rather than volatile data (current ETH price)
- **Use examples carefully** — Past failures are good teaching tools; avoid making them seem current
- **Document versions** — Note when content was last reviewed/updated

---

## Code and Notebook Standards

### Python Style

Follow PEP 8 with these specifics:

```python
# Good: Clear variable names, comments for non-obvious logic
def calculate_impermanent_loss(initial_price, final_price, initial_amount):
    """
    Calculate impermanent loss for an AMM liquidity provider.

    Args:
        initial_price (float): Price ratio at time of deposit
        final_price (float): Current price ratio
        initial_amount (float): Initial liquidity amount

    Returns:
        float: IL percentage (0 = no loss, negative = gain)
    """
    price_ratio = final_price / initial_price
    # IL formula: 2*sqrt(price_ratio) / (1 + price_ratio) - 1
    il = 2 * np.sqrt(price_ratio) / (1 + price_ratio) - 1
    return il * 100

# Avoid: Cryptic names, no comments
def calc_il(p1, p2, amt):
    return 2 * np.sqrt(p2/p1) / (1 + p2/p1) - 1
```

**Guidelines:**
- Maximum line length: 88 characters (Black formatter standard)
- 4-space indentation
- Use meaningful variable names (not `x`, `y`, `tmp`)
- Document functions with docstrings
- Comment non-obvious logic
- Type hints preferred (Python 3.9+)

### Notebook Standards

All notebooks must:

1. **Have a clear structure:**
   - Title cell explaining learning objectives
   - Introduction cell with context
   - Logical sections with markdown headers
   - Conclusion/summary cell

2. **Be runnable top-to-bottom:**
   - All dependencies installed in first cell
   - No hidden state between cells
   - Clear outputs for each code cell
   - No student solutions requiring modification to run

3. **Include explanations:**
   - Markdown before code explaining what the code does
   - Comments in complex code sections
   - Interpretation of outputs (don't just show data, explain it)

4. **Have clear learning objectives:**
   - Start with 2-4 explicit learning goals
   - Activities map to these goals
   - Summary confirms students can achieve them

5. **Example notebook structure:**
   ```
   # NB09: AMM & Impermanent Loss Simulator

   ## Learning Objectives
   By the end, you'll be able to:
   - Explain how Automated Market Makers maintain price discovery
   - Calculate impermanent loss for different price movements
   - Analyze LP profitability considering trading fees

   ## What You'll Do
   [Explanation of the hands-on activity]

   ## Part 1: AMM Mechanics [markdown explanation + code]
   ## Part 2: Impermanent Loss Calculation [markdown explanation + code]
   ## Part 3: Fee Impact Analysis [markdown explanation + code]

   ## Summary & Reflection
   [Questions for reflection]
   ```

6. **Data and dependencies:**
   - Use small, freely available datasets
   - Avoid API keys in notebooks (use environment variables or mock data)
   - Pin package versions in `requirements.txt`
   - Document data sources

### LaTeX/Beamer Slide Standards

For presentation materials:

1. **Consistency:**
   - Use the Digital Finance color scheme (defined in `template_beamer.tex`)
   - Follow the Madrid theme with customizations
   - Keep font sizes readable (24pt+ for body text)
   - Use consistent terminology across all slides

2. **Structure:**
   - Start each day with overview slide
   - Include clear topic transitions
   - End each section with a summary/reflection slide
   - Use speaker notes for key talking points

3. **Visuals:**
   - Include diagrams for abstract concepts (use TikZ for consistency)
   - Avoid text-heavy slides
   - Use color purposefully (not just decoration)
   - Provide alt text descriptions in comments

4. **Code in slides:**
   - Keep code snippets short (5-10 lines maximum)
   - Use syntax highlighting
   - Explain the code, not just show it

---

## Pull Request Process

### Before Starting

1. **Check for existing work**
   - Search issues and PRs for related discussions
   - Start a discussion if proposing major changes
   - Wait for feedback before significant work

2. **Fork and branch**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Digital-Finance-Introduction.git
   cd Digital-Finance-Introduction
   git checkout -b feature/brief-description
   ```

### Making Changes

1. **Single concern per PR**
   - Fix one issue or add one feature
   - Don't combine unrelated changes

2. **Follow style guides**
   - Python: PEP 8 (use `black` for formatting)
   - LaTeX: Existing beamer template
   - Markdown: Consistent with README.md

3. **Update related materials**
   - If you modify a notebook, update the README.md learning path if needed
   - If you fix slide content, verify notebooks reference it correctly
   - Update version date if making substantial changes

4. **Test thoroughly**
   - Run notebooks end-to-end (they should execute without errors)
   - Check all links (internal and external)
   - Verify accessibility (contrast, alt text, semantic structure)
   - Check for typos and clarity

### Submitting a PR

1. **Write a descriptive PR title**
   ```
   Good: "Add explanation of impermanent loss calculation in Day 4.2"
   Bad: "Fix stuff"
   ```

2. **Include PR description:**
   ```markdown
   ## What This PR Does
   [Concise summary of changes]

   ## Why This Change
   [Problem it solves or improvement it makes]

   ## Type of Change
   - [ ] Bug fix (fixes an issue without changing functionality)
   - [ ] Enhancement (adds a feature or improves something)
   - [ ] Content improvement (clearer explanations, better examples)
   - [ ] Accessibility fix
   - [ ] Documentation update

   ## Specific Changes
   - [What changed, where]
   - [What changed, where]

   ## Related Issue
   Closes #[issue number] (if applicable)

   ## Testing
   [How you tested this, especially for notebooks]

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Changes are well-documented
   - [ ] No unnecessary dependencies added
   - [ ] Notebooks run without errors
   - [ ] Links verified
   - [ ] Accessibility standards met
   ```

3. **Respond to reviews**
   - Respond to all feedback promptly
   - Ask questions if feedback is unclear
   - Update PR based on feedback
   - Thank reviewers (they're helping make the course better)

### PR Review Process

The maintainers will review for:

- **Accuracy** — Content must be technically correct
- **Alignment** — Changes must fit the course philosophy and structure
- **Accessibility** — All materials must be accessible
- **Clarity** — Explanations should be understandable to the target audience
- **Completeness** — Related materials should be updated

Expect 3-7 days for initial review on typical PRs.

---

## Commit Conventions

Follow semantic commit messages:

```
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types

- **feat**: A new feature (e.g., new notebook)
- **fix**: Bug fix (e.g., broken link, typo)
- **docs**: Documentation changes
- **style**: Code style (formatting, missing semicolons, etc.)
- **refactor**: Code reorganization without feature change
- **test**: Adding or updating tests
- **chore**: Build, dependencies, or config updates

### Examples

```bash
# Good commits
git commit -m "feat(day-4): Add stablecoin de-peg risk analysis to NB10"
git commit -m "fix(day-2): Correct API endpoint URL in BaaS explanation"
git commit -m "docs(contributing): Update notebook standards section"
git commit -m "style(slides): Reformat code blocks for consistency"

# Avoid
git commit -m "updated stuff"
git commit -m "WIP"
```

### Scope

Use day/section for scope:
- `day-1`, `day-2`, etc.
- `slides` (for presentation materials)
- `notebooks` (for Colab notebooks)
- `docs` (for documentation)

---

## Local Development

### Setting Up Your Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Digital-Finance-Introduction.git
   cd Digital-Finance-Introduction
   ```

2. **Install dependencies** (for local notebook development)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Verify setup**
   ```bash
   python -c "import numpy, pandas, web3; print('Setup successful')"
   ```

### Testing Locally

**For notebooks:**
```bash
# Convert notebook to Python, run it
jupyter nbconvert --to python NB01-Ledger-Simulation.ipynb
python NB01-Ledger-Simulation.py
```

**For slides:**
- Open in your LaTeX editor (Overleaf recommended for collaboration)
- Compile with `pdflatex` or `xelatex`
- Verify formatting and accessibility

**For HTML/web materials:**
- Open `index.html` in a browser
- Test navigation, links, and responsive layout

### IDE/Editor Recommendations

- **Notebooks**: Jupyter Lab or Google Colab
- **LaTeX**: Overleaf (cloud) or TeXShop/MiKTeX (local)
- **Python files**: VS Code, PyCharm, or Sublime Text
- **Markdown**: VS Code or iA Writer
- **HTML**: VS Code with Live Server extension

### Useful Tools

- **Code formatting**: `black` for Python
- **Linting**: `pylint` or `flake8` for Python
- **Spell check**: `aspell` or built-in editor spell checkers
- **Accessibility**: WAVE, Axe DevTools, or Lighthouse

---

## License

All contributions are licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**.

When you contribute, you agree that:
- Your contributions may be used and modified by others
- Attribution to you is provided (in commit history and/or acknowledgments)
- The entire course remains under CC-BY-4.0

### Attribution

If you make substantial contributions (new notebook, major content addition, etc.), you'll be acknowledged in:
- The course README
- The GitHub Pages site
- Slide credits (if applicable)

---

## Getting Help

### Questions About Contributing

- Check this guide first
- Search existing issues and discussions
- Start a GitHub discussion

### Questions About Course Content

- Open an issue with the label "question"
- Post in GitHub Discussions
- Include which day/topic you're asking about

### Contact

For sensitive matters or direct contact:
- Reach out to the course maintainer via GitHub
- Respect response time (maintainers are volunteers)

---

## Recognition

Contributors help improve this course for future learners. We recognize contributions through:

- **Commit attribution** (automatic from Git)
- **README acknowledgments** (for significant contributions)
- **Pull request feedback** (thanking contributors publicly)
- **Issue resolution** (crediting those who identified problems)

Thank you for making digital finance education better!

---

**Last Updated:** 2026-01-28
**Version:** 1.0
