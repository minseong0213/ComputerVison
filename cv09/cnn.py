import torch
from torch import nn, optim
from torch.utils.data import DataLoader

from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor


##데이터 수집
train_data = MNIST(root="data" , train=True , download=True,
                       transform=ToTensor()
                       )
test_data = MNIST(root="data" , train=True , download=True,
                       transform=ToTensor()
                       )

train_Loader = DataLoader(train_data, batch_size=128)
# test_Loader = DataLoader(test_data, batch_size=128)

model = nn.Sequential(
    nn.Conv2d(
        in_channels=1, out_channels=6, kernel_size=5, padding=2),
    nn.ReLU(),
    nn.MaxPool2d(2, stride=2),
    nn.Conv2d(6, 16, 5),
    nn.ReLU(),
    nn.MaxPool2d(2, stride=2),
    nn.Conv2d(16, 120, 5),
    nn.ReLU(),
    nn.Flatten(),
    nn.Linear(in_features=120, out_features=84),
    nn.ReLU(),
    nn.Linear(84, 10)
)

