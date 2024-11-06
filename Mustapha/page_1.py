import streamlit as st

def page_1():
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
