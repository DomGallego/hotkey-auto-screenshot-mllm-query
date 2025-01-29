import keyboard
import pyautogui as pg
from PIL import Image
import os
import google.generativeai as genai
import tempfile

# --- Gemini API Setup ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",  # Using a more recent model name
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
# --- End Gemini API Setup ---

def take_screenshot():
    """Takes a screenshot of the entire screen and returns the image."""
    screenshot = pg.screenshot()
    return screenshot
def process_screenshot_and_question():
    """Handles the screenshot, question prompt, and Gemini API interaction."""
    print("Screenshot hotkey pressed!")

    # 1. Take Screenshot
    screenshot_image = take_screenshot()

    # 2. Save screenshot to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        screenshot_path = tmp_file.name
        screenshot_image.save(screenshot_path)

        # 3. Prompt for question in cmd
        question = input("Ask a question about the screenshot: ")

        # 4. Load image using PIL and process within 'with' block
        with Image.open(screenshot_path) as pil_image: # Use 'with' to open image
            # 5. Prepare content for Gemini API (now just a list of PIL Image and text)
            contents = [pil_image, question]  # Directly pass PIL Image and text

            # 6. Send to Gemini and get response
            try:
                response = chat_session.send_message(contents) # Send the list directly
                print("\nGemini's Response:")
                print(response.text)
            except Exception as e:
                print(f"Error communicating with Gemini API: {e}")

    # 7. Clean up temporary file (now outside the inner 'with' block)
    os.remove(screenshot_path)
    print("Temporary screenshot file removed.")


# Register the hotkey
keyboard.add_hotkey('ctrl+alt+1', process_screenshot_and_question)

# Keep the script running to listen for hotkeys
print("Script is running. Press Ctrl+Alt+1 to take a screenshot and ask a question.")
print("Press ESC to stop the script.")
keyboard.wait('esc')
print("Script stopped.")