import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchmetrics import Accuracy

##데이터 수집
mnist_trainset = MNIST(root="data" , train=True , download=True,
                       transform=ToTensor()
                       )

train_Loader = DataLoader(mnist_trainset, batch_size=128)

##모델 선언
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 128),
    nn.Sigmoid(),
    nn.Linear(128, 10),
    nn.Softmax(dim=1)
)
print(model)

##학습
num_epochs = 10 
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(),lr=0.01)
matric = Accuracy(task="multiclass" ,num_classes=10)

model.train()
for i in range(num_epochs):
    for j ,(x , y) in enumerate(train_Loader):
        y_hat = model(x)
        y = F.one_hot(y , num_classes=10).float()
        loss = loss_fn(y_hat, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        acc = matric(y_hat , y)
        if j % 100 == 0:
            print(f"epoch: {str(i).zfill(2)}, iter: {str(j).zfill(3)}, loss: {loss:7f} , accuracy: {acc:7f}")
        
        
        