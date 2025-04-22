import json

class KYCConnector:
    def __init__(self, data_path="mock_data/kyc_data.json"):
        with open(data_path, "r") as f:
            self.kyc_data = json.load(f)

    def get_kyc_status(self, account_id):
        return self.kyc_data.get(account_id, {"kyc_status": "unknown", "last_updated": None})