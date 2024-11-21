import streamlit as st

def page_2():
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;
            font-size: 14px;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Number of Items")

    # Input for the number of items
    item_count = st.number_input("How many items do you want to use?", min_value=1, step=1)

    if st.button("Confirm"):
        st.session_state.bom_items_count = item_count
        # Automatically generate items from 1 to item_count
        st.session_state.bom_items = [f"Item {i}" for i in range(1, item_count + 1)]
        st.success("Number of items saved.")
