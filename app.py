from flask import Flask, render_template, request, jsonify
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape_url(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "products")))
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        products = []
        product_elements = driver.find_elements(By.CLASS_NAME, "product")
        
        for product in product_elements:
            try:
                # Look for the title within the current product element
                title_element = product.find_element(By.CLASS_NAME, "woocommerce-loop-product__title")
                title = title_element.text.lower()
                url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                products.append({"title": title, "url": url})
            except Exception as e:
                print(f"Error processing product: {e}")
        return products
    finally:
        driver.quit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    try:
        products = scrape_url(url)
        return jsonify({"products": products})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)