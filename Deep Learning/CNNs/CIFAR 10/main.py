import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim

from torch import nn
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision import datasets
from torchvision import transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        #convolutional layer, sees 32x32x3 image tensor
        #has 3 input channels (R,G,B Colors), goes for 16 filters and
        #has a kernel size of 3. To avoid shrinking of the output layers
        #padding is set to 1, since kernel size is 3
        self.conv1 = nn.Conv2d(3,16,3, padding=1)
        self.conv2 = nn.Conv2d(16,32,3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2,2)

        #final classifier
        #linear layer #1:  64 * 4 * 4, 500
        self.fc1 = nn.Linear(64*4*4, 500)
        #output to 10 different classes
        self.fc2 = nn.Linear(500,10)

        #Regularization
        self.dropout = nn.Dropout(.25)

    def forward(self,x):

        #Sequence of Convolutionals
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))

        #flatten image input
        x = x.view(-1, 64 * 4 * 4)

        #add dropout
        x = self.dropout(x)

        #classifier
        #both classifier layers with relu activation and first one with dropout
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)

        return x

batch_size = 20
valid_size = .2

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((.5,.5,.5),(.5,.5,.5))
])

# fetch and store CIFAR 10
train_data = datasets.CIFAR10('data', train=True,
                              download=True, transform=transform)
test_data = datasets.CIFAR10('data', train=False,
                             download=True, transform=transform)


#obtain training indices that will be used for validation
num_train = len(train_data)
indices = list(range(num_train))
np.random.shuffle(indices)
split = int(np.floor(valid_size * num_train))
train_idx, valid_idx = indices[split:], indices[:split]

#samplers for obtaining training and validation batches
train_sampler = SubsetRandomSampler(train_idx)
test_sampler = SubsetRandomSampler(valid_idx)

#prepare data loaders (combine dataset and sampler)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, sampler=train_sampler)
valid_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, sampler=test_sampler)

#image classes
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']


#____Modelling____
model = Net()
print(model)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=.01)

n_epochs = 30

#Track change in validation loss
valid_loss_min = np.Inf

for epoch in range(n_epochs):
    train_loss = 0.0
    valid_loss = 0.0

    ###################
    # train the model #
    ###################
    model.train()

    for data, labels in train_loader:
        #clear the gradients of all optimized variables
        optimizer.zero_grad()

        #forward pass: compute predicted outputs by passing inputs to the model
        output = model(data)

        #calculate the batch loss
        loss = criterion(output, labels)

        #backward pass: compute gradients of the loss with respect to model parameters
        loss.backward()

        #perform a single optimization step (parameter update)
        optimizer.step()

        #update training loss
        train_loss += loss.item() * data.size(0)

    ######################
    # validate the model #
    ######################
    model.eval()
    for data, label in valid_loader:
        output = model(data)
        loss = criterion(output, label)
        valid_loss += loss.item() * data.size(0)

    train_loss = train_loss / len(train_loader)
    valid_loss = valid_loss / len(valid_loader)

    print('Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}'.format(
        epoch, train_loss, valid_loss
    ))

    # save model if validation loss has decreased
    if valid_loss <= valid_loss_min:
        print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(
            valid_loss_min,
            valid_loss))
        torch.save(model.state_dict(), 'model_cifar.pt')
        valid_loss_min = valid_loss