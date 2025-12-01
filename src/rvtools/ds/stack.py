class Stack:
    def __init__(self):
        self.data = []

    def push(self, val):                # O(1)
        self.data.append(val)

    def pop(self):                      # O(1)
        if not self.data:
            raise IndexError("Stack is Empty.")
        return self.data.pop()
    
    def peek(self):                     # O(1)
        if not self.data:
            raise IndexError("Stack is Empty.")
        return self.data[-1]
    
    def is_empty(self):
        return len(self.data) == 0
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f"Stack({self.data})"