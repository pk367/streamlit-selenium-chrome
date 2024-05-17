import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup

@st.cache(allow_output_mutation=True)
def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    return webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

def scrape_google_results(query):
    driver = get_driver()
    driver.get(f"https://www.google.com/search?q={query}")

    # Extracting People Also Ask
    people_also_asked = []
    people_also_asked_section = driver.find_elements_by_css_selector(".ifM9O > div > g-expandable-content > div > div > div > div > div")
    for item in people_also_asked_section:
        people_also_asked.append(item.text)

    # Extracting Related Searches
    related_searches = []
    related_searches_section = driver.find_elements_by_css_selector("#bres > div:nth-child(3) > div > div > div > div.y6Uyqe > a")
    for item in related_searches_section:
        related_searches.append(item.text)

    driver.quit()
    return people_also_asked, related_searches

def main():
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" alt="Google People Also Ask Related Search Keyword Tool">
            <p> </p>
            <p> </p>
            <h5>People Also Ask & Related Search Keyword Tool</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

    query = st.text_input("Enter the search query:", key="search_query", placeholder="Keyword research...")
    num_iterations = st.number_input("Number of searches for each Related keyword:", min_value=1, value=1)

    if st.button(" 🔍 Find keywords"):
        with st.spinner("Fetching data..."):
            try:
                people_also_asked, related_searches = scrape_google_results(query)

                tab1, tab2 = st.columns(2)
                with tab1:
                    st.markdown(f"**People Also Asked Keywords for {query} query**")
                    for question in people_also_asked:
                        st.write(question)

                with tab2:
                    st.markdown(f"**Related Searches Keywords for {query} query**")
                    for search in related_searches:
                        st.write(search)

                    # Perform iterations for each related search keyword
                    for keyword in related_searches:
                        for i in range(num_iterations):
                            st.write(f"Iteration {i+1} for {keyword}:")
                            people_also_asked, related_searches = scrape_google_results(keyword)
                            st.write("People Also Ask:")
                            for question in people_also_asked:
                                st.write(question)
                            st.write("Related Searches:")
                            for search in related_searches:
                                st.write(search)
            except Exception as e:
                st.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
