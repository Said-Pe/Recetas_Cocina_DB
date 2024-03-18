import sqlite3

def create_db():
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    # Creamos la tabla de recetas por si no existe.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_recipe():
    name = input("Nombre de la receta: ")
    ingredients = input("Ingredientes (separados por comas): ")
    steps = input("Pasos de la receta: ")

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?)
    ''', (name, ingredients, steps))

    conn.commit()
    conn.close()

def update_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea actualizar: ")
    name = input("Nuevo nombre de la receta: ")
    ingredients = input("Nuevos ingredientes (separados por comas): ")
    steps = input("Nuevos pasos de la receta: ")

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE recipes
        SET name=?, ingredients=?, steps=?
        WHERE id=?
    ''', (name, ingredients, steps, recipe_id))

    conn.commit()
    conn.close()

def delete_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea eliminar: ")

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM recipes WHERE id=?
    ''', (recipe_id,))

    conn.commit()
    conn.close()

def view_recipes():
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM recipes
    ''')

    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        print("No hay recetas disponibles.")
    else:
        for recipe in recipes:
            print(f"ID: {recipe[0]}, Nombre: {recipe[1]}, Ingredientes: {recipe[2]}, Pasos: {recipe[3]}")

def search_recipe():
    ingredient = input("Ingrese un ingrediente para buscar recetas: ")

    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM recipes WHERE ingredients LIKE ?
    ''', ('%' + ingredient + '%',))

    recipes = cursor.fetchall()
    conn.close()

    if not recipes:
        print(f"No hay recetas que contengan {ingredient}.")
    else:
        for recipe in recipes:
            print(f"ID: {recipe[0]}, Nombre: {recipe[1]}, Ingredientes: {recipe[2]}, Pasos: {recipe[3]}")

if __name__ == "__main__":
    create_db()
    while True:
        print("\n--- Menú Principal ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar ingredientes y pasos de receta")
        print("g) Salir")

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
        elif option == 'g':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

