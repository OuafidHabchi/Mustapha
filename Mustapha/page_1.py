import streamlit as st

def page_1():
     # CSS pour ajuster la taille des boutons
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;  /* Ajuste le padding pour la taille souhaitée */
            font-size: 14px;    /* Ajuste la taille de la police */
            border-radius: 6px; /* Ajoute un peu de bord arrondi pour le style */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Étape 1 : Informations de base")

    # Entrée des informations de base
    product_name = st.text_input("Nom du produit", value=st.session_state.product_info.get("product_name", ""))
    product_code = st.text_input("Code du produit", value=st.session_state.product_info.get("product_code", ""))
    batch_size = st.text_input("Taille du lot", value=st.session_state.product_info.get("batch_size", ""))

    if st.button("Enregistrer"):
        if product_name and product_code and batch_size:
            st.session_state.product_info = {
                "product_name": product_name,
                "product_code": product_code,
                "batch_size": batch_size
            }
            st.success("Informations de base enregistrées.")
        else:
            st.error("Veuillez remplir tous les champs.")
