from src.classify_ticket import TicketClassifier
from src.custom_exception import CustomException

if __name__ == "__main__":
    try:
        classifier = TicketClassifier()

        issue_type = "Pain/Emergency"
        description = "Severe toothache preventing sleep, swollen left cheek, unable to eat any food"

        priority = classifier.classify(issue_type, description)
        print(f"Classified Priority: {priority}")

    except CustomException as e:
        print(f"Classification error: {e}")