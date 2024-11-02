import streamlit as st

# Initialisation de l'état de la session pour stocker la page courante
if "page" not in st.session_state:
    st.session_state["page"] = "welcome"  # Définir la page par défaut comme "welcome"

# Navigation dans la barre latérale
st.sidebar.title("Navigation")
if st.sidebar.button("Create Recipe"):
    st.session_state["page"] = "create"  # Changer pour la page de création de recette
if st.sidebar.button("View Recipes"):
    st.session_state["page"] = "view"  # Changer pour la page d'affichage des recettes

# Définition de la page d'accueil
def welcome_page():
    st.title("Welcome to the Recipe Management App")
    st.write("This application helps you create, view, update, and delete pharmaceutical recipes.")
    st.write("Use the sidebar to navigate between pages.")

# Afficher la page appropriée en fonction de l'état de la session
if st.session_state["page"] == "welcome":
    welcome_page()
elif st.session_state["page"] == "create":
    from options import create_recipe
    create_recipe.create_recipe_page()
elif st.session_state["page"] == "view":
    from options import view_recipes
    view_recipes.view_recipes_page()
