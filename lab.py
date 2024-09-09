import pandas as pd
from graphviz import Digraph

class NodoAVL:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self.left = None
        self.right = None
        self.height = 1
        self.parent = None  # Puntero al padre

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, node, parent=None):
        if not root:
            node.parent = parent  # Asigna el nodo padre
            return node
        elif node.title < root.title:
            root.left = self.insert(root.left, node, root)  # Pasa el nodo actual como padre
            if root.left:
                root.left.parent = root
        else:
            root.right = self.insert(root.right, node, root)  # Pasa el nodo actual como padre
            if root.right:
                root.right.parent = root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rotaciones para balancear el árbol
        if balance > 1 and node.title < root.left.title:
            return self.right_rotate(root)
        if balance < -1 and node.title > root.right.title:
            return self.left_rotate(root)
        if balance > 1 and node.title > root.left.title:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and node.title < root.right.title:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Realizar rotación
        y.left = z
        z.right = T2

        # Actualizar padres
        y.parent = z.parent
        z.parent = y
        if T2:
            T2.parent = z

        # Actualizar alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Realizar rotación
        y.right = z
        z.left = T3

        # Actualizar padres
        y.parent = z.parent
        z.parent = y
        if T3:
            T3.parent = z

        # Actualizar alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def search(self, root, title):
        if not root or root.title == title:
            return root
        elif title < root.title:
            return self.search(root.left, title)
        return self.search(root.right, title)

    def delete(self, root, title):
        if not root:
            return root
        elif title < root.title:
            root.left = self.delete(root.left, title)
            if root.left:
                root.left.parent = root
        elif title > root.title:
            root.right = self.delete(root.right, title)
            if root.right:
                root.right.parent = root
        else:
            if not root.left:
                temp = root.right
                if temp:
                    temp.parent = root.parent
                root = None
                return temp
            elif not root.right:
                temp = root.left
                if temp:
                    temp.parent = root.parent
                root = None
                return temp

            temp = self.get_min_value_node(root.right)
            root.title = temp.title
            root.year = temp.year
            root.right = self.delete(root.right, temp.title)
            if root.right:
                root.right.parent = root

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rotaciones para balancear el árbol
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def level_order(self, root):
      if not root:
          return []
      result = []
      queue = [root]
      while queue:
          node = queue.pop(0)
          result.append(node)  # Cambiado a añadir el nodo completo
          if node.left:
              queue.append(node.left)
          if node.right:
              queue.append(node.right)
      return result

    def get_parent(self, node):
        return node.parent

    def get_grandparent(self, node):
        if node and node.parent:
            return node.parent.parent
        return None

    def get_uncle(self, node):
        # Encuentra el padre del nodo
        parent = self.get_parent(node)
        if not parent:
            return None

        # Encuentra el abuelo del nodo
        grandparent = self.get_grandparent(node)
        if not grandparent:
            return None

        # Encuentra el tío: hermano del padre
        if parent == grandparent.left:
            return grandparent.right
        else:
            return grandparent.left

    def get_depth(self, root, title, level=0):
      if root is None:
          return -1  # Si el nodo no se encuentra
      if root.title == title:
          return level  # Retorna el nivel actual si encuentra el nodo

      # Busca en el subárbol izquierdo
      level_left = self.get_depth(root.left, title, level + 1)
      if level_left != -1:
          return level_left

      # Si no lo encuentra en el subárbol izquierdo, busca en el derecho
      return self.get_depth(root.right, title, level + 1)



def visualize_tree(node, dot=None):
    if dot is None:
        dot = Digraph()
        dot.node(f"{node.title}\n{node.year}", f"{node.title}\n{node.year}")

    if node.left:
        dot.node(f"{node.left.title}\n{node.left.year}", f"{node.left.title}\n{node.left.year}")
        dot.edge(f"{node.title}\n{node.year}", f"{node.left.title}\n{node.left.year}")
        visualize_tree(node.left, dot)

    if node.right:
        dot.node(f"{node.right.title}\n{node.right.year}", f"{node.right.title}\n{node.right.year}")
        dot.edge(f"{node.title}\n{node.year}", f"{node.right.title}\n{node.right.year}")
        visualize_tree(node.right, dot)

    return dot

# Cargar el dataset de películas
dataset = pd.read_csv("dataset_movies.csv")

# Crear el árbol AVL
avl_tree = AVLTree()
root = None

def insert_movie():
    global root
    while True:
        title = input("Ingrese el título de la película (o escriba 'salir' para terminar): ")
        if title.lower() == 'salir':
            break
        if title in dataset['Title'].values:
            movie_info = dataset[dataset['Title'] == title].iloc[0]
            year = movie_info['Year']
            nodo = NodoAVL(title, year)
            root = avl_tree.insert(root, nodo)
            visualize_tree(root).render("avl_tree", format="png")
            print("Película insertada y árbol actualizado.")
        else:
            print("La película no se encuentra en el dataset.")


def delete_movie():
    global root
    title = input("Ingrese el título de la película a eliminar: ")
    root = avl_tree.delete(root, title)
    if root:
        visualize_tree(root).render("avl_tree", format="png", cleanup=True)
    else:
        print("El árbol está vacío después de la eliminación.")
    print("Película eliminada y árbol actualizado.")

