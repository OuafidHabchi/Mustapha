import streamlit as st
from page_1 import page_1
from page_2 import page_2
from page_3 import page_3
from page_4 import page_4

# Inline CSS
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
    .stButton.prev-button>button {
        background-color: #dc3545;
        color: white;
    }
    .stButton.prev-button>button:hover {
        background-color: #c82333;
        color: white;
    }
    .stButton.next-button>button {
        background-color: #28a745;
        color: white;
    }
    .stButton.next-button>button:hover {
        background-color: #218838;
        color: white;
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
if "page_updated" not in st.session_state:
    st.session_state.page_updated = False  # Variable temporaire pour suivre le changement de page

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

# "Précédent" button in the first column with custom styling
with col1:
    if st.session_state.current_step > 1:
        if st.button("Précédent", key="prev_button"):
            st.session_state.current_step -= 1
            st.session_state.page_updated = True  # Marquer la page comme mise à jour

# "Suivant" button in the fifth column with custom styling
with col5:
    if st.session_state.current_step < 4:
        if st.button("Suivant", key="next_button"):
            st.session_state.current_step += 1
            st.session_state.page_updated = True  # Marquer la page comme mise à jour

# Forcer le rafraîchissement si la page a été mise à jour
if st.session_state.page_updated:
    st.session_state.page_updated = False  # Réinitialiser la variable
    st.experimental_rerun()
