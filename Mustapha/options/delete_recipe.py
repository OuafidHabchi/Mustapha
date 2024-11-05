import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

# Connexion à la base de données
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def delete_recipe_page():
    st.title("🗑️ Delete Pharmaceutical Recipe")

    # Récupérer toutes les recettes de la collection MongoDB
    recipes = list(collection.find({}, {"product_info.product_name": 1, "_id": 1}))
    
    # Vérifier s'il y a des recettes à supprimer
    if not recipes:
        st.warning("No recipes found. Please create a recipe first.")
        return

    # Menu déroulant pour sélectionner une recette par nom
    recipe_names = {str(recipe['_id']): recipe['product_info'].get('product_name', 'Unnamed Recipe') for recipe in recipes}
    recipe_names = {"": "Please select a recipe"} | recipe_names

    selected_recipe_id = st.selectbox(
        "Select a recipe to delete", 
        options=list(recipe_names.keys()), 
        format_func=lambda x: recipe_names[x],
        key="delete_recipe_selector"
    )

    # Afficher un bouton de confirmation de suppression
    if selected_recipe_id and selected_recipe_id != "":
        st.warning("This action cannot be undone. Please confirm before deleting.")
        if st.button("Confirm Delete"):
            try:
                # Supprimer la recette sélectionnée
                collection.delete_one({"_id": ObjectId(selected_recipe_id)})
                st.success("Recipe deleted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.info("Please select a recipe to delete.")  
