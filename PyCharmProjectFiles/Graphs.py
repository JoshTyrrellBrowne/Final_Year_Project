import matplotlib
import matplotlib.pyplot as plt, mpld3
matplotlib.use('Agg')
from io import BytesIO
from flask import Flask, send_file
import base64


def getTest():
    img = BytesIO()
    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]

    plt.plot(x, y)

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url

def getHTMLStringOfGraph():
    img = BytesIO()
    # Median Developer Salaries by Age
    ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

    dev_y = [38496, 42000, 46752, 49320, 53200,
         56000, 62316, 64928, 67317, 68748, 73752]

    plt.plot(ages_x, dev_y, 'k--', label='All Devs')

    # py_dev_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] <- this is not needed because dev_x is the same
    py_dev_y = [45372, 48876, 53850, 57287, 63016,
            65998, 70003, 70000, 71496, 75370, 83640]
    plt.plot(ages_x, py_dev_y, 'b', label='Python Devs')

    plt.xlabel('Ages')
    plt.ylabel('Median Salary (USD)')
    plt.title('Median Salary (USD) by Age')
    plt.legend()  # show legend (tells ya what data is)
    #  fig = plt.figure()
    #  mpld3.save_html(fig, "graphExample.html")

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    #  mpld3.fig_to_html(fig)
    return plot_url

# mpld3.show()  this shows the graph
