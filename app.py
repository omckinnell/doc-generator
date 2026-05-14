import streamlit as st
from chain import generate_docs
from utils import read_uploaded_file, to_markdown
from utils import read_uploaded_file, to_markdown, inject_docs_into_code

st.set_page_config(page_title="Python Doc Generator", layout="wide")
st.title("Python Documentation Generator")
st.caption("Paste your code or upload a .py file to generate structured markdown docs.")

input_method = st.radio("Input method", ["Paste Code", "Upload File"], horizontal=True)

code = ""

if input_method == "Paste Code":
    code = st.text_area("Paste your Python code here", height=300)
else:
    uploaded = st.file_uploader("Upload a .py file", type=["py"])
    if uploaded:
        code = read_uploaded_file(uploaded)
        st.code(code, language="python")

if st.button("Generate Docs", disabled=not code):
    with st.spinner("Analyzing your code..."):
        try:
            doc = generate_docs(code)
            markdown = to_markdown(doc)

            st.success("Done!")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Preview")
                st.markdown(markdown)

            with col2:
                st.subheader("Raw Markdown")
                st.code(markdown, language="markdown")

            st.download_button(
                label="Download .md file",
                data=markdown,
                file_name="documentation.md",
                mime="text/markdown"
            )
            st.subheader("Annotated Code")
            annotated = inject_docs_into_code(code, doc)
            st.code(annotated, language="python")

            st.download_button(
                label="Download Annotated .py file",
                data=annotated,
                file_name="documented_code.py",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")