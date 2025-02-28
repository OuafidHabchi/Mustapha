import streamlit as st
from fpdf import FPDF
from io import BytesIO
import os
import pandas as pd

def create_pdf_without_password(product_info, steps, prepared_by, ui_table_data):
    """Generate a professionally designed PDF with product info, a Equipements table, and detailed steps."""
    from fpdf import FPDF
    from io import BytesIO
    import os
    import unicodedata

    # Helper function to normalize text
    def normalize_text(text):
        if isinstance(text, str):
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        return text

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.set_text_color(50, 50, 50)
            self.cell(0, 10, "Process Documentation", align="C", ln=True)
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(128)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    # Initialize PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Logo (Photo)
    logo_path = os.path.join(os.getcwd(), "Mustapha", "options", "images", "image.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)  # Ensure the image is correctly loaded
    else:
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, "Logo not found", ln=True)

    # Prepared by
    pdf.set_xy(10, 30)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, txt=f"Prepared by: {normalize_text(prepared_by)}", ln=True)

    # Product Information
    pdf.set_xy(10, 40)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Product Information", align="C", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    for key, value in product_info.items():
        pdf.cell(0, 8, txt=f"{key}: {normalize_text(value)}", ln=True)
    pdf.ln(5)

    # Equipements Table
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Equipements Table", align="C", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(90, 8, "Equipements", border=1, fill=True, align="C")
    pdf.cell(60, 8, "Value", border=1, fill=True, align="C")
    pdf.cell(40, 8, "Step", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_fill_color(245, 245, 245)
    for idx, row in ui_table_data.iterrows():
        fill = idx % 2 == 0
        pdf.cell(90, 8, normalize_text(row["Equipements"]), border=1, fill=fill, align="L")
        pdf.cell(60, 8, normalize_text(row["Value"]), border=1, fill=fill, align="L")
        pdf.cell(40, 8, normalize_text(row["Step"]), border=1, fill=fill, align="C")
        pdf.ln()

    # Process Steps
    for idx, step in enumerate(steps, start=1):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(220, 240, 240)
        pdf.set_text_color(0, 0, 128)
        pdf.cell(0, 10, f"Step {idx}: {normalize_text(step['step_type'])}", border=0, ln=True, fill=True)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, f"Section: {normalize_text(step['section'])}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)

        # Items Used
        if "selected_items" in step.get("step_fields", {}):
            items_used = step["step_fields"]["selected_items"]
            if items_used:
                pdf.cell(0, 8, "Items Used:", ln=True)
                for item in items_used:
                    pdf.cell(0, 8, f"  - {normalize_text(item)}", ln=True)

        # Details of Step
        for field, value in step.get("step_fields", {}).items():
            if field in ["selected_items", "use_full_quantity"]:  # Skip redundant fields
                continue
            if field == "strengths" and isinstance(value, list):
                for i, strength in enumerate(value, 1):
                    strength_value = strength.get("Strength value (mg)", "N/A")
                    pdf.cell(0, 8, f"Strength {i} ({normalize_text(str(strength_value))} mg):", ln=True)
                    for strength_key, strength_value in strength.items():
                        if strength_key == "Strength value (mg)":
                            continue
                        pdf.cell(0, 8, f"    - {normalize_text(str(strength_key))}: {normalize_text(str(strength_value))}", ln=True)
            else:
                pdf.cell(0, 8, f"{normalize_text(field)}: {normalize_text(str(value)) if value else 'N/A'}", ln=True)

        # Timestamp
        pdf.cell(0, 8, f"Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Output PDF
    pdf_output = BytesIO()
    try:
        pdf_data = pdf.output(dest='S').encode('latin1')  # Generate PDF content as a string
        pdf_output.write(pdf_data)  # Write to BytesIO
        pdf_output.seek(0)  # Reset the pointer
    except Exception as e:
        raise RuntimeError(f"Error generating PDF: {str(e)}")

    return pdf_output







def page_4():
    """Affiche les informations finales et permet de générer un PDF."""
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title(" Complete Overview ")

    # Données par défaut si non présentes
    if 'product_info' not in st.session_state:
        st.session_state.product_info = {'Name': 'Default Product', 'Batch Size': '1000', 'Category': 'Pharmaceutical'}
    if 'steps' not in st.session_state:
        st.session_state.steps = []

    # Affichage des informations du produit
    st.subheader("Product Information")
    product_info = st.session_state.product_info
    for key, value in product_info.items():
        st.write(f"**{key}:** {value}")
        
    # Données par défaut si non présentes
    if 'steps' not in st.session_state:
        st.session_state.steps = []

    # Champs à inclure dans le tableau
    fields_to_include = [
        "BIN SIZE (L)", "COMIL MODEL", "IMPELLER TYPE", "SEIVE SIZE AND TYPE",
        "ROLLER COMPACTOR TF-220", "Mixer Type", "Homogenizer","MANUAL SCREEN",
        "HIGH SHEAR 65L", "FLUID BED DRYER O’HARA 15 KG", "PRESS TYPE/MODEL"
    ]

    # Construire les données pour le tableau
    table_rows = []
    for idx, step in enumerate(st.session_state.steps, start=1):
        # Vérifier les champs directs
        for field in fields_to_include:
            value = step.get("step_fields", {}).get(field, None)
            if value:  # N'inclure que si une valeur existe
                table_rows.append({
                    "Equipements": field,
                    "Value": value,
                    "Step": f"Step {idx}"
                })

         # Vérifier les champs imbriqués (e.g., strengths)
        strengths = step.get("step_fields", {}).get("strengths", [])
        if strengths and isinstance(strengths, list):
            for i, strength in enumerate(strengths, start=1):  # Ajouter le numéro de strength
                if isinstance(strength, dict):
                    press_type = strength.get("Press Type/Model", None)
                    if press_type:
                        table_rows.append({
                            "Equipements": f"PRESS TYPE/MODEL (Strength {i})",  # Inclure le numéro de strength
                            "Value": press_type,
                            "Step": f"Step {idx}"
                        })

    # Afficher le tableau
    st.subheader("Equipements Table")
    if table_rows:
        # Générer le tableau en HTML pour un style propre
        table_html = "<table style='width:100%; border-collapse:collapse; text-align:left;'>"
        table_html += "<tr style='background-color:#f2f2f2;'>"
        table_html += "<th style='border:1px solid black; padding:8px;'>Equipements</th>"
        table_html += "<th style='border:1px solid black; padding:8px;'>Value</th>"
        table_html += "<th style='border:1px solid black; padding:8px;'>Step</th>"
        table_html += "</tr>"

        for row in table_rows:
            table_html += "<tr>"
            table_html += f"<td style='border:1px solid black; padding:8px;'>{row['Equipements']}</td>"
            table_html += f"<td style='border:1px solid black; padding:8px;'>{row['Value']}</td>"
            table_html += f"<td style='border:1px solid black; padding:8px;'>{row['Step']}</td>"
            table_html += "</tr>"

        table_html += "</table>"

        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("No relevant Equipements found to summarize.")
    # Create a DataFrame for the UI table
    ui_table_data = pd.DataFrame(table_rows)

    
    # Affichage des étapes de recette
    st.subheader("Process Steps")
    for idx, step in enumerate(st.session_state.steps, start=1):
        st.markdown(f"### Step {idx}")
        st.write(f"**Section:** {step['section']}")
        st.write(f"**Step:** {step['step_type']}")
         # Display "Items Used" instead of "selected_items"
        if "selected_items" in step.get("step_fields", {}):
            items_used = step["step_fields"]["selected_items"]
            if items_used:  # Ensure there are items to display
                st.write(f"**Items Used:**")
                for item in items_used:
                    st.write(f"  - {item}")
        

        # Display step fields
        for field, value in step.get("step_fields", {}).items():
            if field == "selected_items":  # Skip displaying selected_items
                continue
            if field == "Item to Rinse With" and value:
                # Check and handle "use_full_quantity" explicitly
                use_full_quantity = step["step_fields"].get("use_full_quantity", False)
                use_full_quantity_text = "Yes" if use_full_quantity else "No"
                st.write(f"**{field}:** {value} (Use full quantity: {use_full_quantity_text})")
            elif field == "use_full_quantity":
                # Skip displaying the redundant "use_full_quantity"
                continue
            elif field == "strengths" and isinstance(value, list):
                # Handle strengths only if they exist and are a list
                for i, strength in enumerate(value, 1):
                    # Retrieve the "Strength value (mg)" if it exists
                    strength_value = strength.get("Strength value (mg)", "N/A")
                    st.write(f"  - **Strength {i}** ({strength_value} mg):")
                    # Display other properties of the strength
                    for strength_key, strength_value in strength.items():
                        if strength_key in ["Strength value (mg)", "strength"]:  # Skip these keys
                            continue
                        st.write(f"      - {strength_key}: {strength_value if strength_value else 'N/A'}")
            else:
                # Display other fields
                st.write(f"**{field}:** {value if value else 'N/A'}")

        # Display the timestamp
        st.write(f"Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("---")
        
    # Input pour le nom de la personne qui a préparé la recette
    prepared_by = st.text_input("Process prepared by:")

    # Bouton pour générer le PDF
    if st.button("Generate PDF"):
        if prepared_by:
            pdf_file = create_pdf_without_password(product_info, st.session_state.steps, prepared_by,ui_table_data)
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



# Exécuter la fonction pour afficher la page 4
page_4()
