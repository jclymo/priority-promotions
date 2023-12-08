from .util import node_token, priority_token, player_token, EDGE_MARKER, NODE_MARKER, INPUT_LINE, LINE_SUBTYPE_NODES, LINE_SUBTYPE_EDGES

def tokenize_graph(graph_description):
    """ takes a list of strings
    each item defines a node in a graph as
    number, priority, player, successors, name
    
    returns 
        - list of tokens corresponding to node labels
        - list of tokens to describe each node as label, priority, owner
        - list of tokens to describe each edge as src_node_label, dst_node_label
    """
    def make_edges(i, js):
        j_tokens = [node_token(j) for j in js]
        return [item for value in j_tokens for item in [EDGE_MARKER, node_token(i), value]]

    nodes, node_descriptions, edges = [], [], []
    for graph_line in graph_description[1:]:
        n, p, o, successors, label = graph_line.split()
        node = node_token(n)
        priority = priority_token(p)
        owner = player_token(o)
        node_descriptions.extend([NODE_MARKER, node, priority, owner])
        edges.extend(make_edges(n, successors.split(',')))
        nodes.append(node)

    tokens = [INPUT_LINE, LINE_SUBTYPE_NODES]
    tokens.extend(node_descriptions)
    tokens.append(LINE_SUBTYPE_EDGES)
    tokens.extend(edges)
    
    return nodes, tokens