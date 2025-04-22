import json

class RiskLogsConnector:
    def __init__(self, data_path="mock_data/risk_logs.json"):
        with open(data_path, "r") as f:
            self.risk_logs = json.load(f)

    def get_risk_events(self, account_id):
        return [event for event in self.risk_logs if event["account_id"] == account_id]