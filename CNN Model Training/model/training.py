import os
import shutil
import random
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from piece_classifier import PieceClassifier
from sklearn.metrics import classification_report



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


# Define model
model = PieceClassifier()
optimizer = torch.optim.Adam(model.parameters(), lr= 0.001)
criterion = torch.nn.CrossEntropyLoss()


epochs = 10

model.train()
print("STARTING TRAINING")
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
    print(f"Epoch {epoch+1} | Loss: {avg_loss:.4f} | Val Accuracy: {val_acc*100:.2f}%")


model.eval()
correct = 0
total = 0
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        all_preds.extend(predictions.tolist())
        all_labels.extend(labels.tolist())

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
print(f"Test Accuracy: {accuracy * 100:.2f}%")
print(classification_report(all_labels, all_preds, 
      target_names=train_data.classes))
