# GPT-For-Lab-Robot
Dissertation Project. Using OpenAI API as external brain to convert Natural Language prompts in code executable by lab robot. OUTDATED CODE FOR OPENAI LIBRARY

> A proof-of-concept system that uses the OpenAI API (GPT-3.5/GPT-4) to control a four-wheeled lab robot via natural language prompts — no programming knowledge required.
---

## Overview

This project explores using Large Language Models (LLMs) as an interface layer between users and a physical robot. Instead of manually writing robot control code, users can speak or type natural language commands, which are translated into executable Python code (or Structured English instructions) by the OpenAI API and run on the robot in real time.

The robot used is a simple four-wheeled vehicle capable of:
- Moving **forward** and **backward**
- Turning **left** and **right**
- Capturing images via a fixed **camera**

---

## Project Structure

| File | Description |
|------|-------------|
| `RobotApi.py` | Main API script with voice input and idle state (PC simulation, robot commands commented out) |
| `RobotApiOnRobot.py` | Version designed to run directly on the robot hardware |
| `RobotApiOnPc.py` | Generates Structured English commands (no robot required) |
| `RobotApiOnPcWithVideo.py` | Structured English generation with camera feed context |
| `RobotApiBackup1.py` | First iteration — text input, Python code generation |
| `RobotApiBackup2.py` | Second iteration — adds voice input via SpeechRecognition |
| `ApiTest_With_AFK_Function.py` | Test version with inactivity/idle state logic |
| `ApiTestVoice.py` | Basic voice-to-API test script |
| `ImageTextGet.py` | Captures a camera frame and generates a text description using GPT-4 Vision |
| `UploadImageToCloud.py` | Uploads captured images to Google Cloud Storage for API access |
| `Temp.py` | Standalone camera capture utility for testing |

---

## Features

- **Natural language robot control** — type or speak a command, the robot executes it
- **Voice input** — uses the `SpeechRecognition` library with Google Speech Recognition
- **Idle states** — robot performs gentle animations after 15–30 seconds of inactivity (inspired by video game idle animations)
- **Camera integration** — captures a frame, uploads to Google Cloud, and uses GPT-4 Vision to describe the scene, which is fed into subsequent commands
- **Structured English mode** — generates human-readable step-by-step instructions instead of raw Python, useful when running on PC without robot hardware

---

## Prerequisites

### Hardware
- Four-wheeled robot with PCA9685 motor drivers (front-left, front-right, back-left, back-right)
- Microphone (for voice input)
- Camera (OpenCV-compatible, e.g. USB webcam)

### Software
- Python 3.x (use [Anaconda](https://www.anaconda.com/) on the robot to manage environment compatibility)
- OpenAI API key
- Google Cloud credentials (`credentials.json`) with a configured Storage bucket

### Python Dependencies

```bash
pip install openai speechrecognition opencv-python google-cloud-storage
```

For robot hardware:
```bash
pip install traitlets
```

---

## Setup

1. **Clone the repository** and navigate to the project folder.

2. **Add your API key** — replace the placeholder in whichever script you intend to run:
   ```python
   openai.api_key = "YOUR_OPENAI_API_KEY"
   ```

3. **Add Google Cloud credentials** — place your `credentials.json` file in the same directory as the scripts (required for camera-integrated scripts only).

4. **Install dependencies** (see above).

---

## Usage

### Text-based control (PC, Structured English output)
```bash
python RobotApiOnPc.py
```
Type a command at the prompt (e.g. `move forward slowly`) and receive Structured English instructions. Type `break` to exit.

### Text-based control with camera context
```bash
python RobotApiOnPcWithVideo.py
```
Captures a camera frame before each command and includes a scene description in the prompt.

### Voice-controlled (PC simulation)
```bash
python RobotApi.py
```
Listens for voice commands. After 15 seconds of inactivity, the robot enters an idle animation state. The robot control calls (`robot.forward()`, etc.) are commented out for PC testing.

### On the robot
```bash
python RobotApiOnRobot.py
```
Runs the full system on robot hardware. Uncomment `RobotClass` imports as needed.

---

## Robot API Reference

All movement methods are defined in `RobotClass.py` and accept an optional `speed` parameter (0.0–1.0, default 1.0).

| Method | Description |
|--------|-------------|
| `robot.forward(speed)` | Move forward |
| `robot.backward(speed)` | Move backward |
| `robot.left(speed)` | Turn left (pivot) |
| `robot.right(speed)` | Turn right (pivot) |
| `robot.forward_left(speed)` | Move diagonally forward-left |
| `robot.forward_right(speed)` | Move diagonally forward-right |
| `robot.backward_left(speed)` | Move diagonally backward-left |
| `robot.backward_right(speed)` | Move diagonally backward-right |
| `robot.stop()` | Stop all motors |
| `robot.set_motors(fl, fr, bl, br)` | Set individual motor speeds |

---

## Known Limitations

- **GPT-3.5-turbo** handles straightforward commands well but struggles with abstract or complex prompts — using `gpt-4` may improve results.
- **Voice recognition** accuracy drops for non-native English accents and degrades further with low-quality microphones.
- **Camera input** is limited to single frames; continuous video analysis is not currently supported.
- **Bluetooth microphone detection** on the robot hardware was unresolved during testing, preventing full on-robot deployment.
- **Structured English output** is non-deterministic — the same prompt can produce different responses across runs.
- **Outdated Code** as of 2025.

---

## License

This project was developed as an individual undergraduate project at Loughborough University. Please contact the author before reuse.
