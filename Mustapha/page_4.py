from fpdf import FPDF
from io import BytesIO

def create_pdf_without_password(product_info, steps, prepared_by):
    # Step 1: Generate the PDF content with FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # Chemin du logo
    logo_path = os.path.join(os.getcwd(),"Mustapha", "options", "images", "image.png")   
        
    # Vérifier si le logo existe
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)  # Position (x, y) et largeur (w)
        logo_y_position = 8 + 30  # Ajuste la position y en fonction de la hauteur du logo
    else:
        st.warning("Logo image not found. PDF generated without the logo.")
        logo_y_position = 10  # Position de repli si le logo est absent
    
    # "Prepared by" sous le logo
    pdf.set_xy(10, logo_y_position + 5)  # Positionner "Prepared by" juste en dessous du logo
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Prepared by: {prepared_by}", ln=True)
    
    # Product Info Section
    pdf.set_xy(10, logo_y_position + 20)  # Positionner la section d'infos produit après "Prepared by"
    pdf.set_text_color(0, 102, 204)  # Couleur bleue pour le titre du produit
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Product Information", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Espacement
    for key, value in product_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.cell(200, 10, txt=" ", ln=True)  # Espacement

    # Recipe Steps with Detailed Item Information
    pdf.set_text_color(0, 153, 76)  # Couleur verte pour le titre des étapes
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recipe Steps", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=" ", ln=True)  # Espacement
    
    for idx, step in enumerate(steps, start=1):
        # Entête de l'étape avec une couleur d'arrière-plan
        pdf.set_fill_color(220, 240, 220)  # Vert clair pour les étapes
        pdf.cell(200, 10, txt=f"Step {idx}: {step['step_type']} in {step['section']}", ln=True, fill=True)
        
        # Liste des items dans l'étape
        pdf.cell(200, 10, txt="Items in this step:", ln=True)
        for selected_item in step['selected_items']:
            item_text = f"Item: {selected_item}"
            pdf.cell(200, 10, txt=item_text, ln=True)

        # Champs additionnels de l'étape avec indent
        pdf.set_font("Arial", 'I', 10)
        for field, value in step["step_fields"].items():
            pdf.cell(200, 10, txt=f"  {field}: {value if value else 'N/A'}", ln=True)
        pdf.cell(200, 10, txt=f"  Added on: {step['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        
        # Séparateur pour chaque étape
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
        
    # Input pour le nom de la personne qui a préparé la recette
    prepared_by = st.text_input("Recipe prepared by:")

    # Bouton pour générer le PDF
    if st.button("Generate PDF"):
        if prepared_by:
            pdf_file = create_pdf_without_password(product_info, st.session_state.steps, prepared_by)
            
            # Nommer le fichier PDF en fonction du nom du produit
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
