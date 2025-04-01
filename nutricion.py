import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar en segundo plano
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def buscar_producto_fatsecret(producto):
    url_busqueda = "https://www.fatsecret.es/calorías-nutrición/search?q="
    driver.get(url_busqueda + producto.replace(" ", "+"))
    time.sleep(2)

    try:
        primer_resultado = driver.find_element(By.CSS_SELECTOR, "a.prominent")
        return primer_resultado.get_attribute("href")
    except:
        return None


def extraer_info_nutricional(url_producto):
    driver.get(url_producto)
    time.sleep(2)

    info_nutricional = {}

    try:
        tabla_nutricional = driver.find_element(By.CLASS_NAME, "nutrition_facts")
        elementos = tabla_nutricional.find_elements(By.CLASS_NAME, "nutrient")

        clave_actual = None

        for elem in elementos:
            texto = elem.text.strip()

            if texto and not re.search(r'%$', texto):  # Ignorar los % IR
                if re.search(r'\d', texto):  # Contiene un número, es el valor
                    info_nutricional[clave_actual] = re.sub(r'[^0-9.,]', '', texto)  # Solo número
                else:  # Es el nombre del nutriente
                    clave_actual = texto

    except Exception as e:
        print(f"Error extrayendo datos: {e}")
        return None

    return info_nutricional


# Leer CSV
csv_path = "MercadonaLimpiado3_test.csv"
df = pd.read_csv(csv_path)

# Definir columnas nutricionales
columnas_nutricionales = {
    "Energía (kcal)": "Energía",
    "Grasa (g)": "Grasa",
    "Grasa Saturada (g)": "Grasa Saturada",
    "Carbohidratos (g)": "Carbohidratos",
    "Azúcar (g)": "Azúcar",
    "Proteína (g)": "Proteína",
    "Sal (g)": "Sal"
}

# Asegurar que el DataFrame tiene estas columnas
for col in columnas_nutricionales:
    if col not in df.columns:
        df[col] = None

# Procesar los primeros 3 productos
for i, fila in df.head(3).iterrows():
    producto = fila["display_name"]
    print(f"\n🔍 Buscando: {producto}")

    url_producto = buscar_producto_fatsecret(producto)
    if url_producto:
        info_nutricional = extraer_info_nutricional(url_producto)
        if info_nutricional:
            print("✅ Datos nutricionales encontrados:")
            for clave, valor in info_nutricional.items():
                print(f"   {clave}: {valor}")
                for col, nombre in columnas_nutricionales.items():
                    if clave.startswith(nombre):  # Coincidencia parcial para evitar errores
                        df.at[i, col] = valor
        else:
            print("⚠ No se encontraron datos nutricionales.")
    else:
        print("❌ Producto no encontrado en FatSecret.")

    time.sleep(3)

# Guardar resultados
output_path = "MercadonaLimpiado3_test_actualizado.csv"
df.to_csv(output_path, index=False)
print(f"✅ Datos guardados en {output_path}")

# Cerrar Selenium
driver.quit()