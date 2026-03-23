import logging
import requests
from config.settings import settings

logger = logging.getLogger(__name__)

class SentimentPredictor:
    def __init__(self):
        self.ollama_url = f"{settings.OLLAMA_HOST}/api/generate"
        self.model = "llama2" # Update based on your locally running model (e.g. llama3, mistral)

    def analyze_token_sentiment(self, text_content: str) -> dict:
        """
        Queries the local Ollama LLM to analyze token sentiment or determine if a
        token mention represents a high conviction trading signal.
        """
        prompt = f"""
        Analyze the following text from a DEX trading group/social media for a new crypto token alert.
        Identify the token ticker, the sentiment (bullish/bearish/neutral), and the estimated honeypot risk (1-10).
        Respond ONLY in JSON format: {{"ticker": "TOKEN", "sentiment": "bullish", "risk_score": 5}}

        Text: "{text_content}"
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            logger.info(f"Sending request to local Ollama instance at {self.ollama_url}...")
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json().get('response', '{}')
                logger.info(f"LLM Prediction: {result}")
                return {"success": True, "raw_prediction": result}
            else:
                logger.error(f"Ollama inference failed with status {response.status_code}")
                return {"success": False, "error": response.text}
        except Exception as e:
            logger.error(f"Could not connect to Ollama running locally. Make sure it's active. Error: {e}")
            return {"success": False, "error": str(e)}

sentiment_predictor = SentimentPredictor()
