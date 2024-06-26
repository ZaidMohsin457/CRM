import matplotlib.pyplot as plt
import numpy as np

def bar_char(data):
    name = [entry[0] for entry in data]
    progress = [entry[1] for entry in data]
    plt.figure(figsize=(8.5, 4))
    colors = plt.cm.tab20(np.linspace(0, 1, len(name)))
    plt.bar(name, progress, color=colors)
    plt.xlabel('Name of Project')
    plt.ylabel('Progress')
    plt.title('Progress of Projects')
    plt.xticks(name)
    plt.savefig('static/public/project_graph1.svg')
    
    
    
def projects_graph(data):
    transformed_data = [(int(month), projects) for month, projects in data]
    months = [entry[0] for entry in transformed_data]
    project_counts = [entry[1] for entry in transformed_data]
    plt.figure(figsize=(8.5, 4))
    plt.plot(months, project_counts, marker='o', color='skyblue', linestyle='-')
    plt.scatter(months, project_counts, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Number of Projects')
    plt.title('Projects Made per Month')
    plt.xticks(range(1, 13))
    plt.savefig('static/public/project_graph.svg')