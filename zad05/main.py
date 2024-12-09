"""
Zaimplementuj metody ścieżki krytycznej, która dla podanego przez użytkownika 
zestawu zadań zbuduje sieć AA lub AN, a następnie dla każdego zadania wyliczy 
najwcześniejszy oraz najpóźniejszy moment wykonywania zadania, poda ścieżkę 
krytyczną, harmonogram (wg najszybszych momentów startu) oraz długość uszeregowania.

W tasks.txt mamy:
numer zadania | czas trwania zadania | poprzednicy (numer zadania wchodzącego do obecnego), może być dowolna ilość

W tym rozwiązaniu została zbudowana sieć AN.
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import networkx as nx

class Task:
    def __init__(self, task_id, duration):
        self.task_id = task_id
        self.duration = duration
        self.next_tasks = []
        self.previous_tasks = []
        self.earliest_start = 0
        self.latest_start = math.inf

def load_tasks_from_file(file_name):
    task_map = {}
    with open(file_name, 'r') as file:
        for line in file:
            data = line.split()
            task_id, duration = int(data[0]), int(data[1])
            task = Task(task_id, duration)
            task_map[task_id] = task

            if len(data) > 2:
                previous_task_ids = map(int, data[2:])
                for prev_task_id in previous_task_ids:
                    task.previous_tasks.append(prev_task_id)
                    task_map[prev_task_id].next_tasks.append(task_id)
    return task_map

def calculate_earliest_start(task_map):
    task_stack = [task for task in task_map.values() if not task.previous_tasks]
    processed_tasks = set()

    while task_stack:
        current = task_stack.pop()
        processed_tasks.add(current.task_id)

        for next_task_id in current.next_tasks:
            next_task = task_map[next_task_id]
            next_task.earliest_start = max(
                next_task.earliest_start,
                current.earliest_start + current.duration
            )
            if set(next_task.previous_tasks).issubset(processed_tasks):
                task_stack.append(next_task)

def calculate_latest_start(task_map):
    final_tasks = [task for task in task_map.values() if not task.next_tasks]
    schedule_length = calculate_schedule_length(task_map)

    for final_task in final_tasks:
        final_task.latest_start = schedule_length - final_task.duration

    task_stack = final_tasks[:]
    processed_tasks = set()

    while task_stack:
        current = task_stack.pop()
        processed_tasks.add(current.task_id)

        for prev_task_id in current.previous_tasks:
            prev_task = task_map[prev_task_id]
            prev_task.latest_start = min(
                prev_task.latest_start,
                current.latest_start - prev_task.duration
            )
            if set(prev_task.next_tasks).issubset(processed_tasks):
                task_stack.append(prev_task)

def calculate_schedule_length(task_map):
    return max(
        task.earliest_start + task.duration
        for task in task_map.values()
        if not task.next_tasks
    )

def find_critical_path(task_map):
    critical_path = [
        task.task_id
        for task in task_map.values()
        if task.earliest_start == task.latest_start
    ]
    return critical_path

def generate_schedule(task_map):
    _, ax = plt.subplots()

    sorted_tasks = sorted(task_map.values(), key=lambda t: t.earliest_start)
    machine_end_times = []
    machines = []

    color_map = plt.get_cmap('tab20')
    task_colors = [color_map(i) for i in np.linspace(0, 1, len(sorted_tasks))]

    for task in sorted_tasks:
        task_assigned = False
        for i, machine_end_time in enumerate(machine_end_times):
            if task.earliest_start >= machine_end_time:
                machines[i].append(task)
                machine_end_times[i] = task.earliest_start + task.duration
                task_assigned = True
                break

        if not task_assigned:
            machines.append([task])
            machine_end_times.append(task.earliest_start + task.duration)

    for machine_index, machine_tasks in enumerate(machines):
        for task in machine_tasks:
            color_index = sorted_tasks.index(task)
            ax.broken_barh(
                [(task.earliest_start, task.duration)],
                (machine_index + 0.6, 0.8),
                facecolors=task_colors[color_index]
            )
            ax.text(
                task.earliest_start + task.duration / 2,
                machine_index + 1,
                f'Z{task.task_id}',
                ha='center', va='center', color='white', weight='bold'
            )

    ax.set_xlabel("Czas")
    ax.set_ylabel("Numer maszyny")
    ax.set_xticks(np.arange(0, max(machine_end_times) + 1, step=1))
    ax.set_yticks(np.arange(1, len(machines) + 1, step=1))
    plt.show()


def visualize_network(task_map, critical_path):
    G = nx.DiGraph()

    for task in task_map.values():
        G.add_node(
            task.task_id,
            label=f"Z$_{{{task.task_id}}}$, {task.duration}",
            color="red" if task.task_id in critical_path else "skyblue"
        )
        for next_task_id in task.next_tasks:
            G.add_edge(
                task.task_id, next_task_id,
                color="red" if task.task_id in critical_path and next_task_id in critical_path else "black"
            )

    layers = {}
    for node in nx.topological_sort(G):
        layer = max((layers.get(pred, 0) for pred in G.predecessors(node)), default=0) + 1
        layers[node] = layer

    pos = {}
    layer_counts = {}
    for node, layer in layers.items():
        if layer not in layer_counts:
            layer_counts[layer] = 0
        x_pos = layer * 4
        y_pos = layer_counts[layer] * -2
        pos[node] = (x_pos, y_pos)
        layer_counts[layer] += 1

    node_colors = [data["color"] for _, data in G.nodes(data=True)]
    edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
    labels = nx.get_node_attributes(G, "label")

    plt.figure(figsize=(16, 10))
    nx.draw(
        G, pos, with_labels=False, node_color=node_colors,
        node_size=3000, font_size=10, arrowsize=20, edge_color=edge_colors, alpha=0.8
    )
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_color="black", font_weight="bold")
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    file_name = "tasks.txt"

    task_map = load_tasks_from_file(file_name)

    calculate_earliest_start(task_map)
    calculate_latest_start(task_map)

    critical_path = find_critical_path(task_map)
    schedule_length = calculate_schedule_length(task_map)

    print("Zadanie | Najwcześniejszy moment | Najpóźniejszy moment")
    for task in task_map.values():
        print(
            f"Z{task.task_id:02}     | {task.earliest_start:22} | "
            f"{task.latest_start:20}"
        )

    print(f"\nŚcieżka krytyczna: {', '.join(f'Z{x}' for x in critical_path)}")
    print(f"Długość uszeregowania: {schedule_length}")

    generate_schedule(task_map)
    visualize_network(task_map, critical_path)

if __name__ == "__main__":
    main()