import torch
from torch.utils.data import random_split, DataLoader
from torchvision.datasets import ImageFolder

def load_dataset(data_path, batch_size=8, transform=None, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Load and split the dataset into training, validation, and testing sets.

    Args:
        data_path (str): Path to the dataset directory.
        batch_size (int): Batch size for the DataLoader.
        transform (callable, optional): Transformations to apply to the dataset.
        train_ratio (float): Proportion of the dataset to use for training.
        val_ratio (float): Proportion of the dataset to use for validation.
        test_ratio (float): Proportion of the dataset to use for testing.

    Returns:
        tuple: DataLoaders for training, validation, and testing sets.
    """
    # Load the dataset
    dataset = ImageFolder(data_path, transform=transform)

    # Calculate split sizes
    total_size = len(dataset)
    train_size = int(train_ratio * total_size)
    val_size = int(val_ratio * total_size)
    test_size = total_size - train_size - val_size

    # Split the dataset
    train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader