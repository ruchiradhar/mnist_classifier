# Data: FashionMNIST data
# Model: Classifier

# Importing dependencies
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# DATASET SETUP
# Download and transform data
training_data= datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

test_data= datasets.FashionMNIST(
    root= "data",
    train=False,
    download=True,
    transform=ToTensor()
)

# Create dataloaders
batch_size=64 # each dl element is batch of 64 features and labels
train_dataloader= DataLoader(training_data, batch_size=batch_size)
test_dataloader= DataLoader(test_data, batch_size=batch_size)

for X,y in test_dataloader: 
    print(f"Shape of input: {X.shape}")
    print(f"Shape of y: {y.shape} {y.dtype}")
    break

# MODEL SETUP
# Set device
device=('mps' if torch.backends.mps.is_available else 'cpu')

# Set model
class NeuralNetwork(nn.Module):
    def __init__(self): 
        super().__init__()
        self.flatten=nn.Flatten()
        self.linear_relu_stack=nn.Sequential(
            nn.Linear(28*28,512),
            nn.ReLU(),
            nn.Linear(512,512),
            nn.ReLU(),
            nn.Linear(512,10)

        )
    def forward(self,x): 
        x=self.flatten(x)
        logits= self.linear_relu_stack(x)
        return logits

model=NeuralNetwork().to(device)

# Set loss 
loss_fn=nn.CrossEntropyLoss()

# Set optimizer
optimizer=torch.optim.SGD(model.parameters(),lr=1e-3)


# TRAINING SETUP
def train(dataloader,model,loss_fn,optimizer):
    size=len(dataloader.dataset)
    model.train()
    for batch, (X,y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # compute pred error
        pred=model(X)
        loss=loss_fn(pred,y)

        # backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


# TESTING SETUP
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

# MODEL TRAINING ITERATIONS
epochs = 5
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")
