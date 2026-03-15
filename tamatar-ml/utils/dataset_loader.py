import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_dataloaders(dataset_path, batch_size=8):

    transform = transforms.Compose([
        transforms.Resize((224, 224)),     # required for CNN
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ToTensor()
    ])

    dataset = datasets.ImageFolder(
        root=dataset_path,
        transform=transform
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4
    )

    return dataloader, dataset.classes