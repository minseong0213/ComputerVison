from torchvision.datasets import MNIST

import matplotlib.pyplot as plt

mnist_data = MNIST(root="data" , train=True , download=True)
# print(mnist_data)
# print(mnist_data.data,mnist_data.classes,mnist_data.targets)

plt.figure()
plt.suptitle("MNIST" , fontsize=20)

for i in range(10):
    plt.subplot(1, 10 , i+1)
    plt.imshow(mnist_data.data[i], cmap="gray")

plt.show()