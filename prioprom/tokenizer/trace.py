from .util import priority_token, node_token, PRIORITY_MARKER, LINE_SUBTYPE_PRIORITY
from functools import partial

def tokenize_line(line, nodes, combined=False):
    def get_line_type(line_type_str):
        parts = line_type_str.split()
        main_type = parts[0]
        sub_type = LINE_SUBTYPE_PRIORITY
        if len(parts) > 1:
            sub_type = parts[1].lower()
        return main_type, sub_type

    def tokenize_priority_data(nodes, priority_string):
        """ expects a space separated string of priority values and a list of node labels
        """
        priorities = [priority_token(x) for x in priority_string.split()]
        assert len(priorities) == len(nodes), f"{priorities=}, {nodes=}, {priority_string=}"
        return [item for n, p in zip(nodes, priorities) for item in [PRIORITY_MARKER, n, p]]

    def tokenize_heads_data(data):
        """ input: space separated string of node ids
        output: list of node tokens
        """
        nodes = data.split()
        return [node_token(i) for i in nodes]

    # TODO might be worth distinguishing line start tokens for forced and chosen attraction
    # since they require different data. 
    def tokenize_attr_data(data):
        """input: string of space separated node ids, optionally ending in "to <node_id>".
        output: list of 1 or 2 tokens (src_node_id, dst_node_id[optional])
        """
        data = data.strip()
        if "to" in data:
            src, _, dst = data.split()
            return [node_token(src), node_token(dst)]
        return [node_token(data)]

    def tokenize_prom_data(data):
        """input: string of space separated node ids
        output: list of node label tokens
        """
        return [node_token(x) for x in data.split()]

    def tokenize_reset_data(data):
        """no data for reset line, do nothing
        """
        return []

    line_type_str, data = line.split(':')
    
    main_type, sub_type = get_line_type(line_type_str)
    type_tokens = [f"{main_type}_{sub_type}"] if combined else [main_type, sub_type]

    line_priority_pos = line_type_str.find('(prio ')
    line_prio_token = [] 
    if line_priority_pos != -1:
        line_priority = line_type_str[line_priority_pos + len('(prio '):].strip().strip(')')
        line_prio_token = [priority_token(line_priority)]


    funcs = {'reset': tokenize_reset_data, 
        'attr': tokenize_attr_data, 
        'heads': tokenize_heads_data,
        'priority': partial(tokenize_priority_data, nodes), 
        'prom': tokenize_prom_data}

    data_tokens = funcs[sub_type](data.strip())
    
    return type_tokens + line_prio_token + data_tokens