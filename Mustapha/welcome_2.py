import streamlit as st
from page_1 import page_1
from page_2 import page_2
from page_3 import page_3
from page_4 import page_4

# Inline CSS pour le style des boutons et de la barre de progression
st.markdown("""
    <style>
    .stApp {
        background-color: #cfe8ff;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }

    .progress-bar {
        height: 8px;
        background-color: #cccccc;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .progress-bar-fill {
        height: 100%;
        background-color: #28a745;
        width: 0%;
        transition: width 0.4s ease;
    }

    .stButton>button {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
    }
    .prev-button {
        background-color: #dc3545;
        color: white;
        font-weight: bold;
    }
    .next-button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de l'état de session pour le suivi des étapes
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "product_info" not in st.session_state:
    st.session_state.product_info = {}
if "bom_sections" not in st.session_state:
    st.session_state.bom_sections = {}
if "steps" not in st.session_state:
    st.session_state.steps = []

# Fonction pour afficher la barre de progression
def show_progress():
    progress_percentage = ((st.session_state.current_step - 1) / 3) * 100
    st.markdown(
        f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress_percentage}%;"></div>
        </div>
        """, unsafe_allow_html=True
    )
    st.write(f"Étape {st.session_state.current_step} sur 4")

# Affichage de la barre de progression
show_progress()

# Chargement de la page en fonction de l'étape actuelle
if st.session_state.current_step == 1:
    page_1()
elif st.session_state.current_step == 2:
    page_2()
elif st.session_state.current_step == 3:
    page_3()
elif st.session_state.current_step == 4:
    page_4()

# Conteneur de boutons pour navigation
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Bouton "Précédent" avec style rouge
with col1:
    if st.session_state.current_step > 1:
        if st.button("Précédent", key="prev_button", help="Revenir à l'étape précédente", on_click=lambda: setattr(st.session_state, 'current_step', st.session_state.current_step - 1)):
            pass  # Met à jour current_step sans redémarrer la page

# Bouton "Suivant" avec style vert
with col5:
    if st.session_state.current_step < 4:
        if st.button("Suivant", key="next_button", help="Aller à l'étape suivante", on_click=lambda: setattr(st.session_state, 'current_step', st.session_state.current_step + 1)):
            pass  # Met à jour current_step sans redémarrer la page
