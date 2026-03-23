# 📈 Maximal Extractable Value (MEV) Trading Bot

A high-performance algorithmic trading bot designed to detect and execute MEV opportunities on Ethereum and EVM-compatible blockchains. Built with a modern Python stack and backed by local AI inference.

## 🏗️ Architecture Stack
- **Core Blockchain**: Web3.py with async WSS Mempool Listening
- **Strategies**: Flashbots Bundle Submission (Sandwich Attacks, Arbitrage)
- **Database**: SQLite + SQLAlchemy (for caching Pool Reserves and Trade History)
- **Machine Learning**: Local Ollama LLM integration (Sentiment & Honeypot Risk)
- **Dashboard**: Streamlit (Real-time analytics and statistics)
- **API Engine**: FastAPI (Headless data serving)

## 📂 Directory Structure
```
mev-trading-bot/
├── api/                    # FastAPI Headless endpoints
├── backtester/             # Historical mempool strategy backtesting
├── config/                 # Pydantic environment configurations
├── core/
│   ├── ethereum/           # Web3 connections, Flashbots, Solidity Contracts
│   ├── mempool/            # Async Websocket Pending TX listener
│   └── strategies/         # Strategy execution algorithms (e.g. Sandwich)
├── dashboard/              # Streamlit Web UI
├── db/                     # SQLAlchemy models and SQLite Database
├── logs/                   # System runtime log files
├── ml/                     # Machine learning (Ollama Inference / Sentiment)
├── models/                 # Pre-trained ML weights (if applicable)
├── scripts/                # Utility scripts 
└── tests/                  # Pytest Unit & Integration testing
```

## 🚀 Quick Start

### 1. Install Dependencies
Ensure you have Python 3.10+ installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to a new `.env` file and insert your configuration details:
```bash
cp .env.example .env
```
_You will need a WSS endpoint (from Infura, Alchemy, or a local node) to read the Mempool!_

### 3. Execution
The system uses a unified CLI entry point via `main.py`. You can run different components of the architecture concurrently:

**Run the MEV Bot (Mempool Scanner & Execution):**
```bash
python main.py --mode bot
```

**Run the FastAPI Server:**
```bash
python main.py --mode api
```

**Run the Streamlit Analytics Dashboard:**
```bash
python main.py --mode dashboard
```

## 🛡️ Smart Contract Security
In `core/ethereum/contracts/SandwichBot.sol`, you'll find the execution layer. **Always** use a Smart Contract to bundle atomic swap transactions. Never execute multi-step MEV logic from an Externally Owned Account (EOA) directly into the public mempool without Flashbots routing.

## 🧪 Testing
Run the Pytest suite to validate logic locally before deploying real capital:
```bash
pytest
```
