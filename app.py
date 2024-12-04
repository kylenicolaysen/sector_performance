import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access the variables
tiingo_api_key = os.getenv('TIINGO_API_KEY')
auth = f'Token {tiingo_api_key}'
headers = {
    'Content-Type': 'application/json',
    'Authorization' : auth
    }


def get_data(ticker):
    requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate=2023-12-02&endDate=2024-12-02 ",
            headers=headers)
    print(f'{ticker}: {requestResponse}')
    data = requestResponse.json()
    df = pd.DataFrame(data)
    df['ticker'] = ticker
    return df


def get_performance(df):
    five_days = [0] * 4     #5 days
    one_month = [0] * 19   #20 days
    six_months = [0] * 129  #130 daus

    for i in range(4, len(df)):
        five_days.append((df['close'][df.index[i]] - df['close'][df.index[i-4]]) / df['close'][df.index[i-4]] * 100)
    for i in range(19, len(df)):
        one_month.append((df['close'][df.index[i]] - df['close'][df.index[i-19]]) / df['close'][df.index[i-19]] * 100)
    for i in range(129, len(df)):
        six_months.append((df['close'][df.index[i]] - df['close'][df.index[i-129]]) / df['close'][df.index[i-129]] * 100)
    # print(f'{df['ticker'][df.index[0]]}: {df['close'][-10:]} \n {five_days[-10:]}')
    df['five days'] = five_days
    df['one month'] = one_month
    df['six months'] = six_months
    df.to_pickle(f'./data/{df['ticker'][df.index[0]]}.pkl')
    return df


# def plot_perf(performance_df, ticker):
#     date_list = list(performance_df['date'])
#     formatted_date_list = []
#     for i in date_list:
#         date_obj = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ")
#         formatted_date_list.append(date_obj.strftime("%m-%d"))
#     plt.figure(figsize=(16, 12))
#     plt.title(ticker)
#     plt.xlabel('Date')
#     plt.ylabel('Performance (%)')
#     plt.xticks(performance_df.index[::10], formatted_date_list[::10], rotation=45)
#     plt.plot(performance_df['five days'][performance_df.index[4:]], marker='.')
#     plt.plot(performance_df['one month'][performance_df.index[19:]], marker='.')
#     plt.plot(performance_df['six months'][performance_df.index[129:]], marker='.')
#     plt.savefig(f'outputs/{ticker}.png')
#     plt.show(block=False)
#     time.sleep(2)
#     plt.close()

def plot_5d_perf(performance_df_list, perf_type, hist_length, interval=1):
    hist_length = hist_length * -1
    date_list = list(performance_df_list[0]['date'])
    formatted_date_list = []
    for i in date_list:
        date_obj = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date_list.append(date_obj.strftime("%m-%d"))
    plt.figure(figsize=(16, 12))
    plt.title(f'5 Day Performance of {perf_type} -- {hist_length * -1} Data Points -- {interval} Interval')
    plt.xlabel('Date')
    plt.ylabel('Performance (%)')
    plt.xticks(performance_df_list[0].index[hist_length::10], formatted_date_list[hist_length::10], rotation=45)
    index_list = performance_df_list[0].index.to_list()
    plt.plot(index_list[hist_length:], ([0] * (hist_length*-1)), color='grey', linestyle='--')
    for performance_df in performance_df_list:
        plt.plot(performance_df['five days'][performance_df.index[hist_length:]], label=performance_df['ticker'][performance_df.index[0]], marker='.')
    plt.legend()
    plt.savefig(f'outputs/5day{perf_type}.png')
    plt.show()
    # plt.show(block=False)
    # time.sleep(2)
    # plt.close()

def plot_1m_perf(performance_df_list, perf_type, hist_length, interval=1):
    hist_length = hist_length * -1
    date_list = list(performance_df_list[0]['date'])
    formatted_date_list = []
    for i in date_list:
        date_obj = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date_list.append(date_obj.strftime("%m-%d"))
    plt.figure(figsize=(16, 12))
    plt.title(f'1 Month Performance of {perf_type} -- {hist_length * -1} Data Points -- {interval} Interval')
    plt.xlabel('Date')
    plt.ylabel('Performance (%)')
    plt.xticks(performance_df_list[0].index[hist_length::10], formatted_date_list[hist_length::10], rotation=45)
    index_list = performance_df_list[0].index.to_list()
    plt.plot(index_list[hist_length:], ([0] * (hist_length*-1)), color='grey', linestyle='--')
    for performance_df in performance_df_list:
        plt.plot(performance_df['one month'][performance_df.index[hist_length:]], label=performance_df['ticker'][performance_df.index[0]], marker='.')
    plt.legend()
    plt.savefig(f'outputs/1Month{perf_type}.png')
    plt.show()

def plot_6m_perf(performance_df_list, perf_type, hist_length, interval=1):
    hist_length = hist_length * -1
    date_list = list(performance_df_list[0]['date'])
    formatted_date_list = []
    for i in date_list:
        date_obj = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date_list.append(date_obj.strftime("%m-%d"))
    plt.figure(figsize=(16, 12))
    plt.title(f'6 Month Performance of {perf_type} -- {hist_length * -1} Data Points -- {interval} Interval')
    plt.xlabel('Date')
    plt.ylabel('Performance (%)')
    plt.xticks(performance_df_list[0].index[hist_length::10], formatted_date_list[hist_length::10], rotation=45)
    index_list = performance_df_list[0].index.to_list()
    plt.plot(index_list[hist_length:], ([0] * (hist_length*-1)), color='grey', linestyle='--')
    for performance_df in performance_df_list:
        plt.plot(performance_df['six months'][performance_df.index[hist_length:]], label=performance_df['ticker'][performance_df.index[0]], marker='.')
    plt.legend()
    plt.savefig(f'outputs/6Months{perf_type}.png')
    plt.show()


sector_tickers = ['XLV', 'XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLI', 'XLU', 'XLK', 'SMH', 'QQQ', 'SPY']
sect_perf_data_list = []
for ticker in sector_tickers:
    try:
        performance_data = pd.read_pickle(f'./data/{ticker}.pkl')
        print('File Found')
    except FileNotFoundError:
        print('File Not Found Error')
        data = get_data(ticker)
        performance_data = get_performance(data)
    finally:
        sect_perf_data_list.append(performance_data)

plot_5d_perf(sect_perf_data_list, 'SPDR Sectors', 25)
plot_1m_perf(sect_perf_data_list, 'SPDR Sectors', 25)
plot_6m_perf(sect_perf_data_list, 'SPDR Sectors', 25)

mag7_tickers = ['AMZN', 'AAPL', 'GOOG', 'META', 'MSFT','NVDA', 'TSLA', 'SPY']
mag_perf_data_list = []
for ticker in mag7_tickers:
    try:
        performance_data = pd.read_pickle(f'./data/{ticker}.pkl')
        print('File Found')
    except FileNotFoundError:
        print('File Not Found Error')
        data = get_data(ticker)
        performance_data = get_performance(data)
    finally:
        mag_perf_data_list.append(performance_data)

plot_5d_perf(mag_perf_data_list, 'Mag 7', 25)
plot_1m_perf(mag_perf_data_list, 'Mag 7', 25)
plot_6m_perf(mag_perf_data_list, 'Mag 7', 25)