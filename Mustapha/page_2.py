import streamlit as st

def page_2():
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Étape 2 : Nombre d'items")

    # Saisie du nombre d'items
    item_count = st.number_input("Combien d'items voulez-vous utiliser ?", min_value=1, step=1)

    if st.button("Confirmer"):
        st.session_state.bom_items_count = item_count
        # Générer les items automatiquement de 1 à item_count
        st.session_state.bom_items = [f"Item {i}" for i in range(1, item_count + 1)]
        st.success("Nombre d'items enregistré.")
