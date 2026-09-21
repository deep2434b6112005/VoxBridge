# VoxBridge Gesture Dataset

This directory describes the dataset used for training the VoxBridge hand-gesture recognition model.

The dataset contains gesture samples representing phrases/actions that can be used by a **speech-impaired individual for assistive communication**.

---

## Dataset Purpose

The purpose of the dataset is to train a model that can recognize predefined hand gestures and map them to meaningful communication phrases.

```text
Hand Gesture
     ↓
Gesture Class
     ↓
Communication Phrase
```

---

## Dataset Organization

The recommended structure is:

```text
dataset/
│
├── gesture_1/
│   ├── sample_001.mp4
│   ├── sample_002.mp4
│   └── ...
│
├── gesture_2/
│   ├── sample_001.mp4
│   └── ...
│
├── gesture_3/
│   └── ...
│
└── ...
```

Each directory represents one gesture class.

---

## Example Gesture Classes

Example classes used during development may include communication phrases such as:

```text
Help
Water
Hospital
Medicine
Sorry
Stop
I am hungry
Custom phrases
```

The exact classes can change as the model and application are developed.

---

## Data Processing

Raw videos are processed using MediaPipe.

```text
Video
  ↓
Frame Extraction
  ↓
MediaPipe Hand Detection
  ↓
21 Landmarks / Hand
  ↓
XYZ Coordinates
  ↓
Two-Hand Representation
  ↓
126-Dimensional Feature Vector
  ↓
Temporal Sequence
```

---

## Landmark Representation

Each hand is represented using:

```text
21 landmarks
X coordinate
Y coordinate
Z coordinate
```

For two hands:

```text
21 × 3 × 2 = 126 features
```

The landmark representation allows the model to focus on hand movement and geometry rather than directly learning from raw RGB images.

---

## Sequence Data

Gesture recognition is temporal.

Instead of using only one frame, VoxBridge uses a sequence of landmark frames:

```text
Frame 1
   ↓
Frame 2
   ↓
Frame 3
   ↓
...
Frame N
   ↓
MP-GRU
   ↓
Gesture
```

This allows the model to learn dynamic gestures and movement patterns.

---

## Dataset Quality

For better real-world performance, samples should contain variation in:

* Lighting conditions
* Backgrounds
* Camera distance
* Hand position
* Gesture speed
* Hand orientation
* Different users
* Different execution styles

---

## Privacy

Raw videos may contain identifiable visual information.

For a public GitHub repository, raw personal video data should **not be uploaded unless appropriate consent and permissions have been obtained**.

The public repository can instead contain:

```text
dataset/
└── README.md
```

while keeping the actual dataset privately stored.

---

## Dataset Splitting

The dataset should be divided into separate subsets:

```text
Training Set
Validation Set
Test Set
```

The test set should remain separate from training to provide a more meaningful estimate of real-world performance.

---

## Preprocessing

The preprocessing scripts convert the raw gesture samples into the feature representation required by the MP-GRU model.

The resulting data is then used by the training pipeline in:

```text
../
```

---

## Important Note

The dataset is continuously evolving as new gesture classes, users, and samples are added to VoxBridge.
