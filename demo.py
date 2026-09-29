"""Programa de demostración de Stack, Queue y HashTable."""
from stack import Stack
from queue import Queue
from hash_table import HashTable


def demo_stack():
    # DEMOSTRACION 1: PILA (STACK)
    # Esta seccion demuestra el comportamiento LIFO: el ultimo
    # elemento agregado es el primero que se elimina. Tambien usa
    # la pila para verificar si parentesis, corchetes y llaves estan
    # correctamente balanceados.
    print("=== STACK (LIFO) ===")
    s = Stack()
    for x in (1, 2, 3):
        s.push(x)
        print(f"push({x}) ->", s)
    print("peek:", s.peek())
    while not s.is_empty():
        print("pop:", s.pop())
    # Aplicación clásica: paréntesis balanceados como el problema de leetcode loool
    def balanceado(txt):
        pares, st = {")": "(", "]": "[", "}": "{"}, Stack()
        for c in txt:
            if c in "([{":
                st.push(c)
            elif c in pares:
                if st.is_empty() or st.pop() != pares[c]:
                    return False
        return st.is_empty()
    for t in ("(a+b)*[c]", "(]", "((("):
        print(f"balanceado({t!r}) =", balanceado(t))


def demo_queue():
    # DEMOSTRACION 2: COLA (QUEUE)
    # Esta seccion demuestra el comportamiento FIFO: el primer
    # elemento agregado es el primero que se elimina. front() consulta
    # el primer elemento sin quitarlo y dequeue() lo elimina.
    print("\n=== QUEUE (FIFO) ===")
    q = Queue()
    for x in ("A", "B", "C"):
        q.enqueue(x)
        print(f"enqueue({x}) ->", q)
    print("front:", q.front())
    while not q.is_empty():
        print("dequeue:", q.dequeue())


def demo_hash():
    # DEMOSTRACION 3: TABLA HASH
    # Esta seccion demuestra como guardar pares clave-valor, actualizar
    # valores, buscar claves, comprobar si una clave existe, eliminar
    # entradas y agregar suficientes elementos para provocar un resize.
    print("\n=== HASH TABLE ===")
    h = HashTable()
    h["int"] = "entero"
    h["float"] = "flotante"
    h.put("id", "identificador")
    print(h)
    h["int"] = "INT"  # actualización
    print("get('int'):", h["int"], "| get('nope'):", h.get("nope", "no existe"))
    print("'id' in h:", "id" in h)
    print("remove('float'):", h.remove("float"))
    for i in range(20):  # fuerza redimensionado
        h[f"k{i}"] = i
    print("len:", len(h), "| primeras llaves:", h.keys()[:4])


if __name__ == "__main__":
    demo_stack()
    demo_queue()
    demo_hash()