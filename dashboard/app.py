import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Layout and Theming ---
st.set_page_config(page_title="MEV Sentinel - Advanced Terminal", layout="wide", page_icon="🧿")

# Advanced Custom CSS injected into Streamlit
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');

    /* Global Body and Fonts */
    html, body, [class*="css"]  {
        font-family: 'Rajdhani', sans-serif !important;
        background-color: #0b0f19 !important;
        color: #e2e8f0;
    }
    
    /* Glowing Title */
    .glow-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 56px;
        font-weight: bold;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0,240,255,0.5), 0 0 20px rgba(0,240,255,0.3);
        margin-bottom: -15px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Subtext Styling */
    .terminal-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #8b9bb4;
        font-size: 18px;
        margin-bottom: 30px;
        border-bottom: 1px solid #1a2333;
        padding-bottom: 20px;
    }

    /* Metric Cards Customization */
    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        color: #00f0ff !important;
        font-family: 'Share Tech Mono', monospace;
    }
    [data-testid="stMetricLabel"] {
        font-size: 16px !important;
        color: #a0aec0 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Custom Cards */
    .cyber-card {
        background: linear-gradient(145deg, #111827 0%, #0d131f 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border-left: 4px solid #00f0ff;
        transition: transform 0.2s;
    }
    .cyber-card:hover {
        transform: translateY(-5px);
        border-left: 4px solid #ff0055;
        box-shadow: 0 8px 32px 0 rgba(255, 0, 85, 0.2);
    }
    
    .card-title {
        font-size: 14px;
        color: #64748b;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .card-value {
        font-size: 28px;
        color: white;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Custom Table Styling */
    .cyber-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
    }
    .cyber-table th {
        background-color: #1a2333;
        color: #00f0ff;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #00f0ff;
        text-transform: uppercase;
    }
    .cyber-table td {
        padding: 12px;
        border-bottom: 1px solid #1e293b;
        color: #cbd5e1;
    }
    .cyber-table tr:hover {
        background-color: #151d2b;
    }
    .badge-exec {
        background-color: rgba(0, 240, 255, 0.1);
        color: #00f0ff;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #00f0ff;
    }
    .badge-ignore {
        background-color: rgba(255, 0, 85, 0.1);
        color: #ff0055;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #ff0055;
    }
    .badge-frontrun {
        background-color: rgba(255, 204, 0, 0.1);
        color: #ffcc00;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #ffcc00;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="glow-title">🧿 M.E.V. COMMAND TERMINAL</p>', unsafe_allow_html=True)
st.markdown('<p class="terminal-sub">System Status: ONLINE | Node WSS: CONNECTED | Block: 19483012</p>', unsafe_allow_html=True)

# --- Navigation Tabs ---
tab1, tab2, tab3 = st.tabs(["[ 🛰️ RADAR_OVERVIEW ]", "[ 📡 LIVE_MEMPOOL ]", "[ 🧠 AI_NEURAL_NET ]"])

# --- Helper Data Generators ---
def get_mock_profit_data():
    dates = pd.date_range(end=pd.Timestamp.now(), periods=40, freq='D')
    profits = np.cumsum(np.random.normal(loc=0.3, scale=0.8, size=40))
    profits = np.maximum(profits, 0)
    return pd.DataFrame({'Date': dates, 'Profit (ETH)': profits}).set_index('Date')

# --- TAB 1: OVERVIEW ---
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Custom HTML Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">NET 30D REVENUE</div>
                <div class="card-value">28.45 ETH</div>
                <div style="color: #00f0ff; font-size:12px; margin-top:5px;">▲ 14.2% from last month</div>
            </div>
        ''', unsafe_allow_html=True)
    with m2:
        st.markdown('''
            <div class="cyber-card" style="border-left-color: #ffcc00;">
                <div class="card-title">SANDWICHES EXECUTED</div>
                <div class="card-value">1,402 Tx</div>
                <div style="color: #ffcc00; font-size:12px; margin-top:5px;">Avg ROI: 0.02 ETH / Tx</div>
            </div>
        ''', unsafe_allow_html=True)
    with m3:
        st.markdown('''
            <div class="cyber-card" style="border-left-color: #ff0055;">
                <div class="card-title">REVERTED/FAILED</div>
                <div class="card-value">12 Tx</div>
                <div style="color: #ff0055; font-size:12px; margin-top:5px;">Failure Rate: < 0.8%</div>
            </div>
        ''', unsafe_allow_html=True)
    with m4:
        st.markdown('''
            <div class="cyber-card" style="border-left-color: #00f0ff;">
                <div class="card-title">LATENCY / RPC PING</div>
                <div class="card-value">14 ms</div>
                <div style="color: #00f0ff; font-size:12px; margin-top:5px;">Flashbots Relay: 42ms</div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br><br><h4 style='font-family:Rajdhani; color:#8b9bb4; text-transform:uppercase;'>Cumulative Extracted Value (ETH)</h5>", unsafe_allow_html=True)
    chart_data = get_mock_profit_data()
    st.line_chart(chart_data, color="#00f0ff", height=300)

# --- TAB 2: LIVE MEMPOOL ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("<h4 style='font-family:Rajdhani; color:#8b9bb4;'>Pending Transactions Target Lock</h4>", unsafe_allow_html=True)
        
        # Simulated delay for realistic radar scanning effect
        with st.spinner("Intercepting Mempool Payload..."):
            time.sleep(0.6)
            
        # Custom HTML table for ultimate styling
        table_html = """
        <table class="cyber-table">
            <tr>
                <th>Hash Sig</th>
                <th>DEX Intercepted</th>
                <th>Slippage</th>
                <th>Calculated MEV</th>
                <th>AI Decision</th>
            </tr>
            <tr>
                <td>0x8f...1c9</td><td>Uniswap V3</td><td>> 5.2%</td><td style="color:#00f0ff;">+0.45 ETH</td>
                <td><span class="badge-exec">SANDWICH_EXEC</span></td>
            </tr>
            <tr>
                <td>0x2a...bb4</td><td>SushiSwap</td><td>2.0%</td><td style="color:#ffcc00;">+0.05 ETH</td>
                <td><span class="badge-frontrun">FRONTRUN</span></td>
            </tr>
            <tr>
                <td>0x99...e22</td><td>Curve Fin</td><td>0.1%</td><td style="color:#ff0055;">-0.02 ETH</td>
                <td><span class="badge-ignore">IGNORED</span></td>
            </tr>
            <tr>
                <td>0x1b...55f</td><td>Uniswap V2</td><td>14.0%</td><td style="color:#00f0ff;">+2.10 ETH</td>
                <td><span class="badge-exec">SANDWICH_EXEC</span></td>
            </tr>
            <tr>
                <td>0xaf...cc1</td><td>Balancer</td><td>1.1%</td><td style="color:#ffcc00;">+0.01 ETH</td>
                <td><span class="badge-frontrun">FRONTRUN</span></td>
            </tr>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    with col_b:
        st.markdown("<h4 style='font-family:Rajdhani; color:#8b9bb4;'>Flashbots Flash-Relay</h4>", unsafe_allow_html=True)
        st.markdown('''
        <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #1e293b;">
            <p style="color:#00f0ff; margin:0; font-family:'Share Tech Mono';">=> BUNDLE COMPILED</p>
            <p style="color:#cbd5e1; font-size:12px;">TARGET BLOCK: 19483013</p>
            <p style="color:#cbd5e1; font-size:12px; margin-bottom:5px;">[FRONTRUN] Tx_a9...12</p>
            <p style="color:#ff0055; font-size:12px; margin-bottom:5px;">[VICTIM]   Tx_b1...88</p>
            <p style="color:#00f0ff; font-size:12px; margin-bottom:5px;">[BACKRUN]  Tx_c3...90</p>
            <hr style="border-color:#1e293b;">
            <p style="color:#ffcc00; font-size:12px;">MINER BRIBE: 0.05 ETH</p>
            <p style="color:#00f0ff; font-weight:bold;">EST. PROFIT: 2.05 ETH</p>
        </div>
        ''', unsafe_allow_html=True)

# --- TAB 3: NEURAL NET / ML ---
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-family:Rajdhani; color:#8b9bb4; margin-bottom: 20px;'>Ollama Local NLP Inference Engine</h4>", unsafe_allow_html=True)
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.markdown('''
        <div style="background-color: #0b0f19; padding: 20px; border-radius: 8px; border: 1px dashed #00f0ff;">
            <h5 style="color:#00f0ff; font-family:'Share Tech Mono';">RAW DATA INTERCEPT: TGRAM / DISCORD</h5>
            <p style="color:#8b9bb4; font-family:monospace;">
            > Parsing new message channel ID #alpha-calls...<br><br>
            "Just aped heavily into $DOGE4! Liquidity is locked for 6 months, CA looks incredibly clean and no mint function. Dev renounced! Sending this to 10M mcap tonight."
            </p>
        </div>
        ''', unsafe_allow_html=True)

    with col_y:
        st.markdown('''
        <div style="background-color: #111827; padding: 20px; border-radius: 8px; border-left: 4px solid #ffcc00;">
            <h5 style="color:#ffcc00; font-family:'Share Tech Mono';">LLM PREDICTION MATRIX</h5>
            <pre style="color:#00f0ff; background: transparent; border: none; font-size: 14px; margin:0;">
{
    "ticker": "DOGE4",
    "sentiment": "EXTREME_BULLISH",
    "honeypot_risk_score": "2/10",
    "contract_audits": {
        "mint_function": "false",
        "renounced": "true",
        "liquidity_lock": "detected"
    },
    "mev_directive": "INITIATE_SNIPER_PROTOCOL",
    "confidence_interval": "94.2%"
}
            </pre>
        </div>
        ''', unsafe_allow_html=True)
