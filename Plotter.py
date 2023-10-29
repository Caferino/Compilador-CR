import matplotlib.pyplot as plt # ! Cargar esto hace que el programa corra 2s más lento

def plotThis(x, y) :
    # Create a line plot
    plt.plot(x, y)

    # Add labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Line Plot')
    
    # Display the plot
    plt.show()