import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models



class PreTrainedPieceClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # Load pretrained ResNet18
        self.base = models.resnet18(pretrained=True)
        # Replace final layer for 13 classes
        self.base.fc = nn.Linear(512, 13)

    def forward(self, x):
        return self.base(x)