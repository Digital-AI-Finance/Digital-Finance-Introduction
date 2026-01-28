# Digital Finance Course: Frequently Asked Questions

A comprehensive guide to common questions about the Digital Finance course structure, technical setup, and content. If you can't find an answer here, check the [CONTRIBUTING.md](../CONTRIBUTING.md) for contact information.

---

## General Questions

### Do I need programming experience?

**No.** This course is specifically designed for students from any disciplinary background with no assumed prerequisites in programming, mathematics, or finance.

**What this means for you:**
- All notebooks are pre-written; you don't write code
- You interact with code by running cells, modifying parameters, and analyzing outputs
- Complex concepts are explained from first principles
- Technical terms are defined on first use

**What helps (but isn't required):**
- Basic comfort with digital tools and web browsers
- General curiosity about how technology and finance work
- Willingness to learn new concepts

If you find yourself confused, that's normal—reach out to your instructor or review the relevant day's lecture slides to build context.

---

### What software do I need?

**For the course:** You only need a **web browser and a Google account** (free).

**What you'll use:**
- **Google Colab** — To run interactive notebooks. No installation needed; everything runs in the cloud
- **PDF reader** — To view lecture slides (any browser can do this)
- **GitHub account** (optional) — To access course materials and suggest improvements

**If you want to work locally** (advanced, optional):
- Python 3.9 or later
- Jupyter Notebook or Jupyter Lab
- The packages listed in `requirements.txt` (install via `pip install -r requirements.txt`)

For 99% of students, just use Google Colab—it's free and requires nothing to install.

---

### How do I access the notebooks?

**Via Google Colab (recommended):**
1. Go to the course website: https://joerg-osterrieder.github.io/Digital-Finance-Introduction/
2. Find the day and notebook you want to run
3. Click the Colab link (usually labeled "Open in Colab")
4. The notebook opens in Google Colab in your browser
5. Sign in with your Google account if prompted
6. Click cells and press **Shift+Enter** to run them

**Alternative:**
- Clone or download the course repository from GitHub
- Upload notebooks to Google Colab manually
- Or run locally with Jupyter (see "What software do I need?")

**Pro tip:** Google Colab saves your work, but only in Google Drive if you explicitly save it. If you want to keep your work, save a copy to Drive after running a notebook.

---

### What if I don't have a Google account?

Create one for free at https://accounts.google.com/. It takes 5 minutes and is used only for Google Colab; no special permissions needed.

---

## Technical Setup

### The notebook won't run — what do I do?

**First, check these common issues:**

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: No module named..." | First cell usually installs dependencies. Run it and wait. If still broken, refresh page and try again. |
| Notebook is very slow | Google Colab is sometimes congested. Wait a few minutes or try again later. |
| Cells show old output | Click **Runtime > Restart runtime** (top menu), then re-run cells from top. |
| Colab asks about "untrusted notebook" | Click **"Run anyway"** — these are course materials. |
| Code cells won't run at all | Refresh the page in your browser and try again. |

**If the problem persists:**
1. Check the course GitHub Issues page for your specific error
2. Post your error message in the course discussion or contact your instructor
3. Include: What notebook? What cell? What's the exact error message?

---

### How do I install Python packages?

**In Google Colab:**
Most notebooks handle this automatically in the first cell with:
```python
!pip install numpy pandas web3
```

If you need to install a package manually:
```python
!pip install package_name
```

Then immediately run the next cell that imports it.

**Locally (using Python):**
```bash
# First-time setup:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install all course dependencies:
pip install -r requirements.txt

# Or install individual packages:
pip install web3 numpy pandas
```

**Key packages for this course:**
- `web3` — For blockchain interaction
- `numpy`, `pandas` — For data analysis
- `matplotlib`, `seaborn`, `plotly` — For visualization
- `scikit-learn` — For machine learning (credit scoring model)
- `requests` — For API calls

---

### What if a blockchain API or external service is down?

**Common issues:**
- **Infura API down** — Some notebooks use Infura to access Ethereum. If it's down, notebooks that call `web3.eth.get_block()` will fail
- **Etherscan down** — Some notebooks fetch data from Etherscan. Check their status page
- **External data sources** — Notebooks that fetch live crypto prices or market data may fail if the source is temporarily unavailable

**What to do:**
1. Check if the service is actually down (search "Infura status" or visit https://status.infura.io/)
2. Try again in 5-10 minutes
3. If your instructor provided mock data, use that instead
4. Contact your instructor if it stays down; we can provide fallback datasets

**Note:** This course is designed to work without live APIs when necessary. Notebooks include fallback data where appropriate.

---

### Do I need to be connected to the internet?

**For Google Colab:** Yes, you must be online. Colab requires internet to function.

**For local Python (offline work):** After installing packages, you can work offline on notebooks that don't need external APIs. Notebooks that fetch blockchain data, crypto prices, or market data will fail offline.

---

## Course Content

### What's the difference between FinTech and DeFi?

**Short version:**

| FinTech | DeFi |
|---------|------|
| Improves existing finance using technology | Rebuilds finance from scratch using blockchain |
| Works within regulations and existing financial system | Often operates outside traditional regulatory frameworks |
| Examples: Stripe, Revolut, Robinhood, Apple Pay | Examples: Uniswap, Aave, MakerDAO |
| Requires trust in companies | Trust is replaced by cryptography and code |
| Centralized (companies control the system) | Decentralized (code controls the system) |

**Both matter:** Day 2 covers FinTech. Days 3-4 cover DeFi/blockchain. Day 6 explores how they're converging (e.g., traditional banks building blockchain infrastructure).

**Key insight from the course:** This is not a "crypto vs. banks" fight. They're two different philosophies addressing similar problems.

---

### Do I need to buy cryptocurrency?

**No.** You will not spend any real money in this course.

**What you will do:**
- **Testnet transactions** — Use free testnet ETH (fictional money) to simulate blockchain transactions
- **Read real blockchain data** — We analyze actual Ethereum blockchain data, but just read it; we don't execute transactions
- **Simulate DeFi operations** — Notebooks simulate how lending pools and AMMs work without you trading

**If you're curious about buying crypto later:**
- That's outside the scope of this course
- The course gives you knowledge to evaluate it critically
- Always be cautious and never invest more than you can afford to lose

---

### Is this course about investing advice?

**No.** This is **not** an investment course. We do not recommend you buy or sell any assets.

**What we do cover:**
- How financial technologies work
- How to evaluate financial products critically
- The risks and limitations of different systems
- Real examples of what went wrong and why

**What we don't do:**
- Recommend specific investments
- Make price predictions
- Tell you how to get rich
- Promote any cryptocurrency or company

The course develops your ability to understand and critique digital finance, not to make investment decisions.

---

### Will this course make me an expert in blockchain?

No, but it will give you a solid mental model of how blockchain works and what it can and can't do.

**By the end, you'll be able to:**
- Explain blockchain mechanics to a non-technical person
- Evaluate blockchain solutions critically
- Understand security and design tradeoffs
- Read and understand smart contract code (at a high level)
- Identify hype vs. substance in crypto projects

**You won't be able to:**
- Become a blockchain developer (that requires months of coding practice)
- Build production smart contracts
- Become a security auditor
- Predict which projects will succeed

This is education for critical thinking, not vocational training.

---

## Blockchain Specific

### What is a testnet vs mainnet?

**Mainnet** = Real blockchain with real money. Transactions cost real Ether (ETH) or whatever the native token is. Mistakes are permanent.

**Testnet** = Fake blockchain for testing and learning. You get free fake Ether. Transactions cost nothing. Data resets periodically. Perfect for learning.

**Why we use testnet:**
- You can't buy testnet ETH; you get it free from a faucet
- No real money is at risk
- You can experiment freely without worrying about losing funds
- Once you understand the testnet, you understand how mainnet works

**Main testnets for Ethereum:**
- **Sepolia** (current, recommended)
- **Goerli** (older, still works)
- **Holesky** (large-scale testing)

Your notebook will specify which testnet to use.

---

### How do I get testnet ETH?

**For Sepolia testnet:**

1. **Get a wallet address** — Generate one using MetaMask or the Web3.py code in the notebook
2. **Go to a faucet** — https://sepoliafaucet.com/
3. **Paste your address** — Check the instructions (may require a GitHub account or login)
4. **Wait a few minutes** — Testnet ETH appears in your address
5. **Verify it arrived** — Check with `web3.eth.get_balance(address)`

**Common faucets:**
- Sepolia: https://sepoliafaucet.com/
- Goerli: https://goerlifaucet.com/

**If a faucet is down:**
- Try a different one (there are usually multiple)
- Wait a few hours
- Contact your instructor for alternative testnet ETH

---

### Are the transactions we make real?

**On testnet:** No. Testnet is a separate copy of the blockchain used only for testing. Testnet transactions don't affect mainnet at all. Your testnet ETH has zero real value.

**On mainnet (if we use it):** We will not execute transactions on mainnet in this course. If any notebook touches mainnet, we only read data—we never write transactions.

**Real transaction example:** In Day 3, you might construct a real Ethereum transaction on paper or in code, but you won't actually broadcast it. You'll analyze what it would do without actually doing it.

**Why this matters:** It's important to understand the difference:
- **Testnet** = Learning without risk
- **Mainnet** = Real money at stake
- **Mock data** = Simulations that don't touch blockchain at all

---

### What's the difference between Bitcoin and Ethereum?

**Bitcoin:**
- First and original blockchain (launched 2009)
- Designed primarily as digital money ("peer-to-peer electronic cash")
- Fixed supply of 21 million coins
- Very secure but limited functionality (mainly transfers)
- Uses Proof of Work (miners solve puzzles)

**Ethereum:**
- Second-generation blockchain (launched 2015)
- Designed to run smart contracts (programmable code)
- No fixed supply (depends on economic policy)
- More flexible; can build complex applications on it
- Uses Proof of Stake (stakers validate blocks)

**Why both matter:**
- Bitcoin = The OG. Teaches trust through cryptography.
- Ethereum = Enables DeFi, NFTs, and complex applications.

The course covers Bitcoin conceptually (Day 1) and Ethereum technically (Days 3-4).

---

## Assessments & Grading

### How is the course graded?

This depends on your institution. This course is designed to be flexible.

**Possible assessment approaches:**
- **Attendance** — Show up for all 6 days
- **Participation** — Engage with lectures and discussions
- **Hands-on work** — Complete the 14 Colab notebooks
- **Capstone project** — Day 6 includes an "Innovation Scorecard" analysis (may be graded)
- **Reflection assignments** — Think-piece on a digital finance topic

**Your instructor decides.** Check your course syllabus or ask your instructor for the specific grading scheme.

**Key principle:** This course prioritizes understanding over memorization. We care that you can think critically about digital finance, not that you memorize blockchain mechanics.

---

### Can I work in groups?

**Yes, collaboration is encouraged.**

**How to work together:**
- **Study together:** Discuss concepts, help each other understand
- **Share notebooks:** Google Colab allows real-time collaboration; click "Share" to invite others
- **Discuss findings:** Compare results and debate interpretations

**Important boundaries:**
- Each person should engage with the material personally
- Don't just copy someone else's work
- Acknowledge contributions (e.g., "I worked on this with Sarah")
- Your instructor may require individual submissions

**Best practice:** Work together to understand concepts. Do the analysis individually (or clearly state collaboration).

---

### What if I fall behind?

**This is a 6-day intensive course.** Missing even one day creates gaps because material builds sequentially.

**If you miss a day:**
1. **Watch the recording** (if available) or **ask your instructor for materials**
2. **Read the lecture slides** for that day
3. **Skim the glossary** to learn key terms
4. **Do the notebooks** for that day (they're mostly self-contained)
5. **Talk to classmates** for context you missed
6. **Reach out to your instructor** if you're lost

**If you need to miss:**
- Tell your instructor as soon as possible
- Don't wait until after the course
- Your instructor may adjust expectations or offer catch-up sessions

---

## Frequently Misunderstood Topics

### "Smart contracts are truly 'trustless'"

Actually, smart contracts still require trust, just in different places:
- **Trustless element:** No need to trust the company running the code (the blockchain enforces it)
- **Trust required in:** The code itself (bugs are unfixable), the oracle data (if it's wrong, code acts on wrong info), the validators (they could theoretically conspire)

**Example:** A lending protocol is "trustless" in that you don't trust the company, but you do trust that the code was audited correctly.

---

### "Blockchain solves everything"

Blockchains solve specific problems (decentralized consensus, censorship resistance) but create others:
- **What blockchains are good for:** Transparent records, preventing double-spending, enabling strangers to cooperate without intermediaries
- **What blockchains are bad for:** Speed, privacy, handling mistakes, updating logic

**Key insight:** Blockchain is a tool. Some problems need it; most don't.

---

### "All crypto is a scam"

Wrong. But not all crypto is legitimate either.

**Reality:**
- Some cryptocurrency projects are genuinely useful (Bitcoin for censorship-resistant transfers, Ethereum for programmable contracts)
- Many are over-hyped or pure scams
- The difficulty is distinguishing between them—which is exactly what this course teaches
- Just because something uses blockchain doesn't make it valuable

---

### "You have to be a programmer to understand this"

False. Programming helps but isn't required.

This course explains concepts first, then shows the code. You see what the code does without needing to write it. It's like understanding how a car works without being a mechanic.

---

## Getting Help

### Where do I ask questions?

1. **Check this FAQ first** — Your question might be answered here
2. **Check the GitHub Issues** — Your question might have been asked before
3. **Review relevant slides** — Re-read the material for that topic
4. **Ask your instructor** — During class, office hours, or via email
5. **Ask classmates** — Discuss with peers; collaborative learning helps everyone
6. **Post on GitHub Discussions** — If you think the course materials need clarification

### I found an error in the course materials

**Thank you!** Errors make the course worse for everyone.

Report it:
1. Check GitHub Issues to see if it's already reported
2. **If it's a bug (broken link, code error):** Open an Issue with the label "bug"
3. **If it's unclear content:** Open an Issue with the label "documentation"
4. **Include:** What's wrong? Where is it? What did you expect?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed bug reporting guidelines.

### The course is too fast/too slow

**Let your instructor know.** The course is designed to be flexible.

- **Too fast?** Ask for more time on specific topics or slow-down activities
- **Too slow?** Ask for additional advanced materials or accelerated content

Different cohorts have different needs—feedback helps instructors adapt.

---

## Course Logistics

### What time do classes meet?

This depends on your institution. Check your course schedule or ask your instructor.

This is a **6-day intensive course**, so plan for full-day attendance each day.

---

### What if I have a disability or accessibility need?

**Tell your instructor immediately.** The course materials were designed with accessibility in mind:

**We provide:**
- Markdown slides (accessible text)
- Code notebooks with explanations
- Glossaries and references
- No visual-only content

**Let us know if you need:**
- Additional time for notebooks
- Alternative formats
- Captions for any videos
- Other accommodations

Your institution's accessibility office can also help formalize accommodations.

---

### Can I use this course for my own teaching?

**Yes!** This course is licensed under **Creative Commons Attribution 4.0 (CC-BY-4.0)**.

You can:
- Use the materials
- Adapt and modify them
- Teach your own version
- Create derivatives

**You must:**
- Give credit to Joerg Osterrieder (the original instructor)
- License your version under CC-BY-4.0 as well

See the [LICENSE](../LICENSE) file for full details.

---

## Common Troubleshooting

| Issue | Solution |
|-------|----------|
| "The notebook says it can't find module X" | Run the first cell (usually contains pip install commands) and wait 1 minute. Refresh if needed. |
| "Colab keeps crashing" | You may have hit a memory limit. Restart the runtime (**Runtime > Restart runtime**) and run cells more slowly. |
| "The API call timed out" | The external service may be down. Wait 5 minutes and try again. Check service status pages. |
| "My changes didn't save" | Google Colab only saves to Drive if you explicitly save. Use **File > Save a copy to Drive** to preserve your work. |
| "I got a strange error I don't understand" | Copy the entire error message and search GitHub Issues for it. If not found, post it. |
| "My notebook is running very slowly" | Colab may be congested. Try at a different time or use a local Python environment. |

---

## Still Can't Find an Answer?

1. **Check the course website:** https://joerg-osterrieder.github.io/Digital-Finance-Introduction/
2. **Review CONTRIBUTING.md:** Has more details on reporting issues
3. **Check the glossary:** https://docs.github.com/en/site-policy/github-terms/github-glossary (linked in README.md)
4. **Ask on GitHub Discussions** under the course repository
5. **Contact your instructor** directly

---

## Final Thoughts

This is a challenging but rewarding course. You're learning about technologies shaping the future of finance. Questions are good—they mean you're thinking critically.

**Key principle:** There are no stupid questions. If something's unclear, ask. That's how we all learn.

**You've got this.**

---

**Last Updated:** 2026-01-28

**Course Instructor:** Joerg Osterrieder

**Course License:** CC-BY-4.0
