# VoxBridge

## Edge-AI Assistive Communication System for Speech-Impaired Individuals

**VoxBridge** is an Edge-AI powered assistive communication system designed to help **speech-impaired individuals communicate with others** by converting predefined hand gestures into audible speech.

The system uses a camera mounted on a wearable/chest-mounted device to capture hand gestures. The gestures are processed locally on a Raspberry Pi using MediaPipe and an MP-GRU based deep-learning model. The recognized gesture is converted into a predefined phrase and spoken through a speaker.

> **With VoxBridge, every gesture becomes a voice. Today we translate gestures. Tomorrow we transform lives.**

---

## System Overview

```text
        Hand Gesture
             │
             ▼
      Camera / OV5647
             │
             ▼
     Raspberry Pi 4
             │
             ▼
  MediaPipe Hand Landmarker
             │
             ▼
  126-Dimensional Landmarks
       (21 × XYZ × 2)
             │
             ▼
          MP-GRU
             │
             ▼
    Gesture Classifier
             │
             ▼
 Confidence + Stability
        Filtering
             │
             ▼
      Phrase Generation
             │
             ▼
         Piper TTS
             │
             ▼
          Speaker
```

---

## Key Features

* Assistive communication for speech-impaired individuals
* Edge-AI inference on Raspberry Pi
* Real-time hand gesture recognition
* MediaPipe hand landmark extraction
* MP-GRU temporal gesture modeling
* Support for two-hand gestures
* Confidence and stability filtering
* Customizable gesture-to-phrase mapping
* Offline text-to-speech using Piper
* Firebase-based synchronization for supported features
* Chest-mounted wearable deployment concept

---

## Repository Structure

```text
VoxBridge/
│
├── training/
│   ├── README.md
│   └── ...
│
├── rpi_live_detection/
│   ├── README.md
│   ├── live_detect.py
│   ├── mp_gru.py
│   ├── model.py
│   ├── gesture_classifier.pt
│   ├── labels.json
│   ├── hand_landmarker.task
│   └── ...
│
├── app/
│   └── ...
│
├── hardware/
│   └── ...
│
├── docs/
│   └── ...
│
├── demo/
│   └── ...
│
├── README.md
└── LICENSE
```

---

## AI Pipeline

### 1. Hand Detection

MediaPipe Hand Landmarker detects the hand and extracts 21 landmarks per hand.

For two hands:

```text
21 landmarks × 3 coordinates × 2 hands
= 126 input features
```

### 2. Temporal Modeling

The landmark sequence is passed to an **MP-GRU (MediaPipe-GRU)** model.

The recurrent model captures temporal movement patterns instead of classifying a single frame independently.

### 3. Gesture Classification

The learned temporal representation is passed to a gesture classifier to determine the recognized gesture class.

### 4. Decision Filtering

The live system applies:

* Confidence thresholding
* Top-1 / Top-2 margin checking
* EMA smoothing
* Temporal stability checking
* Gesture cooldown
* Hand-loss reset

This reduces unstable predictions and repeated speech.

### 5. Speech Generation

The recognized gesture is mapped to a predefined phrase.

The phrase is converted to speech using **Piper TTS** and played through the connected speaker.

---

## Hardware

The prototype is designed around:

* Raspberry Pi 4
* Camera module
* Speaker
* Audio amplifier
* Chest-mounted/wearable enclosure
* Power source
* Optional physical mode/control button

---

## Deployment

The trained model is deployed to the Raspberry Pi for local inference.

The intended deployment flow is:

```text
Camera
  ↓
Raspberry Pi
  ↓
MediaPipe
  ↓
MP-GRU
  ↓
Classifier
  ↓
Gesture Decision
  ↓
Phrase
  ↓
Piper TTS
  ↓
Speaker
```

The system is designed to minimize dependency on cloud inference for the core gesture-recognition pipeline.

---

## Training

The `training/` directory contains the machine-learning pipeline used to prepare gesture data, preprocess landmarks, train the MP-GRU/classification model, and evaluate the trained model.

See:

```text
training/README.md
```

---

## Raspberry Pi Live Detection

The `rpi_live_detection/` directory contains the deployment implementation used for real-time gesture recognition on Raspberry Pi.

See:

```text
rpi_live_detection/README.md
```

---

## Intended Application

VoxBridge is intended to assist communication for individuals who have difficulty producing speech by providing an alternative gesture-based communication interface.

The prototype demonstrates the conversion:

```text
Gesture → AI Recognition → Phrase → Voice
```

---

## Project Status

**Prototype / Research & Development**

The system is being developed and tested for real-time assistive communication using Edge AI.

---

## Team

**VoxBridge

Developed as an assistive Edge-AI solution for communication accessibility.
