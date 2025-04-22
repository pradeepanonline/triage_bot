import streamlit as st
from agent.triage_agent import TriageAgent

st.set_page_config(page_title="SRE Triage Assistant", layout="wide")

@st.cache_resource
def load_agent():
    return TriageAgent()

triage_agent = load_agent()

st.title("🔍 Triage Assistant")
st.subheader("Investigate Payment Impacts")

with st.sidebar:
    st.header("🛠️ How to Use")
    st.markdown("""
    1. Enter an **Account ID** (e.g., `ACC001` to `ACC010`).
    2. Describe the **issue or ask a question**.
    3. View the **Charts and Insights**!
    """)
    st.markdown("---")
    st.markdown("🚀 *Powered by OpenAI GPT-4o analysis.*")

account_id = st.text_input("Enter Account ID", value="ACC001")
user_query = st.text_area("Describe the Issue", placeholder="E.g., Why so many declines for this account?", height=150)

if st.button("Start Investigation"):
    if not account_id or not user_query:
        st.warning("Please provide both Account ID and your query.")
    else:
        with st.spinner("Investigating... 🕵️‍♂️"):
            insights, llm_summary = triage_agent.start_investigation(user_query, account_id)
        
        st.success("Investigation Completed!")
        st.markdown("---")

    if insights and isinstance(insights, dict) and insights.get('decline_by_account'):
        st.header("📈 Triage Insights")
        triage_agent.reasoner.generate_charts(insights)

        st.markdown("---")

        st.header("Investigation Summary")
        st.markdown(f"```{llm_summary}```")
    else:
        st.warning("⚠️ No decline insights available to plot for this account. Please try a different account.")

st.markdown("---")
st.caption("Built for internal PoC - Phase 1 + LLM + Visualization 🚀")