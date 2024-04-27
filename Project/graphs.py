import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from Project import models

def bar_char(data):
    name = [entry[0] for entry in data]
    progress = [entry[1] for entry in data]
    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.bar(name, progress, color='darkblue')
    plt.xlabel('Name of Project')
    plt.ylabel('Progress')
    plt.title('Progress of Projects')
    plt.xticks(name)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('static/public/project_graph1.svg')
    
def projects_graph(data):
    transformed_data = [(int(month), projects) for month, projects in data]
    months = [entry[0] for entry in transformed_data]
    project_counts = [entry[1] for entry in transformed_data]

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(months, project_counts, marker='o', color='skyblue', linestyle='-')
    plt.scatter(months, project_counts, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Number of Projects')
    plt.title('Projects Made per Month')
    plt.xticks(range(1, 13))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('static/public/project_graph.svg')