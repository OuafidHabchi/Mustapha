import streamlit as st

def page_1():
    # CSS to adjust the button size
    st.markdown("""
        <style>
        .stButton > button {
            padding: 6px 10px;  /* Adjust padding for desired size */
            font-size: 14px;    /* Adjust font size */
            border-radius: 6px; /* Add some rounded borders for style */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Product Informations")

    # Input for basic information
    product_name = st.text_input("Product Name", value=st.session_state.product_info.get("product_name", ""))
    product_code = st.text_input("Product Code", value=st.session_state.product_info.get("product_code", ""))
    batch_size = st.text_input("Batch Size", value=st.session_state.product_info.get("batch_size", ""))
    
    # Unit selection
    unit = st.selectbox(
        "Unit",
        options=["kg", "g", "tablet", "capsule"],
        index=0  # Default option
    )

    if st.button("Save"):
        if product_name and product_code and batch_size:
            st.session_state.product_info = {
                "product_name": product_name,
                "product_code": product_code,
                "batch_size": batch_size,
                "unit": unit  # Save the selected unit
            }
            st.success("Basic information saved.")
        else:
            st.error("Please fill in all fields.")
