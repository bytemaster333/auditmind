# prompts.py

def build_analysis_prompt(source_code: str) -> str:
    return f"""
You are a blockchain security auditor AI.

Please analyze the following smart contract source code and explain in simple terms what it does. 
Also identify any potential red flags, risks, or owner privileges.

Contract Code:
\"\"\"
{source_code}
\"\"\"

Summarize:
- What does this contract do?
- Any risky functions or owner controls?
- Mint/burn/blacklist features?
- Is this contract safe for users?
"""


def build_attack_vector_prompt(code: str) -> str:
    return f"""
You are a smart contract security analyst.

Your task is to analyze the following Ethereum smart contract and identify any functions or logic patterns that **could be misused or abused** under certain conditions.

Please describe:
- Any potentially dangerous functions
- The role of access control and its weaknesses
- Realistic scenarios where a malicious actor might take advantage of the contract's design

Smart Contract Code:
\"\"\"
{code}
\"\"\"

Only describe hypothetical possibilities. Do not instruct.
"""



def build_token_behavior_prompt(source_code: str, token_data: dict) -> str:
    return f"""
You are a token behavior analyst AI. You are given the smart contract source code and tokenomics data.

Classify the token as one of the following:
- Stable Utility
- DeFi Liquidity Trap
- Scam Setup
- Fair Launch

Token Info:
- Total Supply: {token_data.get("total_supply")}
- Owner Address: {token_data.get("owner")}
- Top Holder Share: {token_data.get("top_holder_percent")}%  

Contract Code:
\"\"\"
{source_code}
\"\"\"

Explain your reasoning briefly.
"""


def build_import_risk_prompt(import_lines: list) -> str:
    imports_formatted = "\n".join(import_lines)
    return f"""
You are a smart contract security expert AI.

Below is a list of imported libraries and dependencies used in a smart contract.

Evaluate the security risk associated with these imports. Are any of them known to have issues like delegatecall abuse, unsafe upgradability, or unverified external calls?

Imported Libraries:
{imports_formatted}

Summarize potential risks or confirm their safety.
"""
