import requests
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import pandas as pd


def construct_search_url(base_url, search_query):
    # URL encode the search query
    encoded_query = quote(search_query)

    # Construct the search URL
    search_url = f"{base_url}/{encoded_query}?_q={encoded_query}&map=ft"

    return search_url

def scrape_walmart_category(url):
    # Enviar una solicitud a la página web
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al recuperar la página web. Código de estado: {response.status_code}")
        return

    # Parsear el contenido de la página web
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todos los contenedores de productos
    product_containers = soup.find_all('div', class_="vtex-search-result-3-x-galleryItem")
    print(len(product_containers))
    # Extraer nombres y precios de productos
    data = []
    for container in product_containers:
        print(container)
        # Encontrar el nombre del producto en el span con la clase especificada
        name_tag = container.find('span', class_='vtex-product-summary-2-x-brandName')
        if name_tag:
            name = name_tag.text.strip()

        # Encontrar el precio del producto
        price_container = container.find('span', class_='vtex-store-components-3-x-currencyContainer vtex-store-components-3-x-currencyContainer--summary')
        if price_container:
            price_tag = price_container.find('span')
            if price_tag:
                price = price_tag.text.strip()

        # Verificar que ambos nombre y precio fueron encontrados
        if name and price:
            data.append({'Nombre': name, 'Precio': price})

    # Crear un DataFrame
    df = pd.DataFrame(data)
    return df


    return df



# Base URL of the Walmart Guatemala website
base_url = 'https://www.walmart.com.gt'
# Item to search for
item_name = 'sin gluten'
# Get the URL for the search results page
search_results_url = construct_search_url(base_url, item_name)
print(search_results_url)

# Extraer datos y guardarlos en un DataFrame
df = scrape_walmart_category(search_results_url)
print(df)

