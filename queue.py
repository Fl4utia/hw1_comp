"""
Cola (FIFO) implementada desde cero con nodos enlazados.

FIFO significa "First In, First Out": el primer elemento que entra es
el primero que sale. _head apunta al frente de la cola y _tail apunta
al ultimo nodo.
"""


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value):
        # Cada nodo guarda el dato y una referencia al siguiente nodo.
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        # _head es el frente: de aqui se extraen elementos.
        self._head = None

        # _tail es el final: aqui se agregan elementos nuevos.
        self._tail = None

        # Se mantiene separado para obtener el tamano en O(1), sin
        # recorrer todos los nodos.
        self._size = 0

    def enqueue(self, item):
        """
        Agrega un elemento al final de la cola.

        Se crea un nodo nuevo. Si la cola estaba vacia, ese nodo es
        simultaneamente el frente y el final. Si ya tenia elementos,
        el nodo anterior del final apunta al nuevo nodo.
        Complejidad: O(1).
        """
        node = _Node(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        """
        Quita y devuelve el elemento del frente.

        _head se mueve al siguiente nodo. Si despues de moverlo queda
        en None, significa que se elimino el ultimo elemento y la cola
        vuelve a estar vacia, por lo que _tail tambien debe ser None.
        Complejidad: O(1).
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def front(self):
        """Devuelve el elemento del frente sin eliminarlo."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._head.value

    def is_empty(self):
        """Devuelve True cuando no hay nodos en la cola."""
        return self._size == 0

    def size(self):
        """Devuelve la cantidad de elementos sin recorrer los nodos."""
        return self._size

    def clear(self):
        """
        Elimina la cadena completa de nodos.

        Al perder las referencias _head y _tail, los nodos quedan
        disponibles para que Python los retire automaticamente.
        """
        self._head = self._tail = None
        self._size = 0

    def __len__(self):
        """Permite usar len(queue)."""
        return self._size

    def __iter__(self):
        """
        Recorre los nodos desde el frente hasta el final.

        yield convierte este metodo en un generador: entrega un valor
        cada vez que el ciclo lo solicita, sin construir otra lista.
        """
        cur = self._head
        while cur:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        """Muestra la cola en el orden frente -> final."""
        return f"Queue(front->back: {list(self)})"


# DIAGRAMA DE LA COLA
#
# Despues de ejecutar:
#
#     queue.enqueue("A")
#     queue.enqueue("B")
#     queue.enqueue("C")
#
# La estructura enlazada queda asi:
#
#     _head                                      _tail
#       |                                          |
#       v                                          v
#     [ A | next ] -> [ B | next ] -> [ C | None ]
#       frente                              final
#
# enqueue("D") agrega un nodo al final:
#
#     _tail.next = nuevo_nodo
#     _tail = nuevo_nodo
#
#     _head                              _tail
#       |                                  |
#       v                                  v
#     [ A ] -> [ B ] -> [ C ] -> [ D | None ]
#
# dequeue() quita siempre desde _head:
#
#     1. Guarda el nodo A.
#     2. Mueve _head hacia B.
#     3. Reduce _size.
#     4. Devuelve el valor A.
#
#     Antes:
#     _head
#       |
#       v
#     [ A ] -> [ B ] -> [ C ]
#
#     Despues:
#              _head
#                |
#                v
#     [ A ]    [ B ] -> [ C ]
#     eliminado
#
# El orden de salida es:
#
#     enqueue("A"), enqueue("B"), enqueue("C")
#     dequeue() -> "A"
#     dequeue() -> "B"
#     dequeue() -> "C"
#
# Este comportamiento es FIFO:
#
#     entra primero  -> [ A ][ B ][ C ] -> sale primero