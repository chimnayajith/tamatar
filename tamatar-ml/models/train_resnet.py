import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from utils.dataset_loader import load_dataset
from sklearn.metrics import classification_report
import pandas as pd
from config import EPOCHS, LEARNING_RATE

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Transforms (IMPORTANT: same for train + test)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Load dataset
train_loader, val_loader, test_loader = load_dataset(
    data_path="dataset",
    batch_size=8,
    transform=transform,
    train_ratio=0.7,
    val_ratio=0.15,
    test_ratio=0.15
)

# Get class names
classes = train_loader.dataset.dataset.classes

# Model
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze layers
for param in model.parameters():
    param.requires_grad = False

# Replace final layer
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(classes))
model = model.to(device)

# Loss & Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

# ========================
# TRAINING
# ========================
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_loss = running_loss / total
    train_acc = 100 * correct / total

    # ========================
    # VALIDATION
    # ========================
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_acc = 100 * val_correct / val_total


    print("\n" + "="*30)
    print(f"Epoch {epoch+1} / {EPOCHS}")
    print("-"*30)
    print(f"Loss     : {train_loss:.4f}")
    print(f"Accuracy : {train_acc:.2f}%")
    print(f"Val Acc  : {val_acc:.2f}%")
    print("="*30)

# Save model
torch.save(model.state_dict(), "resnet18_tomato.pth")
print("\nModel saved as resnet18_tomato.pth")

# ========================
# TESTING
# ========================
model.eval()

all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# ========================
# METRICS
# ========================
report = classification_report(
    all_labels,
    all_preds,
    labels=list(range(len(classes))),
    target_names=classes,
    output_dict=True,
    zero_division=0
)
df = pd.DataFrame(report).transpose()

accuracy = report['accuracy']

print("\n" + "="*50)
print("MODEL PERFORMANCE REPORT")
print("="*50)

print(f"\nOverall Accuracy: {accuracy*100:.2f}%\n")

print("-"*50)
print("Class-wise Metrics")
print("-"*50)

df_clean = df.drop(['accuracy', 'macro avg', 'weighted avg'], errors='ignore')
print(df_clean.round(3))

print("\n" + "="*50)