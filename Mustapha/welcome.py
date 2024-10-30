import streamlit as st

# Initialize session state to store the current page
if "page" not in st.session_state:
    st.session_state["page"] = "welcome"  # Set default page to 'welcome'

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Create Recipe"):
    st.session_state["page"] = "create"  # Switch to create recipe page
if st.sidebar.button("View Recipes"):
    st.session_state["page"] = "view"  # Switch to view recipes page

# Define the Welcome Page
def welcome_page():
    st.title("Welcome to the Recipe Management App")
    st.write("This application helps you create, view, update, and delete recipes.")
    st.write("Use the sidebar to navigate between pages.")

# Display the appropriate page based on session state
if st.session_state["page"] == "welcome":
    welcome_page()  # Show Welcome Page by default
elif st.session_state["page"] == "create":
    # Import and load the Create Recipe page from the options folder
    from options import create_recipe
    create_recipe.create_recipe_page()
elif st.session_state["page"] == "view":
    # Import and load the View Recipes page from the options folder
    from options import view_recipes
    view_recipes.view_recipes_page()
