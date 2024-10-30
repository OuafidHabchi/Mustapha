import streamlit as st
from pymongo import MongoClient

# Database connection
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def view_recipes_page():
    st.title("View Recipes")

    # Retrieve all recipe names and IDs from the MongoDB collection
    recipes = list(collection.find({}, {"recipe_name": 1, "_id": 1}))
    
    # Check if there are any recipes to display
    if not recipes:
        st.write("No recipes found.")
        return
    
    # Create a dropdown to select a recipe by name
    recipe_names = {recipe['_id']: recipe['recipe_name'] for recipe in recipes}
    selected_recipe_id = st.selectbox("Select a recipe to view its details", options=list(recipe_names.keys()), format_func=lambda x: recipe_names[x])
    
    # Fetch the selected recipe details
    if selected_recipe_id:
        selected_recipe = collection.find_one({"_id": selected_recipe_id})

        # Display recipe details
        st.subheader(f"Recipe: {selected_recipe['recipe_name']}")
        st.write(f"**Created At:** {selected_recipe.get('created_at', 'N/A')}")

        # Display each main step in the recipe with its sub-steps and parameters
        st.write("### Recipe Steps")
        for main_step_index, main_step in enumerate(selected_recipe.get("steps", []), start=1):
            st.markdown(f"#### Main Step {main_step_index}: {main_step['main_step']}")
            
            # Display each sub-step within the main step, with numbering
            for sub_step_index, sub_step in enumerate(main_step.get("sub_steps", []), start=1):
                st.markdown(f"- **Sub-Step {main_step_index}.{sub_step_index}:** {sub_step['sub_step']}")
                
                # Display parameters for each sub-step
                if sub_step["parameters"]:
                    st.markdown("<p style='font-size: 0.9em; color: grey;'>Parameters:</p>", unsafe_allow_html=True)
                    for param, value in sub_step["parameters"].items():
                        st.markdown(f"<p style='font-size: 0.9em; color: grey;'>• {param}: {value}</p>", unsafe_allow_html=True)

    # Optional: Back to Welcome Page button
    if st.button("Back to Welcome Page"):
        st.session_state["page"] = "welcome"
