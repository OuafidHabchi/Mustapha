import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Database connection
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def create_recipe_page():
    st.title("Create a New Recipe")

    # Initialize session states
    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "current_main_step" not in st.session_state:
        st.session_state.current_main_step = None
    if "sub_steps" not in st.session_state:
        st.session_state.sub_steps = []
    if "recipe_started" not in st.session_state:
        st.session_state.recipe_started = False
    if "show_recipe_overview" not in st.session_state:
        st.session_state.show_recipe_overview = False

    # Recipe name section
    if not st.session_state.recipe_started:
        st.write("### Recipe Details")
        recipe_name = st.text_input("Recipe Name")
        if st.button("Start Recipe"):
            st.session_state.recipe_started = True
            st.session_state.recipe_name = recipe_name

    # Add Main Step section
    if st.session_state.recipe_started and not st.session_state.current_main_step:
        st.markdown("<h3 style='color:#4a90e2;'>Add a New Main Step</h3>", unsafe_allow_html=True)
        main_step_options = ["Dry Mixing", "autre etape 1", "autre etape 2"]
        selected_main_step = st.selectbox("Select Main Step", options=main_step_options, key="main_step_select")
        
        if st.button("Confirm Main Step"):
            st.session_state.current_main_step = selected_main_step
            st.session_state.sub_steps = []  # Reset sub-steps when a new main step is added
            st.success(f"Main step '{selected_main_step}' selected. Now add sub-steps below.")

    # Add Sub-Step section for the selected main step
    if st.session_state.current_main_step:
        st.markdown(f"<h4 style='color:#7c83fd;'>Adding Sub-Steps to: {st.session_state.current_main_step}</h4>", unsafe_allow_html=True)

        # Define sub-step options and parameters based on selected main step
        if st.session_state.current_main_step == "Dry Mixing":
            sub_step_options = ["Mixing/Lubrication Steps", "Milling Steps", "Manual Sieving Steps"]
            parameters_mapping = {
                "Mixing/Lubrication Steps": ["Blender Size", "Mixing Time", "Mixing Speed"],
                "Milling Steps": ["Comil Model", "Impeller Type", "Sieve Size/Type", "Impeller Speed"],
                "Manual Sieving Steps": ["Screen Size"]
            }
        elif st.session_state.current_main_step == "autre etape 1":
            sub_step_options = ["Sub-step 1.1", "Sub-step 1.2", "Sub-step 1.3"]
            parameters_mapping = {
                "Sub-step 1.1": ["Param 1"],
                "Sub-step 1.2": ["Param 2"],
                "Sub-step 1.3": ["Param 3"]
            }
        elif st.session_state.current_main_step == "autre etape 2":
            sub_step_options = ["Sub-step 2.1", "Sub-step 2.2", "Sub-step 2.3"]
            parameters_mapping = {
                "Sub-step 2.1": ["Setting A"],
                "Sub-step 2.2": ["Setting B"],
                "Sub-step 2.3": ["Setting C"]
            }

        # Select and add sub-step with parameters
        selected_sub_step = st.selectbox("Select Sub-Step", options=sub_step_options)
        parameters = {}
        for param in parameters_mapping.get(selected_sub_step, []):
            parameters[param] = st.text_input(f"{param} for {selected_sub_step}", key=f"{selected_sub_step}_{param}")

        if st.button("Add Sub-Step"):
            st.session_state.sub_steps.append({
                "sub_step": selected_sub_step,
                "parameters": parameters
            })
            st.success(f"Sub-step '{selected_sub_step}' added to '{st.session_state.current_main_step}'")

        # Button to finalize main step
        if st.button("Finalize Main Step"):
            st.session_state.steps.append({
                "main_step": st.session_state.current_main_step,
                "sub_steps": st.session_state.sub_steps
            })
            st.success(f"Main step '{st.session_state.current_main_step}' added to recipe!")
            st.session_state.current_main_step = None  # Reset for a new main step
            st.session_state.sub_steps = []  # Clear sub-steps for next main step

    # Button to toggle recipe overview display
    if st.button("View Recipe"):
        st.session_state.show_recipe_overview = not st.session_state.show_recipe_overview

    # Conditionally display the Recipe Steps Overview based on the toggle
    if st.session_state.show_recipe_overview and st.session_state.steps:
        st.write("### Recipe Steps Overview")
        for idx, step in enumerate(st.session_state.steps, start=1):
            # Main Step Styling: Blue and Bold
            st.markdown(f"<div style='color:blue; font-size:1.2em; font-weight:bold;'>Step {idx}: Main Step - {step['main_step']}</div>", unsafe_allow_html=True)
            # Sub-Step Styling: Bold
            for sub_idx, sub_step in enumerate(step["sub_steps"], start=1):
                st.markdown(f"<div style='font-weight:bold; margin-left: 20px;'>Sub-Step {sub_idx}: {sub_step['sub_step']}</div>", unsafe_allow_html=True)
                for param, value in sub_step["parameters"].items():
                    st.markdown(f"<div style='margin-left: 40px;'>• {param}: {value}</div>", unsafe_allow_html=True)

    # Submit Recipe button
    if st.session_state.steps and st.button("Submit Recipe"):
        recipe_data = {
            "recipe_id": st.session_state.recipe_name.lower().replace(" ", "_"),
            "recipe_name": st.session_state.recipe_name,
            "steps": st.session_state.steps,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        collection.insert_one(recipe_data)
        st.success("Recipe submitted successfully!")
        st.session_state.steps = []  # Clear steps after submission
        st.session_state.current_main_step = None
        st.session_state.sub_steps = []
        st.session_state.recipe_started = False
        st.session_state.show_recipe_overview = False

    # Optional: Back to Welcome Page button
    if st.button("Back to Welcome Page"):
        st.session_state["page"] = "welcome"
