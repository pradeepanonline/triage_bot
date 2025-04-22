import json

class PaymentsConnector:
    def __init__(self, data_path="mock_data/payments_data.json"):
        with open(data_path, "r") as f:
            self.payments_data = json.load(f)

    def get_recent_transactions(self, account_id):
        return [txn for txn in self.payments_data if txn["account_id"] == account_id]