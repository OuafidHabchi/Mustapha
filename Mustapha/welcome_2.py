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

# Initialize session state for step tracking
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "product_info" not in st.session_state:
    st.session_state.product_info = {}
if "bom_sections" not in st.session_state:
    st.session_state.bom_sections = {}
if "steps" not in st.session_state:
    st.session_state.steps = []

# Function to show the progress bar
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

# Display the progress bar
show_progress()

# Load the page based on the current step
if st.session_state.current_step == 1:
    page_1()
elif st.session_state.current_step == 2:
    page_2()
elif st.session_state.current_step == 3:
    page_3()
elif st.session_state.current_step == 4:
    page_4()

# Functions to handle button clicks
def go_previous():
    if st.session_state.current_step > 1:
        st.session_state.current_step -= 1

def go_next():
    if st.session_state.current_step < 4:
        st.session_state.current_step += 1

# Navigation container with button layout
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])  
# "Previous" button in the first column with on_click function
with col1:
    st.button("Précédent", on_click=go_previous, key="prev_button")
    
# Empty space in the other columns for alignment
with col2, col3, col4:
    st.write("")

# "Next" button in the fifth column with on_click function
with col5:
    st.button("Suivant", on_click=go_next, key="next_button")
