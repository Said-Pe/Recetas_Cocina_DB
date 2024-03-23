#Usare las variables en ingles ya que se ve mas cool.

from sqlalchemy import create_engine, Column, Integer, String, Text # Importe los componentes necesarios.
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Creamos la conexión a la base de datos MariaDB
engine = create_engine('mysql+mysqlconnector://root:basesaid@localhost:3306/recetas_db')
Base = declarative_base()

# Definimos la clase Recipe como una tabla en la base de datos
class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)

# Creamos la base de datos si no existe
Base.metadata.create_all(engine)

# Creamos la sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

def add_recipe():
    name = input("Nombre de la receta: ")
    ingredients = input("Ingredientes (separados por comas): ")
    steps = input("Pasos de la receta: ")

    recipe = Recipe(name=name, ingredients=ingredients, steps=steps)
    session.add(recipe)
    session.commit()

def update_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea actualizar: ")
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe:
        name = input("Nuevo nombre de la receta: ")
        ingredients = input("Nuevos ingredientes (separados por comas): ")
        steps = input("Nuevos pasos de la receta: ")

        recipe.name = name
        recipe.ingredients = ingredients
        recipe.steps = steps
        session.commit()
    else:
        print("No se encontró ninguna receta con ese ID.")

def delete_recipe():
    recipe_id = input("Ingrese el ID de la receta que desea eliminar: ")
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe:
        session.delete(recipe)
        session.commit()
    else:
        print("No se encontró ninguna receta con ese ID.")

def view_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No hay recetas disponibles.")
    else:
        for recipe in recipes:
            print(f"ID: {recipe.id}, Nombre: {recipe.name}, Ingredientes: {recipe.ingredients}, Pasos: {recipe.steps}")

def search_recipe():
    ingredient = input("Ingrese un ingrediente para buscar recetas: ")
    recipes = session.query(Recipe).filter(Recipe.ingredients.ilike(f'%{ingredient}%')).all()
    if not recipes:
        print(f"No hay recetas que contengan {ingredient}.")
    else:
        for recipe in recipes:
            print(f"ID: {recipe.id}, Nombre: {recipe.name}, Ingredientes: {recipe.ingredients}, Pasos: {recipe.steps}")

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
