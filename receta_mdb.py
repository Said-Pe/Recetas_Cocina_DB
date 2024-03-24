from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['recetas_db']
collection = db['recipes']

def add_recipe():
    name = input("Nombre de la receta: ")
    ingredients = input("Ingredientes (separados por comas): ")
    steps = input("Pasos de la receta: ")

    recipe = {
        "name": name,
        "ingredients": ingredients.split(','),
        "steps": steps
    }

    collection.insert_one(recipe)
    print("Receta agregada exitosamente.")

def update_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea actualizar: ")
    recipe = collection.find_one({"_id": recipe_id})
    if recipe:
        name = input("Nuevo nombre de la receta: ")
        ingredients = input("Nuevos ingredientes (separados por comas): ")
        steps = input("Nuevos pasos de la receta: ")

        updated_recipe = {
            "name": name,
            "ingredients": ingredients.split(','),
            "steps": steps
        }

        collection.update_one({"_id": recipe_id}, {"$set": updated_recipe})
        print("Receta actualizada exitosamente.")
    else:
        print("No se encontró ninguna receta con ese ID.")

def delete_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea eliminar: ")
    result = collection.delete_one({"_id": recipe_id})
    if result.deleted_count > 0:
        print("Receta eliminada exitosamente.")
    else:
        print("No se encontró ninguna receta con ese ID.")

def view_recipes():
    recipes = collection.find()
    for recipe in recipes:
        print(f"ID: {recipe['_id']}, Nombre: {recipe['name']}, Ingredientes: {', '.join(recipe['ingredients'])}, Pasos: {recipe['steps']}")

def search_recipe():
    ingredient = input("Ingrese un ingrediente para buscar recetas: ")
    recipes = collection.find({"ingredients": {"$regex": ingredient, "$options": "i"}})
    for recipe in recipes:
        print(f"ID: {recipe['_id']}, Nombre: {recipe['name']}, Ingredientes: {', '.join(recipe['ingredients'])}, Pasos: {recipe['steps']}")

if __name__ == "__main__":
    while True:
        print("\n--- Menú Principal ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar ingredientes y pasos de receta")
        print("f) Salir")

        option = input("Ingrese la opción deseada: ").lower()

        if option == 'a':
            add_recipe()
        elif option == 'b':
            update_recipe()
        elif option == 'c':
            delete_recipe()
        elif option == 'd':
            view_recipes()
        elif option == 'e':
            search_recipe()
        elif option == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")
