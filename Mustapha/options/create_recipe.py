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

    # Input for recipe name
    recipe_name = st.text_input("Recipe Name", st.session_state.get("recipe_name", "My Recipe"))

    # Button to add a new Main Step
    if st.button("Add Main Step"):
        st.session_state.current_main_step = None
        st.session_state.sub_steps = []  # Clear sub-steps when a new main step is added

    # Display Main Step options if "Add Main Step" is clicked
    if st.session_state.current_main_step is None:
        main_step_options = ["Dry Mixing", "autre etape 1", "autre etape 2"]
        selected_main_step = st.selectbox("Select Main Step", options=main_step_options)
        
        # Button to confirm and add the selected main step
        if st.button("Confirm Main Step"):
            st.session_state.current_main_step = selected_main_step
            st.success(f"Main step '{selected_main_step}' selected! Now add sub-steps.")

    # Show Sub-Step options if a main step is selected
    if st.session_state.current_main_step:
        st.markdown(f"**Adding sub-steps for Main Step: {st.session_state.current_main_step}**")

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

        # Select Sub-Step
        selected_sub_step = st.selectbox("Select Sub-Step", options=sub_step_options)

        # Input fields for parameters based on the selected sub-step
        parameters = {}
        for param in parameters_mapping.get(selected_sub_step, []):
            parameters[param] = st.text_input(f"{param} for {selected_sub_step}")

        # Button to add the sub-step with parameters
        if st.button("Add Sub-Step"):
            st.session_state.sub_steps.append({
                "sub_step": selected_sub_step,
                "parameters": parameters
            })
            st.success(f"Sub-step '{selected_sub_step}' added to '{st.session_state.current_main_step}'!")

        # Display current sub-steps for the selected main step
        if st.session_state.sub_steps:
            st.write("### Current Sub-Steps")
            for idx, sub_step in enumerate(st.session_state.sub_steps, start=1):
                st.markdown(f"**Sub-Step {idx}: {sub_step['sub_step']}**")
                for param, value in sub_step["parameters"].items():
                    st.markdown(f"- {param}: {value}")

        # Button to finalize the main step with its sub-steps and add to the steps list
        if st.button("Finalize Main Step"):
            st.session_state.steps.append({
                "main_step": st.session_state.current_main_step,
                "sub_steps": st.session_state.sub_steps
            })
            st.success(f"Main step '{st.session_state.current_main_step}' added to recipe!")
            st.session_state.current_main_step = None  # Reset to allow adding a new main step
            st.session_state.sub_steps = []  # Reset sub-steps for new main steps

    # Display the entire recipe sequence for review
    st.write("### Recipe Steps Overview")
    for idx, step in enumerate(st.session_state.steps, start=1):
        st.markdown(f"**Step {idx}: Main Step - {step['main_step']}**")
        for sub_idx, sub_step in enumerate(step["sub_steps"], start=1):
            st.markdown(f"- Sub-Step {sub_idx}: {sub_step['sub_step']}")
            for param, value in sub_step["parameters"].items():
                st.markdown(f"  - {param}: {value}")

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
        st.session_state.current_main_step = None
        st.session_state.sub_steps = []

    # Optional: Back to Welcome Page button
    if st.button("Back to Welcome Page"):
        st.session_state["page"] = "welcome"
