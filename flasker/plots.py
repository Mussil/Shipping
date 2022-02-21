import matplotlib.pyplot as plt


def averageDrivers():
    x = [100, 200, 300, 400, 500]
    y = [0.214, 0.44, 0.554, 0.714, 0.76]  # avg

    plt.plot(x, y)
    plt.xlabel('number of drivers')
    plt.xticks(x, x)
    plt.ylabel('average of success')
    plt.title('50 parcels')
    plt.show()

def medianDrivers():
    x = [100, 200, 300, 400, 500]
    y = [0.21000000000000002, 0.44999999999999996, 0.55, 0.74, 0.75] #median

    plt.plot(x, y)
    plt.xlabel('number of drivers')
    plt.xticks(x, x)
    plt.ylabel('median of success')
    plt.title('50 parcels')
    plt.show()

if __name__=='__main__':

    averageDrivers()
    medianDrivers()