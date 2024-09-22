import re
import requests
from bs4 import BeautifulSoup
import json
import time
from cache import Cache
from notifications import notify

class Scraper:
    def __init__(self):
        self.cache = Cache()

    async def scrape_products(self, limit, proxy):
        scraped_data = []
        for page in range(1, limit + 1):
            url = f"https://dentalstall.com/shop/page/{page}/" if page>1 else "https://dentalstall.com/shop/"
            response = self.fetch_page(url, proxy)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                products = self.extract_products(soup)
                scraped_data.extend(products)

        self.save_to_file(scraped_data)
        notify(len(scraped_data))
        return len(scraped_data)

    def fetch_page(self, url, proxy):
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            print(e)
            time.sleep(5)  # Retry delay
            return self.fetch_page(url, proxy)

    def extract_products(self, soup):
        products = []
        for item in soup.select('.product'):
            title_element = item.select_one('.woo-loop-product__title')
            price_element = item.select_one('.price')
            image_element = item.select_one('img')

            # Check if each element exists before accessing their properties


            # Improved price extraction logic
            if price_element:
                price_text = price_element.text.strip()
                # Find all price values (assuming they are formatted as '₹xxx.xx')
                price_values = re.findall(r'₹[\d,]+\.\d{2}', price_text)
                # Take the first price if available, else default to 0.0
                price = float(price_values[0].replace('₹', '').replace(',', '')) if price_values else 0.0
            else:
                price = 0.0

            image = image_element['src'] if image_element else "N/A"

            products.append({"product_title": title_element.text, "product_price": price, "path_to_image": image})

        return products

    def save_to_file(self, data):
        with open('products.json', 'w') as f:
            json.dump(data, f)
