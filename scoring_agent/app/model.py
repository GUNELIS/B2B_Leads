import pickle
from pathlib import Path

from sklearn.linear_model import LogisticRegression

MODEL_PATH = Path("/app/model.pkl")


class MatchModel:
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def train(self, X, y):
        self.model.fit(X, y)
        self.trained = True
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)

    def load(self):
        if MODEL_PATH.exists():
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            self.trained = True

    def predict(self, X):
        if not self.trained:
            raise ValueError("Model not trained")
        return self.model.predict_proba(X)[:, 1]


model = MatchModel()
