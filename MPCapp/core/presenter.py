from .model import NPCModel
from .sentiment import SentimentAnalyzer


class NPCPresenter:
    def __init__(self):
        self.model = NPCModel()
        self.sentiment = SentimentAnalyzer()

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value

    @property
    def description(self):
        return self.model.description

    @description.setter
    def description(self, value):
        self.model.description = value

    @property
    def moods(self):
        return self.model.moods

    @property
    def world_state(self):
        return self.model.world_state

    @property
    def chat_history(self):
        return self.model.chat_history

    @property
    def has_llm(self):
        return self.model.has_llm

    def handle_player_input(self, text):
        analysis = self.sentiment.analyze(text)

        if analysis["sentiment"] == "positive":
            self.model.update_mood("friendliness", 0.1)
            self.model.update_mood("suspicion", -0.05)
        elif analysis["sentiment"] == "negative":
            self.model.update_mood("friendliness", -0.15)
            self.model.update_mood("suspicion", 0.2)

        if analysis["aggression"] > 0.3:
            self.model.update_mood("friendliness", -0.1)
            self.model.update_mood("suspicion", 0.15)
            self.model.update_mood("energy", 0.1)

        reply = self.model.get_response(text)
        return reply, analysis

    def adjust_mood(self, trait, amount):
        self.model.update_mood(trait, amount)

    def update_world_state(self, key, value):
        self.model.update_world_state(key, value)

    def export_config(self):
        return self.model.to_dict()

    def reset_npc(self, name, description):
        self.model = NPCModel(name, description)
