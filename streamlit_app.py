import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

# Function to get People Also Ask questions and Related Searches
@st.cache(allow_output_mutation=True)
def get_related_info(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
    
    try:
        base_url = "https://www.google.com/search?q="
        search_url = base_url + query
        driver.get(search_url)
        
        # Extract People Also Ask questions
        people_also_asked = driver.find_elements_by_css_selector('.cbphWd')
        people_also_asked_questions = [question.text for question in people_also_asked]
        
        # Extract Related Searches
        related_searches = driver.find_elements_by_css_selector('.w6PXbb')
        related_search_keywords = [related_search.text for related_search in related_searches]
        
        return people_also_asked_questions, related_search_keywords
        
    finally:
        driver.quit()

# Main function
def main():
    st.title("People Also Ask & Related Search Keyword Tool")
    
    query = st.text_input("Enter the search query:", key="search_query", placeholder="Keyword research...")
    
    # Button to trigger code execution
    if st.button("🔍 Find keywords"):
        with st.spinner("Fetching data..."):
            try:
                people_also_asked_questions, related_search_keywords = get_related_info(query)
                
                st.markdown(f"**People Also Ask Keywords for '{query}' query**")
                for question in people_also_asked_questions:
                    st.write(question)
                    
                st.markdown(f"**Related Searches Keywords for '{query}' query**")
                for keyword in related_search_keywords:
                    st.write(keyword)
                
            except Exception as e:
                st.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
