import uuid

class FakeMCPClient:
    def __init__(self):
        self._sessions = {}

    def create_session(self, user_query, account_id):
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "user_query": user_query,
            "account_id": account_id,
            "api_calls": [],
            "raw_data": {},
            "inferences": None,
            "final_summary": None
        }
        return session_id

    def get_session(self, session_id):
        return self._sessions.get(session_id)

    def update_raw_data(self, session_id, source_name, data):
        if session_id in self._sessions:
            self._sessions[session_id]["raw_data"][source_name] = data
            self._sessions[session_id]["api_calls"].append(source_name)

    def save_inference(self, session_id, inference):
        if session_id in self._sessions:
            self._sessions[session_id]["inferences"] = inference

    def save_final_summary(self, session_id, summary_text):
        if session_id in self._sessions:
            self._sessions[session_id]["final_summary"] = summary_text

    def list_sessions(self):
        return list(self._sessions.keys())

    def reset(self):
        self._sessions.clear()