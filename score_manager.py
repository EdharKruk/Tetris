from pymongo import MongoClient

class ScoreManager:
    def __init__(self, db_name="tetris_db", collection_name="scores"):
        uri = "mongodb+srv://s26827:Edgar12478@cluster0.eyfssrh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_score(self, name, score):
        score_data = {
            "name": name,
            "score": score
        }
        self.collection.insert_one(score_data)

    def get_top_scores(self, limit=10):
        return list(self.collection.find().sort("score", -1).limit(limit))

score_manager = ScoreManager()
