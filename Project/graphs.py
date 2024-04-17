import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from Project import models

def bar_char():
    data=models.retreive_data()
    categories, values1, values2, values3 = zip(*data)

    plt.bar(categories, values1, width=0.2, label='Value 1')
    plt.bar(categories, values2, width=0.2, label='Value 2', bottom=values1)
    plt.bar(categories, values3, width=0.2, label='Value 3', bottom=[i+j for i,j in zip(values1, values2)])

    plt.xlabel('Category')
    plt.ylabel('Values')
    plt.title('Bar Chart of Values for each Category')
    plt.legend()

    plt.tight_layout()
    # plt.show()
    file_path = 'static/public/chart.png'
    if os.path.exists(file_path):
        os.remove(file_path)

    plt.savefig(file_path)
