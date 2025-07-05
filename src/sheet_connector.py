import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
from dotenv import load_dotenv
from src.logger import auto_logger
from src.custom_exception import CustomException
import io
from datetime import datetime
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


load_dotenv()
logger = auto_logger(__name__)



class Gsheetupdater():

    def __init__(self):
        try:
            logger.info("Connecting With Gsheet.......")

            self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            self.creds = ServiceAccountCredentials.from_json_keyfile_name("GCP_Creds.json", self.scope)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open("TicketSheet").sheet1

            logger.info("Connection established sucessfully")
        except Exception as e:
            logger.error("Failed to Connect with Gsheet")
            raise CustomException(e)

    def append_ticket(self,Ticket_ID, Name,Email,Contact,Office_Location,Issue_Type,Message,Priority):
        try:
            logger.info("Appending Ticket info at the Gsheet.......")

            Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.sheet.append_row([Date,Ticket_ID,Name, Email,Contact,Office_Location, Issue_Type,Message,Priority, "", "",""])

            logger.info("Ticket info appended sucessfully")
        except Exception as e:
            logger.error("Failed to append ticket info")
            raise CustomException(e)

    
    def rownumber(self):
        """Returns the first row number (1-indexed) where Auto_Reply is empty"""
        try:
            logger.info("Getting row number ")
            # Get all records with header row
            records = self.sheet.get_all_records()
            
            # Find first row with empty Auto_Reply (2nd column is headers)
            for idx, row in enumerate(records, start=2):  # Start=2 because:
                # - Row 1: Headers (excluded by get_all_records)
                # - Row 2: First data row (index 0 in records)
                if not row.get('Auto_Reply', '').strip():
                    return idx
                logger.info(f"Row number fetched sucessfully, Row_Number: {idx}")
            return -1  # No matching rows found
        
        except Exception as e:
            logger.error(f"Error finding row: {e}")
            raise CustomException(e)
        
    
    def update_ticket(self,row_number,col,reply):
        try:
            logger.info("Updating Auto-reply into the Gsheet")    
            self.sheet.update_cell(row_number,col,reply)
            logger.info("Auto-reply sucessfully updated into the Gsheet") 
        except Exception as e:
            logger.error("unable to update Auto-reply into the Gsheet")
            raise CustomException(e)