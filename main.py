from src.classify_ticket import classifier
from src.custom_exception import CustomException

if __name__ == "__main__":
    try:
        ticketclassifier = classifier()

        issue_type = "Marketing"
        description = "Do you offer teeth whitening packages?"

        priority = ticketclassifier.ticket_classifier(issue_type, description)
        print(f"Classified Priority: {priority}")

    except CustomException as e:
        print(f"Classification error: {e}")