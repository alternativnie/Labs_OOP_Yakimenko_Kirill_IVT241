from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class Stack(Generic[T]):
    """LIFO"""

    def __init__(self) -> None:
        """создаём пустой стек"""
        self._items: List[T] = []  # хранение всего

    def push(self, item: T) -> None:
        """добавление элемента на вершину стека"""
        self._items.append(item)  #в конец списка

    def pop(self) -> Optional[T]:
        """берём верхний элемент со стека и убираем его"""
        if self.is_empty():  # если пустой
            return None
        return self._items.pop()  #без индекса берёт последний элемент

    def peek(self) -> Optional[T]:
        """просмотр элемента на вершине стека без удаления"""
        if self.is_empty():
            return None
        return self._items[-1]  #смотрим последний элемент

    def is_empty(self) -> bool:
        """проверяем, пустой ли стек"""
        return len(self._items) == 0

    def size(self) -> int:
        """количество элементов в стеке"""
        return len(self._items)

    def __str__(self) -> str:
        """вид стека при печати"""
        return f"Stack({self._items})"


class Queue(Generic[T]):
    """FIFO"""

    def __init__(self) -> None:
        """создаём пустую очередь"""
        self._items: List[T] = []

    def enqueue(self, item: T) -> None:
        """добавление элемента в конец очереди"""
        self._items.append(item)  #добав в конец

    def dequeue(self) -> Optional[T]:
        """удаление и возврат элемента из начала очереди"""
        if self.is_empty():  #если пустая
            return None
        return self._items.pop(0)  # pop(0) берёт 1 элемент

    def peek(self) -> Optional[T]:
        """просмотр первого элемента очереди без удаления"""
        if self.is_empty():
            return None
        return self._items[0]  # смотрим 1 элемент

    def is_empty(self) -> bool:
        """проверка, пуста ли очередь"""
        return len(self._items) == 0

    def size(self) -> int:
        """количество элементов в очереди"""
        return len(self._items)

    def __str__(self) -> str:
        """вид очереди при печати"""
        return f"Queue({self._items})"



def test_it() -> None:

    # проверяем стек
    print("\n1. Проверяем стек:")
    stack = Stack[int]()

    stack.push(10)
    stack.push(20)
    stack.push(30)
    print(f"после добавления: {stack}")
    print(f"наверху: {stack.peek()}")
    print(f"Количество элементов: {stack.size()}")

    popped = stack.pop()
    print(f"Извлекли сверху: {popped}")
    print(f"После извлечения: {stack}")
    print(f"Проверка пустоты: {stack.is_empty()}")

    print("\n2. проверяем очередь:")
    queue = Queue[str]()

    queue.enqueue("первый")
    queue.enqueue("второй")
    queue.enqueue("третий")
    print(f"после добавления: {queue}")
    print(f"первый элемент: {queue.peek()}")
    print(f"количество элементов: {queue.size()}")

    dequeued = queue.dequeue()
    print(f"Извлекли из начала: {dequeued}")
    print(f"После извлечения: {queue}")
    print(f"Проверка пустоты: {queue.is_empty()}")


if __name__ == "__main__":
    test_it()