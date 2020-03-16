class SocialGraph:
    """ Social graph used for suggesting friends """
    def __init__(self):
        # adjacency list
        self.adj_dict = {}
        self.num_nodes = 0

    def __contains__(self, key):
        return key in self.adj_dict

    def add_friend_node(self, key):
        self.num_nodes = self.num_nodes + 1
        self.adj_dict[key] = []

    def get_friend_connections(self, key):
        # get the edges
        return self.adj_dict.get(key, [])

    def add_friend_edge(self, node, val):
        if node not in self.adj_dict:
            self.add_node(node)
        self.adj_dict[node].append(val)

    def get_nodes(self):
        return self.adj_dict.keys()

    def get_adj_list(self):
        return self.adj_dict
