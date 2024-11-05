import streamlit as st 
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd

# Connexion à la base de données
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def update_recipe_page():
    st.title("🔄 Update Pharmaceutical Recipe")

    # Récupérer toutes les recettes de la collection MongoDB
    recipes = list(collection.find({}, {"product_info.product_name": 1, "_id": 1}))
    
    # Vérifier s'il y a des recettes à afficher
    if not recipes:
        st.warning("No recipes found. Please create a recipe first.")
        return
    
    # Menu déroulant pour sélectionner une recette par nom
    recipe_names = {str(recipe['_id']): recipe['product_info'].get('product_name', 'Unnamed Recipe') for recipe in recipes}
    recipe_names = {"": "Please select a recipe"} | recipe_names

    selected_recipe_id = st.selectbox(
        "Select a recipe to update", 
        options=list(recipe_names.keys()), 
        format_func=lambda x: recipe_names[x],
        key="update_recipe_selector"
    )

    # Afficher les détails de la recette sélectionnée
    if selected_recipe_id and selected_recipe_id != "":
        try:
            selected_recipe = collection.find_one({"_id": ObjectId(selected_recipe_id)})

            if selected_recipe:
                st.subheader(f"📝 Update Recipe: {selected_recipe['product_info'].get('product_name', 'Unnamed Recipe')}")

                # Mise à jour des informations de base de la recette
                st.write("### 🛠 Product Information")
                product_name = st.text_input("Product Name", value=selected_recipe['product_info'].get('product_name', ''))
                product_code = st.text_input("Product Code", value=selected_recipe['product_info'].get('product_code', ''))
                batch_size = st.text_input("Batch Size", value=selected_recipe['product_info'].get('batch_size', ''))

                # Mise à jour du BOM (Bill of Materials)
                st.write("### 🛠 Bill of Materials (BOM)")
                bom_data = []
                for section, items in selected_recipe.get("bom_sections", {}).items():
                    for item in items:
                        item_number = item.get("item_number", "N/A")
                        item_code = st.text_input(f"Item Code (Section: {section}, Item #{item_number})", value=item.get("item_code", ''))
                        item_name = st.text_input(f"Item Name (Section: {section}, Item #{item_number})", value=item.get("item_name", ''))
                        item_quantity = st.text_input(f"Item Quantity (Section: {section}, Item #{item_number})", value=item.get("item_quantity", ''))
                        
                        bom_data.append({
                            "section": section,
                            "item_number": item_number,
                            "item_code": item_code,
                            "item_name": item_name,
                            "item_quantity": item_quantity
                        })

                # Mise à jour des étapes de la recette
                st.write("### 🛠 Recipe Steps")
                steps_data = []
                for step_index, step in enumerate(selected_recipe.get("steps", []), start=1):
                    section = step.get("section", "Unnamed Section")
                    step_name = step.get("step", "Unnamed Step")
                    st.write(f"#### Step {step_index}: {section} - {step_name}")

                    # Mise à jour des items utilisés dans chaque étape
                    selected_items = step.get("selected_items", [])
                    updated_selected_items = st.text_area(f"Items Used in Step {step_index}", value="\n".join(selected_items))

                    # Mise à jour des paramètres spécifiques
                    parameters = {k: v for k, v in step.items() if k not in ["section", "step", "selected_items", "timestamp"]}
                    updated_parameters = {}
                    for param, value in parameters.items():
                        updated_value = st.text_input(f"{param.replace('_', ' ').capitalize()} (Step {step_index})", value=value)
                        updated_parameters[param] = updated_value

                    steps_data.append({
                        "section": section,
                        "step": step_name,
                        "selected_items": updated_selected_items.splitlines(),
                        **updated_parameters
                    })

                # Bouton pour enregistrer les modifications
                if st.button("Save Updates"):
                    # Mettre à jour les informations de base
                    collection.update_one(
                        {"_id": ObjectId(selected_recipe_id)},
                        {"$set": {
                            "product_info.product_name": product_name,
                            "product_info.product_code": product_code,
                            "product_info.batch_size": batch_size,
                            "bom_sections": {
                                section: [
                                    {
                                        "item_number": item["item_number"],
                                        "item_code": item["item_code"],
                                        "item_name": item["item_name"],
                                        "item_quantity": item["item_quantity"]
                                    } for item in bom_data if item["section"] == section
                                ] for section in {item["section"] for item in bom_data}
                            },
                            "steps": steps_data
                        }}
                    )
                    st.success("Recipe updated successfully!")
            else:
                st.error("Recipe not found. Please check the selection.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please select a recipe to update.")    

# Lancer la page de mise à jour des recettes
update_recipe_page()
