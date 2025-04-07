import math
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QHeaderView, QFrame
)
from PyQt5.QtGui import QColor, QFont


# === Mathematische Hilfsfunktionen ===
def is_close_to_int(x, tol=1e-6):
    return abs(x - round(x)) < tol

def is_prime_approx(x):
    if not is_close_to_int(x):
        return False
    n = round(x)
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# === Matrixoperationen ===
def matmul(A, B):
    n = len(A)
    result = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = sum(A[i][k]*B[k][j] for k in range(n))
    return result

def transpose(M):
    return [list(row) for row in zip(*M)]

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def norm(v):
    return math.sqrt(sum(x * x for x in v))

def householder_vector(x):
    e = [0.0] * len(x)
    e[0] = norm(x)
    u = [x[i] - e[i] for i in range(len(x))]
    norm_u = norm(u)
    return [u_i / norm_u for u_i in u] if norm_u != 0 else x

def householder_matrix(v):
    n = len(v)
    H = identity(n)
    for i in range(n):
        for j in range(n):
            H[i][j] -= 2 * v[i] * v[j]
    return H

def extend_to_full(H, n, k):
    Q = identity(n)
    for i in range(k+1, n):
        for j in range(k+1, n):
            Q[i][j] = H[i-(k+1)][j-(k+1)]
    return Q

def to_hessenberg(A):
    n = len(A)
    H = [row[:] for row in A]
    for k in range(n - 2):
        x = [H[i][k] for i in range(k + 1, n)]
        v = householder_vector(x)
        Hv = householder_matrix(v)
        Q = extend_to_full(Hv, n, k)
        H = matmul(Q, matmul(H, transpose(Q)))
    return H


# === Beispielmatrix ===
A = [
    [2, 3, 5, 7],
    [11,13,17,19],
    [23,29,31,37],
    [41,43,47,53]
]

# === Transformation durchführen ===
H = to_hessenberg(A)
primes_with_pos = []

for i in range(len(H)):
    for j in range(len(H[i])):
        if is_prime_approx(H[i][j]):
            val = round(H[i][j])
            primes_with_pos.append((val, (i, j)))

primes_with_pos.sort()
primes_only = [val for val, _ in primes_with_pos]

for idx, (_, (i, j)) in enumerate(primes_with_pos):
    H[i][j] = primes_only[idx]


# === GUI-Klasse ===
class MatrixViewer(QWidget):
    def __init__(self, original, hessenberg, primes):
        super().__init__()
        self.setWindowTitle("Original vs. Hessenberg mit Primzahlen")

        layout = QHBoxLayout(self)

        # Tabelle: Originalmatrix
        orig_widget = self.create_matrix_widget(original, [], "Originalmatrix")
        layout.addWidget(orig_widget)

        # Trenner
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Tabelle: Hessenbergmatrix mit Primzahlen
        hess_widget = self.create_matrix_widget(hessenberg, [pos for _, pos in primes], "Hessenberg-Matrix")
        layout.addWidget(hess_widget)

        self.setLayout(layout)

    def create_matrix_widget(self, matrix, prime_positions, title):
        outer = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Arial", 10, QFont.Bold))
        outer.addWidget(label)

        n = len(matrix)
        table = QTableWidget(n, n)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(n):
            for j in range(n):
                val = round(matrix[i][j])
                item = QTableWidgetItem(str(val))
                if (i, j) in prime_positions:
                    item.setBackground(QColor("lightgreen"))
                table.setItem(i, j, item)

        outer.addWidget(table)
        wrapper = QWidget()
        wrapper.setLayout(outer)
        return wrapper


# === Startpunkt ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixViewer(A, H, primes_with_pos)
    window.resize(800, 400)
    window.show()
    sys.exit(app.exec_())
