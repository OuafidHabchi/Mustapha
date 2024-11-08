import streamlit as st
from datetime import datetime
import uuid  # Import uuid for generating unique step IDs


# Mapping of Step 3 sections to BOM sections
section_mapping = {
    "DRY MIX": ["Pre-Mix", "Final-Mix"],
    "DRY COMPACTION": ["Pre-Mix", "Final-Mix"],
    "HSFB GRANULATION": ["Pre-Mix", "Final-Mix", "Granulation Solution/Suspension"],
    "COMPRESSION": ["Pre-Mix", "Final-Mix"],
    "ENCAPSULATION": ["Encapsulation"],
    "COATING": ["Coating Solution/Suspension"]
}

def filter_items_for_section(step3_section):
    """Filter items based on the selected Step 3 section using section mapping."""
    relevant_bom_sections = section_mapping.get(step3_section, [])
    filtered_items = []
    for section in relevant_bom_sections:
        filtered_items.extend(st.session_state.bom_sections.get(section, []))
    return filtered_items

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
     # CSS pour ajuster la taille des boutons
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;  /* Ajuste le padding pour la taille souhaitée */
            font-size: 14px;    /* Ajuste la taille de la police */
            border-radius: 6px; /* Ajoute un peu de bord arrondi pour le style */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Étape 3 : Créer la recette")

    # Initialize session state for steps and form control
    if 'steps' not in st.session_state:
        st.session_state.steps = []
    if 'edit_step_uuid' not in st.session_state:
        st.session_state.edit_step_uuid = None
    if 'show_step_form' not in st.session_state:
        st.session_state.show_step_form = False

    # Display a simplified overview of all steps with edit buttons directly under the title
    st.subheader("Steps Overview")
    for idx, step in enumerate(st.session_state.steps, start=1):
        # Create columns for the step text and the edit button
        col1, col2 = st.columns([8, 1])  # Adjust column width to control layout

        # Display step details in the first column
        with col1:
            st.markdown(f"**Step {idx}:** {step['step_type']} in {step['section']}")

        # Display the "Edit Step" button in the second column, on the same line
        with col2:
            if st.button(f"Edit", key=f"edit_button_{idx}"):
                st.session_state.edit_step_uuid = step['uuid']
                st.session_state.show_step_form = True
                st.session_state.step_form_key = step['uuid']

    sections = ["DRY MIX", "DRY COMPACTION", "HSFB GRANULATION", "COMPRESSION", "ENCAPSULATION", "COATING"]

    # Button to initiate adding a new step
    if st.button(" ➕ Ajouter une nouvelle étape"):
        st.session_state.edit_step_uuid = None
        st.session_state.show_step_form = True
        st.session_state.step_form_key = str(uuid.uuid4())  # Unique key for the form to store values

    # Display form if adding a new step or editing an existing one
    if st.session_state.show_step_form:
        if st.session_state.edit_step_uuid:
            # Edit mode: Load the step by UUID
            step = next((s for s in st.session_state.steps if s['uuid'] == st.session_state.edit_step_uuid), None)
            st.markdown(f"### Edit Step for Section {step['section']}")
            section_for_steps = st.selectbox("Select a Section", sections, index=sections.index(step["section"]))
            items_in_section = filter_items_for_section(section_for_steps)

            # Generate options and filter selected items that still exist in the options
            options = [f"{item['item_code']} - {item['item_name']}" for item in items_in_section]
            valid_selected_items = [item for item in step["selected_items"] if item in options]

            selected_items = st.multiselect(
                "Select Items for this Step", 
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
            # Add mode: new step
            st.markdown("### Nouvelle étape")
            section_for_steps = st.selectbox("Select a Section", sections)
            items_in_section = filter_items_for_section(section_for_steps)
            selected_items = st.multiselect("Select Items for this Step", [f"{item['item_code']} - {item['item_name']}" for item in items_in_section])
            step_type = st.selectbox("Select a Step Type", ["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"])
            step_fields = initialize_step_fields(step_type, st.session_state.step_form_key)

        # Confirm Step Button
        if st.button("Confirmer l'étape"):
            step_details = {
                "uuid": step.get("uuid", str(uuid.uuid4())) if st.session_state.edit_step_uuid else str(uuid.uuid4()),
                "section": section_for_steps,
                "step_type": step_type,
                "selected_items": selected_items,
                "timestamp": datetime.now(),
                "step_fields": {field: st.session_state.get(f"{field.replace(' ', '_').lower()}_{st.session_state.step_form_key}", "") for field in step_fields}
            }

            # Update or add the step
            if st.session_state.edit_step_uuid:
                for i, s in enumerate(st.session_state.steps):
                    if s['uuid'] == st.session_state.edit_step_uuid:
                        st.session_state.steps[i] = step_details
                        st.success("Step updated!")
                        break
                st.session_state.edit_step_uuid = None
            else:
                st.session_state.steps.append(step_details)
                st.success("New Step added!")

            st.session_state.show_step_form = False

# Run the function to display page 3 if on page 3
if 'current_page' not in st.session_state:
    st.session_state.current_page = 3

if st.session_state.current_page == 3:
    page_3()
