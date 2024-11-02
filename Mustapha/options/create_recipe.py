import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Connexion à la base de données
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]
def create_recipe_page():
    # Initialisation de l'état de la session
    if "recipe_started" not in st.session_state:
        st.session_state.recipe_started = False
    if "product_info" not in st.session_state:
        st.session_state.product_info = {}
    if "bom_sections" not in st.session_state:
        st.session_state.bom_sections = {}
    if "steps" not in st.session_state:
        st.session_state.steps = []

    # Page principale "Create Recipe"
    st.title("Create Pharmaceutical Recipe")

    # Étape 1 : Entrée des informations de base
    if not st.session_state.recipe_started:
        if st.button("Start Recipe Creation"):
            st.session_state.recipe_started = True
            st.success("Recipe creation started! Enter product details.")

    if st.session_state.recipe_started:
        with st.expander("Step 1: Enter Product Details", expanded=True):
            product_name = st.text_input("Product Name")
            product_code = st.text_input("Product Code")
            batch_size = st.text_input("Product Batch Size")

            if st.button("Next to Add BOM"):
                if product_name and product_code and batch_size:
                    st.session_state.product_info = {
                        "product_name": product_name,
                        "product_code": product_code,
                        "batch_size": batch_size
                    }
                    st.success("Product details saved! Proceed to add BOM.")
                else:
                    st.error("Please fill out all fields.")

    # Étape 2 : Add BOM
    if st.session_state.product_info:
        with st.expander("Step 2: Add BOM", expanded=True):
            sections = ["DRY MIX", "DRY COMPACTION", "HSFB GRANULATION", "COMPRESSION", "ENCAPSULATION", "COATING"]
            selected_section = st.selectbox("Select a Section", options=sections)

            if selected_section:
                item_code = st.text_input("Item Code")
                item_name = st.text_input("Item Name")
                item_quantity = st.text_input("Item Quantity")

                if st.button("Add Item to Section"):
                    if item_code and item_name and item_quantity:
                        if selected_section not in st.session_state.bom_sections:
                            st.session_state.bom_sections[selected_section] = []
                        st.session_state.bom_sections[selected_section].append({
                            "item_code": item_code,
                            "item_name": item_name,
                            "item_quantity": item_quantity
                        })
                        st.success(f"Item '{item_name}' added to section '{selected_section}'")
                    else:
                        st.error("Please fill out all item fields.")

            # Afficher les items ajoutés dans la section sélectionnée
            if selected_section in st.session_state.bom_sections:
                st.subheader(f"Items in {selected_section}")
                for idx, item in enumerate(st.session_state.bom_sections[selected_section], start=1):
                    st.write(f"Item {idx}: {item['item_code']} - {item['item_name']} ({item['item_quantity']})")

    # Étape 3 : Add Section Details
    if st.session_state.bom_sections:
        with st.expander("Step 3: Add Section Details", expanded=True):
            section_for_steps = st.selectbox("Select a Section to Add Steps", options=list(st.session_state.bom_sections.keys()))
            steps = ["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"]

            if section_for_steps:
                selected_step = st.selectbox("Select a Step", options=steps)
                if selected_step:
                    st.subheader(f"Items in {section_for_steps}")
                    items_in_section = st.session_state.bom_sections[section_for_steps]
                    selected_items = st.multiselect("Select Items for this Step", options=[f"{item['item_code']} - {item['item_name']}" for item in items_in_section])

                    # Afficher des champs d'entrée spécifiques à chaque étape
                    if selected_step == "Mixing / Lubrication steps":
                        blender_size = st.text_input("Blender Size")
                        mixing_time = st.text_input("Mixing Time")
                        mixing_speed = st.text_input("Mixing Speed")
                    elif selected_step == "Milling steps":
                        comil_model = st.text_input("Comil Model (197/194)")
                        impeller_type = st.text_input("Impeller Type")
                        sieve_size = st.text_input("Sieve Size/Type")
                        impeller_speed = st.text_input("Impeller Speed")
                    elif selected_step == "Manual sieving steps":
                        screen_size = st.text_input("Screen Size")
                    elif selected_step == "Dispersion":
                        approx_qty = st.text_input("Approximate Quantity")

                    if st.button("Add Step"):
                        if selected_items:
                            step_details = {
                                "section": section_for_steps,
                                "step": selected_step,
                                "selected_items": selected_items,
                                "timestamp": datetime.now()
                            }
                            # Ajouter des détails supplémentaires en fonction de l'étape choisie
                            if selected_step == "Mixing / Lubrication steps":
                                if blender_size and mixing_time and mixing_speed:
                                    step_details.update({
                                        "blender_size": blender_size,
                                        "mixing_time": mixing_time,
                                        "mixing_speed": mixing_speed
                                    })
                                else:
                                    st.error("Please fill out all fields for Mixing / Lubrication steps.")
                                    st.stop()
                            elif selected_step == "Milling steps":
                                if comil_model and impeller_type and sieve_size and impeller_speed:
                                    step_details.update({
                                        "comil_model": comil_model,
                                        "impeller_type": impeller_type,
                                        "sieve_size": sieve_size,
                                        "impeller_speed": impeller_speed
                                    })
                                else:
                                    st.error("Please fill out all fields for Milling steps.")
                                    st.stop()
                            elif selected_step == "Manual sieving steps":
                                if screen_size:
                                    step_details["screen_size"] = screen_size
                                else:
                                    st.error("Please fill out the screen size for Manual sieving steps.")
                                    st.stop()
                            elif selected_step == "Dispersion":
                                if approx_qty:
                                    step_details["approx_qty"] = approx_qty
                                else:
                                    st.error("Please fill out the approximate quantity for Dispersion.")
                                    st.stop()

                            # Ajouter l'étape aux étapes enregistrées
                            st.session_state.steps.append(step_details)
                            st.success(f"Step '{selected_step}' added for section '{section_for_steps}'")
                        else:
                            st.error("Please select at least one item.")

            # Récapitulatif des étapes ajoutées
            st.subheader("Steps Overview")
            for idx, step_detail in enumerate(st.session_state.steps, start=1):
                st.markdown(f"**Step {idx}:** {step_detail['step']} in {step_detail['section']}")
                st.write(f"Items: {', '.join(step_detail['selected_items'])}")
                for key, value in step_detail.items():
                    if key not in ["section", "step", "selected_items", "timestamp"]:
                        st.write(f"{key.replace('_', ' ').capitalize()}: {value}")

    # Bouton de soumission pour sauvegarder la recette
    if st.session_state.steps:
        if st.button("Submit Recipe"):
            recipe_data = {
                "product_info": st.session_state.product_info,
                "bom_sections": st.session_state.bom_sections,
                "steps": st.session_state.steps,
                "created_at": datetime.now()
            }
            # Sauvegarde des données dans la base de données MongoDB
            collection.insert_one(recipe_data)
            st.success("Recipe successfully submitted!")
            st.session_state.clear()  # Réinitialiser l'état de la session pour un nouvel essai
