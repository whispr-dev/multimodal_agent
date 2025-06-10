# multimodal_agent
a 'real-time local multimodal agent with live input, feedback, state tracking, and memory'


# Fren-Agent: Real-Time Multimodal AI Assistant

## Overview
Fren-agent is a real-time multimodal AI agent designed to run locally on your computer, integrating live webcam vision, speech recognition, emotional tone detection, long-term memory storage, and voice interaction through a streamlined PyQt5 graphical user interface.

## Features
- **Visual Perception**: Captures live webcam footage, analyzes scenes, and generates captions.
- **Speech Recognition**: Real-time speech-to-text via Whisper model.
- **Emotion Detection**: Basic sentiment analysis to recognize mood.
- **Memory Retention**: Semantic memory storage using FAISS.
- **Dynamic Responses**: Real-time conversational responses from local LLM or Anthropic Claude API.
- **Voice Output**: Realistic speech synthesis with Piper TTS.
- **Intuitive GUI**: Easy-to-use PyQt5 interface with tabs for agent interactions, settings, and logs.

## Directory Structure
multimodal_agent/
├── config/
│ ├── settings.yaml
│ └── identity.yaml
├── data/
│ ├── embeddings/
│ └── logs/
├── modules/
│ ├── audio_input.py
│ ├── emotion.py
│ ├── gui.py
│ ├── llm_core.py
│ ├── memory.py
│ ├── tts_output.py
│ ├── utils.py
│ └── vision.py
├── voices/
│ └── en_US-kristin-medium.onnx
├── main.py
├── gui_main.py
├── requirements.txt
└── .env

bash
Always show details

Copy

## Installation

### Prerequisites
- Python 3.10+
- Git (optional, for cloning the repository)

### Setup
Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/your-repo/fren-agent.git
cd fren-agent
Install dependencies:

bash
Always show details

Copy
pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory and add your Anthropic Claude API key:

bash
Always show details

Copy
CLAUDE_API_KEY=your_actual_claude_api_key_here
Download Voice Models
Download Piper TTS voices and place them in the voices/ directory:

Piper TTS Voice Models

Recommended starter voice: en_US-kristin-medium.onnx.

Running the Agent
CLI mode
bash
Always show details

Copy
python main.py
GUI mode
bash
Always show details

Copy
python gui_main.py
Usage
Agent Tab: Engage in conversations directly with fren-agent.

Vision Tab: Monitor live camera input and scene descriptions.

Audio Tab: Review live speech transcriptions and mood detections.

Memory Tab: View agent's memory log.

Settings Tab: Adjust agent preferences such as voice model.

Logs Tab: View real-time system logs.

Customizing the Agent
Modify config/identity.yaml to change fren-agent's persona.

Adjust config/settings.yaml for technical configurations.

Contributions
Feel free to fork this project and submit pull requests with improvements, new features, or bug fixes.

License
This project is licensed under the MIT License.