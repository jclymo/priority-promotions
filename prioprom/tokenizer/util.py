### available tokens
def node_token(i):
    return f"node_{i}"

def priority_token(i):
    return f"priority_{i}"

def player_token(i):
    return f"player_{i}"

# tokens to hint meaning of following tokens
EDGE_MARKER = "edge"
NODE_MARKER = "node"
PRIORITY_MARKER = "prio" # note "prio" token is different from "priority" token below

# tokens to define input structure
INFO_LINE = "info"
ACTION_LINE = "action"
EFFECT_LINE = "effect"
INPUT_LINE = "input"

LINE_SUBTYPE_PRIORITY = "priority"
LINE_SUBTYPE_HEADS = "heads"
LINE_SUBTYPE_ATTRACTION = "attr"
LINE_SUBTYPE_RESET = "reset"
LINE_SUBTYPE_PROMOTION = "prom"
LINE_SUBTYPE_EDGES = "edge_list"
LINE_SUBTYPE_NODES = "node_list"

# mapping of which line types can have which subtypes
line_types = {
    INFO_LINE: [LINE_SUBTYPE_PRIORITY, LINE_SUBTYPE_HEADS, LINE_SUBTYPE_ATTRACTION, LINE_SUBTYPE_RESET], 
    ACTION_LINE: [LINE_SUBTYPE_ATTRACTION, LINE_SUBTYPE_PROMOTION], 
    EFFECT_LINE: [LINE_SUBTYPE_PRIORITY],
    INPUT_LINE: [LINE_SUBTYPE_EDGES, LINE_SUBTYPE_NODES]}

###
def get_all_tokens(num_nodes, num_players=2, combined=False):
    def line_start_tokens():
        if combined:
            return [f"{k}_{v}" for k, values in line_types.items() for v in values]
        top_level = list(line_types.keys())
        sub_level = list({v for values in line_types.values() for v in values})
        return top_level + sub_level

    def player_tokens():
        return [player_token(i) for i in range(num_players)]

    def node_tokens(num_nodes):
        return [node_token(i) for i in range(num_nodes)]
    
    def priority_tokens(): 
        priorities = [f'T{n}' for n in range(num_players)] + list(range(num_nodes))
        return [priority_token(i) for i in priorities]

    def marker_tokens():
        return [EDGE_MARKER, NODE_MARKER, PRIORITY_MARKER] 

    tokens = line_start_tokens()
    tokens += player_tokens()
    tokens += node_tokens(num_nodes)
    tokens += priority_tokens()
    tokens += marker_tokens()
    return tokens