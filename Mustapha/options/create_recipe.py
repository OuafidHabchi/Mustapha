import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Database connection
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def create_recipe_page():
    st.title("Create a New Recipe")

    # Ensure 'steps' is initialized in session state upon each call
    if "steps" not in st.session_state:
        st.session_state.steps = []

    # Input for recipe name
    recipe_name = st.text_input("Recipe Name", st.session_state.get("recipe_name", "My Recipe"))

    # Main Step Input Section
    with st.container():
        st.markdown("<div style='padding:10px; border:2px solid #4a90e2; border-radius:10px; background-color:#e9f4ff;'><h3 style='color:#4a90e2;'>Main Step</h3></div>", unsafe_allow_html=True)
        
        main_step_options = ["Dry Mixing", "autre etape 1", "autre etape 2"]
        selected_main_step = st.selectbox("Select Main Step", options=main_step_options)
        st.session_state.main_step = selected_main_step

    # Define sub-step options and parameters based on selected main step
    if st.session_state.main_step == "Dry Mixing":
        sub_step_options = ["Mixing/Lubrication Steps", "Milling Steps", "Manual Sieving Steps"]
        parameters_mapping = {
            "Mixing/Lubrication Steps": ["Blender Size", "Mixing Time", "Mixing Speed"],
            "Milling Steps": ["Comil Model", "Impeller Type", "Sieve Size/Type", "Impeller Speed"],
            "Manual Sieving Steps": ["Screen Size"]
        }
    elif st.session_state.main_step == "autre etape 1":
        sub_step_options = ["Sub-step 1.1", "Sub-step 1.2", "Sub-step 1.3"]
        parameters_mapping = {
            "Sub-step 1.1": ["Param 1"],
            "Sub-step 1.2": ["Param 2"],
            "Sub-step 1.3": ["Param 3"]
        }
    elif st.session_state.main_step == "autre etape 2":
        sub_step_options = ["Sub-step 2.1", "Sub-step 2.2", "Sub-step 2.3"]
        parameters_mapping = {
            "Sub-step 2.1": ["Setting A"],
            "Sub-step 2.2": ["Setting B"],
            "Sub-step 2.3": ["Setting C"]
        }

    # Sub-Step Input Section
    with st.container():
        st.markdown("<div style='padding:10px; border:2px solid #7c83fd; border-radius:10px; background-color:#eef1ff;'><h4 style='color:#7c83fd;'>Sub-Step</h4></div>", unsafe_allow_html=True)
        
        selected_sub_step = st.selectbox("Select Sub-Step", options=sub_step_options)
        st.session_state.sub_step = selected_sub_step

        # Display parameter fields based on selected sub-step
        parameters = {}
        for param in parameters_mapping.get(st.session_state.sub_step, []):
            parameters[param] = st.text_input(param, value="")

    # Add Main Step with Sub-Step button
    if st.button("Add Main Step with Sub-Step"):
        # Append the main step along with the selected sub-step and parameters as a unique entry
        # If a main step exists, add the sub-step directly to it, otherwise, create a new main step entry.
        st.session_state.steps.append({
            "main_step": st.session_state.main_step,
            "sub_steps": [{
                "sub_step": st.session_state.sub_step,
                "parameters": parameters
            }]
        })
        
        st.success(f"Main step '{st.session_state.main_step}' with sub-step '{st.session_state.sub_step}' added!")

    # Display the current list of steps in a hierarchical structure with visual styling
    st.write("### Current Recipe Steps")
    for idx, step in enumerate(st.session_state.steps, start=1):
        # Display main step
        st.markdown(f"<div style='color:blue; font-size:1.3em; font-weight:bold;'>Step {idx}: Main Step - {step['main_step']}</div>", unsafe_allow_html=True)
        # Display sub-steps
        for sub_idx, sub_step in enumerate(step["sub_steps"], start=1):
            st.markdown(f"<div style='color:grey; font-size:1.1em; font-weight:bold; margin-left: 20px;'>Sub-Step{sub_idx}: {sub_step['sub_step']}</div>", unsafe_allow_html=True)
            for param, value in sub_step["parameters"].items():
                st.markdown(f"<div style='color:grey;'>&emsp;&emsp;• {param}: {value}</div>", unsafe_allow_html=True)

    # Submit Recipe button
    if st.button("Submit Recipe"):
        recipe_data = {
            "recipe_id": recipe_name.lower().replace(" ", "_"),
            "recipe_name": recipe_name,
            "steps": st.session_state.steps,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        collection.insert_one(recipe_data)
        st.success("Recipe submitted successfully!")
        st.session_state.steps = []  # Clear steps after submission

    # Optional: Back to Welcome Page button
    if st.button("Back to Welcome Page"):
        st.session_state["page"] = "welcome"
