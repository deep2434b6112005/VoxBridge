# VoxBridge Training

This directory contains the **machine-learning training pipeline** for VoxBridge.

The purpose of this pipeline is to train a gesture-recognition model that can later be deployed on the Raspberry Pi chest-mounted device.

---

## Training Pipeline

```text
Raw Gesture Videos
        │
        ▼
Hand Landmark Extraction
        │
        ▼
MediaPipe 21-Point Landmarks
        │
        ▼
Two-Hand Feature Representation
        │
        ▼
126-Dimensional Sequences
        │
        ▼
Preprocessing
        │
        ▼
MP-GRU
        │
        ▼
Gesture Classifier
        │
        ▼
Trained Model
        │
        ▼
Raspberry Pi Deployment
```

---

## Input Representation

VoxBridge uses MediaPipe hand landmarks as the input representation.

Each detected hand contains:

```text
21 landmarks
×
3 coordinates (X, Y, Z)
```

For two hands:

```text
21 × 3 × 2 = 126 features
```

The resulting sequence is provided to the temporal model.

---

## Model Architecture

The current architecture uses:

```text
MediaPipe Landmarks
        ↓
MP-GRU
        ↓
Embedding
        ↓
Gesture Classifier
        ↓
Gesture Class
```

The GRU-based temporal model allows VoxBridge to learn movement patterns across multiple frames rather than relying only on a single image.

---

## Main Training Components

```text
training/
│
├── README.md
│
├── dataset/
│   └── README.md
│
├── preprocessing/
│   ├── preprocess_dataset.py
│   └── feature_extraction.py
│
├── model/
│   ├── mp_gru.py
│   └── model.py
│
├── training/
│   └── train_classifier.py
│
├── evaluation/
│   └── validate_model.py
│
└── requirements.txt
```

---

## Dataset Preparation

Gesture videos are organized by gesture class.

The preprocessing stage converts the videos into landmark sequences suitable for model training.

Example:

```text
Gesture Video
     ↓
MediaPipe
     ↓
Hand Landmarks
     ↓
Normalization / Preprocessing
     ↓
Sequence
     ↓
Training Sample
```

See:

```text
dataset/README.md
```

for dataset organization.

---

## Training

After preparing the dataset, the classifier can be trained using the training script.

Example:

```bash
python train_classifier.py
```

The exact command may depend on the local training configuration.

---

## Model Output

The training process produces a trained classifier checkpoint that can be transferred to the Raspberry Pi deployment environment.

Example:

```text
gesture_classifier.pt
```

The corresponding gesture labels are stored separately:

```text
labels.json
```

---

## Evaluation

The trained model should be evaluated using data that was not used during training.

Important evaluation metrics include:

* Accuracy
* Validation accuracy
* Confusion matrix
* Per-class performance
* False predictions
* Real-world gesture stability

---

## Important Considerations

The training dataset should contain variations in:

* Hand position
* Distance from camera
* Lighting
* Background
* Gesture speed
* Hand orientation
* User hand size
* Single-hand and two-hand situations

This improves robustness during real-world deployment.

---

## Deployment

After training and validation, the trained model is integrated into:

```text
rpi_live_detection/
```

The Raspberry Pi then performs live inference from the camera feed.
