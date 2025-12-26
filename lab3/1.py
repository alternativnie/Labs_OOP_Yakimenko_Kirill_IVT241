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

class PersonEncoderPrivate:
    """кодировщик безнарушений инкапсуляции"""

    def encode(self, obj: Person) -> bytes:
        """сериализация с использованием только публичных методов"""
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


class PersonDecoderPrivate:

    def decode(self, data: bytes) -> Person:
        """десериализация с созданием объектов через конструктор"""
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


#нарушение инкапсуляции
class PersonEncoderPublic:
    """кодировщик С нарушением инкапсуляции"""

    def encode(self, obj: Person) -> bytes:
        """сериализация с прямым доступом к приватным атрибутам"""
        visited: Set[str] = set()
        objects: Dict[str, Dict] = {}

        def collect_objects(current_obj: Person):
            if current_obj._id in visited:
                return

            visited.add(current_obj._id)
            # нарушниее инкапсуляции - прямой доступ к приватным атрибутам
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


class PersonDecoderPublic:
    """С нарушением инкапсуляции"""

    def decode(self, data: bytes) -> Person:
        """десериализация с прямым доступом к приватным атрибутам"""
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
            person._friends = []  #прямой доступ
            for friend_id in obj_data['friends']:
                friend = objects[friend_id]
                person._friends.append(friend)

        return objects[root_id]


if __name__ == "__main__":
    p1 = Person("Kirill", dt.datetime(2006, 7, 27))
    p2 = Person("Alina", dt.datetime(2006, 8, 28))
    p1.add_friend(p2)

    print("без нарушения инкапсуляции")
    encoder_private = PersonEncoderPrivate()
    decoder_private = PersonDecoderPrivate()

    encoded_private = encoder_private.encode(p1)
    recreated_p1_private = decoder_private.decode(encoded_private)

    print(f"Имя: {recreated_p1_private.name}")
    print(f"Родился: {recreated_p1_private.born_in.date()}")
    print(f"Друзей: {len(recreated_p1_private.friends)}")
    print(f"Имена друзей: {recreated_p1_private.friends[0].name}")

    print("\nнарушением инкапсуляции")
    encoder_public = PersonEncoderPublic()
    decoder_public = PersonDecoderPublic()

    encoded_public = encoder_public.encode(p1)
    recreated_p1_public = decoder_public.decode(encoded_public)

    print(f"Имя: {recreated_p1_public._name}")
    print(f"Родился: {recreated_p1_public.born_in.date()}")
    print(f"Друзей: {len(recreated_p1_public._friends)}")
    print(f"Имена друзей: {recreated_p1_public._friends[0]._name}")


# ООП стиль без нарушения инкапсуляции:
#   Отличия от других подходов:
#     • Полностью соблюдает принципы ООП, используя только публичный интерфейс класса
#     • Требует наличия property-методов в исходном классе
#     • Наиболее "чистый" с точки зрения объектно-ориентированного дизайна
#   Проблемы и особенности:
#     • Производительность: Медленнее из-за вызовов методов и копирования списков
#     • Зависимость от API: Требует, чтобы класс предоставлял достаточный публичный интерфейс
#     • Ограниченность: Не может сериализовать объекты без необходимых property-методов
#     • Избыточность: Для простых случаев может создавать много "оберток

# ООП стиль с нарушением инкапсуляции:
#   Отличия от других подходов:
#     • Прямой доступ к приватным атрибутам через _name, _friends, _born_in
#     • Не требует наличия публичного API у сериализуемого класса
#     • Более "прагматичный" подход
#   Проблемы и особенности:
#     • Хрупкость: Ломается при изменении внутренней структуры класса
#     • Нарушение инкапсуляции: Прямой доступ к данным, которые должны быть скрыты
#     • Безопасность: Может обойти валидацию и бизнес-логику, реализованную в методах
#     • Технический долг: Создает скрытые зависимости от реализации