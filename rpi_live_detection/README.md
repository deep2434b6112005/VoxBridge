# VoxBridge Raspberry Pi Live Detection

This directory contains the **real-time Edge-AI inference system** used to run VoxBridge on the Raspberry Pi.

The Raspberry Pi acts as the processing unit of the chest-mounted assistive communication device.

---

## Live System Pipeline

```text
              Camera
                │
                ▼
        Raspberry Pi Camera
                │
                ▼
       Latest Frame Buffer
                │
                ▼
     MediaPipe Hand Landmarker
                │
                ▼
       21 Points / Hand
                │
                ▼
       126-D Feature Vector
                │
                ▼
             MP-GRU
                │
                ▼
      Gesture Classifier
                │
                ▼
    Confidence / Margin Check
                │
                ▼
       Stability Filtering
                │
                ▼
       Gesture → Phrase
                │
          ┌─────┴─────┐
          ▼           ▼
       Piper TTS    Firebase
          │
          ▼
        Speaker
```

---

## Purpose

The live detection system converts a person's hand gestures into audible speech in real time.

It is designed for the **chest-mounted VoxBridge assistive device for speech-impaired individuals**.

---

## Main Files

```text
rpi_live_detection/
│
├── README.md
│
├── live_detect.py
├── mp_gru.py
├── model.py
├── gesture_classifier.pt
├── labels.json
├── hand_landmarker.task
│
├── firebase_worker.py
│
├── tts/
│   └── ...
│
├── config/
│   └── ...
│
└── requirements.txt
```

### `live_detect.py`

Main real-time detection application.

It coordinates:

* Camera input
* MediaPipe processing
* Landmark buffering
* MP-GRU inference
* Gesture classification
* Stability filtering
* Phrase generation
* TTS output

### `mp_gru.py`

Contains the temporal MP-GRU model used for gesture sequence processing.

### `model.py`

Contains the gesture classification architecture used with the MP-GRU representation.

### `gesture_classifier.pt`

Trained model checkpoint used for live inference.

### `labels.json`

Maps classifier output indices to gesture labels.

### `hand_landmarker.task`

MediaPipe Hand Landmarker model used for hand landmark detection.

### `firebase_worker.py`

Handles supported Firebase synchronization and remote state/configuration features.

---

## Raspberry Pi Environment

The prototype is designed for:

```text
Raspberry Pi 4
64-bit Raspberry Pi OS
Python 3
Camera Module
Speaker + Audio Amplifier
```

The inference pipeline is designed to run locally on the Raspberry Pi.

---

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd VoxBridge/rpi_live_detection
```

Create or activate the Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Additional system dependencies may be required for Raspberry Pi camera and audio components.

---

## Running Live Detection

Connect the camera and speaker to the Raspberry Pi.

Then run:

```bash
python3 live_detect.py --source 0 --device cpu
```

For debugging:

```bash
python3 live_detect.py --device cpu --debug
```

The exact command may vary depending on the camera source and deployment configuration.

---

## Gesture Recognition

The live detector receives hand landmarks from MediaPipe and generates a sequence for the MP-GRU model.

The model then produces gesture probabilities.

The decision system uses multiple checks before accepting a gesture.

```text
Model Prediction
      ↓
Confidence Check
      ↓
Top-2 Margin Check
      ↓
EMA Smoothing
      ↓
Temporal Stability
      ↓
Cooldown
      ↓
Accepted Gesture
```

This prevents a single incorrect frame from immediately triggering speech.

---

## Two-Hand Support

The system supports up to two detected hands.

The feature representation is:

```text
Hand 1 → 21 × XYZ
Hand 2 → 21 × XYZ

Total = 126 features
```

When a second hand is not detected, the missing-hand representation is handled by the preprocessing/inference pipeline.

---

## Text-to-Speech

After a gesture is accepted:

```text
Gesture
   ↓
Phrase Mapping
   ↓
Piper TTS
   ↓
Audio Output
   ↓
Speaker
```

Piper provides local text-to-speech capability without requiring cloud-based speech generation for the core output.

---

## Custom Gesture Mode

VoxBridge supports configurable gesture-to-phrase mappings.

Example:

```text
Gesture → "I need water"
Gesture → "Please help me"
Gesture → "I need medicine"
Gesture → "Take me to the hospital"
```

The phrase set can be adapted according to the user's communication requirements.

---

## Firebase Integration

Firebase can be used for supported remote synchronization features such as:

* Mode synchronization
* Custom gesture configuration
* Application/device communication
* Gesture state updates

Sensitive Firebase credentials must never be committed to GitHub.

---

## Security

Do **not** commit:

```text
Firebase service account credentials
API keys
Private keys
Passwords
.env files
Personal user information
Private datasets
```

Use environment variables or local configuration files for sensitive information.

---

## Performance Architecture

The live system uses a producer/consumer-style architecture to prevent slow AI processing from unnecessarily blocking camera acquisition.

Conceptually:

```text
Camera Thread
      │
      ▼
Latest Frame Buffer
      │
      ▼
MediaPipe Processing
      │
      ▼
Latest Result Buffer
      │
      ▼
Inference Worker
      │
      ├── MP-GRU
      ├── Classifier
      ├── Decision Engine
      │
      ├── TTS
      └── Firebase
```

The architecture prioritizes the **latest camera frame** rather than processing every old frame when inference is slower than the camera.

---

## Hardware Deployment

The intended physical arrangement is:

```text
       ┌─────────────────────┐
       │   Chest-Mounted     │
       │     Enclosure       │
       │                     │
       │  Raspberry Pi       │
       │  Camera             │
       │  Audio System       │
       └─────────────────────┘
                 │
                 ▼
          User performs
           hand gesture
                 │
                 ▼
        Gesture recognized
                 │
                 ▼
             Speaker
                 │
                 ▼
          Audible phrase
```

---

## Development Status

The Raspberry Pi implementation is a working prototype under active development.

Current development focuses on:

* Real-time inference
* Recognition stability
* Two-hand gestures
* Custom gesture mode
* TTS reliability
* Firebase synchronization
* Wearable/chest-mounted deployment
* Improving robustness under real-world conditions
