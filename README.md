# 🔍 SRE Triage Assistant (LLM + Visualization Powered)

This project is a **PoC (Proof of Concept)** tool designed to help **SRE and Support Engineers** triage **payment issues** using **natural language queries**.

It combines:
- Real-time data fetching (mocked for now)
- LLM-driven reasoning (GPT-4o)
- Actionable remediation guidance
- Visual charts and insights

---

## 🚀 Features

✅ Natural Language Query Input  
✅ Analyze transactions and decline trends  
✅ Grounded Remediation Steps (via JSON lookup)  
✅ LLM-powered Smart Summary Generation  
✅ Interactive Charts (Decline Rates, Reasons)  
✅ Easy to extend to real APIs and real MCP servers

---

## 📋 System Architecture

```plaintext
[User Query] 
    ↓
[Streamlit UI]
    ↓
[Triage Agent]
    ↓
[Data Connectors] → [Payments / KYC / Risk Mock Data]
    ↓
[Reasoner]
    ↓
- Aggregate Insights
- Lookup Remediations
- Prompt OpenAI LLM
    ↓
[Charts + Final Observations Shown to User]
