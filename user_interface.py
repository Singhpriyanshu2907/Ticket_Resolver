import streamlit as st

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
        elif len(contact) > 10 or len(contact) < 10:
            st.error("Please enter a valid 10-digit contact number")
        elif len(message) > 500:
            st.error("Description exceeds 500 characters")
        else:
            # Success animation
            with st.spinner("Submitting your ticket..."):
                # Here you would add your submission logic
                st.success("Ticket submitted successfully! A confirmation has been sent to your email.")
                
                # Confirmation message (would be replaced with actual data)
                with st.expander("Ticket Summary", expanded=True):
                    st.write(f"**Ticket ID:** CAP-{hash(name+email)%100000:05d}")
                    st.write(f"**Patient:** {name}")
                    st.write(f"**Issue Type:** {issue_type}")
                    st.markdown("**Our Commitment:**")
                    st.markdown("- Emergency: Response within 1 hour")
                    st.markdown("- Urgent: Response within 4 hours")
                    st.markdown("- Routine: Response within 24 hours")





# import streamlit as st

# st.set_page_config(page_title="Submit a Support Ticket", page_icon="📩")

# st.title("📩 Submit a Support Ticket")
# st.markdown("We'll get back to you shortly with a helpful response.")

# with st.form("ticket_form"):
#     name = st.text_input("Full Name")
#     email = st.text_input("Email Address")
#     contact = st.text_input("Contact No.")
#     Office = st.selectbox("Office Location",["Aransas","Azle","Beaumont","Benbrook","Crosby","Calallen","Devine","Elgin","Grangerland","Ganado","Huffman","Jasper","Lavaca","Liberty","Lytle","Mathis","Potranco","Riverwalk","Rockdale","Rio Bravo","Splendora","Springtown","Sinton","Tidwell","Victoria","Westgreen","Winnie"])
#     issue_type = st.selectbox("Issue Type", ["Inquiry", "Emergency", "Appointment/Rescheduling", "Payment", "Billing", "Complaint", "Medication/RX/Request/Question", "Marketing/Sales", "Refund", "Referrals", "Cancellation"])
#     message = st.text_area("Describe your issue", height=200)

#     submitted = st.form_submit_button("Submit Ticket")

#     # if submitted:
#     #     if not name or not email or not message:
#     #         st.error("Please fill in all required fields.")
#     #     else:
#     #         append_ticket_to_sheet(name, email, issue_type, message)
#     #         st.success("✅ Your ticket has been submitted successfully!")