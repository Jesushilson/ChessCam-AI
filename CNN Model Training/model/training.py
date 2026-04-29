import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from piece_classifier import PieceClassifier
from pretrained_model import PreTrainedPieceClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import plotting
import time


TRAIN_FOLDER = "data/squares/train"
TEST_FOLDER = "data/squares/test"
VALIDATION_FOLDER = "data/squares/val"



# Grab the data
# Define transforms
transform = transforms.Compose([
    transforms.Resize((50, 50)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# ImageFolder automatically reads subfolders as class labels
train_data = datasets.ImageFolder(TRAIN_FOLDER, transform=transform)
val_data   = datasets.ImageFolder(VALIDATION_FOLDER, transform=transform)
test_data  = datasets.ImageFolder(TEST_FOLDER, transform=transform)

# Then wrap in DataLoader for batching
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_data,   batch_size=32, shuffle=False)
test_loader  = DataLoader(test_data,  batch_size=32, shuffle=False)


criterion = torch.nn.CrossEntropyLoss()



def train_model(model, optimizer, epochs):
    model.train()
    val_accuracies = []
    train_losses = []
    for epoch in range(epochs):
        total_loss = 0
        for images, labels in train_loader:
            # Forward pass
            outputs = model(images)

            # Compute loss
            loss = criterion(outputs, labels)
            
            # Zero gradients
            optimizer.zero_grad()

            # Backprop
            loss.backward()

            # Update weights
            optimizer.step()
            total_loss += loss.item()

        # Validation after each epoch
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                outputs = model(images)
                predictions = outputs.argmax(dim=1)
                val_correct += (predictions == labels).sum().item()
                val_total += labels.size(0)

        avg_loss = total_loss / len(train_loader)
        val_acc = val_correct / val_total

        train_losses.append(avg_loss)
        val_accuracies.append(val_acc * 100)

        print(f"Epoch {epoch+1} | Loss: {avg_loss:.4f} | Val Accuracy: {val_acc*100:.2f}%")
    
    return train_losses, val_accuracies


# ----------Start Train ----------

# Define models
# Note that both models use the exact same data 
homemade_model = PieceClassifier()
homemade_optimizer = torch.optim.Adam(homemade_model.parameters(), lr= 0.001)

pretrained_model = PreTrainedPieceClassifier()
pretrained_optimizer = torch.optim.Adam(pretrained_model.parameters(), lr= 0.001)

EPOCHS = 40


# Lets start with homemade model
print("----STARTING HOMEMADE TRAINING----")
start = time.time()
homemade_losses, homemade_accs = train_model(homemade_model, homemade_optimizer, EPOCHS)
print("----HOMEMADE DONE----")
homemade_time = time.time() - start
print(f"Homemade training time: {homemade_time/60:.1f} minutes")

print("----STARTING ResNet18 TRAINING----")
start = time.time()
pretrained_losses, pretrained_accs = train_model(pretrained_model, pretrained_optimizer, EPOCHS)
print("----ResNet18 DONE----")
resnet_time = time.time() - start
print(f"ResNet18 training time: {resnet_time/60:.1f} minutes")


# Plot both on the same graph
plotting.plot_comparison(homemade_losses, homemade_accs, pretrained_losses, pretrained_accs)

# ----------Start Testing----------

homemade_model.eval()
pretrained_model.eval()

homemade_preds = []
pretrained_pred = []
all_labels = []

print("\n----TESTING HOMEMADE----\n")
all_labels = [] 
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = homemade_model(images)
        predictions = outputs.argmax(dim=1)

        homemade_preds.extend(predictions.tolist())
        all_labels.extend(labels.tolist())

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
print(f"Test Accuracy Of Homemade: {accuracy * 100:.2f}%")
print(classification_report(all_labels, homemade_preds, 
      target_names=train_data.classes))

print("\n----TESTING ResNet18----\n")
all_labels = [] 
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = pretrained_model(images)
        predictions = outputs.argmax(dim=1)

        pretrained_pred.extend(predictions.tolist())
        all_labels.extend(labels.tolist())

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
print(f"Test Accuracy Of ResNet18: {accuracy * 100:.2f}%")
print(classification_report(all_labels, pretrained_pred, 
      target_names=train_data.classes))

# Plot based on test accuracy across classes
plotting.plot_class_accuracy(all_labels, "Homemade Model", homemade_preds, train_data.classes)
plotting.plot_class_accuracy(all_labels, "ResNet18 Model", pretrained_pred, train_data.classes)

# Check confusion matrix 
plotting.plot_confusion_matrix(all_labels, homemade_preds, train_data.classes, "Homemade CNN")
plotting.plot_confusion_matrix(all_labels, pretrained_pred, train_data.classes, "ResNet18")


# Save
torch.save(homemade_model.state_dict(), "homemade_model.pth")
torch.save(pretrained_model.state_dict(), "resnet_model.pth")