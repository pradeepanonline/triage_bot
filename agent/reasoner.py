from openai import OpenAI
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import json
from collections import Counter

class Reasoner:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4o"
        # Load remediation steps
        remediation_path = os.path.join("mock_data", "remediation_steps.json")
        with open(remediation_path, "r") as f:
            self.remediation_steps = json.load(f)

    def analyze(self, raw_data):
        payments = raw_data.get("payments", [])

        df = pd.DataFrame(payments)
        total_txns = len(df)
        declined_df = df[df["status"] == "DECLINED"]
        total_declines = len(declined_df)
        overall_decline_rate = (total_declines / total_txns) * 100 if total_txns else 0

        decline_by_account = (
            declined_df.groupby("account_id").size() / 
            df.groupby("account_id").size()
        ).fillna(0).sort_values(ascending=False) * 100

        reason_counts = Counter(declined_df["reason_code"])

        insights = {
            "total_txns": total_txns,
            "total_declines": total_declines,
            "overall_decline_rate": overall_decline_rate,
            "decline_by_account": decline_by_account.to_dict(),
            "top_decline_reasons": dict(reason_counts)
        }

        print("DEBUG: Decline accounts to plot:", insights['decline_by_account'])
        print("DEBUG: Top decline reasons to plot:", insights['top_decline_reasons'])

        return insights

    def generate_llm_summary(self, insights):
        prompt = f"""
Analyze the following payment transaction data and generate a summary:

- Total transactions: {insights['total_txns']}
- Overall decline rate: {insights['overall_decline_rate']:.2f}%

Top decline reasons:
"""
        for reason, count in insights['top_decline_reasons'].items():
            prompt += f"    - {reason}: {count} declines\n"

        prompt += "\nSuggested remediation actions:\n"

        for reason in insights['top_decline_reasons'].keys():
            action = self.remediation_steps.get(reason, "No remediation step available.")
            prompt += f"    - {reason}: {action}\n"

        prompt += "\nPlease summarize the data in a table along with percentages. Highlight the most important action to be taken based on the top declines"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    def generate_charts(self, insights):
        st.subheader("📈 Decline Rate by Account")
        decline_accounts = pd.Series(insights['decline_by_account'])
        if decline_accounts.empty:
            st.warning("⚠️ No account decline data available to plot.")
        else:
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            decline_accounts = decline_accounts.sort_values(ascending=False)
            decline_accounts.index = decline_accounts.index.astype(str)  # Force string index
            decline_accounts.plot(kind="bar", ax=ax1)
            ax1.set_ylabel("Decline Rate (%)")
            ax1.set_xlabel("Account ID")
            ax1.set_title("Decline Rate by Account (Last 30 Days)")
            st.pyplot(fig1)

        st.subheader("📊 Top Decline Reasons")
        reasons = pd.Series(insights['top_decline_reasons'])
        if reasons.empty:
            st.warning("⚠️ No decline reason data available to plot.")
        else:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            reasons = reasons.sort_values(ascending=False)
            reasons.index = reasons.index.astype(str)  # Force string index
            reasons.plot(kind="barh", ax=ax2)
            ax2.set_xlabel("Number of Declines")
            ax2.set_ylabel("Decline Reason")
            ax2.set_title("Decline Reasons Distribution")
            st.pyplot(fig2)
