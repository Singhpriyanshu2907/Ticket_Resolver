
import sys
import os
from dotenv import load_dotenv
from typing import Literal
from src.logger import auto_logger
from src.custom_exception import CustomException
from euriai import EuriaiClient

load_dotenv()
logger = auto_logger(__name__)




class ReplyGenerator():
    def __init__(self):
        try:
            logger.info("Intializing LLM for Auto-reply generation")
            self.client = EuriaiClient(
            api_key=os.getenv("EURIAI_API_KEY"),
            model="gpt-4.1-mini")
            logger.info("LLM initialized sucessfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM")
            raise CustomException(e)

    def generate_reply(self, issue, message, Name):
         
        """
        Generates a professional dental support reply
        
        Args:
            issue (str): Type of issue (e.g., "Inquiry", "Emergency", "Appointment/Rescheduling", "Payment", 
             "Billing", "Complaint", "Medication/RX/Request/Question", 
             "Marketing/Sales", "Refund", "Referrals", "Cancellation")
            message (str): Patient's detailed description
            patient_name (str): Optional patient name for personalization
            
        Returns:
            str: Generated response with proper formatting
        """
        prompt = f"""
**Role**: You are Capline Dental's AI Support Agent. Respond professionally yet compassionately.

**Patient Information**:
- Name: {Name if Name else "Patient"}
- Issue Type: {issue}
- Description: {message}

**Response Guidelines**:
1. Start with empathetic acknowledgment
2. Provide clear next steps
3. Include relevant dental advice if applicable
4. Set proper expectations for resolution time
5. End with contact information for urgent matters

**Special Cases**:
- For emergencies: Stress urgency and provide after-hours contact
- For billing: Explain documentation needed
- For appointments: Offer scheduling options

**Output Format**:
[Greeting] [Acknowledgment] [Action Plan] [Closing]

Example:
"Dear [Name], we understand your concern about... Our team will... For immediate assistance..."

**Generate Response**:
"""
        try:
            logger.info("Generating Auto-Reply for the ticket")
            response = self.client.generate_completion(
                prompt=prompt,
                temperature=0.3,  # Slightly higher for varied but professional responses
                max_tokens=200,   
                top_p=0.9
            )
            
            # Extract and clean response
            full_reply = response['choices'][0]['message']['content'].strip()
            
            logger.info("Auto-Reply generated sucessfully for the ticket")
            
            # Ensure proper formatting
            if not full_reply.startswith(("Dear", "Hello", "Hi")):
                full_reply = f"Dear {Name if Name else 'Patient'},\n\n{full_reply}"
                
            return full_reply
            
        except Exception as e:
            error_msg = f"We encountered an error generating your response. Our team has been notified."
            logger.error(f"AI Generation Error: {str(e)}")
            return error_msg