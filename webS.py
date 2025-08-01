from flask import Flask, request, jsonify, render_template, session
import os
from google.cloud import vision
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')

# Set Google credentials
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_creds.json"  # adjust this to your creds file name

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Supported e-commerce XPaths
ECOMMERCE_SITES = {
    'www.amazon.in': '//span[@class="a-price-whole"]',
    'www.myntra.com': '//span[@class="pdp-product-price"]',
    'www.flipkart.com': '//div[contains(@class, "_30jeq3") and contains(@class, "_16Jk6d")]',
    'www.croma.com': '//span[@class="amount"]',
    'www.tatacliq.com': '//span[@class="salePrice"]',
    'www.ajio.com': '//span[@class="prod-sp"]'
}

# Selenium WebDriver Manager
class WebDriverManager:
    def __init__(self):
        self.driver = None

    def get_driver(self):
        if not self.driver:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=options)
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

web_driver_manager = WebDriverManager()

def scrape_price(url, xpath):
    driver = web_driver_manager.get_driver()
    try:
        driver.get(url)
        price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return price_element.text.strip()
    except Exception as e:
        return f"Error: {e}"

def scrape_flipkart_price(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        class_names = ["_1vC4OE _3qQ9m1", "_3auQ3N _1POkHg", "_30jeq3 _16Jk6d", "_3qQ9m1", "Nx9bqj CxhGGd", "yRaY8j A6+E6v"]
        for class_name in class_names:
            price_element = soup.find('div', class_=class_name)
            if price_element:
                return price_element.text.strip()
    except:
        pass
    return "Price not found"

def extract_domain(url):
    return urlparse(url).netloc

def detect_web(image_bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.web_detection(image=image)
    annotations = response.web_detection

    results = {'urls_with_prices': []}

    if annotations.pages_with_matching_images:
        for page in annotations.pages_with_matching_images:
            domain = extract_domain(page.url)
            if domain in ECOMMERCE_SITES:
                xpath = ECOMMERCE_SITES[domain]
                price = scrape_flipkart_price(page.url) if domain == 'www.flipkart.com' else scrape_price(page.url, xpath)
                results['urls_with_prices'].append({'url': page.url, 'price': price})

    if response.error.message:
        raise Exception(response.error.message)

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        image_bytes = file.read()
        results = detect_web(image_bytes)
        session['results'] = results
        return jsonify({'signal': 'search_complete'}), 200
    except Exception as e:
        return jsonify({'signal': 'processing_error', 'error': str(e)}), 500

@app.route('/compare.html', methods=['GET'])
def compare():
    results = session.get('results')
    if not results:
        return "No data found", 404
    urls = [item['url'] for item in results['urls_with_prices']]
    prices = [item['price'] for item in results['urls_with_prices']]
    return render_template('compare.html', urls=urls, prices=prices)

@app.teardown_appcontext
def cleanup_driver(exception=None):
    web_driver_manager.close_driver()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
