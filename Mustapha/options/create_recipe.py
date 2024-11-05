import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Connexion à la base de données
client = MongoClient("mongodb+srv://wafid:wafid@ouafid.aihn5iq.mongodb.net")
db = client["mustapha"]
collection = db["create"]

def filter_items_for_section(section):
    """Filtre les items à afficher en fonction de la section sélectionnée dans l'étape 3."""
    if section in ["DRY MIX", "DRY COMPACTION"]:
        relevant_sections = ["Pre-Mix", "Final-Mix"]
    elif section == "HSFB GRANULATION":
        relevant_sections = ["Pre-Mix", "Final-Mix", "Granulation Solution/Suspension"]
    elif section == "ENCAPSULATION":
        relevant_sections = ["Encapsulation"]
    elif section == "COATING":
        relevant_sections = ["Coating Solution/Suspension"]
    else:
        return []

    # Rassembler les items des sections pertinentes
    items = []
    for relevant_section in relevant_sections:
        items.extend(st.session_state.bom_sections.get(relevant_section, []))
    return items

def create_recipe_page():
    # Initialisation de l'état de la session pour éviter les erreurs d'attribut manquant
    if "recipe_started" not in st.session_state:
        st.session_state.recipe_started = False
    if "product_info" not in st.session_state:
        st.session_state.product_info = {}
    if "bom_sections" not in st.session_state:
        st.session_state.bom_sections = {}
    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "bom_finalized" not in st.session_state:
        st.session_state.bom_finalized = False
    if "dynamic_key_counter" not in st.session_state:
        st.session_state.dynamic_key_counter = 0  # Compteur pour générer des clés dynamiques
    if "global_item_counter" not in st.session_state:
        st.session_state.global_item_counter = 1  # Compteur global pour les items

    # Page principale "Create Recipe"
    st.title("Create Pharmaceutical Recipe")

    # Étape 1 : Entrée des informations de base
    if not st.session_state.recipe_started:
        if st.button("Start Recipe Creation"):
            st.session_state.recipe_started = True

    if st.session_state.recipe_started and not st.session_state.bom_finalized:
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
                else:
                    st.error("Please fill out all fields.")

    # Étape 2 : Add BOM (si les informations de base sont remplies)
    if st.session_state.product_info and not st.session_state.bom_finalized:
        with st.expander("Step 2: Add BOM", expanded=True):
            sections = ["Pre-Mix", "Final-Mix", "Granulation Solution/Suspension", "Coating Solution/Suspension", "Encapsulation"]
            selected_section = st.selectbox("Select a Section", options=sections)

            if selected_section:
                # Clé dynamique pour les widgets
                dynamic_key = st.session_state.dynamic_key_counter
                # Champs d'entrée pour un item
                item_code = st.text_input("Item Code", key=f"item_code_{selected_section}_{dynamic_key}")
                item_name = st.text_input("Item Name", key=f"item_name_{selected_section}_{dynamic_key}")
                item_quantity = st.text_input("Item Quantity", key=f"item_quantity_{selected_section}_{dynamic_key}")

                # Alignement des boutons dans une même ligne
                col1, col2 = st.columns(2)
                with col2:
                    if st.button("New Item"):
                        st.session_state.dynamic_key_counter += 1  # Incrémentation du compteur dynamique
                        st.info("Ready to add a new item")
                with col1:
                    if st.button("Submit Item"):
                        if item_code and item_name and item_quantity:
                            if selected_section not in st.session_state.bom_sections:
                                st.session_state.bom_sections[selected_section] = []
                            # Ajouter l'item avec un numéro séquentiel global
                            st.session_state.bom_sections[selected_section].append({
                                "item_number": st.session_state.global_item_counter,
                                "item_code": item_code,
                                "item_name": item_name,
                                "item_quantity": item_quantity
                            })
                            # Incrémenter le compteur global et le compteur dynamique
                            st.session_state.global_item_counter += 1
                            st.session_state.dynamic_key_counter += 1
                        else:
                            st.error("Please fill out all item fields.")

            # Afficher les items ajoutés dans la section sélectionnée
            if selected_section in st.session_state.bom_sections:
                st.subheader(f"Items in {selected_section}")
                for idx, item in enumerate(st.session_state.bom_sections[selected_section], start=1):
                    st.write(f"Item {item['item_number']}: {item['item_code']} - {item['item_name']} ({item['item_quantity']})")

        # Bouton pour finaliser le BOM
        if st.button("Finalize BOM"):
            st.session_state.bom_finalized = True
            st.success("BOM finalized! Proceed to the next step.")

    # Initialisation de la clé dynamique pour la troisième étape
    if "step_form_key" not in st.session_state:
        st.session_state.step_form_key = 0

    # Étape 3 : Ajout des détails des sections, si le BOM est finalisé
    if st.session_state.bom_finalized:
        with st.expander("Step 3: Create Recipe", expanded=True):
            sections = ["DRY MIX", "DRY COMPACTION", "HSFB GRANULATION", "COMPRESSION", "ENCAPSULATION", "COATING"]
            section_for_steps = st.selectbox("Select a Section to Add Steps", options=sections)
            steps = ["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"]

            if section_for_steps:
                # Filtrer les items en fonction de la section sélectionnée
                items_in_section = filter_items_for_section(section_for_steps)

                st.subheader(f"Items in {section_for_steps}")
                if items_in_section:
                    selected_items = st.multiselect(
                        "Select Items for this Step", 
                        options=[f"{item['item_code']} - {item['item_name']}" for item in items_in_section],
                        key=f"selected_items_{section_for_steps}_{st.session_state.step_form_key}"
                    )

                    # Afficher des champs d'entrée spécifiques à chaque étape
                    step_fields = {}
                    selected_step = st.selectbox(
                        "Select a Step", 
                        options=steps,
                        key=f"selected_step_{section_for_steps}_{st.session_state.step_form_key}"
                    )

                    if selected_step == "Mixing / Lubrication steps":
                        step_fields = {
                            "Blender Size": st.text_input("Blender Size", key=f"blender_size_{st.session_state.step_form_key}"),
                            "Mixing Time": st.text_input("Mixing Time", key=f"mixing_time_{st.session_state.step_form_key}"),
                            "Mixing Speed": st.text_input("Mixing Speed", key=f"mixing_speed_{st.session_state.step_form_key}")
                        }
                    elif selected_step == "Milling steps":
                        step_fields = {
                            "Comil Model (197/194)": st.text_input("Comil Model", key=f"comil_model_{st.session_state.step_form_key}"),
                            "Impeller Type": st.text_input("Impeller Type", key=f"impeller_type_{st.session_state.step_form_key}"),
                            "Sieve Size/Type": st.text_input("Sieve Size/Type", key=f"sieve_size_{st.session_state.step_form_key}"),
                            "Impeller Speed": st.text_input("Impeller Speed", key=f"impeller_speed_{st.session_state.step_form_key}")
                        }
                    elif selected_step == "Manual sieving steps":
                        step_fields = {"Screen Size": st.text_input("Screen Size", key=f"screen_size_{st.session_state.step_form_key}")}
                    elif selected_step == "Dispersion":
                        step_fields = {"Approximate Quantity": st.text_input("Approximate Quantity", key=f"approx_qty_{st.session_state.step_form_key}")}

                    # Alignement des boutons dans une même ligne
                    col1, col2 = st.columns(2)
                    with col2:
                        if st.button("New Step"):
                            st.session_state.step_form_key += 1  # Incrémentation de la clé dynamique pour générer de nouveaux widgets vides
                    with col1:
                        if st.button("Submit Step"):
                            if selected_items:
                                step_details = {
                                    "section": section_for_steps,
                                    "step": selected_step,
                                    "selected_items": selected_items,
                                    "timestamp": datetime.now()
                                }
                                # Ajouter des champs d'étapes spécifiques
                                step_details.update(step_fields)
                                st.session_state.steps.append(step_details)
                                st.success(f"Step '{selected_step}' added for section '{section_for_steps}'")
                            else:
                                st.error("Please select at least one item.")
                else:
                    st.info(f"No items available for {section_for_steps}.")

            # Récapitulatif des étapes ajoutées
            st.subheader("Steps Overview")
            for idx, step_detail in enumerate(st.session_state.steps, start=1):
                st.markdown(f"**Step {idx}:** {step_detail['step']} in {step_detail['section']}")
                st.write(f"Items: {', '.join(step_detail['selected_items'])}")
                for key, value in step_detail.items():
                    if key not in ["section", "step", "selected_items", "timestamp"]:
                        st.write(f"{key}: {value}")

    # Bouton de soumission pour sauvegarder la recette
    if st.session_state.steps and st.button("Submit Recipe"):
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

# Lancer la page de création de recette
create_recipe_page()
