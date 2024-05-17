import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

@st.cache(allow_output_mutation=True)
def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )

# Function to get related searches using WebDriver
@st.cache
def get_related_searches(query):
    base_url = "https://www.google.com/search?q=" + query

    try:
        # Initialize WebDriver
        driver = get_driver()
        driver.get(base_url)

        # Wait for the page to load
        time.sleep(2)  # You may need to adjust this wait time

        # Extract related searches using Selenium
        related_searches_elements = driver.find_elements_by_css_selector('.brs_col > p > a')
        related_searches = [element.text for element in related_searches_elements]

        # Extract People Also Ask questions
        people_also_asked_elements = driver.find_elements_by_css_selector('.related-question-pair')
        people_also_asked = [element.text for element in people_also_asked_elements]

        return related_searches, people_also_asked

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Function to print 'People Also Asked' questions
def print_people_also_asked(people_also_asked):
    if people_also_asked:
        for question in people_also_asked:
            st.write(question)

# Function to visualize keyword iteration as a hierarchy
def visualize_hierarchy(iteration, keyword, related_searches):
    expander_title = f"Iteration {iteration + 1}: {keyword}"
    with st.expander(expander_title, expanded=True):
        if related_searches:
            for search in related_searches:
                st.write(f"- {search}")

# Main function
def main():
    # Display the Google logo centered
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
    num_iterations = st.number_input("Number of search for each Related keyword:", min_value=1, value=1)

    # Button to trigger code execution
    if st.button("🔍 Find keywords"):
        with st.spinner("Fetching data..."):
            try:
                # Get initial related searches
                initial_related_searches, initial_people_also_asked = get_related_searches(query)

                tab1, tab2 = st.columns([1, 1])
                with tab1:
                    st.markdown(f"**People Also Asked Keywords for '{query}' query**")
                    try:
                        print_people_also_asked(initial_people_also_asked)
                    except Exception as e:
                        st.error(f"Error fetching 'People Also Asked' questions: {e}")

                with tab2:
                    st.markdown(f"**Related Searches Keywords for '{query}' query**")
                    if initial_related_searches:
                        for search in initial_related_searches:
                            # Perform iterations for each keyword
                            keywords_to_iterate = initial_related_searches  # Initialize with initial related searches
                            for i in range(num_iterations):
                                new_keywords_to_iterate = []  # Store new keywords extracted in this iteration
                                for keyword in keywords_to_iterate:
                                    with st.spinner(f"Fetching data for '{keyword}'..."):
                                        related_searches, _ = get_related_searches(keyword)
                                    visualize_hierarchy(i, keyword, related_searches)
                                    if related_searches:
                                        new_keywords_to_iterate.extend(related_searches)  # Add newly extracted keywords
                                keywords_to_iterate = new_keywords_to_iterate  # Update keywords for next iteration
            except Exception as e:
                st.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
