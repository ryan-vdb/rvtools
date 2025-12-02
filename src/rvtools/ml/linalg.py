class Vector:
    def __init__(self, data):
        self._data = list(data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, idx):
        return self._data[idx]

    def __setitem__(self, idx, value):
        self._data[idx] = value

    def to_list(self):
        return list(self._data)

    def copy(self):
        return Vector(self._data)

    def __repr__(self):
        return f"Vector({self._data})"
    
    def _check_same_length(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length.")

    def __add__(self, other):
        self._check_same_length(other)
        return Vector(a + b for a, b in zip(self, other))

    def __sub__(self, other):
        self._check_same_length(other)
        return Vector(a - b for a, b in zip(self, other))

    def __rmul__(self, scalar):
        return Vector(scalar * a for a in self)

    def __mul__(self, scalar):
        return Vector(scalar * a for a in self)
    
    def dot(self, other):
        """Dot product self · other."""
        self._check_same_length(other)
        return sum(a * b for a, b in zip(self, other))

    def l2_norm(self):
        """Euclidean norm."""
        return (sum(a * a for a in self)) ** 0.5

    def l1_norm(self):
        """Manhattan norm."""
        return sum(abs(a) for a in self)

    def euclidean_distance(self, other):
        self._check_same_length(other)
        return ((self - other).l2_norm())

    def manhattan_distance(self, other):
        self._check_same_length(other)
        return ((self - other).l1_norm())

    def cosine_similarity(self, other):
        self._check_same_length(other)
        denom = self.l2_norm() * Vector(other).l2_norm()
        if denom == 0:
            raise ValueError("Cannot compute cosine similarity with zero vector.")
        return self.dot(other)

class Matrix:
    """
    Simple 2D matrix wrapper over a list of lists (row-major).

    - rows: list of row vectors (python lists)
    - len(M) -> number of rows
    - M[i][j] indexing
    - M.shape -> (rows, cols)
    - Matrix * Vector -> Vector (matrix-vector product)
    - Matrix @ Matrix -> Matrix (matrix-matrix product)
    - M.T() -> transpose
    """

    def __init__(self, rows):
        if not rows:
            raise ValueError("Matrix requires at least one row.")
        # ensure rectangular
        row_lengths = {len(r) for r in rows}
        if len(row_lengths) != 1:
            raise ValueError("All rows must have the same length.")
        self._rows = [list(r) for r in rows]  # deep copy

    # --- basic protocol ---

    def __len__(self):
        # number of rows
        return len(self._rows)

    @property
    def nrows(self):
        return len(self._rows)

    @property
    def ncols(self):
        return len(self._rows[0])

    @property
    def shape(self):
        return (self.nrows, self.ncols)

    def __getitem__(self, idx):
        # row indexing: M[i] is the i-th row (as list)
        return self._rows[idx]

    def __setitem__(self, idx, value):
        if len(value) != self.ncols:
            raise ValueError("Assigned row must have the correct number of columns.")
        self._rows[idx] = list(value)

    def to_lists(self):
        return [list(r) for r in self._rows]

    def copy(self):
        return Matrix(self._rows)

    def __repr__(self):
        return f"Matrix(rows={self._rows})"

    # --- basic operations ---

    def T(self):
        """Transpose: returns a new Matrix."""
        transposed = []
        for j in range(self.ncols):
            col = [self._rows[i][j] for i in range(self.nrows)]
            transposed.append(col)
        return Matrix(transposed)

    def matvec(self, vec):
        """Matrix-vector product: M @ v -> Vector."""
        if isinstance(vec, Vector):
            v_list = vec.to_list()
        else:
            v_list = list(vec)

        if len(v_list) != self.ncols:
            raise ValueError("Vector length must match number of matrix columns.")

        result = []
        for row in self._rows:
            s = 0
            for a, b in zip(row, v_list):
                s += a * b
            result.append(s)
        return Vector(result)

    def matmat(self, other):
        """Matrix-matrix product: M @ N -> Matrix."""
        if not isinstance(other, Matrix):
            raise TypeError("matmat expects a Matrix.")

        if self.ncols != other.nrows:
            raise ValueError("Inner dimensions must agree for matrix multiplication.")

        other_T = other.T()
        new_rows = []
        for row in self._rows:
            new_row = []
            for col in other_T._rows:
                s = 0
                for a, b in zip(row, col):
                    s += a * b
                new_row.append(s)
            new_rows.append(new_row)
        return Matrix(new_rows)

    def __matmul__(self, other):
        """Use M @ v or M @ N syntax."""
        if isinstance(other, (Vector, list, tuple)):
            return self.matvec(other)
        elif isinstance(other, Matrix):
            return self.matmat(other)
        else:
            raise TypeError("Unsupported operand for @ with Matrix.")

    # simple elementwise add/sub if you want them

    def add(self, other):
        """Elementwise matrix addition: M + N (same shape)."""
        if not isinstance(other, Matrix):
            raise TypeError("add expects a Matrix.")
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape.")

        rows = []
        for r1, r2 in zip(self._rows, other._rows):
            rows.append([a + b for a, b in zip(r1, r2)])
        return Matrix(rows)

    def subtract(self, other):
        """Elementwise matrix subtraction: M - N (same shape)."""
        if not isinstance(other, Matrix):
            raise TypeError("subtract expects a Matrix.")
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape.")

        rows = []
        for r1, r2 in zip(self._rows, other._rows):
            rows.append([a - b for a, b in zip(r1, r2)])
        return Matrix(rows)

def _as_vector(x):
    return x if isinstance(x, Vector) else Vector(x)

def dot(x, y):
    return _as_vector(x).dot(_as_vector(y))

def add(x, y):
    xv = _as_vector(x)
    yv = _as_vector(y)
    xv._check_same_length(yv)
    return (xv + yv).to_list()

def subtract(x, y):
    xv = _as_vector(x)
    yv = _as_vector(y)
    xv._check_same_length(yv)
    return (xv - yv).to_list()

def scalar_mul(s, x):
    return (s * _as_vector(x)).to_list()

def l2_norm(x):
    return _as_vector(x).l2_norm()

def l1_norm(x):
    return _as_vector(x).l1_norm()

def euclidean_distance(x, y):
    return _as_vector(x).euclidean_distance(_as_vector(y))

def manhattan_distance(x, y):
    return _as_vector(x).manhattan_distance(_as_vector(y))

def mean_vector(vectors):
    """
    Elementwise mean of a list of vectors (lists or Vectors).
    """
    vectors = [ _as_vector(v).to_list() for v in vectors ]
    if not vectors:
        raise ValueError("mean_vector() requires at least one vector.")
    n = len(vectors[0])
    for v in vectors:
        if len(v) != n:
            raise ValueError("All vectors must have the same length.")

    sums = [0.0] * n
    count = len(vectors)

    for v in vectors:
        for i, val in enumerate(v):
            sums[i] += val

    return [s / count for s in sums]

def cosine_similarity(x, y):
    return _as_vector(x).cosine_similarity(_as_vector(y))