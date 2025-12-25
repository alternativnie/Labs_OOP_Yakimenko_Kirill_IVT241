from typing import List, Union
from numbers import Number

class Matrix:

    def __init__(self, data: List[List[float]]) -> None:
        """создаём матрицу из двумерного списка"""
        if not data or not data[0]:
            raise ValueError("ne pystyu martix")

        cols = len(data[0])
        if not all(len(row) == cols for row in data):
            raise ValueError("stroci dolgni bit odinacovi dlini")

        self._data = data
        self._rows = len(data)
        self._cols = cols

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def data(self) -> List[List[float]]:
        """копия данных матрицы """
        return [row.copy() for row in self._data]

    def __add__(self, other: 'Matrix') -> 'Matrix':
        """+ матриц"""
        if not isinstance(other, Matrix):
            return NotImplemented

        if self._rows != other._rows or self._cols != other._cols:
            raise ValueError("nyjni odinacovi razmeri")

        result = [
            [self._data[i][j] + other._data[i][j] for j in range(self._cols)]
            for i in range(self._rows)
        ]
        return Matrix(result)

    def __mul__(self, other: Union['Matrix', Number]) -> 'Matrix':
        # умножение матрицы на матрицу или скаляр справа
        if isinstance(other, Number):
            # умножение на скаляр
            return Matrix([
                [elem * other for elem in row]
                for row in self._data
            ])

        if isinstance(other, Matrix):
            if self._cols != other._rows:
                raise ValueError("oshibka razmerovv")

            result = [[0] * other._cols for _ in range(self._rows)]
            for i in range(self._rows):
                for j in range(other._cols):
                    for k in range(self._cols):
                        result[i][j] += self._data[i][k] * other._data[k][j]
            return Matrix(result)

        return NotImplemented

    def __rmul__(self, other: Number) -> 'Matrix':
        """умножение скаляра на матрицу справа"""
        return self * other

    def transpose(self) -> 'Matrix':
        """транспонирование матрицы"""
        return Matrix([
            [self._data[j][i] for j in range(self._rows)]
            for i in range(self._cols)
        ])

    def __str__(self) -> str:
        """для вывода"""
        return '\n'.join(
            '[' + ' '.join(f'{elem:6.1f}' for elem in row) + ']'
            for row in self._data
        )


if __name__ == "__main__":

    m1 = Matrix([[1, 2], [2, 3]])
    m2 = Matrix([[2, 5], [7, 9]])

    print("m1:")
    print(m1)
    print("\nm2:")
    print(m2)

    m3 = m1 + m2
    m4 = m1 * m2
    m5 = m1.transpose()

    print("\nm1 + m2:")
    print(m3)
    print("\nm1 * m2:")
    print(m4)
    print("\nm1.transpose():")
    print(m5)

    print("\nm1 * 3:")
    print(m1 * 3)

    print("\n3 * m1:")
    print(3 * m1)