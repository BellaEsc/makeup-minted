import streamlit as st
import pandas as pd

# Define blush pink and peach colors
blush_pink = "#E2808F"
deep_blush = "#B56A6D"
light_beige = "#F5e2d0"

# Load the CSV file
df = pd.read_csv('/Users/christinanassar/makeup-minted-2/data/skincare_products_1.csv')

# Function to display product information
def display_product_info(product_name):
    product_row = df[df['Name'] == product_name]
    if not product_row.empty:
        product_info = product_row.iloc[0]
        
        # Style for product information box
        product_info_style = (
            f"background-color: {blush_pink};"
            "padding: 20px;"
            "border-radius: 10px;"
            "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
            "margin-bottom: 20px;"
        )

        # Display product information within styled box
        st.markdown(
            f"<div style='{product_info_style}'>"
            "<h2>Product Information</h2>"
            f"<p><strong>Label:</strong> {product_info['Label']}</p>"
            f"<p><strong>Brand:</strong> {product_info['Brand']}</p>"
            f"<p><strong>Name:</strong> {product_info['Name']}</p>"
            f"<p><strong>Price:</strong> {product_info['Price']}</p>"
            f"<p><strong>Rank:</strong> {product_info['Rank']}</p>"
            f"<p><strong>Skin Type:</strong> {', '.join([type for type, value in product_info[['Combination', 'Dry', 'Normal', 'Oily']].items() if value == 1])}</p>"
            f"<p><strong>INCI Name:</strong> {product_info['INCI Name']}</p>"
            "</div>",
            unsafe_allow_html=True
        )

        # Display the list of similar products
        weighted_similarity = product_info['Weighted Similarity Products']
        similar_products = weighted_similarity.strip("[]").replace("'", "").split(", ")
        
        # Style for weighted similarity products box
        weighted_similarity_style = (
            f"background-color: {deep_blush};"  # Use peach color
            "padding: 20px;"
            "border-radius: 10px;"
            "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
            "margin-bottom: 20px;"
        )

        # Display weighted similarity products in a separate box
        st.markdown(
            f"<div style='{weighted_similarity_style}'>"
            "<h2>Similar Products</h2>"
            "<ul>"
            + "".join([f"<li><button onclick='set_value(\"{product}\")' style='background-color: {light_beige}; border-radius: 5px; padding: 5px 10px; margin: 5px; cursor: pointer;'>{product}</button></li>" for product in similar_products]) +
            "</ul>"
            "</div>",
            unsafe_allow_html=True
        )

    else:
        st.warning("Product not found.")

# Define the Streamlit app
def main():
    # Center-aligned title using markdown syntax
    st.markdown("<h1 style='text-align: center; color: black; padding: 20px; background-color:{}; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>Makeup Minted</h1>".format(deep_blush), unsafe_allow_html=True)

    # User input for product name
    product_name = st.text_input('Enter the name of the product:')
    
    if st.button('Search'):
        display_product_info(product_name)

if __name__ == "__main__":
    main()

