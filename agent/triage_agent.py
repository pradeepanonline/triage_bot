from connectors.payments_connector import PaymentsConnector
from connectors.kyc_connector import KYCConnector
from connectors.risk_logs_connector import RiskLogsConnector
from mcp_client.fake_mcp_client import FakeMCPClient
from agent.reasoner import Reasoner

class TriageAgent:
    def __init__(self):
        self.payments_connector = PaymentsConnector()
        self.kyc_connector = KYCConnector()
        self.risk_connector = RiskLogsConnector()
        self.mcp_client = FakeMCPClient()
        self.reasoner = Reasoner()

    def start_investigation(self, user_query, account_id):
        session_id = self.mcp_client.create_session(user_query, account_id)

        payments_data = self.payments_connector.get_recent_transactions(account_id)
        self.mcp_client.update_raw_data(session_id, "payments", payments_data)

        kyc_status = self.kyc_connector.get_kyc_status(account_id)
        self.mcp_client.update_raw_data(session_id, "kyc", kyc_status)

        risk_events = self.risk_connector.get_risk_events(account_id)
        self.mcp_client.update_raw_data(session_id, "risk_logs", risk_events)

        session_context = self.mcp_client.get_session(session_id)
        raw_data = session_context["raw_data"]

        insights = self.reasoner.analyze(raw_data)
        llm_summary = self.reasoner.generate_llm_summary(insights)

        self.mcp_client.save_inference(session_id, insights)
        self.mcp_client.save_final_summary(session_id, llm_summary)

        return insights, llm_summary