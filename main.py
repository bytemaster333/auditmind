import os
from uagents import Agent, Context, Model
from dotenv import load_dotenv

from utils import analyze_contract, calculate_risk_score

# .env'den API anahtarlarını yükle
load_dotenv()
asi_token = os.getenv("ASI_API_TOKEN")
agent_seed = os.getenv("AGENT_SEED")

# Kullanıcıdan gelen kontrat analiz isteklerini temsil eden model
class ContractAnalysisRequest(Model):
    chain: str       # Örn: ethereum, polygon, binance-smart-chain
    address: str     # Smart contract adresi

# Agent oluştur
auditor_agent = Agent(
    name="auditor_agent",
    seed=agent_seed,
    endpoint="http://localhost:8000/submit",
)

# Giriş mesajı
@auditor_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("✅ Smart Contract Auditor Agent is online!")

# İstek geldiğinde analiz et
@auditor_agent.on_message(model=ContractAnalysisRequest)
async def handle_analysis(ctx: Context, msg: ContractAnalysisRequest):
    ctx.logger.info(f"🔍 Analyzing contract at {msg.address} on {msg.chain}...")

    analysis = await analyze_contract(chain=msg.chain, address=msg.address, ctx=ctx)
    score, level = calculate_risk_score(analysis)

    final_report = f"""
📝 Contract Analysis:
{analysis}

⚠️ Risk Score: {score}/100
Risk Level: {level}
"""
    ctx.logger.info(final_report)

# Agent'i başlat
if __name__ == "__main__":
    auditor_agent.run()
