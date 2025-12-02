import random

class Dataset:
    def __init__(self, X, y=None):
        X = list(X)
        if y is not None:
            y = list(y)
            if len(X) != len(y):
                raise ValueError("X and y must have the same length.")
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        if self.y is None:
            return self.X[idx], None
        return self.X[idx], self.y[idx]

    def features(self):
        return self.X

    def labels(self):
        return self.y

    def has_labels(self):
        return self.y is not None

    def subset(self, indices):
        X_sub = [self.X[i] for i in indices]
        if self.y is None:
            y_sub = None
        else:
            y_sub = [self.y[i] for i in indices]
        return Dataset(X_sub, y_sub)

    def shuffled(self, random_state=None):
        n = len(self.X)
        indices = list(range(n))
        rnd = random.Random(random_state)
        rnd.shuffle(indices)
        return self.subset(indices)

    def __repr__(self):
        n = len(self.X)
        labeled = self.y is not None
        return f"Dataset(n={n}, labeled={labeled})"


def tt_split(dataset, test_size=0.2, shuffle=True, random_state=None):
    if not isinstance(dataset, Dataset):
        raise TypeError("train_test_split expects a Dataset instance.")
    
    if not (0.0 < test_size < 1.0):
        raise ValueError("test_size must be between 0 and 1.")
    
    if shuffle:
        ds = dataset.shuffled(random_state=random_state)
    else:
        ds = dataset

    n = len(ds)
    if n == 0:
        raise ValueError("Cannot split empty dataset.")

    test_count = int(n * test_size)
    if test_count == 0:
        test_count = 1
    if test_count == n:
        test_count = n - 1

    indices = list(range(n))
    test_idx = indices[:test_count]
    train_idx = indices[test_count:]

    train_ds = ds.subset(train_idx)
    test_ds = ds.subset(test_idx)

    return train_ds, test_ds