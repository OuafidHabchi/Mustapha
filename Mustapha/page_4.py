import streamlit as st
from fpdf import FPDF
from io import BytesIO
import os

def create_pdf_without_password(product_info, steps, prepared_by):
    # Step 1: Generate the PDF content with FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # Path to the logo image
    logo_path = os.path.join(os.getcwd(),"Mustapha", "options", "images", "image.png")
        
    # Check if the logo exists
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)  # Position (x, y) and width (w)
        logo_y_position = 8 + 30  # Adjust y position based on logo height
    else:
        st.warning("Logo image not found. PDF generated without the logo.")
        logo_y_position = 10  # Fallback position if the logo is absent
    
    # "Prepared by" below the logo
    pdf.set_xy(10, logo_y_position + 5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Prepared by: {prepared_by}", ln=True)
    
    # Product Info Section
    pdf.set_xy(10, logo_y_position + 20)
    pdf.set_text_color(0, 102, 204)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Product Information", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Space
    for key, value in product_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.cell(200, 10, txt=" ", ln=True)  # Space

    # Recipe Steps with Detailed Item Information
    pdf.set_text_color(0, 153, 76)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recipe Steps", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Space
    
    for idx, step in enumerate(steps, start=1):
        # Step header with a background color
        pdf.set_fill_color(220, 240, 220)
        pdf.cell(200, 10, txt=f"Step {idx}: {step['step_type']} in {step['section']}", ln=True, fill=True)
        
        # Items in the step
        pdf.cell(200, 10, txt="Items in this step:", ln=True)
        for selected_item in step['selected_items']:
            item_text = f"Item: {selected_item}"
            pdf.cell(200, 10, txt=item_text, ln=True)

        # Additional step fields with indent
        pdf.set_font("Arial", 'I', 10)
        for field, value in step["step_fields"].items():
            pdf.cell(200, 10, txt=f"  {field}: {value if value else 'N/A'}", ln=True)
        pdf.cell(200, 10, txt=f"  Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        
        # Separator for each step
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt="---------------------------", ln=True)
        pdf.set_text_color(0, 0, 0)
    
    # Output PDF to BytesIO
    pdf_output = BytesIO()
    pdf.output(pdf_output, dest='F')
    pdf_output.seek(0)

    return pdf_output


def page_4():
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Étape 4 : Complete Overview and PDF Export")

    # Default data if not present
    if 'product_info' not in st.session_state:
        st.session_state.product_info = {'Name': 'Default Product', 'Batch Size': '1000', 'Category': 'Pharmaceutical'}
    if 'steps' not in st.session_state:
        st.session_state.steps = []

    # Display product information
    st.subheader("Product Information")
    product_info = st.session_state.product_info
    for key, value in product_info.items():
        st.write(f"**{key}:** {value}")

    # Display recipe steps
    st.subheader("Recipe Steps")
    for idx, step in enumerate(st.session_state.steps, start=1):
        st.markdown(f"<span style='color: green; font-weight: bold;'>**Step {idx}:** {step['step_type']} in {step['section']}</span>", unsafe_allow_html=True)
        st.write("**Items in this step:**")
        for selected_item in step['selected_items']:
            st.write(f"- {selected_item}")

        for field, value in step["step_fields"].items():
            st.write(f"**{field}:** {value if value else 'N/A'}")
        st.write(f"Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("---")
        
    # Input for the name of the person who prepared the recipe
    prepared_by = st.text_input("Recipe prepared by:")

    # Button to generate the PDF
    if st.button("Generate PDF"):
        if prepared_by:
            pdf_file = create_pdf_without_password(product_info, st.session_state.steps, prepared_by)
            
            # Name the PDF file based on the product name
            file_name = f"{product_info.get('product_name', 'Recipe')}.pdf"
            
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=file_name,
                mime="application/pdf"
            )
            st.success("PDF generated successfully!")
        else:
            st.warning("Please enter the name of the person who prepared the recipe.")

# Run the function to display page 4
page_4()
