import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time

# Function to get the TradingView webpage source
@st.cache(allow_output_mutation=True)
def get_tradingview_source(auth_token):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), 
        options=options
    )
    
    try:
        # Set the TradingView URL
        tradingview_url = "https://in.tradingview.com"
        driver.get(tradingview_url)

        # Set cookies for authentication
        driver.add_cookie({'name': 'auth_token', 'value': auth_token})
        driver.refresh()  # Refresh to apply cookies

        # Wait for the page to load
        time.sleep(5)

        # Navigate to the specific chart URL
        chart_url = "https://in.tradingview.com/chart/WvmaGoMa/?symbol=NSE%3Asbin"
        driver.get(chart_url)

        # Wait for the chart to load
        time.sleep(5)

        # Get the page source
        page_source = driver.page_source
        return page_source
        
    finally:
        driver.quit()

# Main function
def main():
    st.title("TradingView Webpage Source Fetcher")
    
    auth_token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'
    
    # Button to trigger code execution
    if st.button("🔍 Fetch TradingView Page Source"):
        with st.spinner("Fetching data..."):
            try:
                page_source = get_tradingview_source(auth_token)
                st.code(page_source)
            except Exception as e:
                st.error(f"An error occurred during the process: {e}")

if __name__ == "__main__":
    main()
