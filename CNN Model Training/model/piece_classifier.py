import torch
import torch.nn as nn
import torch.nn.functional as F

# Architecture of the CNN model that will identify pieces that are shown
class PieceClassifier(nn.Module):
    def __init__(self):
        super().__init__()

        # Layers 
        # First convolutional layers that takes in a color image(3 channels) and applies 16 learnable 
        # Kernels of size 3X3
        # There is about only one channel per input.
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=16,
            kernel_size=3,
            padding= 1
        )
        # Second convolutional layer that takes in 16 channels applies 32 3x3 kernels
        # The output
        self.conv2 = nn.Conv2d(
            in_channels=16,
            out_channels=32,
            kernel_size=3,
            padding= 1
        )
        self.conv3 = nn.Conv2d(
            in_channels=32,
            out_channels=64,
            kernel_size=3,
            padding= 1
        )
        self.pool = nn.MaxPool2d(2, 2)
        
        
        # Fully connected layers
        self.dropout = nn.Dropout(0.2)
        self.fc1 = nn.Linear(2304, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 13)

    def forward(self, x):
        # x is passed through the first convolutional 
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv2(x)     # (N, 32, 25, 25)
        x = F.relu(x)
        x = self.pool(x)      # (N, 32, 8, 8)

        x = self.conv3(x)     # (N, 64, 12, 12)
        x = F.relu(x)
        x = self.pool(x)      # (N, 64, 6, 6)

        x = torch.flatten(x, 1)  # (N, 64*6*6)

        x = self.fc1(x)       # (N, 128)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)       # (N, num_classes) 
        x = F.relu(x)
        x = self.fc3(x)

        return x
    
