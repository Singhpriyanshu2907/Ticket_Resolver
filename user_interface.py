import streamlit as st
from src.classify_ticket import classifier
from src.sheet_connector import Gsheetupdater
from src.generate_reply import ReplyGenerator
from src.gmail_sender import Emailreply
from src.custom_exception import CustomException

ticketclassifier = classifier()
sheetupdater = Gsheetupdater()
replygenrator = ReplyGenerator()
emailsender = Emailreply()

st.set_page_config(
    page_title="Submit a Support Ticket",
    page_icon="📩",
    layout="centered"
)

# Custom CSS for better visuals
st.markdown("""
    <style>
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji and divider
st.title("📩 Dental Support Ticket System")
st.markdown("We'll respond within 24 hours (urgent cases within 1 hour)")
st.divider()

# Form with visual enhancements
with st.form("ticket_form", clear_on_submit=True):
    st.subheader("Patient Information")
    
    # Personal details in columns
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*", placeholder="John Doe")
    with col2:
        email = st.text_input("Email Address*", placeholder="john@example.com")
    
    contact = st.text_input("Contact Number*", placeholder="+1 (555) 123-4567")
    
    # Location and issue type
    st.subheader("Ticket Details")
    col3, col4 = st.columns(2)
    with col3:
        office = st.selectbox(
            "Office Location*",
            ["Aransas", "Azle", "Beaumont", "Benbrook", "Crosby", 
             "Calallen", "Devine", "Elgin", "Grangerland", "Ganado",
             "Huffman", "Jasper", "Lavaca", "Liberty", "Lytle",
             "Mathis", "Potranco", "Riverwalk", "Rockdale", "Rio Bravo",
             "Splendora", "Springtown", "Sinton", "Tidwell", "Victoria",
             "Westgreen", "Winnie"],
            help="Select your nearest clinic location"
        )
    with col4:
        issue_type = st.selectbox(
            "Issue Type*",
            ["Inquiry", "Emergency", "Appointment/Rescheduling", "Payment", 
             "Billing", "Complaint", "Medication/RX/Request/Question", 
             "Marketing/Sales", "Refund", "Referrals", "Cancellation"],
            help="Select the most relevant category"
        )
    
    # Message box with character counter
    message = st.text_area(
        "Describe your issue*",
        height=200,
        placeholder="Please provide detailed information...",
        help="For emergencies, include symptoms and duration"
    )
    st.caption(f"{len(message)}/500 characters")
    
    # Form submission with validation
    submitted = st.form_submit_button("Submit Ticket", type="primary")
    
    if submitted:
        if not all([name, email, contact, message]):
            st.error("Please fill all required fields (*)")
        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address")
        elif len(contact) != 10:
            st.error("Please enter a valid 10-digit contact number")
        elif len(message) > 500:
            st.error("Description exceeds 500 characters")
        else:
            # Success animation
            with st.spinner("Submitting your ticket..."):
                ticket_id = (f"CAP-{hash(name+email)%100000:05d}")
                Priority = ticketclassifier.ticket_classifier(issue_type,message)
                sheetupdater.append_ticket(ticket_id,name,email,contact,office,issue_type,message,Priority)
                row_number = sheetupdater.rownumber()
                reply = replygenrator.generate_reply(issue_type,message,name)
                sheetupdater.update_ticket(row_number,10,reply)
                subject = (f"{issue_type} issue faced at {office} office")
                emailsender.email_sender(email,subject,reply)
                sheetupdater.update_ticket(row_number,11,reply="Email sent")
                
                
                st.success("Ticket submitted successfully! You will shortly recieve a confirmation on your email.")
                
                # Confirmation message (would be replaced with actual data)
                with st.expander("Ticket Summary", expanded=True):
                    st.write(f"**Ticket ID:**{ticket_id}")
                    st.write(f"**Patient:** {name}")
                    st.write(f"**Issue Type:** {issue_type}")
                    st.markdown("**Our Commitment:**")
                    st.markdown("- Emergency: Response within 1 hour")
                    st.markdown("- Urgent: Response within 4 hours")
                    st.markdown("- Routine: Response within 24 hours")
