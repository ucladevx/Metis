

class MajorGraph:

    def __init__(self):
        
        self.m_vertices = {}
    
    # add edge so course "u" unlocks course "v"
    def add_edge(self, u, v):
        # print(u)
        # print(v)
        vertices = self.m_vertices
        if u not in vertices or v not in vertices:
            # print(u + " or " + v + " not found in graph")
            return
        if v not in vertices[u]:
            vertices[u].append(v) # => u unlocks v
        return
    
    # add course "vert"
    def add_vertex(self, vert):
        vertices = self.m_vertices
        if vert in vertices:
            return
        else:
            vertices[vert] = []

    # prints all of the courses that course "cl" unlocks
    def print_unlocks(self, cl):
        vertices = self.m_vertices
        if cl not in vertices:
            print(cl + " not found as major requirement")
            return
        for vert in vertices[cl]:
            print(vert)

    # PRINT FUNCTIONS

    # prints all classes in the graph
    def print_vertices(self):
        for vert in self.m_vertices:
            print(vert)

    # prints all the edges in the graph (requirement relationships)
    def print_edges(self):
        for u in self.m_vertices:
            for v in self.m_vertices[u]:
                print(u + " unlocks " + v)