import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import io

# Configure Google Gemini API
genai.configure(api_key="AIzaSyAf8zbxxg3aF8YgtnFBbTtEJA-Tq20w2JQ")

def extract_text_from_pdfs(pdf_files):
    """Extract text from multiple uploaded PDF files."""
    all_text = ""
    for pdf_file in pdf_files:
        pdf_bytes = pdf_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)  # Convert bytes to a file-like object
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        
        for page in doc:
            all_text += page.get_text("text") + "\n"
    return all_text

def query_gemini(context, user_question):
    """Use Google Gemini to provide detailed insights based on full PDF content."""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Analyze the following document and provide detailed insights, summaries, and explanations for user queries.
    
    Document Content:
    {context}
    
    User Question:
    {user_question}
    """
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("PDF Insights Extractor")
    st.write("Upload multiple PDFs and get detailed insights from their content.")
    
    pdf_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if pdf_files:
        extracted_text = extract_text_from_pdfs(pdf_files)
        st.success("PDFs successfully processed!")
        
        user_question = st.text_input("Ask a question based on the PDFs:")
        
        if st.button("Get Insights") and user_question:
            with st.spinner("Generating detailed insights..."):
                answer = query_gemini(extracted_text, user_question)
                st.subheader("Detailed Answer:")
                st.write(answer)

if __name__ == "__main__":
    main()
