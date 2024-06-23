import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

base_url = 'https://www.jumia.com.ng/mlp-samsung-galaxy-s24/'

def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', {'class': 'prd _fb col c-prd'})
    
    products = []
    for data in articles:
        try:
            head = data.find('a', {'class': 'core'})
            f_head = head.text.strip() if head else 'N/A'
        
            price = data.find('div', {'class': 'prc'})
            f_price = price.text.strip() if price else 'N/A'

            link_tag = data.find('a', {'class': 'core'})
            f_link = link_tag['href'] if link_tag else 'N/A'
            f_link = urljoin(base_url, f_link)
            
            rating = data.find('div', {'class': 'stars'})
            f_rating = rating.get('data-score') if rating else 'N/A'
            
            image = data.find('img', {'class': 'img'})
            f_image = image.get('data-src') if image else 'N/A'
            
            product = {
                'Title': f_head,
                'Price': f_price,
                'Link': f_link,
                'Rating': f_rating,
                'Image': f_image
            }
            
            products.append(product)
            
            print(f"Scraped product: {f_head} | Price: {f_price} | Rating: {f_rating}")
        
        except Exception as e:
            print(f"An error occurred while processing a product: {e}")
    
    return products

def scrape_multiple_pages(base_url, num_pages=6):
    all_products = []
    
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}?page={page_number}#catalog-listing"
        products = scrape_page(url)
        all_products.extend(products)
        time.sleep(1) 
    
    return all_products

products = scrape_multiple_pages(base_url, num_pages=10)

df = pd.DataFrame(products)
df
df.to_csv('samsung.csv')
df.to_excel('samsung.xlsx')