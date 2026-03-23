# 🛡️ Sentinel MEV Dashboard & Trading Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Ethereum-Web3.py-lightgrey" alt="Ethereum">
  <img src="https://img.shields.io/badge/Flashbots-Integration-orange" alt="Flashbots">
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/Security-Smart%20Contracts-success" alt="Security">
</p>

**Sentinel** is a high-performance, real-time algorithmic trading bot designed specifically for discovering and executing **Maximal Extractable Value (MEV)** opportunities on Ethereum and EVM-compatible blockchains. Paired with a sleek **Streamlit Dashboard**, it tracks live mempool transactions, analyzes token sentiment via local AI models, and securely executes strategies like sandwich attacks and arbitrage leveraging Flashbots bundles.

---

## 🏗️ Architecture Stack

- **Core Blockchain Execution**: `Web3.py` equipped with asynchronous WebSocket-based Mempool listeners.
- **MEV Strategies**: Automated direct-to-miner bundle submission via **Flashbots** (encompassing Sandwich Attacks, Front-running, Arbitrage).
- **Data Persistence**: `SQLite` + `SQLAlchemy` for caching DEX/Pool Reservers, trade history, and statistical performance.
- **Machine Learning Analysis**: Local **Ollama LLM** inference to dynamically monitor project sentiment and identify honeypots or malicious tokens on-the-fly.
- **Unified API Engine**: `FastAPI` powering headless data-serving and internal microservices.
- **Analytics Dashboard**: `Streamlit` powering an intuitive and real-time visualization layer to monitor bot ROI and live executions.

---

## ✨ Features

- **Blazing Fast Mempool Scanner**: Async-native architecture monitors pending transactions for actionable spread opportunities.
- **Flashbots Compatibility**: Secures capital and guarantees atomic execution without gas wars. Failed transactions will not land on-chain, eliminating lost gas costs.
- **AI-Powered Token Screening**: Integrated LLM models perform rapid sentiment and risk-checking on newly identified tokens before capital is deployed.
- **Live Strategy Backtester**: Test strategies locally using historical block states before risking live assets.
- **Headless & UI Operation**: Run the bot via API, command line, or visualize ongoing operations using the unified Streamlit interface.

---

## 📂 Directory Structure

```text
mev-trading-bot/
├── api/                    # FastAPI Headless endpoints for interacting with the bot
├── backtester/             # Historical mempool strategy backtesting engine
├── config/                 # Pydantic-powered environment configurations
├── core/
│   ├── ethereum/           # Web3 RPC connections, Flashbots integration, Smart Contracts
│   ├── mempool/            # Async Websocket Pending TX listener
│   └── strategies/         # Strategy execution algorithms (e.g., Sandwich, Arbitrage)
├── dashboard/              # Streamlit Web UI for real-time tracking
├── db/                     # SQLAlchemy models and SQLite Database schema
├── logs/                   # System and transaction runtime logs
├── ml/                     # Machine learning module (Ollama Inference / Sentiment analysis)
├── models/                 # Pre-trained ML weights and LLM configs
├── scripts/                # Utility scripts and database migrations
└── tests/                  # Pytest Unit & Integration testing framework
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites 
Ensure that you have **Python 3.10+** installed on your system. You will also need access to an Ethereum node URL (WSS) such as Alchemy, Infura, or a local Erigon/Geth node.

### 2. Install Dependencies
Clone the repository and install the necessary Python packages:

```bash
git clone https://github.com/vrushabhzade/Sentinel-MEV-Dashboard.git
cd Sentinel-MEV-Dashboard
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the sample environment file to configure your keys and API endpoints:

```bash
cp .env.example .env
```
*Note: Make sure to properly configure your Web3 WS/HTTP endpoints, as well as your Flashbots signer key.*

### 4. Execution
The system uses a unified CLI entry point via `main.py`. You can execute different components simultaneously or individually:

**Run the Core MEV Execution Bot (Mempool Scanner):**
```bash
python main.py --mode bot
```

**Run the FastAPI Headless Data Server:**
```bash
python main.py --mode api
```

**Launch the Streamlit Analytics Dashboard:**
```bash
python main.py --mode dashboard
```

*(You can open up multiple terminals to run the bot, api, and dashboard concurrently).*

---

## 🛡️ Smart Contract Security

The execution layer heavily relies on Smart Contracts (located inside `core/ethereum/contracts/`). 

> [!WARNING]
> **Always** deploy and utilize a specialized Smart Contract to bundle your atomic swap transactions. **Never** execute multi-step MEV logic from an Externally Owned Account (EOA) directly into the public mempool without a Flashbots relay. Doing so exposes your transaction to generalized front-runners.

---

## 🧪 Testing

A sturdy test suite is available. Before running the bot with real capital on Mainnet and executing live trades, always run the pytest suite to validate system logic locally:

```bash
pytest
```

---

*Disclaimer: MEV trading carries significant financial risk. This software is provided "as is", without warranty of any kind. You operate this bot entirely at your own risk.*
