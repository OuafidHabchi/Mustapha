import streamlit as st
import uuid
from datetime import datetime

def initialize_step_fields(step_type, key, step_fields_data=None):
    """Generate specific fields based on step type and populate with saved data if available."""
    fields = {}
    if step_type == "Mixing / Lubrication steps":
        fields = {
            "Blender Size": st.text_input(
                "Blender Size", 
                value=step_fields_data.get("Blender Size", "") if step_fields_data else "",
                key=f"blender_size_{key}"
            ),
            "Mixing Time": st.text_input(
                "Mixing Time", 
                value=step_fields_data.get("Mixing Time", "") if step_fields_data else "",
                key=f"mixing_time_{key}"
            ),
            "Mixing Speed": st.text_input(
                "Mixing Speed", 
                value=step_fields_data.get("Mixing Speed", "") if step_fields_data else "",
                key=f"mixing_speed_{key}"
            )
        }
    elif step_type == "Milling steps":
        fields = {
            "Comil Model": st.selectbox(
                "Comil Model",
                options=["197", "194", "U20"],  # Options disponibles
                index=0 if step_fields_data is None or "Comil Model" not in step_fields_data else ["197", "194", "U20"].index(step_fields_data.get("Comil Model", "197")),
                key=f"comil_model_{key}"
            ),
            "Impeller Type": st.text_input(
                "Impeller Type", 
                value=step_fields_data.get("Impeller Type", "") if step_fields_data else "",
                key=f"impeller_type_{key}"
            ),
            "Sieve Size/Type": st.text_input(
                "Sieve Size/Type", 
                value=step_fields_data.get("Sieve Size/Type", "") if step_fields_data else "",
                key=f"sieve_size_{key}"
            ),
            "Impeller Speed": st.text_input(
                "Impeller Speed", 
                value=step_fields_data.get("Impeller Speed", "") if step_fields_data else "",
                key=f"impeller_speed_{key}"
            )
        }
    elif step_type == "Solution/Suspension Preparation":
        fields = {
            "Container Size (L)": st.text_input(
                "Container Size (L)", 
                value=step_fields_data.get("Container Size (L)", "") if step_fields_data else "",
                key=f"container_size_{key}"
            ),
            "Preparation Method": st.selectbox(
                "Preparation Method",
                ["Mélangeur", "Homogénisateur"],
                index=["Mélangeur", "Homogénisateur"].index(step_fields_data.get("Preparation Method", "Mélangeur")) if step_fields_data else 0,
                key=f"prep_method_{key}"
            )
        }
        if fields["Preparation Method"] == "Mélangeur":
            fields.update({
                "Mixing Time (minutes)": st.text_input(
                    "Mixing Time (minutes)",
                    value=step_fields_data.get("Mixing Time (minutes)", "") if step_fields_data else "",
                    key=f"mixing_time_minutes_{key}"
                ),
                "Agitation Type": st.selectbox(
                    "Agitation Type",
                    ["Base", "Moyenne", "Forte"],
                    index=["Base", "Moyenne", "Forte"].index(step_fields_data.get("Agitation Type", "Base")) if step_fields_data else 0,
                    key=f"agitation_type_{key}"
                )
            })
        elif fields["Preparation Method"] == "Homogénisateur":
            fields.update({
                "Homogenization Time": st.text_input(
                    "Homogenization Time",
                    value=step_fields_data.get("Homogenization Time", "") if step_fields_data else "",
                    key=f"homogenization_time_{key}"
                ),
                "Speed (RPM)": st.text_input(
                    "Speed (RPM)",
                    value=step_fields_data.get("Speed (RPM)", "") if step_fields_data else "",
                    key=f"speed_rpm_{key}"
                )
            })
        fields["Solution/Dispersion BHT"] = st.text_input(
            "Solution/Dispersion BHT (hours)",
            value=step_fields_data.get("Solution/Dispersion BHT (hours)", "") if step_fields_data else "",
            key=f"solution_dispersion_bht_{key}"
        )
    elif step_type == "HS Pre-Mix":
        fields = {
            "Items": st.multiselect(
                "Items",
                st.session_state.bom_items,
                default=step_fields_data.get("Items", []) if step_fields_data else []
            ),
            "Shoper Speed (RPM)": st.text_input(
                "Shoper Speed (RPM)",
                value=step_fields_data.get("Shoper Speed (RPM)", "") if step_fields_data else "",
                key=f"shoper_speed_{key}"
            ),
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_{key}"
            ),
            "Mixing Time (seconds)": st.text_input(
                "Mixing Time (seconds)",
                value=step_fields_data.get("Mixing Time (seconds)", "") if step_fields_data else "",
                key=f"mixing_time_seconds_{key}"
            )
        }
    elif step_type == "Granulation":
        fields = {
            "Solution Addition Time (minutes)": st.text_input(
                "Solution Addition Time (minutes)",
                value=step_fields_data.get("Solution Addition Time (minutes)", "") if step_fields_data else "",
                key=f"solution_addition_time_minutes_{key}"
            ),
            "Solution Addition Time (seconds)": st.text_input(
                "Solution Addition Time (seconds)",
                value=step_fields_data.get("Solution Addition Time (seconds)", "") if step_fields_data else "",
                key=f"solution_addition_time_seconds_{key}"
            ),
            "Solution Flow Rate (g/min)": st.text_input(
                "Solution Flow Rate (g/min)",
                value=step_fields_data.get("Solution Flow Rate (g/min)", "") if step_fields_data else "",
                key=f"solution_flow_rate_{key}"
            ),
            "Shoper Speed (RPM)": st.text_input(
                "Shoper Speed (RPM)",
                value=step_fields_data.get("Shoper Speed (RPM)", "") if step_fields_data else "",
                key=f"shoper_speed_granulation_{key}"
            ),
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_granulation_{key}"
            )
        }
    elif step_type == "Milling":
        fields = {
            "Comil Model": st.selectbox(
                "Comil Model",
                options=["197", "194", "U20"],  # Options disponibles
                index=0 if step_fields_data is None or "Comil Model" not in step_fields_data else ["197", "194", "U20"].index(step_fields_data.get("Comil Model", "197")),
                key=f"comil_model_{key}"
            ),
            "Impeller Type": st.text_input(
                "Impeller Type",
                value=step_fields_data.get("Impeller Type", "") if step_fields_data else "",
                key=f"impeller_type_{key}"
            ),
            "Sieve Size/Type": st.text_input(
                "Sieve Size/Type",
                value=step_fields_data.get("Sieve Size/Type", "") if step_fields_data else "",
                key=f"sieve_size_{key}"
            ),
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_{key}"
            )
        }
    elif step_type == "Manual sieving steps":
        fields = {
            "Screen Size": st.text_input(
                "Screen Size",
                value=step_fields_data.get("Screen Size", "") if step_fields_data else "",
                key=f"screen_size_{key}"
            )
        }
    elif step_type == "Dispersion":
        # Lecture directe des valeurs dans session_state ou initialisation à False
        use_full_quantity_key = f"use_full_quantity_{key}"
        keep_bag_for_rinsing_dispersion_key = f"keep_bag_for_rinsing_dispersion_{key}"
        
        # Définition des cases à cocher
        use_full_quantity = st.checkbox(
            "Utiliser toute la quantité",
            value=st.session_state.get(use_full_quantity_key, False),
            key=use_full_quantity_key
        )
        keep_bag_for_rinsing_dispersion = st.checkbox(
            "Keep the Bag for rinsing",
            value=st.session_state.get(keep_bag_for_rinsing_dispersion_key, False),
            key=keep_bag_for_rinsing_dispersion_key
        )

        # Initialisation des champs
        fields = {}
        if not use_full_quantity:
            fields["Approximate Quantity"] = st.text_input(
                "Approximate Quantity",
                value=step_fields_data.get("Approximate Quantity", "") if step_fields_data else "",
                key=f"approximate_quantity_{key}"
            )
        fields["Dispersion Time (seconds)"] = st.text_input(
            "Dispersion Time (seconds)",
            value=step_fields_data.get("Dispersion Time (seconds)", "") if step_fields_data else "",
            key=f"dispersion_time_{key}"
        )
        fields["Speed (RPM)"] = st.text_input(
            "Speed (RPM)",
            value=step_fields_data.get("Speed (RPM)", "") if step_fields_data else "",
            key=f"dispersion_speed_{key}"
        )

    # Les valeurs sont directement mises à jour par Streamlit


    # for field_name, field_input in fields.items():
    #     st.session_state[f"{field_name.replace(' ', '_').lower()}_{key}"] = field_input
    
    return fields


