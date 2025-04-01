import re
from fatsecret import Fatsecret

# Claves de API
consumer_key = "323d77a2801c4cb290c67c207a28f3a5"
consumer_secret = "4446f6b14ac544aab3acdc7776df7d8a"
fs = Fatsecret(consumer_key, consumer_secret)


def extraer_nutrientes(descripcion):
    """ Extrae calorías, grasa, carbohidratos y proteínas de la descripción nutricional """
    match = re.search(r'Calories: (\d+)kcal \| Fat: ([\d\.]+)g \| Carbs: ([\d\.]+)g \| Protein: ([\d\.]+)g',
                      descripcion)
    if match:
        return {
            "calorias": float(match.group(1)),
            "grasas": float(match.group(2)),
            "carbohidratos": float(match.group(3)),
            "proteinas": float(match.group(4)),
        }
    return None


def buscar_producto(nombre_producto):
    """ Busca el producto en la API de FatSecret y lo procesa """
    productos = fs.foods_search(nombre_producto, max_results=10)

    productos_procesados = []
    for producto in productos:
        nutrientes = extraer_nutrientes(producto['food_description'])
        if nutrientes:
            producto["nutrientes"] = nutrientes
            productos_procesados.append(producto)

    if not productos_procesados:
        print("No se encontraron productos con ese nombre.")
        return

    # Definir mejor producto (criterio: más proteínas, menos calorías, menos grasa)
    def puntaje(producto):
        n = producto["nutrientes"]
        return (n["proteinas"] * 2) - (n["calorias"] * 0.5) - (n["grasas"] * 5)

    # Ordenar productos por puntaje
    top_productos = sorted(productos_procesados, key=puntaje, reverse=True)[:3]

    # Mostrar resultados en consola
    print("\nLos tres mejores productos en términos nutricionales son:")
    for i, producto in enumerate(top_productos, start=1):
        print(f"{i}. {producto['food_name']} ({producto.get('brand_name', 'Genérico')})")
        print(producto['food_description'])
        print(producto['food_url'])
        print("-")


if __name__ == "__main__":
    nombre_producto = input("Ingrese el nombre del producto a buscar: ")
    buscar_producto(nombre_producto)
