import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
BASE_URL = "https://culture-bonus-merchant-gateway.bonoculturajoven.gob.es/merchant-api/map/v1/salespoints/online"
TOTAL_PAGES = 29
PAGE_SIZE = 10

# Diccionario para traducir las categorías de la API a un formato legible
CATEGORY_MAP = {
    "LIVE_ARTS": "Artes en vivo, patrimonio cultural y artes audiovisuales",
    "PHYSICAL_SUPPORT": "Productos culturales en soporte físico",
    "DIGITAL_SUPPORT": "Consumo digital o online"
}

# --- SCRIPT ---
all_establishments = []
print("Iniciando scraping...")

for page_num in range(TOTAL_PAGES):
    params = {'page': page_num, 'pageSize': PAGE_SIZE}
    print(f"Obteniendo datos de la página {page_num + 1}/{TOTAL_PAGES}...")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        establishments_on_page = data.get('content', [])

        if not establishments_on_page:
            print("No se encontraron más establecimientos. Terminando.")
            break

        for item in establishments_on_page:
            # Extrae las subcategorías como un string (ej: "LIVE_ARTS,PHYSICAL_SUPPORT")
            subcat_string = item.get('subCategories', '')
            
            # Divide el string por la coma para obtener una lista (ej: ["LIVE_ARTS", "PHYSICAL_SUPPORT"])
            subcat_list = subcat_string.split(',')
            
            # Traduce cada categoría usando el diccionario y las une de nuevo
            translated_cats = [CATEGORY_MAP.get(cat, cat) for cat in subcat_list]
            types_str = ', '.join(translated_cats)

            all_establishments.append({
                'nombre': item.get('name'),
                'web': item.get('webAddress'), # <-- Clave corregida
                'tipos': types_str             # <-- Lógica corregida
            })

        time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        break

print(f"\nScraping finalizado. Se encontraron {len(all_establishments)} establecimientos.")

if all_establishments:
    df = pd.DataFrame(all_establishments)
    df.to_csv('establecimientos_bono_cultural.csv', index=False, encoding='utf-8-sig')
    print("Los datos se han guardado en 'establecimientos_bono_cultural.csv'")
else:
    print("No se extrajeron datos.")
