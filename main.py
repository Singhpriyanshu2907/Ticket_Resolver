from src.classify_ticket import classifier
from src.sheet_connector import Gsheetupdater
from src.generate_reply import ReplyGenerator
from src.gmail_sender import Emailreply
from src.custom_exception import CustomException

if __name__ == "__main__":
    try:
        ticketclassifier = classifier()
        sheetupdater = Gsheetupdater()
        replygenrator = ReplyGenerator()
        emailsender = Emailreply()

        ticket_id = 'CAP-123456'
        name = 'john doe'
        email = 'abcxyz@outlook.com'
        Contact = 8900000045
        office= 'Mathis'
        issue = 'Rescheduling'
        Message = "I want to reschedule my appointment which was for 07/10/2025 to any day after 15th of july"
        Priority = ticketclassifier.ticket_classifier(issue,Message)
        sheetupdater.append_ticket(ticket_id,name,email,Contact,office,issue,Message,Priority)
        row_number = sheetupdater.rownumber()
        reply = replygenrator.generate_reply(issue,Message,name)
        sheetupdater.update_ticket(row_number,10,reply)
        subject = (f"{issue} issue faced at {office} office")
        emailsender.email_sender(email,subject,reply)
        sheetupdater.update_ticket(row_number,11,reply="Email sent")
        print("Email send sucessfully and sheet updated")

    except CustomException as e:
        print(f"Classification error: {e}")