# hotkey-auto-screenshot-mllm-query

A Python application that captures screenshots with a hotkey, processes them with Google's Gemini model, and provides responses via command line or GUI interface.

## Features
- Press **Ctrl+Alt+1** to capture a screenshot
- Two interface options:
  - CLI version ([main.py](main.py)): Command-line interface with simple text output
  - GUI version ([main_gui_skeletal.py](main_gui_skeletal.py)): Graphical interface with chat-like display
- Real-time statistics including:
  - Response time
  - Screenshot size
  - Token usage metrics
- Automatic temporary file management
- Support for the Gemini 2.0 Flash model

## Requirements

* Python 3.8+
* Windows OS
* Gemini API key

## Setup
1. Set `GEMINI_API_KEY` in your environment variables.
2. Install requirements:
   ```bash
   pip install keyboard pyautogui Pillow google-generativeai
   ```
3. Usage

    Command Line Interface

    ```python
    python main.py
    ```
    GUI Interface

    ```python
    python main_gui_skeletal.py
    ```
    
4. Operation
    - Press Ctrl+Alt+1 to capture a screenshot
    - Enter your question about the screenshot
    - View the Gemini model's response and analyse statistics


5. Exit

    Press Esc to stop the script.
