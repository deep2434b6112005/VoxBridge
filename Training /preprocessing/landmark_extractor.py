import numpy as np

NUM_LANDMARKS = 21
COORDS_PER_LANDMARK = 3
MAX_HANDS = 2

SLOT_SIZE = NUM_LANDMARKS * COORDS_PER_LANDMARK
INPUT_SIZE = SLOT_SIZE * MAX_HANDS


def build_hand_landmarker(
    model_path: str,
    num_hands: int = MAX_HANDS,
    min_hand_detection_confidence: float = 0.35,
    min_hand_presence_confidence: float = 0.35,
    min_tracking_confidence: float = 0.35,
):
    """
    Build MediaPipe HandLandmarker in VIDEO mode.

    Lower thresholds are intentional for product-level robustness:
    the detector should not disappear too easily during fast/sudden gestures.
    """

    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision

    base_options = mp_python.BaseOptions(
        model_asset_path=model_path
    )

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=num_hands,

        min_hand_detection_confidence=min_hand_detection_confidence,
        min_hand_presence_confidence=min_hand_presence_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    landmarker = vision.HandLandmarker.create_from_options(options)

    return landmarker, mp


def landmarks_to_vector(result):
    """
    Convert MediaPipe result into:

        x:
            shape (126,)
            float32

        confidence:
            scalar float in [0, 1]

    Layout:

        [Left hand:  63 values]
        [Right hand: 63 values]

    Each hand:

        landmark 0 -> x,y,z
        landmark 1 -> x,y,z
        ...
        landmark 20 -> x,y,z

    Missing hands are zero-filled.
    """

    x = np.zeros(INPUT_SIZE, dtype=np.float32)

    if not result.hand_landmarks:
        return x, 0.0

    confidences = []

    for hand_idx, hand_landmarks in enumerate(result.hand_landmarks):

        if hand_idx >= MAX_HANDS:
            break

        # ---------------------------------------------------------
        # Determine Left / Right slot
        # ---------------------------------------------------------

        label = None
        score = 0.0

        try:
            handedness = result.handedness[hand_idx]

            if handedness:
                category = handedness[0]

                label = category.category_name
                score = float(category.score)

        except (IndexError, AttributeError, TypeError):
            pass

        # ---------------------------------------------------------
        # Fallback if handedness unavailable
        # ---------------------------------------------------------

        if label not in ("Left", "Right"):

            # deterministic fallback
            label = "Left" if hand_idx == 0 else "Right"

        if score <= 0.0:
            score = 1.0

        # ---------------------------------------------------------
        # Assign feature slot
        # ---------------------------------------------------------

        if label == "Left":
            slot = 0
        else:
            slot = 1

        offset = slot * SLOT_SIZE

        # ---------------------------------------------------------
        # Copy 21 landmarks
        # ---------------------------------------------------------

        for landmark_idx, lm in enumerate(hand_landmarks):

            if landmark_idx >= NUM_LANDMARKS:
                break

            base = offset + landmark_idx * COORDS_PER_LANDMARK

            x[base] = float(lm.x)
            x[base + 1] = float(lm.y)
            x[base + 2] = float(lm.z)

        confidences.append(score)

    # -------------------------------------------------------------
    # Overall confidence
    #
    # MAX is used because one clearly visible hand should remain
    # usable even if the second hand is poorly detected.
    # -------------------------------------------------------------

    confidence = max(confidences) if confidences else 0.0

    confidence = float(np.clip(confidence, 0.0, 1.0))

    return x, confidence


def extract_landmarks_from_result(result):
    """
    Alias for readability in other modules.
    """

    return landmarks_to_vector(result)