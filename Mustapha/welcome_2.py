import streamlit as st
from page_1 import page_1
from page_2 import page_2
from page_3 import page_3
from page_4 import page_4

# Inline CSS
st.markdown("""
    <style>
    /* Arrière-plan bleu ciel */
    .stApp {
        background-color: #cfe8ff; /* Bleu ciel pour un effet apaisant */
        color: #333333; /* Couleur de texte sombre pour contraste */
        font-family: 'Arial', sans-serif;
    }

    /* Barre de progression moderne */
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
        background-color: #28a745; /* Vert pour indiquer la progression */
        width: 0%;
        transition: width 0.4s ease;
    }

    /* Style des boutons */
    .stButton>button {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
    }
    /* Bouton Précédent rouge */
    .stButton.prev-button>button {
        background-color: #dc3545;
        color: white;
    }
    .stButton.prev-button>button:hover {
        background-color: #c82333;
        color: white;
    }
    /* Bouton Suivant vert */
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
    prev_button_placeholder = st.empty()
    if st.session_state.current_step > 1:
        with prev_button_placeholder.container():
            if st.button("Précédent", key="prev_button"):
                st.session_state.current_step -= 1
                st.experimental_rerun()
    st.markdown('<div class="stButton prev-button"></div>', unsafe_allow_html=True)

# Empty space in the other columns for alignment
with col2, col3, col4:
    st.write("")

# "Suivant" button in the fifth column with custom styling
with col5:
    next_button_placeholder = st.empty()
    if st.session_state.current_step < 4:
        with next_button_placeholder.container():
            if st.button("Suivant", key="next_button"):
                st.session_state.current_step += 1
                st.experimental_rerun()
    st.markdown('<div class="stButton next-button"></div>', unsafe_allow_html=True)
