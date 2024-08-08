import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def read_heart_rate_data():
    conn = sqlite3.connect('heart_rate.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date, bpm FROM heart_rate")
    data = cursor.fetchall()
    conn.close()
    return data

def plot_heart_rate(data):
    dates = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f") for record in data]
    bpm = [record[1] for record in data]

    plt.subplot(5, 1, 1)
    plt.plot(dates, bpm, marker='.', linestyle='-', color='b')
    plt.title('Heart Rate Over Time')
    plt.xlabel('Time')
    plt.ylabel('BPM')
    plt.grid(True)

def plot_rri(data):
    dates = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f") for record in data]
    rr_intervals = [60_000 / record[1] for record in data]

    plt.subplot(5, 1, 2)
    plt.plot(dates, rr_intervals, marker='.', linestyle='-', color='r')
    plt.title('R-R Intervals Over Time')
    plt.xlabel('Interval index')
    plt.ylabel('RRI (ms)')
    plt.grid(True)

    deviation_dates = []
    deviations = []
    deviation_window = timedelta(minutes=10)

    # calculate the deviation for points in every 10 minutes

    current_batch = []
    current_date = dates[0]

    for i, date in enumerate(dates):
        rri = rr_intervals[i]

        if date > (current_date + deviation_window):
            deviations.append(np.std(current_batch))
            deviation_dates.append(current_date)
            current_date += deviation_window
            current_batch = []

        current_batch.append(rri)

    plt.subplot(5, 1, 3)
    plt.plot(deviation_dates, deviations, marker='.', linestyle='-', color='r')
    plt.title('R-R Intervals STD deviation (10 min window)')
    plt.xlabel('Interval index')
    plt.ylabel('deviation')
    plt.grid(True)

data = read_heart_rate_data()
plt.figure(figsize=(12, 9))
plot_heart_rate(data)
plot_rri(data)
plt.tight_layout()
plt.show()
