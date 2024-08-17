import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
from efficientnet_pytorch import EfficientNet

class DocumentClassifier(nn.Module):
    def __init__(self, num_classes=3):
        super(DocumentClassifier, self).__init__()
        self.backbone = EfficientNet.from_pretrained('efficientnet-b0')
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        num_features = self.backbone._fc.in_features
        
        self.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.6),  # Increased dropout rate
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.6),  # Increased dropout rate
            nn.Linear(256, num_classes),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        x = self.backbone.extract_features(x)
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# Enhanced data augmentation with grayscale conversion
train_transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # Convert to grayscale with 3 channels
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),  # Added vertical flip
    transforms.RandomRotation(20),  # Increased rotation range
    transforms.ColorJitter(brightness=0.3, contrast=0.3),  # Increased jitter
    transforms.RandomAffine(degrees=15, translate=(0.15, 0.15)),  # Increased translation
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

val_test_transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # Convert to grayscale with 3 channels
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Dataset and DataLoader
base_dir = '/mnt/c/Users/Rahul/Desktop/Datasets'
train_dataset = datasets.ImageFolder(root=os.path.join(base_dir, 'train'), transform=train_transform)
val_dataset = datasets.ImageFolder(root=os.path.join(base_dir, 'val'), transform=val_test_transform)
test_dataset = datasets.ImageFolder(root=os.path.join(base_dir, 'test'), transform=val_test_transform)

train_loader = DataLoader(dataset=train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(dataset=val_dataset, batch_size=32, shuffle=False, num_workers=4)
test_loader = DataLoader(dataset=test_dataset, batch_size=32, shuffle=False, num_workers=4)

# Initialize model, loss, optimizer, and scheduler
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DocumentClassifier(num_classes=3).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)

from torch.optim import lr_scheduler
scheduler = lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.7)

# Early Stopping class
class EarlyStopping:
    def __init__(self, patience=7):
        self.patience = patience
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0

# Training and validation loop
def train_and_validate(model, train_loader, val_loader, num_epochs=25):
    early_stopping = EarlyStopping(patience=7)
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total_train += labels.size(0)
            correct_train += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_accuracy = correct_train / total_train
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.4f}')
        
        val_loss = validate(model, val_loader)
        early_stopping(val_loss)
        scheduler.step()  # Update the learning rate
        
        if early_stopping.early_stop:
            print("Early stopping")
            break
    
    # Save the model
    torch.save(model.state_dict(), 'document_classifier.pth')

# Validation
def validate(model, val_loader):
    model.eval()
    val_loss = 0.0
    correct_val = 0
    total_val = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()
    val_loss /= len(val_loader.dataset)
    val_accuracy = correct_val / total_val
    print(f'Validation Loss: {val_loss:.4f}, Accuracy: {val_accuracy:.4f}')
    return val_loss

# Testing
def test(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    all_labels = []
    all_preds = []
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            all_labels.extend(labels.cpu().numpy())
            all_preds.extend(predicted.cpu().numpy())
    
    accuracy = accuracy_score(all_labels, all_preds)
    print(f'Test Accuracy: {accuracy:.4f}')
    
    # Class mapping
    class_mapping = {0: 'citizenship', 1: 'license', 2: 'passport'}

    # Display actual vs predicted
    print("Actual vs Predicted:")
    for label, pred in zip(all_labels, all_preds):
        print(f'Actual: {class_mapping[label]}, Predicted: {class_mapping[pred]}')

    # Visualize some predictions
    import matplotlib.pyplot as plt
    import numpy as np

    def imshow(img, title=None):
        img = img / 2 + 0.5  # Unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        if title is not None:
            plt.title(title)
        plt.axis('off')

    dataiter = iter(test_loader)
    images, labels = next(dataiter)
    outputs = model(images.to(device))
    _, preds = torch.max(outputs, 1)
    
    # Plotting the images with actual and predicted labels
    plt.figure(figsize=(12, 12))
    for idx in range(16):
        plt.subplot(4, 4, idx + 1)
        imshow(images[idx])
        plt.title(f'Actual: {class_mapping[labels[idx].item()]}\nPred: {class_mapping[preds[idx].item()]}')
        plt.axis('off')
    plt.show()

# Call training and validation
train_and_validate(model, train_loader, val_loader, num_epochs=30)
# Call testing
test(model, test_loader)

# To load the model later, use:
# model = DocumentClassifier(num_classes=3)
# model.load_state_dict(torch.load('document_classifier.pth'))
# model.to(device)
