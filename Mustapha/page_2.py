import streamlit as st
import uuid  # Import uuid for generating unique item IDs

def page_2():
    st.title("Étape 2 : Ajouter les éléments BOM")

    # Initialize session state for BOM sections, item entries, and item counter if they don't exist
    if 'bom_sections' not in st.session_state:
        st.session_state.bom_sections = {}
    if 'item_entries' not in st.session_state:
        st.session_state.item_entries = []
    if 'show_new_item_form' not in st.session_state:
        st.session_state.show_new_item_form = False
    if 'edit_item_index' not in st.session_state:
        st.session_state.edit_item_index = None
    if 'original_item_uuid' not in st.session_state:
        st.session_state.original_item_uuid = None
    if 'item_counter' not in st.session_state:
        st.session_state.item_counter = 1  # Initialize a global item counter

    # Function to display the input fields for each entry with numbering
    def display_item_fields(entry_index, section="", code="", name="", quantity=""):
        sections = ["Pre-Mix", "Final-Mix", "Granulation Solution/Suspension", "Coating Solution/Suspension", "Encapsulation"]
        
        # Display item number based on global item_counter or actual item number if editing
        st.subheader(f"Item {st.session_state.item_entries[entry_index]['item_number'] if entry_index < len(st.session_state.item_entries) else st.session_state.item_counter}")

        # Create unique keys for each widget
        selected_section = st.selectbox("Sélectionner une section", sections, index=sections.index(section) if section in sections else 0, key=f"section_{entry_index}")
        item_code = st.text_input("Code de l'item", value=code, key=f"item_code_{entry_index}")
        item_name = st.text_input("Nom de l'item", value=name, key=f"item_name_{entry_index}")
        item_quantity = st.text_input("Quantité de l'item", value=quantity, key=f"item_quantity_{entry_index}")
        
        return selected_section, item_code, item_name, item_quantity

    # Display all saved item entries with edit buttons
    for i, entry in enumerate(st.session_state.item_entries):
        # Create columns for the item text and the edit button
        col1, col2 = st.columns([8, 1])  # Adjust the column width ratio as needed

        # Display item details in the first column
        with col1:
            st.write(f"**Item Number {entry['item_number']}**  -  **Code** : {entry['item_code']}  -  **Name** : {entry['item_name']}  -  **Quantity** : {entry['item_quantity']}  -  **Section** : {entry['section']}")

        # Display the "Edit" button in the second column
        with col2:
            if st.button("Edit", key=f"edit_button_{i}"):
                st.session_state.edit_item_index = i
                st.session_state.original_item_uuid = entry['uuid']
                st.session_state.show_new_item_form = False

    # Show new item form if "Ajouter l'item" button is clicked
    if st.button("Ajouter l'item"):
        st.session_state.show_new_item_form = True
        st.session_state.edit_item_index = None
        st.session_state.original_item_uuid = None

    # Display the form to edit an existing item if an item is selected for editing
    if st.session_state.edit_item_index is not None:
        index = st.session_state.edit_item_index
        entry = st.session_state.item_entries[index]
        section, code, name, quantity = display_item_fields(index, entry['section'], entry['item_code'], entry['item_name'], entry['item_quantity'])

        # Save the changes after editing
        if st.button("Save Changes", key="save_changes"):
            edited_item = {
                'uuid': st.session_state.original_item_uuid,
                'item_number': entry['item_number'],  # Preserve original item number
                'section': section,
                'item_code': code,
                'item_name': name,
                'item_quantity': quantity
            }

            # Update the specific entry in item_entries
            st.session_state.item_entries[index] = edited_item

            # Update bom_sections based on UUID
            if section in st.session_state.bom_sections:
                for idx, item in enumerate(st.session_state.bom_sections[section]):
                    if item['uuid'] == st.session_state.original_item_uuid:
                        st.session_state.bom_sections[section][idx] = edited_item
                        break
                else:
                    st.session_state.bom_sections[section].append(edited_item)
            else:
                st.session_state.bom_sections[section] = [edited_item]
            
            st.success(f"Item {entry['item_number']} updated in section {section}")

            # Reset edit mode
            st.session_state.edit_item_index = None
            st.session_state.original_item_uuid = None

    # Display the form to add a new item if "Ajouter l'item" was clicked
    elif st.session_state.show_new_item_form:
        new_entry_index = len(st.session_state.item_entries)
        section, code, name, quantity = display_item_fields(new_entry_index)

        # Add the new item only if all fields are filled
        if st.button("Confirmer l'ajout de l'item", key="confirm_add"):
            if code and name and quantity:
                # Generate a unique UUID and assign item number from counter
                new_uuid = str(uuid.uuid4())
                
                new_item = {
                    'uuid': new_uuid,
                    'item_number': st.session_state.item_counter,  # Assign the current item counter as item number
                    'section': section,
                    'item_code': code,
                    'item_name': name,
                    'item_quantity': quantity
                }
                
                # Add to item entries and bom_sections
                st.session_state.item_entries.append(new_item)
                if section not in st.session_state.bom_sections:
                    st.session_state.bom_sections[section] = []
                
                # Append to the BOM section
                st.session_state.bom_sections[section].append(new_item)
                
                # Increment the item counter for the next item
                st.session_state.item_counter += 1
                
                st.success(f"Item {new_item['item_number']} ajouté à la section {section}")

                # Hide new item form after addition
                st.session_state.show_new_item_form = False
            else:
                st.error("Veuillez remplir tous les champs pour ajouter un item.")

# Run the function to display the page
page_2()
