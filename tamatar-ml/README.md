# Tamatar ML Pipeline 🍅

Machine learning pipeline for **Tomato Leaf Disease Detection** using the **PlantVillage dataset**.

This project implements the pipeline described in the paper:

> *Tomato Leaf Disease Classification via Compact Convolutional Neural Networks with Transfer Learning and Feature Selection*

The model trains CNN architectures such as **ResNet18, MobileNet, and ShuffleNet** to classify tomato leaf diseases.

---

# Project Structure

```

tamatar/
│
├── tamatar-frontend/       # PWA frontend
│
└── tamatar-ml/
├── dataset/            # dataset directory (not committed)
├── models/
│   └── train_resnet.py
│
├── utils/
│   └── dataset_loader.py
│
├── test_dataset.py
├── requirements.txt
└── README.md

````

---

# Requirements

- Python **3.10+**
- NVIDIA GPU (optional but recommended)
- CUDA drivers installed (if using GPU)

---

# Setup

Clone the repository:

```bash
git clone https://github.com/chimnayajith/tamatar.git
cd tamatar/tamatar-ml
````

---

# Create Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# Install Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

# Dataset Setup

This project uses the **PlantVillage dataset**.

Download from:

[https://www.kaggle.com/datasets/emmarex/plantdisease](https://www.kaggle.com/datasets/emmarex/plantdisease)

After downloading and extracting, copy **only the tomato classes** into:

```
tamatar-ml/dataset/
```

Your dataset directory should look like this:

```
dataset/
├── Tomato_Bacterial_spot
├── Tomato_Early_blight
├── Tomato_Late_blight
├── Tomato_Leaf_Mold
├── Tomato_Septoria_leaf_spot
├── Tomato_Spider_mites_Two_spotted_spider_mite
├── Tomato__Target_Spot
├── Tomato__Tomato_YellowLeaf__Curl_Virus
├── Tomato__Tomato_mosaic_virus
└── Tomato_healthy
```

The dataset contains **10 tomato leaf classes**.

---

## Verify Dataset Loader

Before starting development or training models, verify that the dataset loads correctly.

Run:

```bash
python test_dataset.py
```

Expected output:

```
Classes: ['Tomato___Bacterial_spot', ...]
Batch shape: torch.Size([8, 3, 224, 224])
```

This confirms:

* images are loaded correctly
* preprocessing pipeline is working


---

## Data Preprocessing

The dataset loader automatically applies preprocessing and augmentation using PyTorch transforms.

Current preprocessing pipeline:

- Resize images to **224 × 224**
- Random horizontal flipping
- Random rotation
- Random affine transformation (scale + shear)
- Convert images to PyTorch tensors
- Normalize using ImageNet statistics

These steps improve model generalization and prepare the dataset for CNN training.

---

## Current Implementation Status

The following components are currently implemented:

- Dataset loader
- Data preprocessing pipeline
- Data augmentation
- Dataset verification script (`test_dataset.py`)

This ensures that the dataset can be loaded and prepared correctly for model training.

---

## Planned Pipeline

The full pipeline will consist of the following stages:

1. Image preprocessing
2. Data augmentation
3. CNN training (ResNet18 / MobileNet / ShuffleNet)
4. Deep feature extraction
5. Feature concatenation
6. Hybrid feature selection
7. Machine learning classifier training

---

## Contributing

If you are contributing to the project, please follow this workflow:

1. Clone the repository
2. Set up the Python environment
3. Download the PlantVillage dataset
4. Run `test_dataset.py` to verify the dataset loader
5. Implement or extend components in the `tamatar-ml` directory

---

## Notes

- The dataset is **not included in the repository** due to its large size.
- A GPU is recommended for training models.
- The frontend application is located in `tamatar-frontend`.

---

## Development Roadmap

- [x] Dataset loader
- [x] Data preprocessing pipeline
- [ ] ResNet18 training script
- [ ] MobileNet training script
- [ ] ShuffleNet training script
- [ ] Feature extraction module
- [ ] Feature selection module
- [ ] Final classifier training
---