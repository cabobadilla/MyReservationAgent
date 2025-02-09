import streamlit as st
from datetime import datetime, timedelta
import json
from smol_agents import CodeAgent, HfApiModel
from typing import Dict

# Set page config
st.set_page_config(
    page_title="Restaurant Reservation Assistant",
    page_icon="🍽️",
    layout="wide"
)

# Initialize session state
if 'reservation_history' not in st.session_state:
    st.session_state.reservation_history = []

# Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🍽️ Restaurant Reservation Assistant")
st.markdown("Let our AI agent help you find and book the perfect restaurant!")

# Initialize the Hugging Face Agent
@st.cache_resource
def get_agent():
    hf_token = st.secrets["HUGGINGFACE_API_TOKEN"]
    model = HfApiModel(
        model_name="meta-llama/Llama-2-70b-chat-hf",
        api_token=hf_token
    )
    return CodeAgent(model=model)

try:
    agent = get_agent()
except Exception as e:
    st.error("Error initializing the AI agent. Please check your Hugging Face API token.")
    st.stop()

# Country and Region Selection
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox(
        "Select Country",
        ["United States", "Canada", "Mexico", "Spain", "France", "Italy"]
    )

with col2:
    regions = {
        "United States": ["New York", "California", "Texas", "Florida", "Illinois"],
        "Canada": ["Ontario", "British Columbia", "Quebec", "Alberta"],
        "Mexico": ["Mexico City", "Jalisco", "Nuevo León", "Quintana Roo"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Seville"],
        "France": ["Paris", "Lyon", "Marseille", "Bordeaux"],
        "Italy": ["Rome", "Milan", "Florence", "Venice"]
    }
    region = st.selectbox("Select Region", regions[country])

# Cuisine Type
cuisine_type = st.selectbox(
    "Type of Cuisine",
    ["Italian", "Japanese", "Mexican", "American", "French", "Indian", "Chinese", "Spanish"]
)

# Date and Time Selection
col3, col4 = st.columns(2)
with col3:
    # Set min date to today and max date to 30 days from now
    min_date = datetime.now().date()
    max_date = min_date + timedelta(days=30)
    date = st.date_input("Select Date", min_value=min_date, max_value=max_date)

with col4:
    time = st.time_input("Select Time", datetime.now().time())

# Email Input
email = st.text_input("Email for Reservation")

# Additional Notes
notes = st.text_area("Additional Notes or Preferences (optional)")

def validate_inputs() -> tuple[bool, str]:
    if not email or '@' not in email:
        return False, "Please enter a valid email address."
    if date < datetime.now().date():
        return False, "Please select a future date."
    if date == datetime.now().date() and time < datetime.now().time():
        return False, "Please select a future time."
    return True, ""

def format_prompt(data: Dict) -> str:
    return f"""
    Task: Process a restaurant reservation request and provide recommendations.
    
    Reservation Details:
    - Location: {data['region']}, {data['country']}
    - Cuisine Type: {data['cuisine_type']}
    - Date: {data['date']}
    - Time: {data['time']}
    - Customer Email: {data['email']}
    - Special Notes: {data['notes']}
    
    Please:
    1. Suggest 2-3 highly-rated restaurants matching the cuisine type and location
    2. Provide estimated price range for each suggestion
    3. Confirm if the requested date and time would likely be available
    4. Include any relevant notes about dress code or special requirements
    5. Format the response in a clear, customer-friendly way
    """

# Make Reservation Button
if st.button("Make Reservation"):
    # Validate inputs
    is_valid, error_message = validate_inputs()
    
    if not is_valid:
        st.error(error_message)
    else:
        # Show processing message
        with st.spinner("Processing your reservation request..."):
            # Prepare data for the agent
            reservation_data = {
                "country": country,
                "region": region,
                "cuisine_type": cuisine_type,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M"),
                "email": email,
                "notes": notes
            }
            
            try:
                # Get response from the agent
                prompt = format_prompt(reservation_data)
                response = agent.chat(prompt)
                
                # Store reservation in history
                st.session_state.reservation_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "details": reservation_data,
                    "response": response
                })
                
                # Display success message
                st.success("Reservation request processed successfully!")
                st.write("Agent Response:", response)
                
            except Exception as e:
                st.error(f"An error occurred while processing your reservation: {str(e)}")

# Display Reservation History
if st.session_state.reservation_history:
    st.markdown("### Recent Reservations")
    for reservation in reversed(st.session_state.reservation_history[-5:]):
        with st.expander(f"Reservation on {reservation['details']['date']} at {reservation['details']['time']}"):
            st.write("Location:", f"{reservation['details']['region']}, {reservation['details']['country']}")
            st.write("Cuisine:", reservation['details']['cuisine_type'])
            st.write("Email:", reservation['details']['email'])
            st.write("Agent Response:", reservation['details']['response'])

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Hugging Face") 