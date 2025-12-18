from typing import TypeVar, List, Optional, Tuple

T = TypeVar('T')


#Stack

def create_stack() -> List[T]:
    """пустой стек"""
    return []


def stack_push(stack: List[T], item: T) -> List[T]:
    """добавить элемент в стек (возвращает новый стек)"""
    return stack + [item]


def stack_pop(stack: List[T]) -> Tuple[Optional[T], List[T]]:
    """удалить и вернуть верхний элемент + новый стек"""
    if not stack:
        return None, stack
    return stack[-1], stack[:-1]  #срез создаёт новый список


def stack_peek(stack: List[T]) -> Optional[T]:
    """посмотреть верхний элемент"""
    return stack[-1] if stack else None


def stack_is_empty(stack: List[T]) -> bool:
    """проверка пустоты очереди"""
    return len(stack) == 0


def stack_size(stack: List[T]) -> int:
    """количество элементов в стеке"""
    return len(stack)


#Queue

def create_queue() -> List[T]:
    """создать пустую очередь"""
    return []


def queue_enqueue(queue: List[T], item: T) -> List[T]:
    """добавить элемент в очередь (возвращает новую очередь)"""
    return queue + [item]


def queue_dequeue(queue: List[T]) -> Tuple[Optional[T], List[T]]:
    """удалить и вернуть первый элемент + новую очередь"""
    if not queue:
        return None, queue
    return queue[0], queue[1:]


def queue_peek(queue: List[T]) -> Optional[T]:
    """посмотреть первый элемент"""
    return queue[0] if queue else None


def queue_is_empty(queue: List[T]) -> bool:
    """проверка пустоты очереди"""
    return len(queue) == 0


def queue_size(queue: List[T]) -> int:
    """количество элементов в стеке"""
    return len(queue)


#демонстрация

if __name__ == "__main__":

    #Queue
    print("\nQueue:")
    q = create_queue()
    print(f"Создана пустая очередь: {q}")
    print(f"Проверка пустоты {queue_is_empty(q)}")

    q = queue_enqueue(q, 10)
    q = queue_enqueue(q, 20)
    q = queue_enqueue(q, 30)
    print(f"После добавления 10, 20, 30: {q}")
    print(f"Размер очереди: {queue_size(q)}")

    item1, q = queue_dequeue(q)
    print(f"Извлеченный элемент: {item1}")
    print(f"Очередь после dequeue: {q}")

    item2, q = queue_dequeue(q)
    print(f"Извлеченный элемент: {item2}")
    print(f"Очередь после dequeue: {q}")

    #Stack
    print("\nStack:")
    s = create_stack()
    print(f"Создан пустой стек: {s}")
    print(f"Проверка пустоты: {stack_is_empty(s)}")

    s = stack_push(s, "A")
    s = stack_push(s, "B")
    s = stack_push(s, "C")
    print(f"После добавления 'A', 'B', 'C': {s}")
    print(f"Размер стека: {stack_size(s)}")

    popped1, s = stack_pop(s)
    print(f"Извлеченный элемент: {popped1}")
    print(f"Стек после pop: {s}")

    popped2, s = stack_pop(s)
    print(f"Извлеченный элемент: {popped2}")
    print(f"Стек после pop: {s}")