def search_movie():
    title = input("Ingrese el nombre de la película: ")

    # Buscar el nodo en el árbol AVL
    node = avl_tree.search(root, title)

    if node is not None:
        # Buscar la película en el dataset
        result = dataset[dataset['Title'] == title]

        if not result.empty:
            print("Detalles de la película:")
            for index, row in result.iterrows():
                print(f"""
                Título: {row['Title']}
                Año: {row['Year']}
                Ingresos Nacionales: {row['Domestic Earnings']}
                Porcentaje de Ingresos Nacionales: {row['Domestic Percent Earnings']}%
                Ingresos Internacionales: {row['Foreign Earnings']}
                Porcentaje de Ingresos Internacionales: {row['Foreign Percent Earnings']}%
                """)
        else:
            print("No se encontró la película en el dataset.")
    else:
        print("La película no se encontró en el árbol AVL.")

def search_movies_by_criteria():
    year = int(input("Ingrese el año de estreno: "))
    foreign_earnings_max = float(input("Ingrese el máximo de ingresos internacionales (0 para no limitar): "))

    filtered_movies = dataset[(dataset['Year'] == year) & ((foreign_earnings_max == 0) | (dataset['Foreign Earnings'] <= foreign_earnings_max))]

    # Filtra las películas que están en el árbol AVL
    valid_titles = {node.title for node in avl_tree.level_order(root)}  # Ahora es correcto
    filtered_movies = filtered_movies[filtered_movies['Title'].isin(valid_titles)]

    if filtered_movies.empty:
        print("No se encontraron películas que cumplan con los criterios.")
    else:
        print("Películas encontradas:")
        for index, row in filtered_movies.iterrows():
            print(f"""
            Título: {row['Title']}
            Año: {row['Year']}
            Ingresos Nacionales: {row['Domestic Earnings']}
            Porcentaje de Ingresos Nacionales: {row['Domestic Percent Earnings']}%
            Ingresos Internacionales: {row['Foreign Earnings']}
            Porcentaje de Ingresos Internacionales: {row['Foreign Percent Earnings']}%
            """)

def level_order_traversal(root):
    def traverse_level(current_level_nodes, next_level_nodes, level):
        if not current_level_nodes:
            return

        print(f"Nivel {level}:")
        for node in current_level_nodes:
            print(f"{node.title} ({node.year})", end=" | ")
            if node.left:
                next_level_nodes.append(node.left)
            if node.right:
                next_level_nodes.append(node.right)
        print("\n")
        traverse_level(next_level_nodes, [], level + 1)

    traverse_level([root], [], 0)

# Función para llamar al recorrido por niveles
def level_order_traversal_call():
    if root:
        level_order_traversal(root)
    else:
        print("El árbol está vacío.")


def get_node_details():
    title = input("Ingrese el título de la película para obtener detalles del nodo: ")
    node = avl_tree.search(root, title)

    if node:
        depth = avl_tree.get_depth(root, title)
        balance = avl_tree.get_balance(node)
        parent = avl_tree.get_parent(node)
        grandparent = avl_tree.get_grandparent(node)
        uncle = avl_tree.get_uncle(node)
        print(f"Nodo: {node.title}")
        print(f"Año: {node.year}")
        print(f"Nivel: {depth}")
        print(f"Factor de balanceo: {balance}")
        print(f"Padre del nodo: {parent.title if parent else 'None'}")
        print(f"Abuelo del nodo: {grandparent.title if grandparent else 'None'}")
        print(f"Tío del nodo: {uncle.title if uncle else 'None'}")

    else:
        print("Película no encontrada.")



def menu():
    while True:
        print("""
                    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
                    ████╗ ████║██╔════╝████╗  ██║██║   ██║
                    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
                    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║╚██╗ ██╔╝
                    ██║ ╚═╝ ██║███████╗██║ ╚████║ ╚████╔╝
                    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝  ╚═══╝

        ╔══════════════════════════════════════════════════════════╗
        ║                     🎬 MOVIE MENU 🎬                    ║
        ╚══════════════════════════════════════════════════════════╝
        ║ 1. 🎥 Insertar película                                  ║
        ║ 2. ❌ Eliminar película                                  ║
        ║ 3. 🔍 Buscar película                                    ║
        ║ 4. 🎯 Buscar películas por criterios                     ║
        ║ 5. 🏞️ Mostrar recorrido por niveles                      ║
        ║ 6. ℹ️  Obtener detalles del nodo                           ║
        ║ 7. 👥 Información del grupo                              ║
        ║ 8. 🚪 Salir                                              ║
        ╚══════════════════════════════════════════════════════════╝
""")


        choice = input("Seleccione una opción: ")
        if choice == '1':
            insert_movie()
        elif choice == '2':
            delete_movie()
        elif choice == '3':
            search_movie()
        elif choice == '4':
            search_movies_by_criteria()
        elif choice == '5':
            level_order_traversal_call()
        elif choice == '6':
            get_node_details()
        elif choice == '7':
            show_group_info()
        elif choice == '8':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def show_group_info():
    print("""
        ╔══════════════════════════════════════════════════════════╗
        ║                    👥INFORMACIÓN DEL GRUPO               ║
        ╚══════════════════════════════════════════════════════════╝
        ║ Integrantes del grupo:                                   ║
        ║ - Jose Mestre                                            ║
        ║ - Sergio Perez                                           ║
        ║ - Juan David Arbelaez                                    ║
        ║                                                          ║
        ║                                                          ║
        ║ Asignación del proyecto: Desarrollo de un árbol AVL      ║
        ║ Objetivo: Manejar datos de películas y realizar          ║
        ║ operaciones como inserción, eliminación, búsqueda,       ║
        ║ recorrido y visualización.                               ║
        ╚══════════════════════════════════════════════════════════╝
    """)

# Ejecutar el menú
menu()
