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

class classifier:

    def __init__(self):
        self.client = EuriaiClient(
        api_key=os.getenv("EURIAI_API_KEY"),
        model="gpt-4.1-mini")
    
    def ticket_classifier(self,issue,description):
        Prompt = f"""
You are a dental practice ticket classification expert. 
Analyze this ticket and classify its priority based on these STRICT RULES:

**Priority Framework:**
1. HIGH (Respond within 1 hour):
   - Emergency dental situations (severe pain, swelling, trauma)
   - Life-threatening medication reactions
   - Immediate post-operative complications

2. MEDIUM (Respond within 4 hours):
   - Appointment rescheduling requests
   - Appointment cancellation requests
   - Billing/payment disputes
   - Lab case follow-ups
   - Medication refill requests
   - Referral processing
   - Complaint resolution

3. LOW (Respond within 24 hours):
   - General inquiries about services
   - Marketing/sales questions
   - Non-urgent cancellations
   - Insurance verification requests
   - Routine prescription questions

**Special Considerations for Dental Cases:**
- Prioritize pain-related issues higher when swelling or infection is mentioned
- Elevate priority if patient mentions bleeding or trauma
- Payment issues become Medium priority when affecting treatment continuation

**Ticket Details:**
Issue Type: {issue}
Description: {description}

**Classification Rules:**
1. First determine if this matches any HIGH priority scenarios
2. If not, check against MEDIUM criteria
3. Default to LOW only if clearly non-urgent

**Output Format:**
Respond with EXACTLY one word in uppercase: HIGH, MEDIUM, or LOW
"""
        response = self.client.generate_completion(
            prompt = Prompt,
            temperature = 0.2,
            max_tokens = 20
        )

        return response['choices'][0]['message']['content']

