import re


class SentimentAnalyzer:
    POSITIVE_WORDS = {
        "hello", "hi", "greetings", "nice", "great", "wonderful", "amazing",
        "thanks", "thank", "please", "friend", "help", "beautiful", "good",
        "love", "happy", "glad", "excellent", "kind", "generous", "peace",
        "respect", "admire", "cheerful", "delightful", "pleasant",
    }

    NEGATIVE_WORDS = {
        "die", "kill", "hate", "stupid", "ugly", "terrible", "awful",
        "leave", "bad", "evil", "curse", "demon", "monster",
        "pathetic", "worthless", "idiot", "fool", "scum", "trash",
        "disgusting", "vile", "contemptible", "despicable",
    }

    AGGRESSIVE_WORDS = {
        "attack", "fight", "threaten", "destroy",
        "surrender", "obey", "submit",
    }

    @classmethod
    def analyze(cls, text):
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        bigrams = set(re.findall(r'\b\w+\s+\w+\b', text_lower))

        pos_count = sum(1 for w in cls.POSITIVE_WORDS if w in words or w in bigrams)
        neg_count = sum(1 for w in cls.NEGATIVE_WORDS if w in words or w in bigrams)
        agg_count = sum(1 for w in cls.AGGRESSIVE_WORDS if w in words or w in bigrams)

        total = pos_count + neg_count + agg_count
        if total == 0:
            return {"sentiment": "neutral", "score": 0.0, "aggression": 0.0}

        sentiment_score = (pos_count - neg_count - agg_count) / max(total, 1)
        aggression_score = agg_count / max(total, 1)

        if sentiment_score > 0.2:
            sentiment = "positive"
        elif sentiment_score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "aggression": aggression_score,
        }
