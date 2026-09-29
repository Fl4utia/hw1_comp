"""
Pruebas automaticas para Stack, Queue y HashTable.

Este archivo usa unittest, una biblioteca incluida con Python. Una prueba
automaticamente:

1. Crea una estructura de datos.
2. Ejecuta una operacion.
3. Compara el resultado real con el resultado esperado.
4. Marca la prueba como correcta o fallida.

Para ejecutar todas las pruebas desde esta carpeta:

    python3 tests.py

Cada metodo cuyo nombre comienza con test_ se ejecuta automaticamente.
"""

import unittest

# Estos imports buscan stack.py, queue.py y hash_table.py en esta carpeta.
from stack import Stack
from queue import Queue
from hash_table import HashTable


class TestStack(unittest.TestCase):
    """
    Grupo de pruebas para la clase Stack.

    Heredar de unittest.TestCase proporciona metodos como assertEqual,
    assertTrue, assertRaises y assertIsNone.
    """

    def test_lifo_order(self):
        """Comprueba que la pila siga el orden LIFO."""
        s = Stack()

        # Insertamos 1, despues 2 y finalmente 3.
        for x in (1, 2, 3):
            s.push(x)

        # LIFO significa que el ultimo en entrar sale primero:
        # 3, despues 2 y finalmente 1.
        self.assertEqual([s.pop(), s.pop(), s.pop()], [3, 2, 1])

    def test_peek_does_not_remove(self):
        """Comprueba que peek consulte el tope sin eliminarlo."""
        s = Stack()
        s.push("a")

        # peek() debe devolver "a".
        self.assertEqual(s.peek(), "a")

        # La pila debe seguir teniendo un elemento.
        self.assertEqual(len(s), 1)

    def test_empty_errors(self):
        """Comprueba los errores al usar una pila vacia."""
        s = Stack()
        self.assertTrue(s.is_empty())

        # assertRaises verifica que la operacion lance IndexError.
        with self.assertRaises(IndexError):
            s.pop()
        with self.assertRaises(IndexError):
            s.peek()

    def test_clear_and_size(self):
        """Comprueba que clear elimine todos los elementos."""
        s = Stack()
        s.push(1)
        s.push(2)

        self.assertEqual(s.size(), 2)
        s.clear()
        self.assertTrue(s.is_empty())


class TestQueue(unittest.TestCase):
    """Grupo de pruebas para la clase Queue."""

    def test_fifo_order(self):
        """Comprueba que la cola siga el orden FIFO."""
        q = Queue()

        # Insertamos 1, 2 y 3 en ese orden.
        for x in (1, 2, 3):
            q.enqueue(x)

        # FIFO significa que sale primero el elemento que entro primero.
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])

    def test_front_and_size(self):
        """Comprueba front() y size()."""
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")

        # front() consulta el primer elemento sin quitarlo.
        self.assertEqual(q.front(), "a")
        self.assertEqual(q.size(), 2)

    def test_empty_errors(self):
        """Comprueba los errores de dequeue y front en una cola vacia."""
        q = Queue()

        with self.assertRaises(IndexError):
            q.dequeue()
        with self.assertRaises(IndexError):
            q.front()

    def test_reuse_after_emptying(self):
        """Comprueba que la cola pueda reutilizarse despues de vaciarse."""
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        q.enqueue(2)

        # La cola debe contener solamente el nuevo elemento 2.
        self.assertEqual(list(q), [2])

    def test_clear(self):
        """Comprueba que clear elimine todos los nodos."""
        q = Queue()
        q.enqueue(1)
        q.clear()
        self.assertTrue(q.is_empty())


