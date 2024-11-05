import streamlit as st 
from pymongo import MongoClient
from bson import ObjectId  # Pour convertir l'ID en ObjectId pour MongoDB
from PIL import Image
import os
import pandas as pd

# Connexion à la base de données
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def view_recipes_page():
    # Charger et afficher le logo avec un chemin absolu
    logo_path = os.path.join(os.getcwd(), "options", "images", "image.png")
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, use_column_width=True)
    except FileNotFoundError:
        st.sidebar.error("Logo image not found. Please check the file path.")
    
    st.title("💊 Pharmaceutical Recipe Viewer")

    # Récupérer toutes les recettes de la collection MongoDB
    recipes = list(collection.find({}, {"product_info.product_name": 1, "_id": 1}))
    
    # Vérifier s'il y a des recettes à afficher
    if not recipes:
        st.warning("No recipes found. Please create a recipe first.")
        return
    
    # Menu déroulant pour sélectionner une recette par nom avec un key unique
    recipe_names = {str(recipe['_id']): recipe['product_info'].get('product_name', 'Unnamed Recipe') for recipe in recipes}
    recipe_names = {"": "Please select a recipe"} | recipe_names

    selected_recipe_id = st.selectbox(
        "Select a recipe to view its details", 
        options=list(recipe_names.keys()), 
        format_func=lambda x: recipe_names[x],
        key="view_recipe_selector"
    )
    
    # Afficher les détails de la recette sélectionnée
    if selected_recipe_id and selected_recipe_id != "":
        try:
            selected_recipe = collection.find_one({"_id": ObjectId(selected_recipe_id)})

            if selected_recipe:
                st.subheader(f"📝 Recipe: {selected_recipe['product_info'].get('product_name', 'Unnamed Recipe')}")
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px;">
                            <strong>🆔 Product Code:</strong> {selected_recipe['product_info'].get('product_code', 'N/A')}<br>
                            <strong>📦 Batch Size:</strong> {selected_recipe['product_info'].get('batch_size', 'N/A')}<br>
                            <strong>🕒 Created At:</strong> {selected_recipe.get('created_at', 'N/A')}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

                # Affichage du BOM sous forme de tableau
                st.write("### 📋 Bill of Materials (BOM)")
                bom_data = []
                for section, items in selected_recipe.get("bom_sections", {}).items():
                    for item in items:
                        bom_data.append({
                            "Item Number": item.get("item_number", "N/A"),
                            "Section": section,
                            "Item Code": item.get("item_code", "N/A"),
                            "Item Name": item.get("item_name", "N/A"),
                            "Quantity": item.get("item_quantity", "N/A")
                        })
                
                # Afficher le BOM sous forme de tableau avec "Item Number" en premier
                if bom_data:
                    df_bom = pd.DataFrame(bom_data, columns=["Item Number", "Section", "Item Code", "Item Name", "Quantity"])
                    st.dataframe(df_bom)
                else:
                    st.write("No BOM items available for this recipe.")

                # Affichage des étapes de la recette
                st.write("### 📚 Recipe Steps")
                for main_step_index, main_step in enumerate(selected_recipe.get("steps", []), start=1):
                    section = main_step.get("section", "Unnamed Section")
                    step_name = main_step.get("step", "Unnamed Step")
                    st.markdown(f"#### 🔹 Step {main_step_index}: {section} - {step_name}")
                    
                    selected_items = main_step.get("selected_items", [])
                    if selected_items:
                        st.write("**Items Used:**")
                        st.markdown("<ul>", unsafe_allow_html=True)
                        for item in selected_items:
                            # Extraire les détails des items : code et nom
                            item_details = item.split(" - ")
                            if len(item_details) == 2:
                                code, name = item_details
                                # Récupérer le numéro et la quantité de l'item dans le BOM
                                item_number = quantity = None
                                for section_items in selected_recipe['bom_sections'].values():
                                    for section_item in section_items:
                                        if section_item["item_code"] == code:
                                            item_number = section_item.get("item_number", "N/A")
                                            quantity = section_item.get("item_quantity", "N/A")
                                            break
                                    if quantity:
                                        break
                                st.markdown(f"<li><strong>Item Number:</strong> {item_number} | <strong>Code:</strong> {code} | <strong>Name:</strong> {name} | <strong>Quantity:</strong> {quantity}</li>", unsafe_allow_html=True)
                        st.markdown("</ul>", unsafe_allow_html=True)

                    parameters = {k: v for k, v in main_step.items() if k not in ["section", "step", "selected_items", "timestamp"]}
                    if parameters:
                        st.write("**Parameters:**")
                        st.markdown("<ul>", unsafe_allow_html=True)
                        for param, value in parameters.items():
                            st.markdown(f"<li>{param.replace('_', ' ').capitalize()}: {value}</li>", unsafe_allow_html=True)
                        st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.error("Recipe not found. Please check the selection.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please select a recipe to view its details.")    

# Lancer la page d'affichage des recettes
view_recipes_page()
