from .graph import tokenize_graph
from .util import get_all_tokens, INPUT_LINE, LINE_SUBTYPE_NODES, LINE_SUBTYPE_EDGES
from .trace import tokenize_line

END_INPUT = "ORIGINAL RUN\n"
START_OPTIMAL_RUN = "OPTIMAL RUN\n"

def tokenize(graph_trace_description_string, combined=False):
    """ given a string input containing a graph description and up to two algorithm traces,
    create a single sequence of tokens. 
    
    The file MUST contain a non-optimised ('original') algorithm trace
    and MAY additionally contain an optimised algorithm trace.

    The input string is expected to have the form
    "parity <num_nodes>;
    <graph description>
    ORIGINAL RUN
    <trace description>
    OPTIMAL RUN # optional
    <trace description> # optional
    """
    end_input_pos = graph_trace_description_string.find(END_INPUT)
    start_optimal_pos = graph_trace_description_string.find(START_OPTIMAL_RUN)

    graph_description = graph_trace_description_string[ : end_input_pos]
    original_algorithm_trace = graph_trace_description_string[end_input_pos + len(END_INPUT) : start_optimal_pos]
    if start_optimal_pos != -1: # optimal trace included
        optimal_algorithm_trace = graph_trace_description_string[start_optimal_pos + len(START_OPTIMAL_RUN) : ]

    graph_description = [x.strip(';') for x in graph_description.strip('\n').split('\n')]
    num_nodes = int(graph_description[0].split()[1])

    nodes, graph_tokens = tokenize_graph(graph_description)

    original_trace_tokens = []
    original_algorithm_trace = original_algorithm_trace.strip('\n').split('\n')
    for line in original_algorithm_trace:
        original_trace_tokens.extend(tokenize_line(line, nodes, combined))

    optimal_trace_tokens = []
    if start_optimal_pos != -1:
        optimal_algorithm_trace = optimal_algorithm_trace.split('\n')
        for line in optimal_algorithm_trace:
            optimal_trace_tokens.extend(tokenize_line(line, nodes, combined))

    available_tokens = get_all_tokens(num_nodes)    
    for tok in graph_tokens + original_trace_tokens + optimal_trace_tokens:
        assert tok in available_tokens, f"unknown token {tok}."
        
    return graph_tokens, original_trace_tokens, optimal_trace_tokens

