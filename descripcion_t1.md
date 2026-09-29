# Estructuras de datos desde cero

- **Stack (pila):** sigue el principio LIFO (*Last In, First Out*).
- **Queue (cola):** sigue el principio FIFO (*First In, First Out*).
- **HashTable (tabla hash):** almacena pares clave-valor y permite buscarlos
  rapidamente.

La demostracion esta dividida en tres partes:

### 1. Pila (`Stack`)

La funcion `demo_stack()`:

- Inserta `1`, `2` y `3` con `push()`.
- Muestra el elemento superior con `peek()`.
- Elimina los elementos con `pop()`.
- Comprueba si diferentes expresiones tienen parentesis, corchetes y llaves
  balanceados.

Como la pila es LIFO, los elementos salen en este orden:

```text
3, 2, 1
```

### 2. Cola (`Queue`)

La funcion `demo_queue()`:

- Inserta `A`, `B` y `C` con `enqueue()`.
- Consulta el primer elemento con `front()`.
- Elimina los elementos con `dequeue()`.

Como la cola es FIFO, los elementos salen en este orden:

```text
A, B, C
```

### 3. Tabla hash (`HashTable`)

La funcion `demo_hash()`:

- Guarda datos usando claves como `"int"`, `"float"` e `"id"`.
- Actualiza el valor de una clave existente.
- Busca claves con corchetes y con `get()`.
- Comprueba si una clave existe usando `in`.
- Elimina una entrada con `remove()`.
- Inserta 20 claves adicionales para provocar el redimensionamiento automatico.

## Como ejecutar las pruebas

Desde la carpeta `Tarea 1`, ejecuta:

```bash
python3 tests.py
```

Para ver el nombre y el resultado de cada prueba:

```bash
python3 -m unittest -v tests.py
```

Una ejecucion correcta muestra:

```text
Ran 19 tests

OK
```

## Casos probados

Las pruebas no solo comprueban casos normales. Tambien revisan errores y
situaciones especiales.

### Casos de `Stack`

- **Orden LIFO:** se insertan `1`, `2` y `3`, y se verifica que salgan como
  `3`, `2`, `1`.
- **`peek()` no elimina:** se consulta el tope y se comprueba que el tamano
  de la pila no cambie.
- **`pop()` en una pila vacia:** debe lanzar `IndexError`.
- **`peek()` en una pila vacia:** debe lanzar `IndexError`.
- **`clear()`:** se agregan elementos, se limpia la pila y se verifica que
  quede vacia.
- **`size()` y `len()`:** se comprueba que informen la cantidad correcta.

### Casos de `Queue`

- **Orden FIFO:** se insertan `1`, `2` y `3`, y se verifica que salgan como
  `1`, `2`, `3`.
- **`front()` consulta sin eliminar:** se verifica que el primer elemento
  continue en la cola y que el tamano no cambie.
- **`dequeue()` en una cola vacia:** debe lanzar `IndexError`.
- **`front()` en una cola vacia:** debe lanzar `IndexError`.
- **Reutilizacion despues de vaciar:** se elimina el unico elemento, se
  agrega otro y se comprueba que la cola siga funcionando.
- **`clear()`:** se eliminan todos los nodos y se verifica que la cola quede
  vacia.

### Casos de `HashTable`

- **Insertar y obtener:** se guarda una clave y se recupera su valor.
- **Actualizar una clave:** se modifica el valor de `"a"` y se comprueba que
  el tamano siga siendo uno.
- **Clave inexistente con `get()`:** devuelve `None` o un valor predeterminado.
- **Clave inexistente con corchetes:** `table["x"]` debe lanzar `KeyError`.
- **Eliminar una clave inexistente:** `remove("x")` debe lanzar `KeyError`.
- **`contains` y operador `in`:** se verifica la existencia antes y despues
  de eliminar una clave.
- **Redimensionamiento:** se insertan 200 elementos y se comprueba que todos
  conserven sus valores despues de aumentar la tabla.
- **Colisiones:** se crean claves diferentes con el mismo valor hash y se
  comprueba que ambas puedan almacenarse y recuperarse.
- **Orden de insercion:** `keys()` conserva el orden en que se insertaron las
  claves.
- **Valor `None`:** se verifica que una clave pueda tener `None` como valor
  sin dejar de existir.
- **Eliminar cabeza, elemento intermedio y cola:** se comprueba que la lista
  doblemente ligada mantenga sus conexiones correctamente.
- **Eliminar todas las claves y reutilizar:** la tabla queda vacia y despues
  vuelve a aceptar datos.
- **`clear()`:** elimina todas las entradas y reinicia la tabla.

## Complejidad aproximada

| Estructura | Operacion | Complejidad promedio |
|---|---|---:|
| Stack | `push`, `pop`, `peek` | O(1) |
| Queue | `enqueue`, `dequeue`, `front` | O(1) |
| HashTable | `put`, `get`, `remove` | O(1) |

En la tabla hash, el redimensionamiento individual puede costar O(n), porque
debe reubicar las entradas. Sin embargo, ocurre ocasionalmente y el costo
promedio de insertar permanece cercano a O(1).

## Ejemplo rapido

```python
from stack import Stack
from queue import Queue
from hash_table import HashTable

stack = Stack()
stack.push("primero")
stack.push("segundo")
print(stack.pop())  # segundo

queue = Queue()
queue.enqueue("primero")
queue.enqueue("segundo")
print(queue.dequeue())  # primero

table = HashTable()
table["nombre"] = "Ana"
print(table["nombre"])  # Ana
```
