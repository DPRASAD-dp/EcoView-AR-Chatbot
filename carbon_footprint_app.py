import streamlit as st
from backend import TextGenerator, PDFReader

API_KEY = "Enter your API key here."

def main():
    st.title("Eco View AR")

    text_generator = TextGenerator(API_KEY)
    pdf_reader = PDFReader(text_generator)

    if 'questions' not in st.session_state:
        st.session_state.questions = []
        st.session_state.responses = []

    option = st.radio("Choose an option:", ("Get Personalized Tips", "Review My Report"))

    if option == "Get Personalized Tips":
        st.subheader("Ask for personalized carbon footprint reduction tips")

        user_query = st.text_input("Your question (e.g., 'How can I reduce my carbon footprint in daily life?'):")

        if st.button("Ask"):
            if user_query:
                with st.spinner("Generating tips..."):
                    response = text_generator.generate_and_format_text(user_query)
                    st.session_state.questions.append(user_query)
                    st.session_state.responses.append(response)
            else:
                st.warning("Please enter a question to get personalized tips.")

        # Display the conversation history
        if st.session_state.questions:
            st.subheader("Your Questions and Responses:")
            for i, (question, response) in enumerate(zip(st.session_state.questions, st.session_state.responses)):
                st.write(f"**Q{i+1}:** {question}")
                st.write(f"**A{i+1}:** {response}")
                st.write("")  # Add a blank line between questions

    else:  # Review My Report
        st.subheader("Upload your report for review")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            with st.spinner("Processing PDF..."):
                formatted_sections = pdf_reader.analyze_pdf(uploaded_file)
            
            st.subheader("Recommendations based on your report:")
            for section in formatted_sections:
                st.write(section)
                st.write("")  # Add a blank line between sections

if __name__ == "__main__":
    main()
