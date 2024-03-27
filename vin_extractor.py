import requests
import pandas as pd
import streamlit as st

# Function to make API calls and collect VIN numbers
def get_vin_numbers():
    start = 0
    vin_numbers = []

    while True:
        url = f"https://www.garberbuick.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?start={start}"
        response = requests.get(url)
        
        # Break the loop if the response is not successful or empty
        if not response.ok or not response.json():
            break
        
        data = response.json()

        # Extract VIN numbers from the response
        for item in data.get('inventory', []):
            vin = item.get('vin')
            if vin:
                vin_numbers.append(vin)
        
        start += 18  # Assuming each response contains 18 items

    return vin_numbers

# Streamlit app
def main():
    st.title('VIN Number Extractor')

    if st.button('Fetch VIN Numbers'):
        vin_numbers = get_vin_numbers()
        if vin_numbers:
            st.success(f"Found {len(vin_numbers)} VIN numbers.")
            # Convert to DataFrame for easy CSV download
            df = pd.DataFrame(vin_numbers, columns=['VIN Numbers'])
            st.write(df)

            # Download link
            st.download_button(label='Download VIN numbers as CSV', data=df.to_csv(index=False), file_name='vin_numbers.csv', mime='text/csv')
        else:
            st.error("No VIN numbers found.")

if __name__ == "__main__":
    main()
