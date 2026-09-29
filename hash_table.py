"""
Tabla hash (diccionario) desde cero: encadenamiento separado + redimensionado.

Conserva el orden de inserción con una lista doblemente ligada que atraviesa
las entradas (como LinkedHashMap), así put/get/remove son O(1) promedio.

Cada entrada participa en dos estructuras al mismo tiempo:

1. Una cadena de bucket, usada para encontrar una clave.
2. Una lista doblemente ligada, usada para conservar el orden de insercion.
"""


class _Entry:
    """Nodo que representa un par clave-valor dentro de la tabla."""

    __slots__ = ("key", "value", "next", "before", "after")

    def __init__(self, key, value, next=None):
        # Datos que el usuario realmente guarda.
        self.key = key
        self.value = value

        # next conecta esta entrada con otras entradas que cayeron en
        # el mismo bucket. Esta es la cadena para resolver colisiones.
        self.next = next

        # before y after conectan las entradas en orden de insercion,
        # independientemente del bucket al que pertenezcan.
        self.before = None
        self.after = None


class HashTable:
    # La tabla comienza con ocho posiciones de bucket.
    _INITIAL_CAPACITY = 8

    # Al superar este factor, se duplica la cantidad de buckets.
    _MAX_LOAD = 0.75

    def __init__(self):
        # Cada posicion empieza sin ninguna entrada. None representa
        # una cadena vacia; si hay colision, se forma una cadena de
        # objetos _Entry usando sus referencias next.
        self._buckets = [None] * self._INITIAL_CAPACITY

        # Cantidad de claves diferentes almacenadas.
        self._size = 0

        # La lista doblemente ligada conserva el orden de insercion.
        self._head = None
        self._tail = None

    def _index(self, key, capacity=None):
        """
        Calcula el bucket de una clave.

        hash(key) produce un entero. El modulo limita el resultado al
        rango valido 0..capacity-1. Si no se proporciona capacity, se
        usa la capacidad actual de la tabla.
        """
        return hash(key) % (capacity or len(self._buckets))

    def _find(self, key):
        """
        Busca una entrada recorriendo solo su cadena de bucket.

        Si hubo colisiones, cur avanza mediante cur.next hasta hallar
        la clave o llegar a None.
        """
        cur = self._buckets[self._index(key)]
        while cur:
            if cur.key == key:
                return cur
            cur = cur.next
        return None

    def put(self, key, value):
        """
        Inserta una clave nueva o actualiza su valor.

        Si la clave ya existe, solo se modifica value. Si es nueva, se
        agrega al bucket y al final de la lista de orden de insercion.
        """
        entry = self._find(key)
        if entry:
            # Actualizar no cambia el numero de claves.
            entry.value = value
            return

        # El nuevo nodo se coloca al inicio de la cadena del bucket.
        # Insertarlo al frente evita recorrer esa cadena.
        i = self._index(key)
        entry = _Entry(key, value, self._buckets[i])
        self._buckets[i] = entry

        # Ahora se agrega al final de la lista de orden global.
        entry.before = self._tail
        if self._tail:
            self._tail.after = entry
        else:
            self._head = entry
        self._tail = entry
        self._size += 1

        # Si la tabla supera 75% de ocupacion, se duplica y se
        # recalculan las posiciones de todas las entradas.
        if self._size / len(self._buckets) > self._MAX_LOAD:
            self._resize(len(self._buckets) * 2)

    def get(self, key, default=None):
        """Devuelve el valor o default si la clave no existe."""
        entry = self._find(key)
        return entry.value if entry else default

    def remove(self, key):
        """
        Elimina una entrada y devuelve su valor.

        Hay que quitarla de dos estructuras: la cadena del bucket y la
        lista doblemente ligada de insercion.
        """
        i = self._index(key)
        prev, cur = None, self._buckets[i]
        while cur:
            if cur.key == key:
                # Desenlazar de la cadena del bucket. Si prev es None,
                # cur era la primera entrada de esa cadena.
                if prev:
                    prev.next = cur.next
                else:
                    self._buckets[i] = cur.next

                # Desenlazar de la lista de orden. Los vecinos se
                # conectan entre si para saltar la entrada eliminada.
                if cur.before:
                    cur.before.after = cur.after
                else:
                    self._head = cur.after
                if cur.after:
                    cur.after.before = cur.before
                else:
                    self._tail = cur.before
                self._size -= 1
                return cur.value
            prev, cur = cur, cur.next

        # Llegar aqui significa que la clave no se encontro.
        raise KeyError(key)

    def contains(self, key):
        """Devuelve True si la clave existe y False si no existe."""
        return self._find(key) is not None

    def _entries(self):
        """
        Genera las entradas siguiendo el orden de insercion.

        yield entrega una entrada por vez y avanza usando after.
        """
        cur = self._head
        while cur:
            yield cur
            cur = cur.after

    def keys(self):
        """Devuelve las claves en el orden en que fueron insertadas."""
        return [e.key for e in self._entries()]

    def values(self):
        """Devuelve los valores en el orden de sus respectivas claves."""
        return [e.value for e in self._entries()]

    def items(self):
        """Devuelve pares (clave, valor) en orden de insercion."""
        return [(e.key, e.value) for e in self._entries()]

    def clear(self):
        """Reinicia la tabla, eliminando todas sus entradas."""
        self.__init__()

    def _resize(self, new_capacity):
        """
        Reubica todas las entradas en una tabla mas grande.

        El orden de insercion no se pierde porque se recorren las
        entradas mediante after. Solo se reconstruyen las cadenas de
        buckets usando una nueva capacidad.
        """
        new_buckets = [None] * new_capacity
        for e in self._entries():
            # El modulo cambia porque new_capacity es diferente.
            i = self._index(e.key, new_capacity)
            e.next = new_buckets[i]
            new_buckets[i] = e
        self._buckets = new_buckets

    # Interfaz tipo diccionario
    def __setitem__(self, key, value):
        """Permite usar table[key] = value."""
        self.put(key, value)

    def __getitem__(self, key):
        """Permite usar table[key] y lanza KeyError si falta."""
        entry = self._find(key)
        if entry is None:
            raise KeyError(key)
        return entry.value

    def __delitem__(self, key):
        """Permite usar del table[key]."""
        self.remove(key)

    def __contains__(self, key):
        """Permite usar key in table."""
        return self.contains(key)

    def __len__(self):
        """Permite usar len(table)."""
        return self._size

    def __iter__(self):
        """Permite recorrer directamente las claves de la tabla."""
        return iter(self.keys())

    def __repr__(self):
        """Muestra el contenido como HashTable({...})."""
        return "HashTable({" + ", ".join(f"{k!r}: {v!r}" for k, v in self.items()) + "})"


