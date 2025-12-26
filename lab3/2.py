import datetime as dt
import json
from typing import Dict, List, Any, Set
import uuid


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        """создаём Person"""
        self._name = name
        self._friends: List['Person'] = []
        self._born_in = born_in
        self._id = str(uuid.uuid4())

    def add_friend(self, friend: 'Person') -> None:
        """добавление друга"""
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def born_in(self) -> dt.datetime:
        return self._born_in

    @property
    def friends(self) -> List['Person']:
        """копия списка друзей"""
        return self._friends.copy()


def encode_person_functional_correct(obj: Person) -> bytes:
    """функциональный стиль БЕЗ нарушения инкапсуляции"""
    visited: Set[str] = set()
    objects: Dict[str, Dict] = {}

    def collect_objects(current_obj: Person):
        if current_obj._id in visited:
            return

        visited.add(current_obj._id)
        # используем только публичные методы
        objects[current_obj._id] = {
            'name': current_obj.name,
            'born_in': current_obj.born_in.isoformat(),
            'friends': [friend._id for friend in current_obj.friends]
        }

        for friend in current_obj.friends:
            collect_objects(friend)

    collect_objects(obj)

    data = {
        'objects': objects,
        'root_id': obj._id
    }
    return json.dumps(data, indent=2).encode('utf-8')


def decode_person_functional_correct(data: bytes) -> Person:
    """функциональный стиль БЕЗ нарушения инкапсуляции"""
    json_data = json.loads(data.decode('utf-8'))
    objects_data = json_data['objects']
    root_id = json_data['root_id']

    # создаём объекты через конструктор
    objects: Dict[str, Person] = {}
    for obj_id, obj_data in objects_data.items():
        born_in = dt.datetime.fromisoformat(obj_data['born_in'])
        person = Person(obj_data['name'], born_in)
        person._id = obj_id
        objects[obj_id] = person

    for obj_id, obj_data in objects_data.items():
        person = objects[obj_id]
        for friend_id in obj_data['friends']:
            friend = objects[friend_id]
            person.add_friend(friend)

    return objects[root_id]


def encode_person_functional_incorrect(obj: Person) -> bytes:
    """функциональный стиль С нарушением инкапсуляции"""
    visited: Set[str] = set()
    objects: Dict[str, Dict] = {}

    def collect_objects(current_obj: Person):
        if current_obj._id in visited:
            return

        visited.add(current_obj._id)
        # нарушение инкапсуляции - прямой доступ к приватным атрибутам
        objects[current_obj._id] = {
            'name': current_obj._name,
            'born_in': current_obj._born_in.isoformat(),
            'friends': [friend._id for friend in current_obj._friends]
        }

        for friend in current_obj._friends:
            collect_objects(friend)

    collect_objects(obj)

    data = {
        'objects': objects,
        'root_id': obj._id
    }
    return json.dumps(data, indent=2).encode('utf-8')


def decode_person_functional_incorrect(data: bytes) -> Person:
    """функциональный стиль С нарушением инкапсуляции"""
    json_data = json.loads(data.decode('utf-8'))
    objects_data = json_data['objects']
    root_id = json_data['root_id']

    # создаём объекты через конструктор
    objects: Dict[str, Person] = {}
    for obj_id, obj_data in objects_data.items():
        born_in = dt.datetime.fromisoformat(obj_data['born_in'])
        person = Person(obj_data['name'], born_in)
        person._id = obj_id
        objects[obj_id] = person

    # восстанавливаем связи с прямым доступом
    for obj_id, obj_data in objects_data.items():
        person = objects[obj_id]
        person._friends = []  # прямой доступ
        for friend_id in obj_data['friends']:
            friend = objects[friend_id]
            person._friends.append(friend)  # прямой доступ

    return objects[root_id]


if __name__ == "__main__":
    p1 = Person("Kirill", dt.datetime(2006, 7, 27))
    p2 = Person("Alina", dt.datetime(2006, 8, 28))
    p1.add_friend(p2)

    print("функциональный стиль БЕЗ нарушения инкапсуляции")

    encoded_correct = encode_person_functional_correct(p1)
    recreated_p1_correct = decode_person_functional_correct(encoded_correct)

    print(f"Имя: {recreated_p1_correct.name}")
    print(f"Родился: {recreated_p1_correct.born_in.date()}")
    print(f"Друзей: {len(recreated_p1_correct.friends)}")
    if recreated_p1_correct.friends:
        print(f"Имя друга: {recreated_p1_correct.friends[0].name}")

    print("\nфункциональный стиль С нарушением инкапсуляции")

    encoded_incorrect = encode_person_functional_incorrect(p1)
    recreated_p1_incorrect = decode_person_functional_incorrect(encoded_incorrect)

    print(f"Имя: {recreated_p1_incorrect._name}")
    print(f"Родился: {recreated_p1_incorrect.born_in.date()}")
    print(f"Друзей: {len(recreated_p1_incorrect._friends)}")
    if recreated_p1_incorrect._friends:
        print(f"Имя друга: {recreated_p1_incorrect._friends[0]._name}")



    # Функциональный стиль без нарушения инкапсуляции:
    #   Отличия от других подходов:
    #     • Использует чистые функции без состояния
    #     • Не создает специализированных классов-сериализаторов
    #     • Более декларативный стиль программирования
    #     • Соблюдает инкапсуляцию через использование публичного API
    #   Проблемы и особенности:
    #     • Масштабируемость: Сложнее добавлять новую функциональность
    #     • Повторное использование: Функции труднее расширять через наследование
    #     • Управление состоянием: При сложной логике может потребоваться много параметров
    #     • Тестируемость: Хотя функции легче тестировать, сложные рекурсивные функции могут затруднить работу


    # Функциональный стиль с нарушением инкапсуляции:
    #   Отличия от других подходов:
    #     • Сочетает функциональный стиль с прямым доступом к данным
    #     • Использует конструктор для создания объектов, но нарушает инкапсуляцию при восстановлении связей
    #     • Промежуточный подход между чистым ФП и ООП
    #   Проблемы и особенности:
    #     • Гибридность: Сочетает преимущества и недостатки обоих подходов
    #     • Нарушение контракта класса: Прямой доступ к приватным атрибутам _friends
    #     • Непоследовательность: Использует конструктор, но обходит методы класса

    #     • Сложность отладки: Проблемы могут проявляться не сразу
