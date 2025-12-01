class LLNode:
    def __init__(self, data):
        self.data = data
        self.next: LLNode = None
    
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):             # O(n)
        new_node = LLNode(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        
        current.next = new_node
    
    def prepend(self, data):            # O(1)
        new_node = LLNode(data)
        new_node.next = self.head
        self.head = new_node
    
    def insert(self, idx, data):        # O(n)
        new_node = LLNode(data)

        if idx == 0:
            self.prepend(data)
            return
        
        current = self.head
        current_idx = 0

        while current is not None and current_idx < idx - 1:
            current = current.next
            current_idx += 1
        
        if current == None:
            raise IndexError("Index out of Range")
        
        new_node.next = current.next
        current.next = new_node

    def delete_val(self, val):          # O(n)
        if self.head is None:
            return

        if self.head.data == val:
            self.head = self.head.next
            return

        current = self.head

        while current.next is not None and current.next.data != val:
            current = current.next
        
        if current.next is None:
            return
        
        node_del = current.next
        current.next = node_del.next
    
    def delete_idx(self, idx):
        if idx == 0:
            self.head = self.head.next
            return

        current = self.head
        current_idx = 0

        if current is not None and current_idx < idx - 1:
            current = current.next
            current_idx += 1
        
        if current is None or current.next is None:
            raise IndexError("Index out of Range")
        
        current.next = current.next.next
    
    def contains_val(self, val):        # O(n)
        current = self.head

        while current is not None:
            if current.data == val:
                return True
            current = current.next
        
        return False
    
    def reverse(self):                  # O(n)
        prev = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev
    
    def length(self):                   # O(n)
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count
    
    def get(self, idx):                 # O(n)
        current = self.head
        current_idx = 0

        while current is not None:
            if current_idx == idx:
                return current.data
            current = current.next
            current_idx += 1
        
        raise IndexError("Index out of Range")
     
    def find_middle(self):              # O(n)
        slow = self.head
        fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow.data if slow else None
    
    def get_reverse(self, idx):         # O(n)
        first = self.head
        second = self.head

        for _ in range(idx):
            if first is None:
                return None
            first = first.next
        
        while first:
            first = first.next
            second = second.next
        
        return second.data if second else None

    def is_cycle(self):                 # O(n)
        slow = self.head
        fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
    
    def to_list(self):                  # O(n)
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def from_list(self, values):        # O(n)
        for v in values:
            self.append(v)

    def remove_duplicates(self):        # O(n^2)
        current = self.head
        while current:
            runner = current
            while runner.next:
                if runner.next.data == current.data:
                    runner.next = runner.next.next
                else:
                    runner = runner.next
            current = current.next
        
    def get_tail(self):                 # O(n)
        current = self.head
        if not current:
            return None
        while current.next:
            current = current.next
        return current
    
    def clear(self):                    # O(1)
        self.head = None

    def __contains__(self, val):
        return self.contains_val(val)
    
    def __len__(self):
       return self.length()

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self):
        return " -> ".join(str(x) for x in self) + " -> None"