def page_3():
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

    if "show_step_form" not in st.session_state:
        st.session_state.show_step_form = False
    if "edit_step_uuid" not in st.session_state:
        st.session_state.edit_step_uuid = None
    if "step_form_key" not in st.session_state:
        st.session_state.step_form_key = str(uuid.uuid4())
    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "bom_items" not in st.session_state or not st.session_state.bom_items:
        st.warning("Please define the number of items in Step 2.")
        return

    st.title("PROCESS FLOW ")

    st.subheader("Process Overview ")
    for idx, step in enumerate(st.session_state.steps, start=1):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"**Step {idx}:** {step['step_type']} in {step['section']}")
        with col2:
            if st.button(f"Edit Step {idx}", key=f"edit_button_{idx}"):
                st.session_state.edit_step_uuid = step['uuid']
                st.session_state.show_step_form = True
                st.session_state.step_form_key = step['uuid']

    sections = ["DRY MIX", "DRY COMPACTION", "HS GRANULATION", "FB DRYING", "COMPRESSION", "ENCAPSULATION", "COATING"]

    if st.button("Add a Step"):
        st.session_state.edit_step_uuid = None
        st.session_state.show_step_form = True
        st.session_state.step_form_key = str(uuid.uuid4())

    if st.session_state.show_step_form:
        if st.session_state.edit_step_uuid:
            existing_step = next(step for step in st.session_state.steps if step['uuid'] == st.session_state.edit_step_uuid)
            step_number = st.session_state.steps.index(existing_step) + 1
            st.markdown(f"**Update Step {step_number}**")
            button_label = "Confirm the modifications"
            step_fields_data = existing_step.get("step_fields", {})
            selected_items = existing_step.get("selected_items", [])
            section = existing_step.get("section", sections[0])
            step_type = existing_step.get("step_type", "")
        else:
            step_number = len(st.session_state.steps) + 1
            st.markdown(f"**Create the New Step {step_number}**")
            button_label = "Confirm the step"
            step_fields_data = {}
            selected_items = []
            section = sections[0]
            step_type = ""

        section = st.selectbox("Select a section", sections, index=sections.index(section))
        step_type_options = (
            ["Solution/Suspension Preparation", "HS Pre-Mix", "Granulation", "Milling"]
            if section == "HS GRANULATION" else
            ["Mixing / Lubrication steps", "Milling steps", "Manual sieving steps", "Dispersion"]
        )
        step_type = st.selectbox(
            "Select a step type",
            step_type_options,
            index=step_type_options.index(step_type) if step_type in step_type_options else 0,
            key=f"step_type_select_{st.session_state.step_form_key}"
        )

       # 1. Calculer les items utilisés
        used_items = [
            item for step in st.session_state.steps
            if step["uuid"] != st.session_state.edit_step_uuid
            for item in step.get("selected_items", [])
        ]

        # 2. Calculer les items disponibles
        available_items = [item for item in st.session_state.bom_items if item not in used_items]

        # 3. Vérifier si "Item 1" est disponible
        item_1_available = "Item 1" in available_items

        # 4. Construire la liste des options pour le multiselect
        #    (ajoutant les items disponibles, sélectionnés et les résultats d'étapes)
        options = available_items + selected_items + [
            f"Step {i} result " for i in range(1, len(st.session_state.steps) + 1)
        ]

        # 5. Afficher la checkbox si "# Vérifiez si la clé existe dans st.session_state
        keep_bag_for_rinsing = False
        if item_1_available:
                keep_bag_for_rinsing = st.checkbox(
                    "Keep Bag for rinsing ",
                    value=st.session_state.get("keep_bag_for_rinsing", False)
                )

        

        # 6. Afficher le multiselect pour choisir les items
        selected_items = st.multiselect(
            "Select the items for this step",
            options=options,
            default=selected_items,
            help="Choose the items to use in this step.."
        )

        

        step_fields = initialize_step_fields(step_type, st.session_state.step_form_key, step_fields_data)
        
        if "step_form_key" not in st.session_state:
            st.session_state.step_form_key = str(uuid.uuid4())

        step_key = st.session_state.step_form_key  # Utiliser step_form_key comme identifiant unique


        if st.button(button_label):
            if st.session_state.edit_step_uuid:
                step_details = next(step for step in st.session_state.steps if step['uuid'] == st.session_state.edit_step_uuid)
                step_details["section"] = section
                step_details["step_type"] = step_type
                step_details["selected_items"] = selected_items
                step_details["step_fields"] = step_fields
                st.success(f"Step {step_number} successfully updated! ")
            else:
                step_details = {
                    "uuid": str(uuid.uuid4()),
                    "section": section,
                    "step_type": step_type,
                    "timestamp": datetime.now(),
                    "selected_items": selected_items,
                    "step_fields": step_fields,
                    # Gestion des deux champs de rincing
                    "keep_bag_for_rinsing": keep_bag_for_rinsing,  # Enregistrement explicite
                    "keep_bag_for_rinsing_dispersion": st.session_state.get(f"keep_bag_for_rinsing_dispersion_{step_key}", False),
                    "use_full_quantity": st.session_state.get(f"use_full_quantity_{step_key}", False)
                }
                st.session_state.steps.append(step_details)
                st.success(f"New step {step_number} added!")

                # Nettoyage des clés après ajout
                if "keep_for_rinsing" in st.session_state:
                    del st.session_state["keep_for_rinsing"]
                if f"keep_bag_for_rinsing_dispersion_{step_key}" in st.session_state:
                    del st.session_state[f"keep_bag_for_rinsing_dispersion_{step_key}"]
                if f"use_full_quantity_{step_key}" in st.session_state:
                    del st.session_state[f"use_full_quantity_{step_key}"]

            st.session_state.show_step_form = False

