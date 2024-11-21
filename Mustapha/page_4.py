import streamlit as st
from fpdf import FPDF
from io import BytesIO
import os

def create_pdf_without_password(product_info, steps, prepared_by):
    """Génère un PDF esthétique avec chaque étape sur une page distincte."""
    pdf = FPDF()
    pdf.add_page()

    # Chemin du logo
    logo_path = os.path.join(os.getcwd(), "options", "images", "image.png")

    # Vérifier si le logo existe
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)  # Position (x, y) et largeur (w)
        logo_y_position = 8 + 30  # Ajuste la position y en fonction de la hauteur du logo
    else:
        st.warning("Logo image not found. PDF generated without the logo.")
        logo_y_position = 10  # Position de repli si le logo est absent

    # "Prepared by" sous le logo
    pdf.set_xy(10, logo_y_position + 5)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 128)  # Bleu foncé
    pdf.cell(200, 10, txt=f"Prepared by: {prepared_by}", ln=True)

    # Section "Product Information"
    pdf.set_xy(10, logo_y_position + 20)
    pdf.set_text_color(0, 102, 204)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Product Information", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Espacement
    for key, value in product_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.cell(200, 10, txt=" ", ln=True)  # Espacement

    # Section "Recipe Steps"
    for idx, step in enumerate(steps, start=1):
        pdf.add_page()  # Ajouter une nouvelle page pour chaque étape

        # Titre de l'étape
        pdf.set_fill_color(220, 240, 220)  # Vert clair pour le fond
        pdf.set_text_color(0, 51, 0)  # Vert foncé pour le texte de l'étape
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Step {idx}:", ln=True, fill=True)

        # Section et type d'étape
        pdf.set_text_color(0, 102, 204)  # Bleu pour les sous-titres
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt=f"  Section: {step['section']}", ln=True)
        pdf.cell(200, 10, txt=f"  Step: {step['step_type']}", ln=True)

        # Items inclus dans l'étape
        pdf.set_text_color(0, 0, 0)  # Noir pour les items
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt="  Items in this step:", ln=True)
        for selected_item in step['selected_items']:
            pdf.cell(200, 10, txt=f"    - {selected_item}", ln=True)

        # Champs additionnels
        for field, value in step.get("step_fields", {}).items():
            pdf.cell(200, 10, txt=f"    {field}: {value if value else 'N/A'}", ln=True)

        # Afficher les données des checkboxes
        if step.get("keep_bag_for_rinsing", False):
            pdf.set_text_color(255, 69, 0)  # Rouge pour attirer l'attention
            pdf.cell(200, 10, txt="    Keep Bag for rinsing: Yes", ln=True)
        if step["step_type"] == "Dispersion":
            if step.get("use_full_quantity", False):
                pdf.set_text_color(0, 128, 128)  # Teal
                pdf.cell(200, 10, txt="    Use full quantity: Yes", ln=True)
            if step.get("keep_bag_for_rinsing_dispersion", False):
                pdf.set_text_color(255, 140, 0)  # Orange
                pdf.cell(200, 10, txt="    Keep Bag for rinsing (Dispersion): Yes", ln=True)

        # Date d'ajout
        pdf.set_text_color(0, 0, 0)  # Noir
        pdf.cell(200, 10, txt=f"    Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

        # Espacement entre les sections
        pdf.cell(200, 10, txt=" ", ln=True)

    # Output PDF to BytesIO
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
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

    # Affichage des étapes de recette
    st.subheader("Process Steps")
    for idx, step in enumerate(st.session_state.steps, start=1):
        st.markdown(f"### Step {idx}")
        st.write(f"**Section:** {step['section']}")
        st.write(f"**Step:** {step['step_type']}")
        st.write("**Items in this step:**")
        for selected_item in step['selected_items']:
            st.write(f"- {selected_item}")
        for field, value in step.get("step_fields", {}).items():
            st.write(f"**{field}:** {value if value else 'N/A'}")

        # Afficher les données des checkboxes
        if step.get("keep_bag_for_rinsing", False):
            st.write("**Keep Bag for rinsing:** Yes")
        if step["step_type"] == "Dispersion":
            if step.get("use_full_quantity", False):
                st.write("**Use full quantity:** Yes")
            if step.get("keep_bag_for_rinsing_dispersion", False):
                st.write("**Keep Bag for rinsing (Dispersion):** Yes")

        st.write(f"Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("---")
        
    # Input pour le nom de la personne qui a préparé la recette
    prepared_by = st.text_input("Process prepared by:")

    # Bouton pour générer le PDF
    if st.button("Generate PDF"):
        if prepared_by:
            pdf_file = create_pdf_without_password(product_info, st.session_state.steps, prepared_by)
            file_name = f"{product_info.get('Name', 'Recipe')}.pdf"
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
