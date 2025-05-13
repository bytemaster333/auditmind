import requests
from dotenv import load_dotenv
import os
from prompts import (
    build_analysis_prompt,
    build_attack_vector_prompt,
    build_token_behavior_prompt,
    build_import_risk_prompt,
)

from uagents import Context

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")


def fetch_contract_data(chain: str, address: str) -> str:
    if chain != "ethereum":
        return "Only Ethereum is supported with Etherscan."
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] != "1":
            return f"Error from Etherscan: {data['message']}"
        result = data["result"][0]
        source_code = result.get("SourceCode")
        return source_code or "No contract source code found for this address."
    except Exception as e:
        return f"Error fetching contract data: {str(e)}"


def calculate_risk_score(analysis_text: str) -> tuple[int, str]:
    score = 0
    text = analysis_text.lower()
    risk_keywords = {
        "unlimited mint": 30,
        "mint": 20,
        "burn": 5,
        "pause": 10,
        "owner": 15,
        "blacklist": 25,
        "backdoor": 40,
        "admin": 15,
        "withdraw": 10,
        "arbitrary": 20,
        "self destruct": 40,
        "transfer from": 5,
    }
    for keyword, weight in risk_keywords.items():
        if keyword in text:
            score += weight
    score = min(score, 100)
    if score <= 25:
        level = "🟢 Low Risk"
    elif score <= 60:
        level = "🟡 Medium Risk"
    else:
        level = "🔴 High Risk"
    return score, level


# 🟢 STREAMLIT - OpenLLM kullanımına özel
async def analyze_with_llm(code: str, llm) -> str:
    prompt = build_analysis_prompt(code)
    try:
        return await llm.complete(prompt=prompt, temperature=0.2)
    except Exception as e:
        return f"LLM Error: {str(e)}"


# 🟢 AGENT için (ctx.llm)
async def analyze_contract(chain: str, address: str, ctx: Context) -> str:
    code = fetch_contract_data(chain, address)
    if "No contract" in code or "Error" in code:
        return code
    prompt = build_analysis_prompt(code)
    try:
        return await ctx.llm.complete(prompt=prompt, temperature=0.2)
    except Exception as e:
        return f"LLM Error: {str(e)}"


# Ek modüller (streamlit kullanımı için)
async def generate_attack_vector(code: str, llm) -> str:
    prompt = build_attack_vector_prompt(code)
    return await llm.complete(prompt=prompt, temperature=0.2)

async def classify_token_behavior(code: str, token_data: dict, llm) -> str:
    prompt = build_token_behavior_prompt(code, token_data)
    return await llm.complete(prompt=prompt, temperature=0.2)

async def analyze_import_risks(code: str, llm) -> str:
    import_lines = [line.strip() for line in code.splitlines() if line.strip().startswith("import")]
    if not import_lines:
        return "No imports found in contract."
    prompt = build_import_risk_prompt(import_lines)
    return await llm.complete(prompt=prompt, temperature=0.2)
