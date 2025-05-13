import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from utils import (
    fetch_contract_data,
    calculate_risk_score,
    generate_attack_vector,
    classify_token_behavior,
    analyze_import_risks,
    analyze_with_llm
)
from llm import OpenLLM
from report_generator import generate_pdf_report, generate_csv_report

# Ortam değişkenlerini yükle
load_dotenv()
llm = OpenLLM()

# Sayfa ayarları
st.set_page_config(page_title="🛡️ AuditMind", layout="wide")

# Stil kutusu
def colored_box(text, color):
    st.markdown(
        f"""
        <div style='padding: 1rem; border-radius: 12px; background-color: {color}; color: white; font-size: 16px; text-align: center; font-weight: 600;'>
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Sayfa başlığı
st.markdown(
    """
    <h1 style='text-align: center; color: #1abc9c;'>🛡️ AuditMind</h1>
    <p style='text-align: center; font-size:18px;'>Analyze Ethereum smart contracts using Fetch.ai’s ASI1-mini LLM and get full risk insights.</p>
    """,
    unsafe_allow_html=True
)

# Adres formu
with st.form("contract_form"):
    st.markdown("### 🔎 Enter Smart Contract Address")
    address = st.text_input("Ethereum contract address", placeholder="e.g. 0xdAC17F958D2ee523a2206206994597C13D831ec7")
    submitted = st.form_submit_button("🚀 Analyze Now")

# Form gönderildiyse
if submitted:
    if not address.startswith("0x") or len(address) != 42:
        st.error("❌ Invalid Ethereum contract address.")
    else:
        with st.spinner("⏳ Analyzing contract..."):
            chain = "ethereum"
            code = fetch_contract_data(chain, address)

            if "No contract" in code or "Error" in code:
                st.error(code)
            else:
                analysis = asyncio.run(analyze_with_llm(code, llm))
                score, level = calculate_risk_score(analysis)
                attack_vector = asyncio.run(generate_attack_vector(code, llm))
                token_data = {
                    "total_supply": "1000000",
                    "owner": address,
                    "top_holder_percent": "85"
                }
                token_behavior = asyncio.run(classify_token_behavior(code, token_data, llm))
                import_risks = asyncio.run(analyze_import_risks(code, llm))

                # Sekmeli içerik
                tabs = st.tabs(["📝 Summary", "⚔️ Attack Vector", "🧬 Behavior", "📦 Imports", "📊 Risk Score"])

                with tabs[0]:
                    st.subheader("📝 Contract Summary")
                    st.text_area("LLM Output", analysis, height=350)

                with tabs[1]:
                    st.subheader("⚔️ Potential Attack Simulation")
                    st.text_area("Exploit Simulation (LLM generated)", attack_vector, height=300)

                with tabs[2]:
                    st.subheader("🧬 Token Behavior Classification")
                    colored_box(token_behavior, "#34495e")

                with tabs[3]:
                    st.subheader("📦 Import Risk Analysis")
                    st.text_area("Import Review", import_risks, height=250)

                with tabs[4]:
                    st.subheader("📊 Overall Risk Score")
                    if score <= 25:
                        colored_box(f"🟢 LOW RISK – Score: {score}/100", "#27ae60")
                    elif score <= 60:
                        colored_box(f"🟡 MEDIUM RISK – Score: {score}/100", "#f39c12")
                    else:
                        colored_box(f"🔴 HIGH RISK – Score: {score}/100", "#e74c3c")

                st.markdown("### 📥 Download Report")

                # Raporları oluştur
                pdf_path = generate_pdf_report(address, analysis, score, level, attack_vector, token_behavior, import_risks)
                csv_path = generate_csv_report(address, score, level, token_behavior)

                col1, col2 = st.columns(2)
                with col1:
                    with open(pdf_path, "rb") as f:
                        st.download_button("📄 Download PDF Report", f, file_name=f"audit_{address}.pdf")
                with col2:
                    with open(csv_path, "rb") as f:
                        st.download_button("📊 Download CSV Summary", f, file_name=f"audit_{address}.csv")

                st.markdown("---")
                st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Powered by ASI1-mini LLM · Built with ❤️ by AuditMind</p>", unsafe_allow_html=True)
