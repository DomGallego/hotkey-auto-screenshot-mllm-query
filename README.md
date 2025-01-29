# hotkey-auto-screenshot-mllm-query

A Python script that captures a screenshot with a hotkey, prompts for a question, and sends both to a Gemini model for a response.

## Features
- Press **Ctrl+Alt+1** to run `process_screenshot_and_question`.
- Takes a screenshot with `take_screenshot` from `main.py`.
- Prompts for user input, sends data to Gemini, and prints the result.

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
3. Run
    ```python
    python main.py
    ```
4. Usage

    Press **Ctrl+Alt+1** to:

        Capture screenshot -> Input your question -> Get answer to your query

5. Exit

    Press Esc to stop the script.
