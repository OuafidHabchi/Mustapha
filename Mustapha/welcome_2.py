import streamlit as st
from page_1 import page_1
from page_2 import page_2
from page_3 import page_3
from page_4 import page_4

# Inline CSS
st.markdown("""
    <style>
    /* Barre de progression */
    .progress-bar {
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .progress-bar-fill {
        height: 100%;
        background-color: #4CAF50;
        width: 0%;
        transition: width 0.3s ease;
    }
    /* Boutons de navigation */
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .nav-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .nav-button:disabled {
        background-color: #ddd;
        cursor: not-allowed;
    }
    .nav-button:hover:not(:disabled) {
        background-color: #45a049;
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
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# Set up five columns for navigation
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# "Précédent" button in the first column
with col1:
    if st.session_state.current_step > 1:
        st.button("Précédent", key="prev_button", on_click=lambda: setattr(st.session_state, 'current_step', st.session_state.current_step - 1), help="Revenir à l'étape précédente")

# Empty space in the other columns for alignment
with col2, col3, col4:
    st.write("")

# "Suivant" button in the fifth column
with col5:
    if st.session_state.current_step < 4:
        st.button("Suivant", key="next_button", on_click=lambda: setattr(st.session_state, 'current_step', st.session_state.current_step + 1), help="Aller à l'étape suivante")
