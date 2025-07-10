import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import re

st.set_page_config(page_title="PDF Number Clicker", layout="wide")

st.title("📄 PDF Number Clicker")
st.write("Upload a PDF, click on numbers, and build a list!")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

clicked_numbers = st.session_state.get("clicked_numbers", [])

def extract_numbers_from_page(page_text):
    return re.findall(r"\b\d+(?:\.\d+)?\b", page_text)

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page_num = st.number_input("Page number", min_value=1, max_value=len(doc), value=1)
    page = doc[page_num - 1]

    pix = page.get_pixmap(dpi=150)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    st.image(img, caption=f"Page {page_num}", use_column_width=True)

    text = page.get_text()
    numbers = extract_numbers_from_page(text)
    st.markdown("### Click a number to add it to the list:")
    cols = st.columns(5)
    for i, number in enumerate(numbers):
        if cols[i % 5].button(number, key=f"num_{i}"):
            clicked_numbers.append(number)
            st.session_state.clicked_numbers = clicked_numbers

    st.markdown("### ✅ Clicked Numbers:")
    st.write(clicked_numbers)

    if clicked_numbers:
        txt = "\n".join(clicked_numbers)
        st.download_button("Download List", txt, file_name="clicked_numbers.txt")
