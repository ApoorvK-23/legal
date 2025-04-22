import streamlit as st
from docxtpl import DocxTemplate
import tempfile
import os

st.title("Legal Form Filler App")

# Define available templates
TEMPLATE_OPTIONS = {
    "Form 5": "form_5_cleaned_placeholders.docx"
}

form_choice = st.selectbox("Select a form to fill", list(TEMPLATE_OPTIONS.keys()))

if form_choice:
    template_path = TEMPLATE_OPTIONS[form_choice]

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Copy template to temp directory
        docx_path = os.path.join(tmpdirname, template_path)
        with open(template_path, "rb") as src, open(docx_path, "wb") as dst:
            dst.write(src.read())

        # Load and extract placeholders
        doc = DocxTemplate(docx_path)
        fields = doc.get_undeclared_template_variables()

        st.subheader(f"Fill in the fields for {form_choice}")
        context = {}
        for field in sorted(fields):
            label = field.replace('_', ' ').capitalize()
            context[field] = st.text_area(label)

        if st.button("Generate DOCX"):
            filled_docx_path = os.path.join(tmpdirname, "filled_form.docx")
            doc.render(context)
            doc.save(filled_docx_path)

            with open(filled_docx_path, "rb") as f:
                st.download_button(
                    label="Download Filled Form as DOCX",
                    data=f,
                    file_name=f"{form_choice.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