class TestHashTable(unittest.TestCase):
    """
    Grupo de pruebas para HashTable.

    Se verifican insercion, actualizacion, busqueda, eliminacion,
    colisiones, redimensionamiento y la interfaz tipo diccionario.
    """

    def test_put_get_update(self):
        """Comprueba insertar una clave y actualizar su valor."""
        h = HashTable()
        h.put("a", 1)
        h.put("a", 2)

        # La segunda llamada actualiza el valor, no crea otra clave.
        self.assertEqual(h.get("a"), 2)
        self.assertEqual(len(h), 1)

    def test_missing_key(self):
        """Comprueba el comportamiento al buscar una clave inexistente."""
        h = HashTable()

        # get() devuelve None o el valor predeterminado proporcionado.
        self.assertIsNone(h.get("x"))
        self.assertEqual(h.get("x", 0), 0)

        # Con corchetes y remove(), una clave inexistente produce KeyError.
        with self.assertRaises(KeyError):
            h["x"]
        with self.assertRaises(KeyError):
            h.remove("x")

    def test_remove_and_contains(self):
        """Comprueba contains, remove y la sintaxis con corchetes."""
        h = HashTable()
        h["a"] = 1

        # assertIn utiliza internamente __contains__.
        self.assertIn("a", h)

        # remove() devuelve el valor que elimino.
        self.assertEqual(h.remove("a"), 1)
        self.assertNotIn("a", h)

    def test_resize_keeps_data(self):
        """Comprueba que el redimensionamiento conserve los datos."""
        h = HashTable()

        # Esta cantidad obliga a aumentar varias veces los buckets.
        for i in range(200):
            h[i] = i * 2

        self.assertEqual(len(h), 200)

        # all() exige que cada clave conserve su valor correcto.
        self.assertTrue(all(h[i] == i * 2 for i in range(200)))

    def test_collisions(self):
        """Comprueba que la tabla pueda manejar colisiones."""

        class Bad:
            # Todas las instancias devuelven el mismo hash y caen en
            # el mismo bucket deliberadamente.
            def __init__(self, n):
                self.n = n

            def __hash__(self):
                return 1

            def __eq__(self, other):
                return self.n == other.n

        h = HashTable()
        a, b = Bad(1), Bad(2)
        h[a] = "A"
        h[b] = "B"

        # Aunque comparten bucket, __eq__ permite distinguirlas.
        self.assertEqual((h[a], h[b]), ("A", "B"))

        h.remove(a)
        self.assertEqual(h[b], "B")

    def test_insertion_order(self):
        """Comprueba que keys conserve el orden de insercion."""
        h = HashTable()
        for k in ("z", "a", "m"):
            h[k] = 0

        self.assertEqual(h.keys(), ["z", "a", "m"])

        # Quitar "a" conserva el orden relativo de las restantes.
        h.remove("a")
        self.assertEqual(h.keys(), ["z", "m"])

    def test_none_value_is_valid(self):
        """Comprueba que None pueda ser un valor valido."""
        h = HashTable()
        h["k"] = None

        # La clave existe aunque su valor sea None.
        self.assertIn("k", h)

    def test_remove_head_middle_tail_keeps_order(self):
        """Comprueba eliminar primero, medio y ultimo de la lista."""
        h = HashTable()
        for k in "abcde":
            h[k] = 0

        # Se eliminan la cabeza, un elemento intermedio y la cola.
        h.remove("a")
        h.remove("c")
        h.remove("e")
        self.assertEqual(h.keys(), ["b", "d"])

        # Una clave nueva se agrega al final del orden.
        h["f"] = 1
        self.assertEqual(h.keys(), ["b", "d", "f"])

    def test_remove_all_then_reuse(self):
        """Comprueba vaciar completamente la tabla y volver a usarla."""
        h = HashTable()

        for i in range(50):
            h[i] = i
        for i in range(50):
            h.remove(i)

        self.assertEqual(len(h), 0)
        self.assertEqual(h.keys(), [])

        # Debe seguir funcionando despues de quedar completamente vacia.
        h["x"] = 1
        self.assertEqual(h.items(), [("x", 1)])

    def test_clear(self):
        """Comprueba que clear reinicie la tabla."""
        h = HashTable()
        h["a"] = 1
        h.clear()

        self.assertEqual(len(h), 0)
        self.assertNotIn("a", h)


if __name__ == "__main__":
    # Este bloque se ejecuta con:
    #
    #     python3 tests.py
    #
    # unittest.main() descubre y ejecuta todos los metodos test_*.
    unittest.main()
