import redis  #----> importamos redis

# Hacemos una conexión a la base de datos Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def add_recipe():
  # Generate a new recipe ID using INCR
  recipe_id = r.incr('recipe_id')
  # Construct the recipe key using f-string
  recipe_key = f'recipe:{recipe_id}'

  # Prompt user for recipe details
  name = input("Nombre de la receta: ")
  ingredients = input("Ingredientes (separados por comas): ")
  steps = input("Pasos de la receta: ")


  r.hset(recipe_key, 'name', name)
  r.hset(recipe_key, 'ingredients', ingredients)
  r.hset(recipe_key, 'steps', steps)
  print("Receta agregada exitosamente.")

def update_recipe():
  # Get recipe ID from user input
  recipe_id = input("Ingrese el ID de la receta que desea actualizar: ")
  # Construct the recipe key
  recipe_key = f'recipe:{recipe_id}'

  # Check if recipe exists using EXISTS
  if r.exists(recipe_key):
    # Get user input for updates
    name = input("Nuevo nombre de la receta: ")
    ingredients = input("Nuevos ingredientes (separados por comas): ")
    steps = input("Nuevos pasos de la receta: ")

    # Prepare updated recipe data dictionary
    updated_recipe = {'name': name, 'ingredients': ingredients, 'steps': steps}

    # Update recipe data using HMSET
    r.hmset(recipe_key, updated_recipe)
    print("Receta actualizada exitosamente.")
  else:
    print("No se encontró ninguna receta con ese ID.")

def delete_recipe():
  # Get recipe ID from user input
  recipe_id = input("Ingrese el ID de la receta que desea eliminar: ")
  # Construct the recipe key
  recipe_key = f'recipe:{recipe_id}'

  # Check if recipe exists using EXISTS
  if r.exists(recipe_key):
    # Delete the recipe using DEL
    r.delete(recipe_key)
    print("Receta eliminada exitosamente.")
  else:
    print("No se encontró ninguna receta con ese ID.")

def view_recipes():
  # Get all recipe keys using KEYS
  keys = r.keys('recipe:*')
  # Check if any recipes are found
  if keys:
    for key in keys:
      # Retrieve recipe details using HGETALL
      recipe = r.hgetall(key)
      # Decode bytes and format output
      print(f"ID: {key.decode()}, Nombre: {recipe[b'name'].decode()}, Ingredientes: {recipe[b'ingredients'].decode()}, Pasos: {recipe[b'steps'].decode()}")
  else:
    print("No hay recetas disponibles.")

def search_recipe():
  # Get ingredient to search for
  ingredient = input("Ingrese un ingrediente para buscar recetas: ")
  # Get all recipe keys using KEYS
  keys = r.keys('recipe:*')
  found_recipes = []
  for key in keys:
    # Retrieve recipe details using HGETALL
    recipe = r.hgetall(key)
    ingredients = recipe[b'ingredients'].decode()
    # Search ingredient (case-insensitive)
    if ingredient.lower() in ingredients.lower():
      found_recipes.append(recipe)

  # Check if any recipes were found
  if found_recipes:
    for recipe in found_recipes:
      # Decode bytes and format output
      print(f"ID: {key.decode()}, Nombre: {recipe[b'name'].decode()}, Ingredientes: {recipe[b'ingredients'].decode()}, Pasos: {recipe[b'steps'].decode()}")
  else:
    print(f"No hay recetas que contengan {ingredient}.")

def main():
  while True:
    # Mostrar el menú principal
    print("\n--- Menú Principal ---")
    print("a) Agregar nueva receta")
    print("b) Actualizar receta existente")
    print("c) Eliminar receta existente")
    print("d) Ver listado de recetas")
    print("e) Buscar ingredientes y pasos de receta")
    print("f) Salir")

    # Obtener la opción del usuario
    option = input("Ingrese la opción deseada: ").lower()

    # Validar la opción
    if option not in ("a", "b", "c", "d", "e", "f"):
      print("Opción no válida. Por favor, elija una opción válida.")
      continue

    # Salir del bucle si la opción es "f"
    if option == "f":
      print("¡Hasta luego!")
      break

    # Llamar a la función correspondiente
    if option == "a":
      add_recipe()
    elif option == "b":
      update_recipe()
    elif option == "c":
      delete_recipe()
    elif option == "d":
      view_recipes()
    elif option == "e":
      search_recipe()

if __name__ == "__main__":
  main()