class BTNode:
    def __init__(self, data):
        self.data = data
        self.left: BTNode = None
        self.right: BTNode = None

class BinaryTree:
    def __init__(self):
        self.head = None
        self.size = 0
  
    def append(self, data):             # O(log n)        
        new_node = BTNode(data)
        self.size += 1

        if self.head is None:
            self.head = new_node
            return
        
        current = self.head
        while True:
            if data < current.data:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
        
    def contains_val(self, val):        # O(log n)
        current = self.head
        while current is not None:
            if val == current.data:
                return True
            elif val < current.data:
                current = current.left
            else:
                current = current.right
        return False
    
    def min(self):                      # O(log n)
        if self.head is None:
            raise ValueError("Tree is Empty.")
        current = self.head
        while current.left is not None:
            current = current.left
        return current.data
    
    def max(self):                      # O(log n)
        if self.head is None:
            raise ValueError("Tree is Empty.")
        current = self.head
        while current.right is not None:
            current = current.right
        return current.data
    
    def inorder(self):                  # O(n)
        result = []

        def _inorder(node):
            if node is None:
                return
            _inorder(node.left)
            result.append(node.data)
            _inorder(node.right)

        _inorder(self.head)
        return result
    
    def to_sorted_list(self):
        return self.inorder()
    
    def preorder(self):                 # O(n)
        result = []

        def _preorder(node):
            if node is None:
                return
            result.append(node.data)
            _preorder(node.left)
            _preorder(node.right)
        
        _preorder(self.head)
        return result
    
    def to_list(self):
        return self.preorder()

    def postorder(self):                # O(n)
        result = []

        def _postorder(node):
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            result.append(node.data)
        
        _postorder(self.head)
        return result
    
    def height(self):                   # O(n)
        def _height(node):
            if node is None:
                return 0
            left_h = _height(node.left)
            right_h = _height(node.right)
            return 1 + max(left_h, right_h)
        
        return _height(self.head)
    
    def is_balanced(self):              # O(n)
        def _check(node):
            if node is None:
                return 0, True
            
            left_h, left_bal = _check(node.left)
            right_h, right_bal = _check(node.right)

            height = 1 + max(left_h, right_h)
            balanced = (
                left_bal
                and right_bal
                and abs(left_h - right_h) <= 1
            )
            return height, balanced
        
        _, balanced = _check(self.head)
        return balanced 
    
    def delete(self, val):              # O(log n)
        def _delete(node, val):
            if node is None:
                return None
            
            if val < node.data:
                node.left = _delete(node.left, val)
                return node
            elif val > node.data:
                node.right = _delete(node.right, val)
                return node
            
            if node.left is None and node.right is None:
                return None
            
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            successor = node.right
            while successor.left is not None:
                successor = successor.left

            node.data = successor.data

            node.right = _delete(node.right, successor.data)

            return node
        
        self.head = _delete(self.head, val)

    def balance(self):                  # O(n)
        vals = self.inorder()

        def build_balanced(sorted_vals):
            if not sorted_vals:
                return None

            mid = len(sorted_vals) // 2
            node = BTNode(sorted_vals[mid])
            node.left = build_balanced(sorted_vals[:mid])
            node.right = build_balanced(sorted_vals[mid+1:])
            return node

        self.head = build_balanced(vals)

    def clear(self):                    # O(1)
        self.head = 0
        self.size = 0
    
    def pretty_print(self):
        def _print(node, indent="", last=True):
            if node is None:
                return
            
            print(indent, "`- " if last else "|- ", node.data, sep="")

            indent += "   " if last else "|  "

            has_left = node.left is not None
            has_right = node.right is not None

            if not has_left and not has_right:
                return

            _print(node.left, indent, False)
            _print(node.right, indent, True)

        _print(self.head)
                
    def __contains__(self, val):
        return self.contains_val(val)
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return iter(self.inorder())
    
    def __str__(self):
        return "BinaryTree(" + ", ".join(str(x) for x in self.inorder()) + ")"