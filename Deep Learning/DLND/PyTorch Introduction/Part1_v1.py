import torch

def activation(x):
    """
    Sigmoid activation function

    :param x:
    :type x: torch.Tensor
    :return:
    :rtype:
    """
    return 1/(1 + torch.exp(-x))

#set seed
torch.manual_seed(7)

# features are 5 random normal variables
features = torch.randn((1,5))

# true weights for our data, random normal variables again
weights = torch.randn_like(features)

# and a true bias term
bias = torch.randn((1,1))

y = activation(torch.sum(features * weights) + bias)
#y = activation((features * weights).sum() + bias)

#doing the matrix multiplication via torch.mm
# print(activation(torch.mm(features,weights.view(5,1)) + bias))
# print(y)


#_____________________________________________________#

#define the size of each layer in our network
n_input = features.shape[1]
n_hidden = 2
n_output = 1

#weights for inputs to hidden layer
W1 = torch.randn(n_input, n_hidden)
W2 = torch.randn(n_hidden, n_output)

B1 = torch.randn((1, n_hidden))
B2 = torch.randn((1, n_output))

f = activation

y = f(torch.mm(f(torch.mm(features, W1) + B1), W2) + B2)

#print(y)


#_____________________________________________________#
import numpy as np

a = np.random.rand(4,3)
b = torch.from_numpy(a)
#print(b.numpy())

#Multiply PyTorch Tensor by 2, in place
#print(b.mul_(2))

#Numpy array matches new values from tensor
#print(a)



#_____________________________________________________#
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((.5,  .5, .5), (.5, .5, .5))
])

trainset = datasets.MNIST('mnist_data/', download=True, train=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

dataiter = iter(trainloader)
images, labels = dataiter.next()

print(type(images))
print(images.shape)
print(labels.shape)

plt.imshow(images[1].numpy().squeeze(), cmap='Greys_r');
plt.show()

def activation(x):
    return 1 / (1 + torch.exp(-x))

def softmax(x):
    return torch.exp(x) / torch.sum(torch.exp(x), dim=1).view(-1,1)


#flatten the input images
inputs = images.view(images.shape[0], -1)

#create parameters
w1 = torch.randn(784,256)
b1 = torch.randn(256)

w2 = torch.randn(256,10)
b2 = torch.randn(10)

h = activation(torch.mm(inputs, w1) + b1)
out = torch.mm(h, w2) + b2
probabilities = softmax(out)

#print(probabilities.shape)
#print(probabilities.sum(dim=1))


