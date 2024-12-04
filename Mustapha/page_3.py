import streamlit as st
import uuid
from datetime import datetime

def initialize_step_fields(step_type, key, step_fields_data=None):
    """Generate specific fields based on step type and populate with saved data if available."""
    fields = {}
    if step_type == "Mixing / Lubrication steps":
        fields = {
            "BIN SIZE (L)": st.text_input(
                "BIN SIZE (L)",
                value=step_fields_data.get("BIN SIZE (L)", "") if step_fields_data else "",
                key=f"bin_size_{key}"
            ),
            "Mixing Time (sec)": st.text_input(
                "Mixing Time (sec)",
                value=step_fields_data.get("Mixing Time (sec)", "") if step_fields_data else "",
                key=f"mixing_time_{key}"
            ),
            "Mixing Speed (RPM)": st.text_input(
                "Mixing Speed (RPM)",
                value=step_fields_data.get("Mixing Speed (RPM)", "") if step_fields_data else "",
                key=f"mixing_speed_{key}"
            )
        }
    elif step_type == "Milling steps":
        fields = {
            "COMIL MODEL": st.selectbox(
                "COMIL MODEL",
                options=["197", "194"],
                index=0 if step_fields_data is None or "COMIL MODEL" not in step_fields_data else ["197", "194"].index(step_fields_data.get("COMIL MODEL", "197")),
                key=f"comil_model_{key}"
            ),
            "IMPELLER TYPE": st.selectbox(
                "IMPELLER TYPE",
                options=["2C1601", "2C1609", "2C1612", "2A1601"],
                index=0 if step_fields_data is None or "IMPELLER TYPE" not in step_fields_data else ["2C1601", "2C1609", "2C1612", "2A1601"].index(step_fields_data.get("IMPELLER TYPE", "2C1601")),
                key=f"impeller_type_{key}"
            ),
            "SIEVE SIZE AND TYPE": st.text_input(
                "SIEVE SIZE AND TYPE",
                value=step_fields_data.get("SIEVE SIZE AND TYPE", "") if step_fields_data else "",
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
            "MANUAL SCREEN": "MANUAL SCREEN",  # Insère directement la phrase "MANUAL SCREEN"
            "Screen Size (Mesh)": st.text_input(
                "Screen Size (Mesh)",
                value=step_fields_data.get("Screen Size (Mesh)", "") if step_fields_data else "",
                key=f"screen_size_{key}"
            )
        }

    elif step_type == "Dispersion":
        use_full_quantity_key = f"use_full_quantity_{key}"
        use_full_quantity = st.checkbox(
            "Use Full Quantity",
            value=step_fields_data.get("use_full_quantity", False) if step_fields_data else False,
            key=use_full_quantity_key
        )

        # Sélection des items pour rinçage
        item_to_rinse = st.selectbox(
            "Item to Rinse With",
            options=st.session_state.get("bom_items", []),  # Liste des items disponibles
            index=0 if "Item to Rinse With" not in step_fields_data else st.session_state["bom_items"].index(
                step_fields_data.get("Item to Rinse With", st.session_state["bom_items"][0])
            ),
            key=f"item_rinse_dispersion_{key}"
        )

        fields = {"Item to Rinse With": item_to_rinse}

        if not use_full_quantity:  # Si "Use Full Quantity" n'est pas coché, afficher le champ pour la quantité
            fields["Approximate Quantity"] = st.text_input(
                "Approximate Quantity",
                value=step_fields_data.get("Approximate Quantity", ""),
                key=f"approximate_quantity_dispersion_{key}"
            )

        # Champs supplémentaires pour Dispersion
        fields["Dispersion Time (seconds)"] = st.text_input(
            "Dispersion Time (seconds)",
            value=step_fields_data.get("Dispersion Time (seconds)", ""),
            key=f"dispersion_time_{key}"
        )
        fields["Speed (RPM)"] = st.text_input(
            "Speed (RPM)",
            value=step_fields_data.get("Speed (RPM)", ""),
            key=f"dispersion_speed_{key}"
        )


    elif step_type == "API Bag Rinsing":
        use_full_quantity_key = f"use_full_quantity_apibag_{key}"
        use_full_quantity = st.checkbox(
            "Use Full Quantity",
            value=st.session_state.get(use_full_quantity_key, False),
            key=use_full_quantity_key
        )

        # Sélection des items pour rinçage
        item_to_rinse = st.selectbox(
            "Item to Rinse With",
            options=st.session_state.get("bom_items", []),  # Liste des items disponibles
            index=0 if "Item to Rinse With" not in step_fields_data else st.session_state["bom_items"].index(
                step_fields_data.get("Item to Rinse With", st.session_state["bom_items"][0])
            ),
            key=f"item_rinse_apibag_{key}"
        )

        fields = {"Item to Rinse With": item_to_rinse}

        if not use_full_quantity:  # Si "Use Full Quantity" n'est pas coché, afficher le champ pour la quantité
            fields["Quantity (Total/Portion)"] = st.text_input(
                "Quantity (Total/Portion)",
                value=step_fields_data.get("Quantity (Total/Portion)", ""),
                key=f"quantity_rinse_apibag_{key}"
            )

        # Champs supplémentaires pour API Bag Rinsing
        fields["Dispersion Time (seconds)"] = st.text_input(
            "Dispersion Time (seconds)",
            value=step_fields_data.get("Dispersion Time (seconds)", ""),
            key=f"dispersion_time_rinse_apibag_{key}"
        )


        
    elif step_type == "Dry Compaction":
        fields = {
            "Roller Compactor TF-220": "Roller Compactor TF-220",
            "Screw Speed (RPM)": st.text_input(
                "Screw Speed (RPM)",
                value=step_fields_data.get("Screw Speed (RPM)", "") if step_fields_data else "",
                key=f"screw_speed_{key}"
            ),
            "Roll Speed (RPM)": st.text_input(
                "Roll Speed (RPM)",
                value=step_fields_data.get("Roll Speed (RPM)", "") if step_fields_data else "",
                key=f"roll_speed_{key}"
            ),
            "Roll Force (Ton)": st.text_input(
                "Roll Force (Ton)",
                value=step_fields_data.get("Roll Force (Ton)", "") if step_fields_data else "",
                key=f"roll_force_{key}"
            ),
            "Roll Gap (mm)": st.text_input(
                "Roll Gap (mm)",
                value=step_fields_data.get("Roll Gap (mm)", "") if step_fields_data else "",
                key=f"roll_gap_{key}"
            )
        }
    elif step_type == "Preparation of Granulation Solution/Suspension":
        fields = {
            "Preparation Method": st.selectbox(
                "Preparation Method",
                ["Mixing", "Homogenizing"],
                index=0 if step_fields_data is None or "Preparation Method" not in step_fields_data else ["Mixing", "Homogenizing"].index(step_fields_data.get("Preparation Method", "Mixing")),
                key=f"prep_method_{key}"
            )
        }
        if fields["Preparation Method"] == "Mixing":
            fields.update({
                "Mixer Type ": st.selectbox(
                    "Mixer Type (Pneumatic/Electric)",
                    options=["Pneumatic", "Electric"],  # Options for the selectbox
                    index=0 if step_fields_data is None or "Mixer Type (Pneumatic/Electric)" not in step_fields_data 
                            else ["Pneumatic", "Electric"].index(step_fields_data.get("Mixer Type (Pneumatic/Electric)", "Pneumatic")),
                    key=f"mixer_type_{key}"
                ),
                "Container Size (L)": st.text_input(
                    "Container Size (L)",
                    value=step_fields_data.get("Container Size (L)", "") if step_fields_data else "",
                    key=f"container_size_{key}"
                ),
                "Mixing Time": st.text_input(
                    "Mixing Time",
                    value=step_fields_data.get("Mixing Time", "") if step_fields_data else "",
                    key=f"mixing_time_{key}"
                ),
                "Holding Time (Hours)": st.text_input(
                    "Holding Time (Hours)",
                    value=step_fields_data.get("Holding Time (Hours)", "") if step_fields_data else "",
                    key=f"holding_time_{key}"
                )
            })

        elif fields["Preparation Method"] == "Homogenizing":
            fields.update({
                "Homogenizer Type": "Homogenizer Type",
                "Container Size (L)": st.text_input(
                    "Container Size (L)",
                    value=step_fields_data.get("Container Size (L)", "") if step_fields_data else "",
                    key=f"container_size_{key}"
                ),
                "Homogenizing Time (SEC)": st.text_input(
                    "Homogenizing Time (SEC)",
                    value=step_fields_data.get("Homogenizing Time (SEC)", "") if step_fields_data else "",
                    key=f"homogenizing_time_{key}"
                ),
                "Homogenizing Speed (RPM)": st.text_input(
                    "Homogenizing Speed (RPM)",
                    value=step_fields_data.get("Homogenizing Speed (RPM)", "") if step_fields_data else "",
                    key=f"homogenizing_speed_{key}"
                ),
                "Holding Time (Hours)": st.text_input(
                    "Holding Time (Hours)",
                    value=step_fields_data.get("Holding Time (Hours)", "") if step_fields_data else "",
                    key=f"holding_time_{key}"
                )
            })

    elif step_type == "HS Pre-Mix":
        fields = {
            "High Shear (65L)": "High Shear (65L)",
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_hspremix_{key}"
            ),
            "Shopper Speed (RPM)": st.text_input(
                "Shopper Speed (RPM)",
                value=step_fields_data.get("Shopper Speed (RPM)", "") if step_fields_data else "",
                key=f"shopper_speed_hspremix_{key}"
            ),
            "Mixing Time (sec)": st.text_input(
                "Mixing Time (sec)",
                value=step_fields_data.get("Mixing Time (sec)", "") if step_fields_data else "",
                key=f"mixing_time_hspremix_{key}"
            )
        }
    elif step_type == "WT Granulation":
        fields = {
            "HIGH SHEAR 65L": "HIGH SHEAR 65L",
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_wtgranulation_{key}"
            ),
            "Shopper Speed (RPM)": st.text_input(
                "Shopper Speed (RPM)",
                value=step_fields_data.get("Shopper Speed (RPM)", "") if step_fields_data else "",
                key=f"shopper_speed_wtgranulation_{key}"
            ),
            "Mixing (SEC)": st.text_input(
                "Mixing (SEC)",
                value=step_fields_data.get("Mixing (SEC)", "") if step_fields_data else "",
                key=f"mixing_time_wtgranulation_{key}"
            )
        }

    elif step_type == "Kneading":
        fields = {
            "Impeller Speed (RPM)": st.text_input(
                "Impeller Speed (RPM)",
                value=step_fields_data.get("Impeller Speed (RPM)", "") if step_fields_data else "",
                key=f"impeller_speed_kneading_{key}"
            ),
            "Shopper Speed (RPM)": st.text_input(
                "Shopper Speed (RPM)",
                value=step_fields_data.get("Shopper Speed (RPM)", "") if step_fields_data else "",
                key=f"shopper_speed_kneading_{key}"
            ),
            "Kneading Time (sec)": st.text_input(
                "Kneading Time (sec)",
                value=step_fields_data.get("Kneading Time (sec)", "") if step_fields_data else "",
                key=f"kneading_time_{key}"
            )
        }
    elif step_type == "Preheating Parameters":
        fields = {
            "FLUID BED DRYER O’HARA 15 KG": "FLUID BED DRYER O’HARA 15 KG",
            "Inlet Temperature (°C)": st.text_input(
                "Inlet Temperature (°C)",
                value=step_fields_data.get("Inlet Temperature (°C)", "") if step_fields_data else "",
                key=f"inlet_temperature_{key}"
            ),
            "Dew Point (°C)": st.text_input(
                "Dew Point (°C)",
                value=step_fields_data.get("Dew Point (°C)", "") if step_fields_data else "",
                key=f"dew_point_{key}"
            ),
            "Outlet Temperature (°C)": st.text_input(
                "Outlet Temperature (°C)",
                value=step_fields_data.get("Outlet Temperature (°C)", "") if step_fields_data else "",
                key=f"outlet_temperature_{key}"
            )
        }
    elif step_type == "Drying Parameters":
        fields = {
            "Air Flow Volume (CFM)": st.text_input(
                "Air Flow Volume (CFM)",
                value=step_fields_data.get("Air Flow Volume (CFM)", "") if step_fields_data else "",
                key=f"air_flow_volume_{key}"
            ),
            "Inlet Temperature (°C)": st.text_input(
                "Inlet Temperature (°C)",
                value=step_fields_data.get("Inlet Temperature (°C)", "") if step_fields_data else "",
                key=f"inlet_temperature_drying_{key}"
            ),
            "Dew Point (°C)": st.text_input(
                "Dew Point (°C)",
                value=step_fields_data.get("Dew Point (°C)", "") if step_fields_data else "",
                key=f"dew_point_drying_{key}"
            ),
            "Product Temperature (°C)": st.text_input(
                "Product Temperature (°C)",
                value=step_fields_data.get("Product Temperature (°C)", "") if step_fields_data else "",
                key=f"product_temperature_{key}"
            ),
            "Outlet Temperature (°C)": st.text_input(
                "Outlet Temperature (°C)",
                value=step_fields_data.get("Outlet Temperature (°C)", "") if step_fields_data else "",
                key=f"outlet_temperature_drying_{key}"
            ),
            "LOD (%)": st.text_input(
                "LOD (%)",
                value=step_fields_data.get("LOD (%)", "") if step_fields_data else "",
                key=f"lod_{key}"
            )
        }
    elif step_type == "Compression":
        # Charger les items disponibles depuis le BOM
        bom_items = st.session_state.get("bom_items", [])
        if not bom_items:
            st.warning("No BOM items available. Please define BOM items in Step 2.")
            return

        # Récupérer les items consommés et les résultats des étapes précédentes
        consumed_items = st.session_state.get("consumed_items", set())
        step_results = [f"Step {i} result" for i in range(1, len(st.session_state.steps) + 1)]

        # Calculer les items restants
        available_items = [
            item for item in bom_items if item not in consumed_items
        ] + step_results

        # Initialisation des forces
        strengths_key = f"compression_strengths_{key}"
        if strengths_key not in st.session_state:
            st.session_state[strengths_key] = step_fields_data.get("strengths", [])

        strengths = st.session_state[strengths_key]

        # Déterminer le nombre de forces
        num_strengths = st.number_input(
            "Number of Strengths",
            min_value=1,
            value=len(strengths) or 1,
            step=1,
            key=f"num_strengths_{key}"
        )

        # Ajuster les forces pour correspondre au nombre
        if len(strengths) != num_strengths:
            strengths = [
                strengths[i] if i < len(strengths) else {
                    "strength": "",
                    "Press Type/Model": "BETA PRESS",
                    "Average Weight (mg)": "",
                    "Individual Weight (mg)": "",
                    "Hardness (kp)": "",
                    "Thickness (mm)": "",
                    "Items for this Strength": []
                }
                for i in range(num_strengths)
            ]
            st.session_state[strengths_key] = strengths

        # Gestion dynamique des items restants pour chaque force
        force_remaining_items = available_items.copy()

        # Mise à jour des champs spécifiques pour chaque force
        for idx in range(1, num_strengths + 1):
            strength = strengths[idx - 1]  # Récupérer ou initialiser la force actuelle

            with st.expander(f"Strength {idx}", expanded=True):
                # Champs pour les propriétés spécifiques de la force
                strength["Strength value (mg)"] = st.text_input(
                    f"Strength value (mg) (Strength {idx})",
                    value=strength.get("Strength value (mg)", ""),
                    key=f"Strength_value_{key}_{idx}"
                )
                
                strength["Press Type/Model"] = st.selectbox(
                    f"Press Type/Model (Strength {idx})",
                    ["BETA PRESS", "XL100", "XL100 PRO", "X3 SFP"],
                    index=["BETA PRESS", "XL100", "XL100 PRO", "X3 SFP"].index(strength.get("Press Type/Model", "BETA PRESS")),
                    key=f"press_type_{key}_{idx}"
                )
                strength["Average Weight (mg)"] = st.text_input(
                    f"Average Weight (mg) (Strength {idx})",
                    value=strength.get("Average Weight (mg)", ""),
                    key=f"avg_weight_{key}_{idx}"
                )
                strength["Individual Weight (mg)"] = st.text_input(
                    f"Individual Weight (mg) (Strength {idx})",
                    value=strength.get("Individual Weight (mg)", ""),
                    key=f"ind_weight_{key}_{idx}"
                )
                strength["Hardness (kp)"] = st.text_input(
                    f"Hardness (kp) (Strength {idx})",
                    value=strength.get("Hardness (kp)", ""),
                    key=f"hardness_{key}_{idx}"
                )
                strength["Thickness (mm)"] = st.text_input(
                    f"Thickness (mm) (Strength {idx})",
                    value=strength.get("Thickness (mm)", ""),
                    key=f"thickness_{key}_{idx}"
                )

                # Multiselect pour les items spécifiques à cette force
                default_items = [item for item in strength.get("Items for this Strength", []) if item in force_remaining_items]
                strength["Items for this Strength"] = st.multiselect(
                    f"Select Items for Strength {idx}",
                    options=force_remaining_items,  # Items disponibles
                    default=default_items,  # Items déjà sélectionnés
                    key=f"items_strength_{key}_{idx}"
                )

                # Mise à jour des items restants pour les forces suivantes
                selected_items = strength["Items for this Strength"]
                force_remaining_items = [item for item in force_remaining_items if item not in selected_items]

        # Enregistrer les forces mises à jour dans `st.session_state`
        st.session_state[strengths_key] = strengths
        # step_fields["strengths"] = strengths  # Associer les forces mises à jour aux champs de l'étape





    elif step_type == "Encapsulation":
        # Charger les items disponibles depuis le BOM
        bom_items = st.session_state.get("bom_items", [])
        if not bom_items:
            st.warning("No BOM items available. Please define BOM items in Step 2.")
            return

        # Récupérer les items consommés et les résultats des étapes précédentes
        consumed_items = st.session_state.get("consumed_items", set())
        step_results = [f"Step {i} result" for i in range(1, len(st.session_state.steps) + 1)]

        # Calculer les items restants
        available_items = [
            item for item in bom_items if item not in consumed_items
        ] + step_results

        # Initialisation des forces
        strengths_key = f"encapsulation_strengths_{key}"
        if strengths_key not in st.session_state:
            st.session_state[strengths_key] = step_fields_data.get("strengths", [])

        strengths = st.session_state[strengths_key]

        # Déterminer le nombre de forces
        num_strengths = st.number_input(
            "Number of Strengths",
            min_value=1,
            value=len(strengths) or 1,
            step=1,
            key=f"num_strengths_encap_{key}"
        )

        # Ajuster les forces pour correspondre au nombre
        if len(strengths) != num_strengths:
            strengths = [
                strengths[i] if i < len(strengths) else {
                    "Strength": "",
                    "Capsule Size": "",
                    "Dosing Disk Size": "",
                    "Average Weight (mg)": "",
                    "Individual Weight (mg)": "",
                    "Items for this Strength": []
                }
                for i in range(num_strengths)
            ]
            st.session_state[strengths_key] = strengths

        # Gestion dynamique des items restants pour chaque force
        force_remaining_items = available_items.copy()

        # Mise à jour des champs spécifiques pour chaque force
        for idx in range(1, num_strengths + 1):
            strength = strengths[idx - 1]  # Récupérer ou initialiser la force actuelle

            with st.expander(f"Strength {idx}", expanded=True):
                # Champs pour les propriétés spécifiques de la force
                strength["Strength value (mg)"] = st.text_input(
                    f"Strength value (mg) (Strength {idx})",
                    value=strength.get("Strength value (mg)", ""),
                    key=f"Strength_value_{key}_{idx}"
                )
                strength["Capsule Size"] = st.text_input(
                    f"Capsule Size (Strength {idx})",
                    value=strength.get("Capsule Size", ""),
                    key=f"capsule_size_{key}_{idx}"
                )
                strength["Dosing Disk Size"] = st.text_input(
                    f"Dosing Disk Size (Strength {idx})",
                    value=strength.get("Dosing Disk Size", ""),
                    key=f"dosing_disk_size_{key}_{idx}"
                )
                strength["Average Weight (mg)"] = st.text_input(
                    f"Average Weight (mg) (Strength {idx})",
                    value=strength.get("Average Weight (mg)", ""),
                    key=f"avg_weight_encap_{key}_{idx}"
                )
                strength["Individual Weight (mg)"] = st.text_input(
                    f"Individual Weight (mg) (Strength {idx})",
                    value=strength.get("Individual Weight (mg)", ""),
                    key=f"ind_weight_encap_{key}_{idx}"
                )

                # Multiselect pour les items spécifiques à cette force
                default_items = [item for item in strength.get("Items for this Strength", []) if item in force_remaining_items]
                strength["Items for this Strength"] = st.multiselect(
                    f"Select Items for Strength {idx}",
                    options=force_remaining_items,  # Items disponibles
                    default=default_items,  # Items déjà sélectionnés
                    key=f"items_strength_encap_{key}_{idx}"
                )

                # Mise à jour des items restants pour les forces suivantes
                selected_items = strength["Items for this Strength"]
                force_remaining_items = [item for item in force_remaining_items if item not in selected_items]

        # Enregistrer les forces mises à jour dans `st.session_state`
        st.session_state[strengths_key] = strengths
        # Ajouter les forces mises à jour aux champs
        fields["strengths"] = strengths

        
        
    elif step_type == "Preparation of Coating Solution/Suspension":
        fields = {
            "Container Size (L)": st.text_input(
                "Container Size (L)",
                value=step_fields_data.get("Container Size (L)", "") if step_fields_data else "",
                key=f"container_size_coating_{key}"
            ),
            "Solid Content (%)": st.text_input(
                "Solid Content (%)",
                value=step_fields_data.get("Solid Content (%)", "") if step_fields_data else "",
                key=f"solid_content_{key}"
            ),
            "Mixing Time (minutes)": st.text_input(
                "Mixing Time (minutes)",
                value=step_fields_data.get("Mixing Time (minutes)", "") if step_fields_data else "",
                key=f"mixing_time_coating_{key}"
            ),
            "Holding Time (Hours)": st.text_input(
                "Holding Time (Hours)",
                value=step_fields_data.get("Holding Time (Hours)", "") if step_fields_data else "",
                key=f"holding_time_coating_{key}"
            )
        }
    elif step_type == "Coating":
        fields = {
            "Pan Size (Inch)": st.text_input(
                "Pan Size (Inch)",
                value=step_fields_data.get("Pan Size (Inch)", "") if step_fields_data else "",
                key=f"pan_size_{key}"
            ),
            "Number of Loads": st.text_input(
                "Number of Loads",
                value=step_fields_data.get("Number of Loads", "") if step_fields_data else "",
                key=f"num_loads_{key}"
            ),
            "Number of Guns": st.text_input(
                "Number of Guns",
                value=step_fields_data.get("Number of Guns", "") if step_fields_data else "",
                key=f"num_guns_{key}"
            ),
            "Pan Load (g)": st.text_input(
                "Pan Load (g)",
                value=step_fields_data.get("Pan Load (g)", "") if step_fields_data else "",
                key=f"pan_load_{key}"
            ),
            "Pan Speed (RPM)": st.text_input(
                "Pan Speed (RPM)",
                value=step_fields_data.get("Pan Speed (RPM)", "") if step_fields_data else "",
                key=f"pan_speed_{key}"
            ),
            "Gun-to-Bed Distance (cm)": st.text_input(
                "Gun-to-Bed Distance (cm)",
                value=step_fields_data.get("Gun-to-Bed Distance (cm)", "") if step_fields_data else "",
                key=f"gun_bed_distance_{key}"
            ),
            "Atomizing Air Pressure (PSI)": st.text_input(
                "Atomizing Air Pressure (PSI)",
                value=step_fields_data.get("Atomizing Air Pressure (PSI)", "") if step_fields_data else "",
                key=f"atomizing_air_pressure_{key}"
            ),
            "Pattern Air Pressure (PSI)": st.text_input(
                "Pattern Air Pressure (PSI)",
                value=step_fields_data.get("Pattern Air Pressure (PSI)", "") if step_fields_data else "",
                key=f"pattern_air_pressure_{key}"
            ),
            "Flow Rate (g/min)": st.text_input(
                "Flow Rate (g/min)",
                value=step_fields_data.get("Flow Rate (g/min)", "") if step_fields_data else "",
                key=f"flow_rate_{key}"
            ),
            "Air Volume (CFM)": st.text_input(
                "Air Volume (CFM)",
                value=step_fields_data.get("Air Volume (CFM)", "") if step_fields_data else "",
                key=f"air_volume_{key}"
            ),
            "Exhaust Temperature (°C)": st.text_input(
                "Exhaust Temperature (°C)",
                value=step_fields_data.get("Exhaust Temperature (°C)", "") if step_fields_data else "",
                key=f"exhaust_temperature_{key}"
            ),
            "Weight Gain (%)": st.text_input(
                "Weight Gain (%)",
                value=step_fields_data.get("Weight Gain (%)", "") if step_fields_data else "",
                key=f"weight_gain_{key}"
            )
        }

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

    # Initialisation des états
    if "show_step_form" not in st.session_state:
        st.session_state.show_step_form = False
    if "edit_step_uuid" not in st.session_state:
        st.session_state.edit_step_uuid = None
    if "step_form_key" not in st.session_state:
        st.session_state.step_form_key = str(uuid.uuid4())
    if "steps" not in st.session_state:
        st.session_state.steps = []
    if "consumed_items" not in st.session_state:
        st.session_state.consumed_items = set()  # Pour les items complètement utilisés
    if "remaining_items" not in st.session_state:
        st.session_state.remaining_items = {}  # Pour les items partiellement consommés
    if "bom_items" not in st.session_state or not st.session_state.bom_items:
        st.warning("Please define the number of items in Step 2.")
        return

    # Titre principal
    st.title("PROCESS FLOW ")

    # Aperçu des étapes existantes
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

    # Définition des sections et des steps associés
    section_steps_mapping = {
        "DRY MIX": [
            "Mixing / Lubrication steps",  # Correspond à "Mixing/Lubrication"
            "Milling steps",              # Correspond à "Milling"
            "Manual sieving steps",       # Correspond à "Manual Sieving"
            "Dispersion",                 # Pas de modification
            "API Bag Rinsing"             # Pas de modification
        ],
        "DRY COMPACTION": [
            "Dry Compaction"              # Pas de modification
        ],
        "HIGH SHEAR GRANULATION": [
            "Preparation of Granulation Solution/Suspension", # Pas de modification
            "HS Pre-Mix",                 # Pas de modification
            "WT Granulation",             # Pas de modification
            "Kneading"                    # Pas de modification
        ],
        "FLUID BED DRYING": [
            "Preheating Parameters",      # Pas de modification
            "Drying Parameters"           # Pas de modification
        ],
        "COMPRESSION (per strength)": [
            "Compression"                 # Pas de modification
        ],
        "ENCAPSULATION (per strength)": [
            "Encapsulation"               # Pas de modification
        ],
        "COATING": [
            "Preparation of Coating Solution/Suspension", # Pas de modification
            "Coating"                    # Pas de modification
        ]
}



    sections = list(section_steps_mapping.keys())

    if st.button("Add a Step"):
        st.session_state.edit_step_uuid = None
        st.session_state.show_step_form = True
        st.session_state.step_form_key = str(uuid.uuid4())

    # Gestion du formulaire pour ajouter ou éditer une étape
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

        # Sélection de la section et des types de steps
        section = st.selectbox("Select a section", sections, index=sections.index(section))
        step_type_options = section_steps_mapping[section]
        step_type = st.selectbox(
            "Select a step type",
            step_type_options,
            index=step_type_options.index(step_type) if step_type in step_type_options else 0,
            key=f"step_type_select_{st.session_state.step_form_key}"
        )

        # Gestion des items utilisés et disponibles
        used_items = [
            item for step in st.session_state.steps
            if step["uuid"] != st.session_state.edit_step_uuid
            for item in step.get("selected_items", [])
        ]

        # Exclure les items complètement consommés et ceux qui ont une version "restant"
        available_items = [
            item for item in st.session_state.bom_items
            if item not in st.session_state.consumed_items and item not in st.session_state.remaining_items
        ]

        # Ajouter uniquement les versions "restantes" (partiellement consommées)
        available_items += list(st.session_state.remaining_items.values())
        
        # Construction des options pour multiselect
        options = available_items + selected_items + [
            f"Step {i} result" for i in range(1, len(st.session_state.steps) + 1)
        ]
        
        # Multiselect pour choisir les items
        selected_items = st.multiselect(
            "Select the items for this step",
            options=options,
            default=selected_items,
            help="Choose the items to use in this step."
        )


        # Initialisation des champs spécifiques au type de step
        step_fields = initialize_step_fields(step_type, st.session_state.step_form_key, step_fields_data)

        if st.button(button_label):
            # Ensure the key is properly initialized
            key = st.session_state.get("step_form_key", str(uuid.uuid4()))
            
            if st.session_state.edit_step_uuid:
                step_index = next(
                    (i for i, step in enumerate(st.session_state.steps) if step['uuid'] == st.session_state.edit_step_uuid), 
                    None
                )

                if step_index is not None:
                     # Add the checkbox value to step_fields
                    use_full_quantity_key = f"use_full_quantity_{st.session_state.step_form_key}"
                    step_fields["use_full_quantity"] = st.session_state.get(use_full_quantity_key, False)
                    step_fields["selected_items"] = selected_items  # Lié au multiselect
                    st.session_state.steps[step_index] = {
                        "uuid": st.session_state.edit_step_uuid,
                        "section": section,
                        "step_type": step_type,
                        "timestamp": datetime.now(),
                        "selected_items": step_fields.get("selected_items", []),
                        "step_fields": step_fields,
                    }
                    st.success(f"Step {step_number} successfully updated!")
                else:
                    st.error("Step not found. Please try again.")
            else:
                # Ajouter une nouvelle étape
                # Add the checkbox value to step_fields
                use_full_quantity_key = f"use_full_quantity_{st.session_state.step_form_key}"
                step_fields["use_full_quantity"] = st.session_state.get(use_full_quantity_key, False)
                step_fields["selected_items"] = selected_items  # Lié au multiselect
                step_details = {
                    "uuid": str(uuid.uuid4()),
                    "section": section,
                    "step_type": step_type,
                    "timestamp": datetime.now(),
                    "selected_items": step_fields.get("selected_items", []),
                    "step_fields": step_fields,
                }
                st.session_state.steps.append(step_details)
                st.success(f"New step {step_number} added!")


                # Mise à jour des forces dans Compression et Encapsulation
            if step_type in ["Compression", "Encapsulation"]:
                step_fields["selected_items"] = selected_items  # Lié au multiselect
                # Vérification et initialisation des clés globales
                global_items_key = f"selected_items_global_{key}"
                if global_items_key not in st.session_state:
                    st.session_state[global_items_key] = []  # Initialisation avec une liste vide

                # Définir la clé pour sauvegarder les forces (Compression ou Encapsulation)
                strengths_key = f"{step_type.lower()}_strengths_{key}"
                if strengths_key not in st.session_state:
                    st.session_state[strengths_key] = step_fields.get("strengths", [])

                # Sauvegarde des forces
                strengths = st.session_state[strengths_key]

                # Sauvegarder les forces mises à jour dans st.session_state
                st.session_state[strengths_key] = strengths

                # Ajouter les forces aux champs de l'étape
                step_fields["strengths"] = strengths

            # Mise à jour des items consommés ou partiellement consommés
            item_to_rinse = step_fields.get("Item to Rinse With")  # L'item sélectionné pour rinçage
            if step_type in ["Dispersion", "API Bag Rinsing"]:
                # Gérer uniquement l'item "Item to Rinse With"
                use_full_quantity_key = f"use_full_quantity_{st.session_state.step_form_key}"
                if st.session_state.get(use_full_quantity_key, False):
                    # Si "Use Full Quantity" est coché
                    st.session_state.consumed_items.add(item_to_rinse)
                    if item_to_rinse in st.session_state.remaining_items:
                        del st.session_state.remaining_items[item_to_rinse]
                else:
                    # Si "Use Full Quantity" n'est pas coché
                    st.session_state.remaining_items[item_to_rinse] = f"The rest of {item_to_rinse}"

            # Tous les autres items sont considérés comme entièrement consommés
            for item in selected_items:
                # Si "The rest of Item X" est utilisé comme item principal, le marquer comme consommé
                if "The rest of" in item:
                    st.session_state.consumed_items.add(item)
                    remaining_original = [key for key, value in st.session_state.remaining_items.items() if value == item]
                    if remaining_original:
                        del st.session_state.remaining_items[remaining_original[0]]
                elif item != item_to_rinse:  # Ne pas retraiter l'item "Item to Rinse With"
                    st.session_state.consumed_items.add(item)
                    if item in st.session_state.remaining_items:
                        del st.session_state.remaining_items[item]



            # Fermer le formulaire après confirmation
            st.session_state.show_step_form = False


