# 🛡️ AuditMind – Smart Contract Risk Intelligence Agent

AuditMind is an autonomous smart contract auditor built with Fetch.ai’s uAgents framework and powered by the ASI1-mini LLM. It automatically analyzes Ethereum smart contracts to detect potential risks, attack vectors, behavioral patterns, and import vulnerabilities. Results are presented in a user-friendly Streamlit UI and are exportable as PDF/CSV reports.

---

## 🔍 Problem Statement

Smart contract users and investors often struggle with:

- ⚠️ Understanding what a contract actually does
- ❌ Identifying hidden mint, burn, or backdoor functions
- 🧨 Detecting potential rug pulls or centralization risks
- 🧠 Interpreting security from the source code without prior expertise

Even developers and auditors need a fast, intelligent assistant to summarize risks and simulate exploit possibilities. AuditMind solves this by combining a lightweight uAgent with a powerful LLM interface to deliver security intelligence in seconds.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| ✅ **LLM-Powered Code Analysis** | Fetch.ai’s ASI1-mini interprets contract logic and explains it in human-readable form. |
| 🔐 **Risk Score Engine** | Evaluates risk level based on LLM output using keyword mapping and threat heuristics. |
| ⚔️ **Attack Vector Simulator** | Simulates realistic exploit paths using LLM prompt-based attack modeling. |
| 🧬 **Token Behavior Classifier** | Detects if the contract behaves like a utility token, memecoin, stablecoin, or scam. |
| 📦 **Import Vulnerability Detection** | Inspects Solidity imports to check for risky or external dependencies. |
| 💻 **Modern Streamlit UI** | Tabbed layout with responsive design and colored severity boxes. |
| 📄 **PDF / CSV Export** | One-click export for full audit reports and summary tables. |
| 🌐 **Etherscan API Integration** | Fetches verified contract source code across any Ethereum address. |

---

## 🧠 Powered By

- 🧠 **ASI1-mini LLM** via [ASI:One](https://asi1.ai/)
- ⚙️ **uAgents framework** by Fetch.ai
- 📡 **Etherscan API** for smart contract retrieval
- 🛠️ **Streamlit** for interactive web interface
- 📄 `fpdf` and `pandas` for report generation

---

## 🔑 Environment Variables (`.env`)

ASI_API_TOKEN=sk_... # Fetch.ai LLM key
AGENT_SEED=test-agent://... # Agent seed
ETHERSCAN_API_KEY=... # Etherscan key

---

## 🗺️ Roadmap

### ✅ Phase 1: MVP (Completed)
- [x] Fetch source code from Etherscan
- [x] Analyze via ASI1-mini LLM
- [x] Score risks based on heuristics
- [x] Display results on Streamlit UI
- [x] PDF and CSV report generation

### 🔄 Phase 2: Advanced Modules (Planned)
- [ ] Multi-chain contract fetching (Polygon, BSC via Etherscan V2)
- [ ] Wallet reputation scoring (rug-prone owners)
- [ ] Auto-email PDF report to user
- [ ] Auto-submission to audit registries
- [ ] Live URL deployment (via Streamlit Cloud or Render)

### 💡 Phase 3: Innovation
- [ ] Timeline-based audit: contract evolution across versions
- [ ] Comparative audit: analyze and compare two contracts
- [ ] Risk heatmap visualization with Streamlit charts

---

## 📦 Installation

```bash
git clone https://github.com/bytemaster333/AuditMind
cd AuditMind
pip install -r requirements.txt
streamlit run streamlit_app.py
```
⚠️ Don't forget to create a .env file with your API keys.

## ✨ Author
🛠️ DevOps & Blockchain Infrastructure Engineer
🔗 github.com/bytemaster333