# DIAGRAMA DE LA TABLA HASH
#
# Ejemplo conceptual:
#
#     table["nombre"] = "Ana"
#
# 1. Se calcula el indice:
#
#     hash("nombre") % cantidad_de_buckets
#                         |
#                         v
#                    bucket 3
#
# 2. La entrada se guarda en dos conexiones diferentes:
#
#     Buckets (busqueda por hash):
#
#     bucket 0 -> None
#     bucket 1 -> Entry("edad", 20) -> None
#     bucket 2 -> None
#     bucket 3 -> Entry("nombre", "Ana") -> Entry("email", "...") -> None
#
#     Lista de insercion (orden):
#
#     _head
#       |
#       v
#     [edad] <-> [nombre] <-> [email] <-> None
#                                             ^
#                                             |
#                                           _tail
#
# Cada Entry tiene:
#
#     key    -> la clave
#     value  -> el valor
#     next   -> siguiente entrada del mismo bucket
#     before -> entrada anterior en orden de insercion
#     after  -> entrada siguiente en orden de insercion
#
# Flujo de get("nombre"):
#
#     clave
#       |
#       v
#     hash(clave) % capacidad
#       |
#       v
#     seleccionar un bucket
#       |
#       v
#     recorrer Entry usando next
#       |
#       v
#     comparar entry.key == clave
#       |
#       +--> coincide: devolver entry.value
#       |
#       +--> no coincide: continuar o devolver default
#
# Flujo de remove("nombre"):
#
#     1. Localiza la entrada en su cadena de bucket.
#     2. Conecta el nodo anterior con el siguiente usando next.
#     3. Conecta before con after en la lista de insercion.
#     4. Reduce _size.
#     5. Devuelve el valor eliminado.
#
# Redimensionamiento:
#
#     capacidad 8, 6 entradas -> 6 / 8 = 0.75
#                              |
#                              v
#                  crear 16 buckets
#                              |
#                              v
#             recalcular hash(key) % 16
#                              |
#                              v
#                    reubicar cada Entry