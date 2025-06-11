# src/classifier.py

import sys
import os
from dotenv import load_dotenv
from typing import Literal
from src.logger import auto_logger
from src.custom_exception import CustomException
from euriai import EuriaiClient

load_dotenv()
logger = auto_logger(__name__)

class TicketClassifier:
    
    
    
    def __init__(self):
        try:
            logger.info("Getting API credentials for EuriAPI")    
            apikey = os.getenv("EURIAI_API_KEY")
            model = os.getenv("EURIAI_MODEL", "gpt-4.1-mini")

            self.client = EuriaiClient(api_key=apikey, model=model)
            self.valid_priorities = {"High", "Medium", "Low"}
        
        except Exception as e:
            logger.error("Getting error while getting Euriapi creds")
            raise CustomException(e,sys)
    
    
    
    
    
    
    def classify(self, issue_type: str, description: str) -> Literal["High", "Medium", "Low"]:
        try:
            logger.info("Starting ticket classification")
            prompt = f"""
You are a triage assistant for dental support tickets.

Classify the ticket as **High**, **Medium**, or **Low** priority based on the urgency and impact described. Consider both the *Issue Type* and *Description* carefully.

**Guidelines:**
- High: Immediate risk to patient care, severe pain, broken equipment, or urgent operational failure.
- Medium: Impacts workflow but not urgent or critical (e.g. software glitch, scheduling issue).
- Low: General inquiries, minor inconveniences, or non-urgent requests.

**Issue Type:** {issue_type}
**Description:** {description}

Respond ONLY with one word: High, Medium, or Low.
"""

            response = self.client.generate_completion(
                prompt=prompt,
                temperature=0.2,
                max_tokens=10
            )

            # Extract 'completion' string from response dict
            priority_text = response.get("completion", "")
            priority = self._sanitize_priority(priority_text.strip())

            logger.info(f"Classified as {priority} priority")
            return priority

        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            raise CustomException(e,sys)


    def _sanitize_priority(self, raw_priority: str) -> Literal["High", "Medium", "Low"]:
        words = raw_priority.split()
        
        if not words:
            logger.warning("Empty priority received. Defaulting to Medium")
            return "Medium"

        clean = words[0].strip().capitalize()

        if clean not in self.valid_priorities:
            logger.warning(f"Invalid priority '{raw_priority}', defaulting to Medium")
            return "Medium"

        return clean
