import streamlit as st
from fpdf import FPDF
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
import pandas as pd

def create_pdf_with_password(product_info, bom_items, steps, password):
    # Step 1: Generate the PDF content with FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # Set up fonts and colors
    pdf.set_font("Arial", size=12)
    
    # Product Info Section
    pdf.set_text_color(0, 102, 204)  # Blue color for product title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Product Information", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer
    for key, value in product_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer

    # BOM Items Table
    pdf.set_text_color(204, 51, 0)  # Dark red for BOM title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="BOM Items", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer

    # Table Headers with background color
    pdf.set_fill_color(200, 200, 200)  # Light gray for headers
    pdf.cell(40, 10, "Item Number", 1, 0, 'C', fill=True)
    pdf.cell(40, 10, "Code", 1, 0, 'C', fill=True)
    pdf.cell(60, 10, "Name", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Quantity", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Section", 1, 1, 'C', fill=True)

    # Table Rows with alternating row colors
    for idx, item in enumerate(bom_items):
        if idx % 2 == 0:
            pdf.set_fill_color(240, 240, 240)  # Light gray for alternate rows
        else:
            pdf.set_fill_color(255, 255, 255)  # White for normal rows

        pdf.cell(40, 10, str(item['item_number']), 1, 0, 'C', fill=True)
        pdf.cell(40, 10, item['item_code'], 1, 0, 'C', fill=True)
        pdf.cell(60, 10, item['item_name'], 1, 0, 'C', fill=True)
        pdf.cell(30, 10, item['item_quantity'], 1, 0, 'C', fill=True)
        pdf.cell(30, 10, item['section'], 1, 1, 'C', fill=True)

    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer

    # Recipe Steps with Detailed Item Information
    pdf.set_text_color(0, 153, 76)  # Green color for steps title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recipe Steps", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer
    
    for idx, step in enumerate(steps, start=1):
        # Step header with a background color
        pdf.set_fill_color(220, 240, 220)  # Light green for steps
        pdf.cell(200, 10, txt=f"Step {idx}: {step['step_type']} in {step['section']}", ln=True, fill=True)
        
        # List each item in the step
        pdf.cell(200, 10, txt="Items in this step:", ln=True)
        for selected_item in step['selected_items']:
            # Split selected_item to retrieve only item_code (format: "item_code - item_name")
            item_code = selected_item.split(" - ")[0].strip()
            item_found = False
            for section, items in st.session_state.bom_sections.items():
                for item in items:
                    if item['item_code'] == item_code:
                        item_text = (f"Item Number: {item['item_number']} - Code: {item['item_code']} - "
                                     f"Name: {item['item_name']} - Quantity: {item['item_quantity']}")
                        pdf.cell(200, 10, txt=item_text, ln=True)
                        item_found = True
                        break
                if item_found:
                    break
            if not item_found:
                pdf.cell(200, 10, txt=f"Item with code '{item_code}' not found in BOM.", ln=True)

        # Additional step fields with indent
        pdf.set_font("Arial", 'I', 10)
        for field, value in step["step_fields"].items():
            pdf.cell(200, 10, txt=f"  {field}: {value if value else 'N/A'}", ln=True)
        pdf.cell(200, 10, txt=f"  Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        
        # Divider for each step
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt="---------------------------", ln=True)
        pdf.set_text_color(0, 0, 0)
    
    # Step 2: Output PDF to byte string and load into BytesIO
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Generate PDF as byte string
    pdf_output = BytesIO(pdf_bytes)  # Load into BytesIO for further processing
    
    # Step 3: Apply password protection using PyPDF2
    pdf_reader = PdfReader(pdf_output)
    pdf_writer = PdfWriter()
    
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    
    pdf_writer.encrypt(password)
    
    protected_pdf_output = BytesIO()
    pdf_writer.write(protected_pdf_output)
    protected_pdf_output.seek(0)

    return protected_pdf_output

def page_4():
    st.title("Étape 4 : Complete Overview and PDF Export")

    # Ensure data exists in session state
    if 'product_info' not in st.session_state:
        st.session_state.product_info = {'Name': 'Default Product', 'Batch Size': '1000', 'Category': 'Pharmaceutical'}
    if 'bom_sections' not in st.session_state:
        st.session_state.bom_sections = {}
    if 'steps' not in st.session_state:
        st.session_state.steps = []

    # 1. Display Product Information (Step 1)
    st.subheader("Product Information")
    product_info = st.session_state.product_info
    for key, value in product_info.items():
        st.write(f"**{key}:** {value}")

    # 2. Display BOM Items (Step 2) in a Table Format
    st.subheader("BOM Items")
    bom_items = []
    for section, items in st.session_state.bom_sections.items():
        for item in items:
            bom_items.append({
                'item_number': item['item_number'],
                'item_code': item['item_code'],
                'item_name': item['item_name'],
                'item_quantity': item['item_quantity'],
                'section': section
            })

    bom_df = pd.DataFrame(bom_items)
    st.table(bom_df)  # Display BOM items as a table in Streamlit

    # 3. Display Recipe Steps (Step 3) with formatted item details
    st.subheader("Recipe Steps")
    for idx, step in enumerate(st.session_state.steps, start=1):
        # Display step header
        st.markdown(f"<span style='color: green; font-weight: bold;'>**Step {idx}:** {step['step_type']} in {step['section']}</span>", unsafe_allow_html=True)

        # List each item in this step with detailed format
        st.write("**Items in this step:**")
        for selected_item in step['selected_items']:
            # Split to get only the item_code (format: "item_code - item_name")
            item_code = selected_item.split(" - ")[0].strip()
            item_found = False
            for section, items in st.session_state.bom_sections.items():
                for item in items:
                    if item['item_code'] == item_code:
                        st.write(f"Item Number: {item['item_number']} - Code: {item['item_code']} - "
                                 f"Name: {item['item_name']} - Quantity: {item['item_quantity']}")
                        item_found = True
                        break
                if item_found:
                    break
            if not item_found:
                st.write(f"Item with code '{item_code}' not found in BOM.")

        # Display additional fields and timestamp
        for field, value in step["step_fields"].items():
            st.write(f"**{field}:** {value if value else 'N/A'}")
        st.write(f"Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("---")

    # Input for PDF password
    password = st.text_input("Enter a password for the PDF:", type="password")

    if st.button("Generate PDF"):
        if password:
            pdf_file = create_pdf_with_password(product_info, bom_items, st.session_state.steps, password)
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="complete_overview.pdf",
                mime="application/pdf"
            )
            st.success("PDF generated and secured with your password!")
        else:
            st.warning("Please enter a password to secure the PDF.")

# Ensure the data is stored in session state before running page_4
page_4()
