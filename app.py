from flask import Flask, request, jsonify, send_from_directory
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import tempfile
import os

app = Flask(__name__)

# Function to create the Selenium WebDriver
def create_driver():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')  # Serve the HTML file

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        driver = create_driver()
        driver.get(url)
        
        # Example logic to extract product data
        products = []
        product_elements = driver.find_elements_by_css_selector('.product-class')  # Replace with actual CSS selector
        
        for product in product_elements:
            title = product.find_element_by_css_selector('.title-class').text  # Replace with actual CSS selector
            product_url = product.find_element_by_css_selector('a').get_attribute('href')
            products.append({"title": title, "url": product_url})
        
        driver.quit()
        return jsonify({"products": products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        temp_dirs = [f.path for f in os.scandir(tempfile.gettempdir()) if f.is_dir()]
        for temp_dir in temp_dirs:
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
