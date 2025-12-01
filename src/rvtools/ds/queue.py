class Queue:
    def __init__(self):
        self._in = []
        self.out = []

    def enqueue(self, val):             # O(1)
        self._in.append(val)

    def dequeue(self):                  # O(1)
        if self.is_empty():
            raise IndexError("Queue is Empty.")
        
        if not self.out:
            while self._in:
                self.out.append(self._in.pop())
        
        return self.out.pop()

    def peek(self):                     # O(1)
        if self.is_empty():
            raise IndexError("Queue is Empty.")
        
        if not self.out:
            while self._in:
                self.out.append(self._in.pop())
        
        return self.out[-1]
    
    def is_empty(self):
        return len(self._in) == 0 and len(self.out) == 0

    def __len__(self):
        return len(self._in) + len(self.out)

    def __repr__(self):
        out_copy = list(reversed(self.out))
        in_copy = self._in.copy()
        return f"Queue({out_copy + in_copy})"