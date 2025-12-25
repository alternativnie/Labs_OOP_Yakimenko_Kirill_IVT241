from typing import List, Union, Tuple
from copy import deepcopy
from numbers import Number

def create_matrix(data: List[List[float]]) -> Tuple[List[List[float]], int, int]:
    """создаём матрицу из двумерного списка"""
    if not data or not data[0]:
        raise ValueError("матрица не должна ббыть пустой")

    rows = len(data)
    cols = len(data[0])

    if not all(len(row) == cols for row in data):
        raise ValueError("все строки должны быть одинаковой длины")

    return deepcopy(data), rows, cols

def matrix_add(m1: List[List[float]], r1: int, c1: int,
               m2: List[List[float]], r2: int, c2: int) -> Tuple[List[List[float]], int, int]:
    """сложение матриц"""
    if r1 != r2 or c1 != c2:
        raise ValueError("матрицы должны быть одного размера")

    result = [[m1[i][j] + m2[i][j] for j in range(c1)] for i in range(r1)]
    return result, r1, c1

def matrix_multiply(m1: List[List[float]], r1: int, c1: int,
                    m2: List[List[float]], r2: int, c2: int) -> Tuple[List[List[float]], int, int]:
    """умножение матриц"""
    if c1 != r2:
        raise ValueError("несовместимые размеры")

    result = [[0] * c2 for _ in range(r1)]
    for i in range(r1):
        for j in range(c2):
            for k in range(c1):
                result[i][j] += m1[i][k] * m2[k][j]

    return result, r1, c2

def matrix_scalar_multiply(matrix: List[List[float]], rows: int, cols: int,
                           scalar: Union[int, float]) -> Tuple[List[List[float]], int, int]:
    """умножение матрицы на скаляр"""
    result = [[matrix[i][j] * scalar for j in range(cols)] for i in range(rows)]
    return result, rows, cols

def matrix_transpose(matrix: List[List[float]], rows: int, cols: int) -> Tuple[List[List[float]], int, int]:
    """транспонирование матрицы"""
    result = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
    return result, cols, rows


def matrix_to_str(matrix: List[List[float]]) -> str:
    """вывод матрицы"""
    rows_str = []
    for row in matrix:
        row_str = "  ".join(f"{elem:6}" for elem in row)
        rows_str.append(f"[{row_str}]")
    return "\n".join(rows_str)



if __name__ == "__main__":

    m1, r1, c1 = create_matrix([[1, 2], [2, 3]])
    m2, r2, c2 = create_matrix([[2, 5], [7, 9]])

    print(f"m1 ({r1}x{c1}) = ")
    print(matrix_to_str(m1))
    print(f"\nm2 ({r2}x{c2}) = ")
    print(matrix_to_str(m2))

    m3, r3, c3 = matrix_add(m1, r1, c1, m2, r2, c2)
    print(f"\nm1 + m2 = ")
    print(matrix_to_str(m3))

    m4, r4, c4 = matrix_multiply(m1, r1, c1, m2, r2, c2)
    print(f"\nm1 * m2 = ")
    print(matrix_to_str(m4))

    m5, r5, c5 = matrix_scalar_multiply(m1, r1, c1, 3)
    print(f"\nm1 * 3 = ")
    print(matrix_to_str(m5))

    m6, r6, c6 = matrix_transpose(m1, r1, c1)
    print(f"\nm1.transpose() = ")
    print(matrix_to_str(m6))
