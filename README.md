
# EcoView AR

## Overview
This project is a web-based application designed to help users reduce their carbon footprint by providing personalized tips and analyzing reports. It utilizes IBM Watson services to generate text-based recommendations and Streamlit for the user interface.

## Features
1. **Personalized Carbon Footprint Tips**: Users can input specific questions related to reducing their carbon footprint, and the application will generate personalized recommendations.
2. **Report Analysis**: Users can upload a PDF report (e.g., energy consumption report), and the application will analyze it to provide actionable recommendations.

## Dependencies
- Python 3.7+
- `ibm-watson`: For IBM Watson services (API token generation).
- `requests`: To make HTTP requests to the IBM Watson API.
- `PyPDF2`: For reading and extracting text from PDF files.
- `Streamlit`: For building the web-based user interface.

## Installation
1. Clone the repository to your local machine.
2. Install the required Python packages using pip:
   ```bash
   pip install ibm-watson requests PyPDF2 streamlit
   ```
3. Ensure you have an IBM Cloud account to obtain the `API_KEY` for IBM Watson services.

## How It Works
### 1. **Token Generation**:
   - The `TokenGenerator` class handles the generation of an IBM Watson API token using the provided `API_KEY`.

### 2. **Text Generation**:
   - The `TextGenerator` class uses the IBM Watson text generation model to create personalized recommendations based on user input.
   - The `generate_text` method sends a request to the IBM Watson API with specific parameters to generate the text.
   - The `format_response` method formats the generated text into a structured, readable format.

### 3. **PDF Analysis**:
   - The `PDFReader` class extracts text from the uploaded PDF and generates recommendations based on the content.
   - The `analyze_pdf` method combines the text extraction and text generation to provide actionable recommendations from the PDF content.

### 4. **User Interface**:
   - The Streamlit-based UI provides two main options:
     1. **Get Personalized Tips**: Users can ask questions and receive tips directly in the app.
     2. **Review My Report**: Users can upload a PDF report, and the app will analyze it to provide tailored recommendations.

## Usage
1. Run the Streamlit app using:
   ```bash
   streamlit run carbon_footprint_app.py
   ```
2. Access the app in your browser to either ask for personalized tips or upload a report for analysis.

## Example
- **Personalized Tips**:
  - User asks: "How can I reduce my carbon footprint in daily life?"
  - The app returns a list of actionable tips formatted as bullet points.
  
- **Report Analysis**:
  - User uploads a PDF report.
  - The app returns structured recommendations based on the content of the report.

## Notes
- Ensure the `API_KEY` is correctly set in the application for IBM Watson services.
- The app is designed to focus on individual actions that can easily be incorporated into daily routines.
