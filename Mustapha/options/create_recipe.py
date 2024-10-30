import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Database connection
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def create_recipe_page():
    st.title("🍲 Recipe Creator")

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
    with st.expander("Recipe Details", expanded=not st.session_state.recipe_started):
        recipe_name = st.text_input("Enter Recipe Name")
        if st.button("Start Recipe", key="start_recipe"):
            st.session_state.recipe_started = True
            st.session_state.recipe_name = recipe_name
            st.success("Recipe started! Use 'Add Main Step' to begin.")

    # Main Step selection and sub-steps addition
    if st.session_state.current_main_step:
        with st.expander(f"Add Main Step - {st.session_state.current_main_step}", expanded=True):
            main_step_options = ["Dry Mixing", "autre etape 1", "autre etape 2"]
            selected_main_step = st.selectbox("Select a Main Step", options=main_step_options)

            if st.button("Confirm Main Step", key="confirm_main_step"):
                st.session_state.current_main_step = selected_main_step
                st.session_state.sub_steps = []  # Clear sub-steps for new main step
                st.success(f"Main step '{selected_main_step}' selected! Add sub-steps below.")

            # Sub-Step section for the selected main step
            if st.session_state.current_main_step != "new_step":
                sub_step_options, parameters_mapping = [], {}
                
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

                selected_sub_step = st.selectbox("Select Sub-Step", options=sub_step_options)
                parameters = {param: st.text_input(f"{param}", key=f"{selected_sub_step}_{param}") for param in parameters_mapping.get(selected_sub_step, [])}

                if st.button("Add Sub-Step", key="add_sub_step"):
                    st.session_state.sub_steps.append({
                        "sub_step": selected_sub_step,
                        "parameters": parameters
                    })
                    st.success(f"Added sub-step '{selected_sub_step}' to '{st.session_state.current_main_step}'")

                # Finalize main step button
                if st.button("Finalize Main Step", key="finalize_main_step"):
                    st.session_state.steps.append({
                        "main_step": st.session_state.current_main_step,
                        "sub_steps": st.session_state.sub_steps
                    })
                    st.success(f"Main step '{st.session_state.current_main_step}' finalized and added to recipe!")
                    st.session_state.current_main_step = None  # Reset to show "Add Main Step" button again
                    st.session_state.sub_steps = []  # Clear sub-steps for next main step

    # Persistent Bottom Buttons Section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Button to add a new Main Step
    with col1:
        if st.button("➕ Add Main Step", key="bottom_add_main_step"):
            st.session_state.current_main_step = "new_step"

    # Toggle button for Recipe Overview
    with col2:
        if st.button("📄 View Recipe Overview", key="view_recipe"):
            st.session_state.show_recipe_overview = not st.session_state.show_recipe_overview

    # Submit Recipe button
    with col3:
        if st.button("✅ Submit Recipe", key="submit_recipe"):
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

    # Conditionally display the Recipe Steps Overview
    if st.session_state.show_recipe_overview and st.session_state.steps:
        st.markdown("---")
        with st.expander("Recipe Steps Overview", expanded=True):
            for idx, step in enumerate(st.session_state.steps, start=1):
                # Main Step Styling
                st.markdown(f"<div style='color:blue; font-size:1.2em; font-weight:bold;'>Step {idx}: Main Step - {step['main_step']}</div>", unsafe_allow_html=True)
                # Sub-Step Styling
                for sub_idx, sub_step in enumerate(step["sub_steps"], start=1):
                    st.markdown(f"<div style='font-weight:bold; margin-left: 20px;'>Sub-Step {sub_idx}: {sub_step['sub_step']}</div>", unsafe_allow_html=True)
                    for param, value in sub_step["parameters"].items():
                        st.markdown(f"<div style='margin-left: 40px;'>• {param}: {value}</div>", unsafe_allow_html=True)
