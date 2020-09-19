import matplotlib.pyplot as plt

x = [1,3,4,5,9]
y = [2,5.2,6.8,8.4,14.8]

plt.plot(x,y,'o-')
plt.savefig('plot.png')
plt.show()