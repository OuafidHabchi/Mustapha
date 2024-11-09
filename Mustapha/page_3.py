import streamlit as st
import uuid
from datetime import datetime

def initialize_step_fields(step_type, key, step_fields_data=None):
    """Generate specific fields based on step type and populate with saved data if available."""
    fields = {}
    if step_type == "Mixing / Lubrication steps":
        fields = {
            "Blender Size": st.text_input("Blender Size", value=st.session_state.get(f"blender_size_{key}", step_fields_data.get("Blender Size", "") if step_fields_data else "")),
            "Mixing Time": st.text_input("Mixing Time", value=st.session_state.get(f"mixing_time_{key}", step_fields_data.get("Mixing Time", "") if step_fields_data else "")),
            "Mixing Speed": st.text_input("Mixing Speed", value=st.session_state.get(f"mixing_speed_{key}", step_fields_data.get("Mixing Speed", "") if step_fields_data else ""))
        }
    elif step_type == "Milling steps":
        fields = {
            "Comil Model": st.text_input("Comil Model", value=st.session_state.get(f"comil_model_{key}", step_fields_data.get("Comil Model", "") if step_fields_data else "")),
            "Impeller Type": st.text_input("Impeller Type", value=st.session_state.get(f"impeller_type_{key}", step_fields_data.get("Impeller Type", "") if step_fields_data else "")),
            "Sieve Size/Type": st.text_input("Sieve Size/Type", value=st.session_state.get(f"sieve_size_{key}", step_fields_data.get("Sieve Size/Type", "") if step_fields_data else "")),
            "Impeller Speed": st.text_input("Impeller Speed", value=st.session_state.get(f"impeller_speed_{key}", step_fields_data.get("Impeller Speed", "") if step_fields_data else ""))
        }
    elif step_type == "Manual sieving steps":
        fields = {"Screen Size": st.text_input("Screen Size", value=st.session_state.get(f"screen_size_{key}", step_fields_data.get("Screen Size", "") if step_fields_data else ""))}
    elif step_type == "Dispersion":
        fields = {"Approximate Quantity": st.text_input("Approximate Quantity", value=st.session_state.get(f"approx_qty_{key}", step_fields_data.get("Approximate Quantity", "") if step_fields_data else ""))}
    
    # Save field values to session state to retain them on rerender
    for field_name, field_input in fields.items():
        st.session_state[f"{field_name.replace(' ', '_').lower()}_{key}"] = field_input
    
    return fields

def page_3():
    # Initialiser les variables de session si elles ne sont pas déjà présentes
    if "show_step_form" not in st.session_state:
        st.session_state.show_step_form = False
    if "edit_step_uuid" not in st.session_state:
        st.session_state.edit_step_uuid = None
    if "step_form_key" not in st.session_state:
        st.session_state.step_form_key = str(uuid.uuid4())

    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Étape 3 : Créer la recette")

    # Vérifie si la liste des items a été définie
    if "bom_items" not in st.session_state or not st.session_state.bom_items:
        st.warning("Veuillez définir le nombre d'items dans l'étape 2.")
        return

    # Afficher une vue d'ensemble simplifiée de toutes les étapes précédentes avec leurs résultats
    st.subheader("Aperçu des étapes")
    for idx, step in enumerate(st.session_state.steps, start=1):
        col1, col2 = st.columns([8, 1])

        with col1:
            st.markdown(f"**Étape {idx}:** {step['step_type']} dans {step['section']}")
        with col2:
            if st.button(f"Éditer Étape {idx}", key=f"edit_button_{idx}"):
                st.session_state.edit_step_uuid = step['uuid']
                st.session_state.show_step_form = True
                st.session_state.step_form_key = step['uuid']

    # Définition des sections spécifiques
    sections = ["DRY MIX", "DRY COMPACTION", "HSFB GRANULATION", "COMPRESSION", "ENCAPSULATION", "COATING"]

    # Bouton pour ajouter une nouvelle étape avec numéro d'étape
    if st.button("Ajouter une étape"):
        st.session_state.edit_step_uuid = None
        st.session_state.show_step_form = True
        st.session_state.step_form_key = str(uuid.uuid4())

    # Formulaire pour ajouter/éditer une étape
    if st.session_state.show_step_form:
        # Calcul du numéro de la nouvelle étape
        step_number = len(st.session_state.steps) + 1 if st.session_state.edit_step_uuid is None else [i+1 for i, s in enumerate(st.session_state.steps) if s['uuid'] == st.session_state.edit_step_uuid][0]

        if st.session_state.edit_step_uuid:
            # Mode édition : charger l'étape par UUID
            step = next((s for s in st.session_state.steps if s['uuid'] == st.session_state.edit_step_uuid), None)
            section_for_steps = st.selectbox("Select a Section", sections, index=sections.index(step["section"]))

            # Liste des items initiaux + résultats des étapes précédentes
            options = st.session_state.bom_items + [f"Résultat de l'étape {i}" for i in range(1, len(st.session_state.steps) + 1)]
            valid_selected_items = [item for item in step["selected_items"] if item in options]

            selected_items = st.multiselect(
                "Sélectionnez les items pour cette étape", 
                options=options,
                default=valid_selected_items
            )
            step_type = st.selectbox(
                "Select a Step Type", 
                options=["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"],
                index=["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"].index(step["step_type"])
            )
            step_fields = initialize_step_fields(step_type, st.session_state.step_form_key, step["step_fields"])
        else:
            # Mode ajout : nouvelle étape avec numéro d'étape
            st.markdown(f"### Nouvelle étape : Étape {step_number}")
            section_for_steps = st.selectbox("Select a Section", sections)

            # Liste des items initiaux + résultats des étapes précédentes
            options = st.session_state.bom_items + [f"Résultat de l'étape {i}" for i in range(1, len(st.session_state.steps) + 1)]
            selected_items = st.multiselect("Sélectionnez les items pour cette étape", options)
            step_type = st.selectbox("Select a Step Type", ["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"])
            step_fields = initialize_step_fields(step_type, st.session_state.step_form_key)

        # Confirmation de l'étape
        if st.button("Confirmer l'étape"):
            step_details = {
                "uuid": step.get("uuid", str(uuid.uuid4())) if st.session_state.edit_step_uuid else str(uuid.uuid4()),
                "section": section_for_steps,
                "step_type": step_type,
                "selected_items": selected_items,
                "timestamp": datetime.now(),
                "step_fields": {field: st.session_state.get(f"{field.replace(' ', '_').lower()}_{st.session_state.step_form_key}", "") for field in step_fields}
            }

            # Ajouter ou mettre à jour l'étape
            if st.session_state.edit_step_uuid:
                for i, s in enumerate(st.session_state.steps):
                    if s['uuid'] == st.session_state.edit_step_uuid:
                        st.session_state.steps[i] = step_details
                        st.success("Étape mise à jour !")
                        break
                st.session_state.edit_step_uuid = None
            else:
                st.session_state.steps.append(step_details)
                st.success(f"Nouvelle étape {step_number} ajoutée !")

            st.session_state.show_step_form = False

# Appel de la fonction pour afficher la page 3
page_3()
