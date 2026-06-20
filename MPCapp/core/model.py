import os


class NPCModel:
    def __init__(self, name="Aldric", description="A seasoned knight guarding the castle gates."):
        self.name = name
        self.description = description
        self.moods = {
            "friendliness": 0.5,
            "suspicion": 0.1,
            "energy": 0.7,
        }
        self.world_state = {
            "location": "Castle Gates",
            "time_of_day": "Day",
            "player_held_item": "Nothing",
        }
        self.chat_history = []
        self._openai_client = None
        self._llm_healthy = True
        self._init_openai()

    def _init_openai(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=api_key)
            except ImportError:
                self._openai_client = None

    @property
    def has_llm(self):
        return self._openai_client is not None and self._llm_healthy

    def update_mood(self, trait, amount):
        if trait in self.moods:
            self.moods[trait] = max(0.0, min(1.0, self.moods[trait] + amount))

    def update_world_state(self, key, value):
        self.world_state[key] = value

    def generate_system_prompt(self):
        f = self.moods["friendliness"]
        s = self.moods["suspicion"]
        e = self.moods["energy"]

        friendliness_desc = (
            "warm and welcoming" if f > 0.7
            else "cold and dismissive" if f < 0.3
            else "neutral but polite"
        )
        suspicion_desc = (
            "highly paranoid and wary" if s > 0.7
            else "cautious but open" if s > 0.4
            else "trusting and at ease"
        )
        energy_desc = (
            "alert and vigorous" if e > 0.7
            else "tired and sluggish" if e < 0.3
            else "calm and steady"
        )

        ws = self.world_state
        world_context = (
            f"\nCurrent Scene: It is {ws['time_of_day']} at {ws['location']}. "
            f"The player approaches holding {ws['player_held_item']}."
        )

        return (
            f"You are {self.name}, an NPC in a fantasy world. {self.description}\n"
            f"Current Mental State: You feel {friendliness_desc}, {suspicion_desc}, and {energy_desc}.{world_context}\n"
            f"Guidelines: Stay in character. Keep responses under 3 sentences. "
            f"Do not break immersion or refer to being an AI."
        )

    def get_response(self, player_input):
        self.chat_history.append({"role": "user", "content": player_input})
        messages = [{"role": "system", "content": self.generate_system_prompt()}]
        for msg in self.chat_history[-10:]:
            messages.append(msg)

        if self._openai_client:
            try:
                response = self._openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150,
                )
                reply = response.choices[0].message.content.strip()
            except Exception:
                self._llm_healthy = False
                reply = self._mock_response(player_input)
        else:
            reply = self._mock_response(player_input)

        self.chat_history.append({"role": "assistant", "content": reply})
        return reply

    def _mock_response(self, player_input):
        f = self.moods["friendliness"]
        s = self.moods["suspicion"]
        greeting = "Hmph." if f < 0.3 else "Greetings, traveler."
        suspicion = " What business do you have here?" if s > 0.5 else ""
        return f"{greeting}{suspicion} (Mock response \u2014 set OPENAI_API_KEY for LLM replies.)"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "moods": dict(self.moods),
            "world_state": dict(self.world_state),
            "chat_history": self.chat_history,
        }

    @classmethod
    def from_dict(cls, data):
        npc = cls(data["name"], data["description"])
        npc.moods.update(data["moods"])
        npc.world_state.update(data["world_state"])
        npc.chat_history = data.get("chat_history", [])
        return npc
