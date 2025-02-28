import streamlit as st
from PIL import Image
import os

# Initialisation de l'état de la session pour stocker la page courante
if "page" not in st.session_state:
    st.session_state["page"] = "welcome"  # Définir la page par défaut comme "welcome"

# Navigation dans la barre latérale
st.sidebar.title("Navigation")
if st.sidebar.button("Create Recipe"):
    st.session_state["page"] = "create"  # Changer pour la page de création de recette
if st.sidebar.button("View Recipes"):
    st.session_state["page"] = "view"  # Changer pour la page d'affichage des recettes
if st.sidebar.button("Update Recipe"):
    st.session_state["page"] = "update"  # Changer pour la page de mise à jour de recette
if st.sidebar.button("Delete Recipe"):  # Nouveau bouton pour la page de suppression
    st.session_state["page"] = "delete"  # Changer pour la page de suppression de recette

# Définition de la page d'accueil
def welcome_page():
    st.title("Welcome to the Recipe Management App")
    st.write("This application helps you create, view, update, and delete pharmaceutical recipes.")
    st.write("Use the sidebar to navigate between pages.")
    
    
# Charger et afficher le logo avec un chemin absolu
    logo_path = os.path.join(os.getcwd(),"Mustapha", "options", "images", "image.png")
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, use_column_width=True)
    except FileNotFoundError:
        st.sidebar.error("Logo image not found. Please check the file path.")

# Afficher la page appropriée en fonction de l'état de la session
if st.session_state["page"] == "welcome":
    welcome_page()
elif st.session_state["page"] == "create":
    from options import create_recipe
    create_recipe.create_recipe_page()
elif st.session_state["page"] == "view":
    from options import view_recipes
    view_recipes.view_recipes_page()
elif st.session_state["page"] == "update":
    from options import update_recipe
    update_recipe.update_recipe_page()
elif st.session_state["page"] == "delete":  # Nouvelle page pour supprimer une recette
    from options import delete_recipe  # Assurez-vous que le fichier delete_recipe.py existe
    delete_recipe.delete_recipe_page()  # Appeler la fonction pour afficher la page de suppression
