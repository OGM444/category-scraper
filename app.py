from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import tempfile
import os

app = Flask(__name__)

# Function to create the Selenium WebDriver
def create_driver():
    chromedriver_autoinstaller.install()  # Ensures the appropriate ChromeDriver version is installed
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Create a unique temporary directory for user data
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    
    service = Service()  # No need to specify path, chromedriver-autoinstaller handles it
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route('/')
def home():
    return "The app is running!"

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        driver = create_driver()
        driver.get(url)
        
        # Example logic to extract product data (modify as per your requirements)
        products = []
        product_elements = driver.find_elements_by_css_selector('.product-class')  # Replace with actual CSS selector
        
        for product in product_elements:
            title = product.find_element_by_css_selector('.title-class').text  # Replace with actual CSS selector
            product_url = product.find_element_by_css_selector('a').get_attribute('href')  # Replace with actual selector
            products.append({"title": title, "url": product_url})
        
        driver.quit()  # Close the driver
        return jsonify({"products": products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure all temp directories are cleaned up
        temp_dirs = [f.path for f in os.scandir(tempfile.gettempdir()) if f.is_dir()]
        for temp_dir in temp_dirs:
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass

if __name__ == '__main__':
    # Production-ready run configuration
    app.run(host='0.0.0.0', port=5000, debug=False)
