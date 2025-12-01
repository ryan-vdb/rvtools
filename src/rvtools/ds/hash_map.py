class HashMap:
    def __init__(self):
        self._key_to_val = {}
        self._val_to_key = {}

    def append(self, key, value=None):
        if value is None and isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError("Tuple must be length 2 (key, value)")
            key, value = key

        if value is None:
            raise ValueError("append expects either (key, value) or key, value")

        if key in self._key_to_val:
            raise KeyError(f"Key {key} already exists.")
        if value in self._val_to_key:
            raise KeyError(f"Value {value} already exists.")

        self._key_to_val[key] = value
        self._val_to_key[value] = key

    def get_val(self, key):
        return self._key_to_val.get(key)

    def get_key(self, value):
        return self._val_to_key.get(value)

    def remove_key(self, key):
        if key not in self._key_to_val:
            raise KeyError(key)
        value = self._key_to_val.pop(key)
        self._val_to_key.pop(value)

    def remove_val(self, value):
        if value not in self._val_to_key:
            raise KeyError(value)
        key = self._val_to_key.pop(value)
        self._key_to_val.pop(key)

    def __len__(self):
        return len(self._key_to_val)

    def __contains__(self, key):
        return key in self._key_to_val

    def keys(self):
        return list(self._key_to_val.keys())

    def values(self):
        return list(self._key_to_val.values())

    def items(self):
        return list(self._key_to_val.items())

    def __repr__(self):
        return f"HashMap({self._key_to_val})"