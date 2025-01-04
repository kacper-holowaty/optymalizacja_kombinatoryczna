# Zaimplementować algorytm Hu dla problemu P | p_j=1,in-tree | C_max. 
# Program powinien działać dla drzew i lasów - zarówno wchodzących jak i wychodzących.

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def load_edges_from_file(file):
    edges = []
    try:
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    start, end = map(int, line.split(','))
                    edges.append((start, end))
    except FileNotFoundError:
        print(f"File {file} do not exist!")
        raise
    except ValueError:
        print(f"File {file} contains incorrect data!")
        raise
    return edges

def is_in_tree(graph):
    roots = [node for node in graph.nodes if graph.out_degree(node) == 0]
    if len(roots) != 1:
        return False
    for node in graph.nodes:
        if node != roots[0] and graph.out_degree(node) != 1:
            return False
    return True

def is_out_tree(graph):
    roots = [node for node in graph.nodes if graph.in_degree(node) == 0]
    if len(roots) != 1:
        return False
    for node in graph.nodes:
        if node != roots[0] and graph.in_degree(node) != 1:
            return False
    return True

def is_in_forest(graph):
    for node in graph.nodes:
        if len(list(graph.successors(node))) > 1:
            return False
    
    roots = [node for node in graph.nodes if graph.in_degree(node) == 0]
    
    if not roots:
        return False
    if not nx.is_directed_acyclic_graph(graph):
        return False
    return True

def is_out_forest(graph):
    reversed_graph = graph.reverse()
    return is_in_forest(reversed_graph)

def calculate_levels(graph, root):
    levels = {}
    visited = set()
    queue = [(root, 1)]
    while queue:
        node, level = queue.pop(0)
        if node not in visited:
            visited.add(node)
            levels[node] = level
            for neighbor in graph.predecessors(node):
                queue.append((neighbor, level + 1))
    
    return levels

def hu_algorithm(edges, m):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    is_out_forest_graph = False

    if is_in_tree(graph):
        print("Graph is an in-tree.")
        root = next(node for node in graph.nodes if graph.out_degree(node) == 0)
        levels = calculate_levels(graph, root)
        tasks = [(task_id, levels[task_id]) for task_id in levels]
        max_level = max(level for _, level in tasks)
        tasks = [(task_id, max_level - level + 1) for task_id, level in tasks]
        
    elif is_out_tree(graph):
        print("Graph is an out-tree.")
        reversed_graph = graph.reverse()
        root = next(node for node in reversed_graph.nodes if reversed_graph.out_degree(node) == 0)
        levels = calculate_levels(reversed_graph, root)
        tasks = [(task_id, levels[task_id]) for task_id in levels]

    elif is_in_forest(graph):
        print("Graph is an in-forest.")
        nodes_without_outgoing_edges = [node for node in graph.nodes if len(list(graph.successors(node))) == 0]
        super_root = max(graph.nodes) + 1
        graph.add_node(super_root)
        for node in nodes_without_outgoing_edges:
            graph.add_edge(node, super_root)
        root = super_root
        levels = calculate_levels(graph, root)
        del levels[super_root]
        tasks = [(task_id, levels[task_id]) for task_id in levels]
        max_level = max(level for _, level in tasks)
        tasks = [(task_id, max_level - level + 1) for task_id, level in tasks]

    elif is_out_forest(graph):
        print("Graph is an out-forest.")
        is_out_forest_graph = True
        nodes_without_ingoing_edges = [node for node in graph.nodes if len(list(graph.predecessors(node))) == 0]
        super_root = max(graph.nodes) + 1
        graph.add_node(super_root)
        for node in nodes_without_ingoing_edges:
            graph.add_edge(super_root, node)
        reversed_graph = graph.reverse()
        root = super_root
        levels = calculate_levels(reversed_graph, root)
        tasks = [(task_id, levels[task_id] - 1) for task_id in levels]
    
    else:
        print("Graph does not belong to any expected type: in-forest, out-forest, in-tree, or out-tree.")
        return
    
    t = 1
    scheduled_tasks = {i: [] for i in range(m)}
    remaining_tasks = tasks[:]
    completed_tasks = set()

    while remaining_tasks:
        available_tasks = [
            task for task in remaining_tasks
            if task[1] <= t and all(pred in completed_tasks for pred in graph.predecessors(task[0]))
        ]

        available_tasks.sort(key=lambda x: x[1], reverse=False)
        machine_id = 0
        while available_tasks and machine_id < m:
            task = available_tasks.pop(0)
            if is_out_forest_graph:
                scheduled_tasks[machine_id].append((task[0], t-1))
                if scheduled_tasks[machine_id][0][1] == 0:
                    scheduled_tasks[machine_id].pop(0) 
            else:
                scheduled_tasks[machine_id].append((task[0], t))
            remaining_tasks.remove(task)
            completed_tasks.add(task[0])  
            machine_id += 1
        t += 1

    return scheduled_tasks


def visualize_graph(graph):
    pos = nx.spring_layout(graph, seed=64)

    labels = {node: f'Z{node}' for node in graph.nodes}

    nx.draw(graph, pos, with_labels=False, node_color='skyblue', node_size=1200, font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_weight='bold', font_color='black')
    plt.show()

def generate_schedule(scheduled_tasks):
    _, ax = plt.subplots()
    color_map = plt.get_cmap('tab20')
    all_tasks = [task for tasks in scheduled_tasks.values() for task in tasks]
    task_colors = {task_id: color_map(i) for i, task_id in enumerate({task[0] for task in all_tasks})}

    min_start_time = min(task[1] for task in all_tasks)

    for machine_id, tasks in scheduled_tasks.items():
        for task_id, start_time in tasks:
            adjusted_start_time = start_time - min_start_time
            ax.broken_barh(
                [(adjusted_start_time, 1)],
                (machine_id + 0.6, 0.8),
                facecolors=task_colors[task_id]
            )
            ax.text(
                adjusted_start_time + 0.5,
                machine_id + 1,
                f'Z{task_id}',
                ha='center', va='center', color='white', weight='bold'
            )

    ax.set_xlabel("Czas")
    ax.set_ylabel("Numer maszyny")
    ax.set_xticks(np.arange(0, max(task[1] - min_start_time + 1 for task in all_tasks) + 1, step=1))
    ax.set_yticks(np.arange(1, len(scheduled_tasks) + 1, step=1))
    plt.show()

def main():
    file = "krawedzie1.txt"
    edges = load_edges_from_file(file)
    machines = 3

    scheduled_tasks = hu_algorithm(edges, machines)

    if scheduled_tasks:
        print("Harmonogram:")
        for machine_id, tasks in scheduled_tasks.items():
            print(f"M{machine_id + 1}: {tasks}")
        
        generate_schedule(scheduled_tasks)

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    visualize_graph(graph)

if __name__ == "__main__":
    main()