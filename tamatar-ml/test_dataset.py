from utils.dataset_loader import get_dataloaders

loader, classes = get_dataloaders("dataset/PlantVillage")

print("Classes:", classes)

for images, labels in loader:
    print("Batch shape:", images.shape)
    print("Labels:", labels)
    break