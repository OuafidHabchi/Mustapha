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

    # Main step selection
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

    # Sub-step selection
    selected_sub_step = st.selectbox("Select Sub-Step", options=sub_step_options)
    st.session_state.sub_step = selected_sub_step

    # Display parameter fields based on selected sub-step
    parameters = {}
    for param in parameters_mapping.get(st.session_state.sub_step, []):
        parameters[param] = st.text_input(param, value="")

    # Add Sub-Step button
    if st.button("Add Sub-Step"):
        # Find the selected main step and add a sub-step to it
        main_step_exists = any(step["main_step"] == st.session_state.main_step for step in st.session_state.steps)
        
        # If main step exists, append sub-step; otherwise, create it
        if main_step_exists:
            for step in st.session_state.steps:
                if step["main_step"] == st.session_state.main_step:
                    step["sub_steps"].append({
                        "sub_step": st.session_state.sub_step,
                        "parameters": parameters
                    })
                    break
        else:
            st.session_state.steps.append({
                "main_step": st.session_state.main_step,
                "sub_steps": [{
                    "sub_step": st.session_state.sub_step,
                    "parameters": parameters
                }]
            })
        
        st.success(f"Sub-step '{st.session_state.sub_step}' added under main step '{st.session_state.main_step}'!")

    # Display the current list of steps in a hierarchical structure
    st.write("### Current Recipe Steps")
    for step in st.session_state.steps:
        st.markdown(f"**Main Step:** <span style='color:blue; font-size: 1.2em;'>{step['main_step']}</span>", unsafe_allow_html=True)
        for sub_step in step["sub_steps"]:
            st.markdown(f"<span style='color:grey; font-size: 1em;'>&emsp;- Sub-Step: {sub_step['sub_step']}</span>", unsafe_allow_html=True)
            for param, value in sub_step["parameters"].items():
                st.markdown(f"<span style='color:grey;'>&emsp;&emsp;• {param}: {value}</span>", unsafe_allow_html=True)

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
