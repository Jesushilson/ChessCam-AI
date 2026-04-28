import torch
import torch.nn as nn
import torch.nn.functional as F


# Self made Architecture of the CNN model that will identify pieces that are shown
class PieceClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # Layers 
        # First convolutional layers that takes in a color image(3 channels) and applies 16 learnable 
        # Kernels of size 3X3
        # There is about only one channel per input.
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=32,
            kernel_size=3,
            padding= 1
        )
        self.bn1 = nn.BatchNorm2d(32)  # matches conv1 out_channels
        # Second convolutional layer that takes in 32 channels applies 64 3x3 kernels
        # The output
        self.conv2 = nn.Conv2d(
            in_channels=32,
            out_channels=64,
            kernel_size=3,
            padding= 1
        )
        self.bn2 = nn.BatchNorm2d(64)  # matches conv2 out_channels

        self.conv3 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=3,
            padding= 1
        )
        self.bn3 = nn.BatchNorm2d(128)  # matches conv1 out_channels
        self.pool = nn.MaxPool2d(2, 2)
        
        
        # Fully connected layers
        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.2)
        self.fc1 = nn.Linear(4608, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 13)

    def forward(self, x):
        # x is passed through the first convolutional 
        x = self.conv1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv2(x)     
        x = self.bn2(x)
        x = F.relu(x)
        x = self.pool(x)     

        x = self.conv3(x)     
        x = self.bn3(x)
        x = F.relu(x)
        x = self.pool(x)    

        x = torch.flatten(x, 1)  # (N, 128*6*6)

        x = self.fc1(x)   
        x = F.relu(x)
        x = self.dropout1(x)
        x = self.fc2(x)       
        x = self.dropout2(x)
        x = F.relu(x)
        x = self.fc3(x)

        return x
    
