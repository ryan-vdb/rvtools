class Vertex:
    def __init__(self, id, data=None):
        self.id = id
        self.data = data

    def __repr__(self):
        return f"Vertex({self.id}, data={self.data})"

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"Edge({self.start.id} -> {self.end.id})"


class Graph:
    def __init__(self, directed=False):
        self.vertices = {}
        self.edges = []
        self.directed = directed

    def add_vertex(self, id, data=None):# O(1)
        if id not in self.vertices:
            v = Vertex(id, data)
            self.vertices[id] = v
        return self.vertices[id]
    
    def add_edge(self, start, end):     # O(1)
        if start not in self.vertices:
            raise ValueError(f"Start Vertex '{start}' Not Found.")
        if end not in self.vertices:
            raise ValueError(f"End Vertex '{end}' Not Found.")
        
        e = Edge(self.vertices[start], self.vertices[end])
        self.edges.append(e)

        if not self.directed:
            e_rev = Edge(self.vertices[end], self.vertices[start])
            self.edges.append(e_rev)
        
        return e
    
    def outgoing(self, id):             # O(E)
        if id not in self.vertices:
            raise ValueError(f"Vertex '{id}' Not Found.")
        return [e.end for e in self.edges if e.start.id == id]
    
    def following(self, id):
        return self.outgoing(id)
    
    def incoming(self, id):             # O(E)
        if id not in self.vertices:
            raise ValueError(f"Vertex '{id}' Not Found.")
        return [e.start for e in self.edges if e.end.id == id]
    
    def followers(self, id):
        return self.incoming(id)
    
    def connections(self, id):          # O(E)
        inc = self.incoming(id)
        out = self.outgoing(id)

        combined = inc + [v for v in out if v not in inc]
        return combined
    
    def neighbors(self, id):
        return self.connections(id)
    
    def bfs(self, start_id):            # O(V*E)
        if start_id not in self.vertices:
            return []
        
        visited = set()
        order = []

        queue = [start_id]
        front = 0
        visited.add(start_id)

        while front < len(queue):
            vid = queue[front]
            front += 1
            order.append(vid)

            for neighbor_vertex in self.outgoing(vid):
                nid = neighbor_vertex.id
                if nid not in visited:
                    visited.add(nid)
                    queue.append(nid)
            
        return order

    def dfs(self, start_id):            # O(V*E)
        if start_id not in self.vertices:
            return []
        
        visited = set()
        order = []
        stack = [start_id]

        while stack:
            vid = stack.pop()
            if vid in visited:
                continue

            visited.add(vid)
            order.append(vid)

            neighbors = self.outgoing(vid)
            for neighbor_vertex in reversed(neighbors):
                nid = neighbor_vertex.id
                if nid not in visited:
                    stack.append(nid)
        
        return order
    
    def shortest_path_bfs(self, start_id, goal_id): # O(V*E)

        if start_id not in self.vertices or goal_id not in self.vertices:
            return []
        
        from_parent = {start_id: None}
        visited = set([start_id])

        queue = [start_id]
        front = 0

        found = False

        while front < len(queue):
            vid = queue[front]
            front += 1

            if vid == goal_id:
                found = True
                break

            for neighbor_vertex in self.outgoing(vid):
                nid = neighbor_vertex.id
                if nid not in visited:
                    visited.add(nid)
                    from_parent[nid] = vid
                    queue.append(nid)

        if not found:
            return []
            
        path = []
        cur = goal_id
        while cur is not None:
            path.append(cur)
            cur = from_parent[cur]
        path.reverse()
        return path
    
    def __repr__(self):
        return f"Graph(directed={self.directed}, vertices={list(self.vertices.keys())}, edges={len(self.edges)})"
        

