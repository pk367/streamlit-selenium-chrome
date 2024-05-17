import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Function to get the webpage source
@st.cache(allow_output_mutation=True)
def get_webpage_source(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), 
        options=options
    )
    
    try:
        base_url = "https://www.google.com/search?q="
        search_url = base_url + query
        driver.get(search_url)
        
        # Get the page source
        page_source = driver.page_source
        return page_source
        
    finally:
        driver.quit()

# Main function
def main():
    st.title("Google Search Webpage Source Fetcher")
    
    query = st.text_input("Enter the search query:", key="search_query", placeholder="Keyword research...")
    
    # Button to trigger code execution
    if st.button("🔍 Fetch Page Source"):
        with st.spinner("Fetching data..."):
            try:
                page_source = get_webpage_source(query)
                st.code(page_source)
            except Exception as e:
                st.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
