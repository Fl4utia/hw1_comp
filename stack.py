"""
Pila (LIFO) implementada desde cero usando una lista de Python.

LIFO significa "Last In, First Out": el ultimo elemento que entra es
el primero que sale. La lista _items representa la pila de abajo hacia
arriba, por lo que el final de la lista siempre es el tope.
"""


class Stack:
    def __init__(self):
        # La lista comienza vacia. El ultimo elemento de esta lista
        # representa el tope de la pila.
        self._items = []

    def push(self, item):
        """
        Inserta un elemento en el tope de la pila.

        append() agrega el elemento al final de la lista. Esa posicion
        se considera el tope y permite que pop() lo quite despues.
        Complejidad: O(1) amortizado.
        """
        self._items.append(item)

    def pop(self):
        """
        Quita y devuelve el elemento que esta en el tope.

        Primero se comprueba si la pila esta vacia para evitar intentar
        quitar una posicion inexistente. Si esta vacia, se informa el
        error con IndexError. Si tiene elementos, pop() elimina el
        ultimo elemento, que es precisamente el tope.
        Complejidad: O(1).
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Devuelve el tope sin quitarlo.

        El indice -1 significa "ultimo elemento" de una lista. A
        diferencia de pop(), aqui solo se consulta ese elemento.
        Complejidad: O(1).
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """Devuelve True si no hay elementos y False en caso contrario."""
        return not self._items

    def size(self):
        """Devuelve cuantos elementos contiene actualmente la pila."""
        return len(self._items)

    def clear(self):
        """Elimina todos los elementos y deja la pila vacia."""
        self._items.clear()

    def __len__(self):
        """Permite usar len(stack) para obtener el tamano de la pila."""
        return len(self._items)

    def __iter__(self):
        """
        Permite recorrer la pila desde el tope hacia el fondo.

        reversed() no crea otra pila: devuelve un iterador que recorre
        la lista original en orden inverso.
        """
        return reversed(self._items)

    def __repr__(self):
        """Devuelve una representacion que muestra la base y el tope."""
        return f"Stack(bottom->top: {self._items})"


# DIAGRAMA DE LA PILA
#
# Despues de ejecutar:
#
#     stack.push("A")
#     stack.push("B")
#     stack.push("C")
#
# La lista interna queda asi:
#
#     _items = ["A", "B", "C"]
#               base       tope
#                |           |
#                v           v
#     fondo  [ "A" ][ "B" ][ "C" ]  tope
#
# Operacion pop():
#
#     1. Revisa que la pila no este vacia.
#     2. Quita el elemento del final.
#     3. Devuelve "C".
#
#     Antes:  ["A", "B", "C"]
#     Despues: ["A", "B"]
#
# Por eso el orden de salida es:
#
#     push("A"), push("B"), push("C")
#     pop() -> "C"
#     pop() -> "B"
#     pop() -> "A"
#
# Este comportamiento es LIFO:
#
#                    entra ultimo
#                         |
#                         v
#     fondo  [ A ][ B ][ C ]  tope
#                         |
#                         v
#                    sale primero