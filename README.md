# Restaurant Reservation Assistant

A Streamlit-based application that helps users make restaurant reservations using AI assistance. The application uses the Hugging Face smolagents library to process reservation requests and provide intelligent responses.

## Features

- Country and region selection
- Cuisine type selection
- Date and time picker
- Email confirmation
- AI-powered restaurant suggestions using Hugging Face LLMs
- Reservation history tracking
- Modern and user-friendly interface

## Requirements

- Python 3.7+
- Streamlit
- smolagents
- huggingface-hub
- python-dotenv

## Setup and Deployment

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Deploy to Streamlit Cloud:
   - Fork this repository to your GitHub account
   - Connect your GitHub repository to Streamlit Cloud
   - Add the following secrets in your Streamlit Cloud deployment:
     - `HUGGINGFACE_API_TOKEN`: Your Hugging Face API token

## Local Development

1. Create a `.env` file in the root directory
2. Add your Hugging Face API token:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select your country and region
2. Choose your preferred cuisine type
3. Pick a date and time for your reservation
4. Enter your email address
5. Add any additional notes or preferences
6. Click "Make Reservation"
7. The AI agent will process your request and provide restaurant suggestions and availability

## Note

Make sure to keep your API tokens secure and never commit them to version control. Always use environment variables or Streamlit's secrets management for sensitive information. 