import matplotlib
import matplotlib.pyplot as plt, mpld3
from matplotlib.ticker import MultipleLocator
from io import BytesIO
import base64
import pandas as pd


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

def getSentimentGraph():
    # Load Data
    main_df = pd.read_csv('MachineLearning/MyDatasets/ML_training_data_BTCUSDT.csv')

    # Refactor the datetime col to just be the date
    #main_df["datetime"] = pd.to_datetime(main_df["datetime"]).dt.date
    print(main_df["datetime"])
    main_df.set_index('datetime', drop=True, inplace=True)

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.set_title('Bitcoin Sentiment/Price Visualisation')
    ax1.plot(main_df["avg_twitter_sentiment"])
    ax1.xaxis.set_tick_params(rotation=30, labelsize=5)
    # Change the tick interval
    ax1.xaxis.set_major_locator(MultipleLocator(24))
    #ax1.title('Ethereum Sentiment')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sentiment Score')

    ax2.plot(main_df["close"])
    ax2.xaxis.set_tick_params(rotation=30, labelsize=5)
    # Change the tick interval
    ax2.xaxis.set_major_locator(MultipleLocator(24))
    #ax2.title('Ethereum Price')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price')


    plt.savefig('BTC_LongTerm_SentimentGraph.png', format='png')
    plt.show()


getSentimentGraph()
