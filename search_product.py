import pandas as pd
import webbrowser
import urllib.parse

# --- CONSTANTES ---
CSV_FILE = 'establecimientos_bono_cultural.csv'

# Mapeo de categorías para la lógica interna y el menú de usuario
CATEGORY_MAP = {'físico': 'Productos culturales en soporte físico', 'digital': 'Consumo digital o online', 'vivo': 'Artes en vivo, patrimonio cultural y artes audiovisuales'}
CATEGORY_MENU = {'físico': 'Libros, vinilos, CDs, cómics...', 'digital': 'E-books, videojuegos, suscripciones...', 'vivo': 'Entradas de conciertos, teatro, cine...'}

# Mapeo de buscadores con sus límites específicos
SEARCH_ENGINES = {
    'google': {'name': 'Google', 'url': 'https://www.google.com/search?q=', 'url_limit': 2048},
    'kagi': {'name': 'Kagi', 'url': 'https://kagi.com/search?q=', 'query_char_limit': 1024, 'query_word_limit': 32, 'note': 'eficiente, puede abrir múltiples pestañas'},
    'duckduckgo': {'name': 'DuckDuckGo', 'url': 'https://duckduckgo.com/?q=', 'url_limit': 2048},
    'brave': {'name': 'Brave Search', 'url': 'https://search.brave.com/search?q=', 'url_limit': 2048}
}

# --- SCRIPT PRINCIPAL ---
def main():
    print("--- Búsqueda de Productos en Tiendas del Bono Cultural ---")

    # 1. Input de producto
    product_to_search = input("¿Qué producto quieres buscar?: ")
    if not product_to_search: exit("Error: Debes introducir un nombre de producto.")

    # 2. Selección de categoría mediante un menú numerado
    print("\nElige una categoría para tu producto:")
    category_options = list(CATEGORY_MENU.keys())
    for i, key in enumerate(category_options, 1):
        print(f"  {i}. {key.capitalize():<8} ({CATEGORY_MENU[key]})")
    try:
        choice_num = int(input(f"Introduce el número de la categoría (1-{len(category_options)}): "))
        category_input = category_options[choice_num - 1]
    except (ValueError, IndexError):
        exit("\nError: Selección de categoría no válida.")
    target_category = CATEGORY_MAP[category_input]

    # 3. Selección del motor de búsqueda mediante un menú numerado
    print("\nElige un motor de búsqueda:")
    engine_options = list(SEARCH_ENGINES.keys())
    for i, key in enumerate(engine_options, 1):
        engine = SEARCH_ENGINES[key]
        note = f" ({engine['note']})" if 'note' in engine else ""
        print(f"  {i}. {engine['name']}{note}")
    try:
        choice_str = input(f"Introduce tu elección (deja en blanco para '{SEARCH_ENGINES[engine_options[0]]['name']}'): ")
        engine_choice = engine_options[int(choice_str) - 1] if choice_str else engine_options[0]
    except (ValueError, IndexError):
        exit("\nError: Selección de buscador no válida.")

    chosen_engine = SEARCH_ENGINES[engine_choice]
    base_search_url = chosen_engine['url']

    # 4. Carga y filtrado de datos
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        exit(f"\nError: No se encontró '{CSV_FILE}'. Asegúrate de que está en la misma carpeta.")
    
    filtered_df = df[df['tipos'].str.contains(target_category, na=False)].dropna(subset=['web'])
    if filtered_df.empty:
        exit(f"\nNo se encontraron tiendas para la categoría '{target_category}'.")

    final_urls = []
    sites_searched_count = 0

    # 5. Lógica de construcción de URLs
    if engine_choice == 'kagi':
        # --- WORKAROUND EFICIENTE PARA KAGI ---
        base_query_part = f'"{product_to_search}"'
        all_batches, current_batch = [], []
        
        for url in filtered_df['web']:
            temp_batch = current_batch + [url]
            sites_part = " OR ".join([f"site:{s.strip()}" for s in temp_batch])
            temp_query_chars = len(base_query_part) + len(sites_part) + 1
            temp_query_words = len(base_query_part.split()) + sum([2 if i==0 else 3 for i in range(len(temp_batch))])

            if temp_query_chars > chosen_engine['query_char_limit'] or temp_query_words > chosen_engine['query_word_limit']:
                if current_batch: all_batches.append(current_batch)
                current_batch = [url]
            else:
                current_batch = temp_batch
                
        if current_batch: all_batches.append(current_batch)

        for batch in all_batches:
            sites_part = " OR ".join([f"site:{s.strip()}" for s in batch])
            final_urls.append(base_search_url + urllib.parse.quote_plus(f'{base_query_part} {sites_part}'))
        sites_searched_count = len(filtered_df)

    else:
        # --- LÓGICA ESTÁNDAR PARA OTROS BUSCADORES ---
        base_query = f'"{product_to_search}"'
        current_query = base_query
        url_limit = chosen_engine['url_limit']
        for url in filtered_df['web']:
            site_component = f" site:{url.strip()}"
            potential_addition = f" OR{site_component}" if sites_searched_count > 0 else site_component
            if len(base_search_url + urllib.parse.quote_plus(current_query + potential_addition)) > url_limit:
                break
            current_query += potential_addition
            sites_searched_count += 1
        final_urls.append(base_search_url + urllib.parse.quote_plus(current_query))

    # 6. Resumen y ejecución
    print("\n" + "="*60)
    print(f"Buscando '{product_to_search}'...")
    if engine_choice == 'kagi':
        print(f"Se abrirán {len(final_urls)} pestañas en Kagi para buscar en {sites_searched_count} tiendas.")
    else:
        print(f"Se buscará en {sites_searched_count} de {len(filtered_df)} tiendas encontradas en una sola pestaña.")
    print(f"Abriendo resultados en {chosen_engine['name']}...")
    print("="*60)

    for i, url in enumerate(final_urls):
        webbrowser.open(url, new=(1 if i > 0 else 0))

if __name__ == "__main__":
    main()
