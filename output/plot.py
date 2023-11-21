import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

fig1 = plt.figure()
fig2 = plt.figure()
fig1.tight_layout()
fig2.tight_layout()
volttime = fig1.add_subplot(2, 1, 1)
currenttime = fig1.add_subplot(2, 1, 2)
volttemp = fig2.add_subplot(3, 1, 1)
currenttemp = fig2.add_subplot(3, 1, 2)
temptime = fig2.add_subplot(3, 1, 3)
print("Please enter data file to plot from")
filename = input()
print("Please chose between plot or liveplot p/l?")
option = input().lower()

def readdata(filename: str):
    file = open(filename, 'r')
    data = pd.read_csv(file)
    column_names = data.columns
    file.close()
    # print(f'Data column names: {list(column_names)}')
    return data, list(column_names)


def animate(i):
    graph_data, col_names = readdata(filename)
    volttimex = graph_data[:][col_names[0]]
    volttimey = graph_data[:][col_names[1]]
    currentx = graph_data[:][col_names[0]]
    currenty = graph_data[:][col_names[2]]
    volttime.clear()
    volttime.plot(volttimex, volttimey)
    currenttime.clear()
    currenttime.plot(currentx, currenty)
    for i, j, k in zip((volttime, currenttime), ("Voltage", "Current"), ("Time", "Time")):
        i.set_ylabel(j)
        i.set_xlabel(k)
    fig1.tight_layout()
    fig2.tight_layout()


def animate2(i):
    data, col_names = readdata(filename)
    volttemp.clear()
    currenttemp.clear()
    temptime.clear()
    for i, j, k in zip((volttemp, currenttemp, temptime), ("Voltage", "Cureent", "Temperature"),
                       ("Temperature", "Temperature", "Time")):
        i.set_xlabel(k)
        i.set_ylabel(j)
    volttemp.plot(data[:][col_names[4]], data[:][col_names[1]])
    currenttemp.plot(data.loc[:, col_names[4]], data.loc[:, col_names[2]])
    temptime.plot(data.loc[:, col_names[0]], data.loc[:, col_names[4]])

if option == 'l':
    ani1 = animation.FuncAnimation(fig1, animate, interval=1000)
    ani2 = animation.FuncAnimation(fig2, animate2, interval=1000)
    plt.show()
elif option == 'p':
    graph_data, col_names = readdata(filename)
    volttimex = graph_data[:][col_names[0]]
    volttimey = graph_data[:][col_names[1]]
    currentx = graph_data[:][col_names[0]]
    currenty = graph_data[:][col_names[2]]
    volttime.plot(volttimex, volttimey)
    currenttime.plot(currentx, currenty)
    for i, j, k in zip((volttime, currenttime), ("Voltage", "Current"), ("Time", "Time")):
        i.set_ylabel(j)
        i.set_xlabel(k)
    for i, j, k in zip((volttemp, currenttemp, temptime), ("Voltage", "Cureent", "Temperature"),
                       ("Temperature", "Temperature", "Time")):
        i.set_xlabel(k)
        i.set_ylabel(j)
    volttemp.plot(graph_data[:][col_names[4]], graph_data[:][col_names[1]])
    currenttemp.plot(graph_data.loc[:, col_names[4]], graph_data.loc[:, col_names[2]])
    temptime.plot(graph_data.loc[:, col_names[0]], graph_data.loc[:, col_names[4]])
    plt.show()
else:
    print("wrong option")