import torch
import numpy as np
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
from pathlib import Path

# device
device = torch.device("cpu")

# transform (same as training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

BASE_DIR = Path(__file__).resolve().parent

def load_resnet(path):
    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features, 10)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model


def load_mobilenet(path):
    model = models.mobilenet_v2()
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 10)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model


def load_shufflenet(path):
    model = models.shufflenet_v2_x1_0()
    model.fc = nn.Linear(model.fc.in_features, 10)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model

resnet_path = BASE_DIR / "models" / "resnet18_tomato.pth"
mobilenet_path = BASE_DIR / "models" / "mobilenet_tomato.pth"
shufflenet_path = BASE_DIR / "models" / "shufflenet_v2_tomato.pth"

resnet = load_resnet(resnet_path)
mobilenet = load_mobilenet(mobilenet_path)
shufflenet = load_shufflenet(shufflenet_path)

def extract_features(image_path):
    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        r = resnet(tensor).squeeze().numpy()      # (10,)
        m = mobilenet(tensor).squeeze().numpy()  # (10,)
        s = shufflenet(tensor).squeeze().numpy() # (10,)

        features = np.hstack([r, m, s])
    return features  # (30,)