import keyboard
import pyautogui as pg
from PIL import Image
import os
import google.generativeai as genai
import tempfile
import time  # Import the time module

# --- Gemini API Setup ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",  
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
# --- End Gemini API Setup ---

def take_screenshot():
    """Takes a screenshot of the entire screen and returns the image."""
    screenshot = pg.screenshot()
    return screenshot

def process_screenshot_and_question():
    """Handles the screenshot, question prompt, and Gemini API interaction and prints stats."""
    print("Screenshot hotkey pressed!")

    # 1. Take Screenshot
    screenshot_image = take_screenshot()

    # 2. Save screenshot to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        screenshot_path = tmp_file.name
        screenshot_image.save(screenshot_path)
        screenshot_size_bytes = os.path.getsize(screenshot_path) # Get file size in bytes
        screenshot_size_kb = screenshot_size_bytes / 1024 # Convert to KB

        # 3. Prompt for question in cmd
        question = input("Ask a question about the screenshot: ")

        # 4. Load image using PIL and process within 'with' block
        with Image.open(screenshot_path) as pil_image: # Use 'with' to open image
            # 5. Prepare content for Gemini API (now just a list of PIL Image and text)
            contents = [pil_image, question]  # Directly pass PIL Image and text

            # [OPTIONAL] Pre-calculate input tokens (before sending to Gemini)
            # input_tokens_pre_call = model.count_tokens(contents).total_tokens
            # print(f"\nEstimated Input Tokens (before API call): {input_tokens_pre_call}")

            # 6. Send to Gemini and get response
            try:
                start_time = time.time()  # Record start time
                response = chat_session.send_message(contents) # Send the list directly
                end_time = time.time()    # Record end time
                response_time = end_time - start_time # Calculate response time

                print("\nGemini's Response:")
                print(response.text)
                print("\n--- Stats ---")
                print(f"Response Time: {response_time:.2f} seconds") # Print response time
                print(f"Screenshot Size: {screenshot_size_kb:.2f} KB") # Print screenshot size


                # Check for token usage information (if available in the response object)
                if hasattr(response, 'usage_metadata'): # Check if usage_metadata exists
                    usage = response.usage_metadata
                    print("\nToken Usage:")
                    print(f"  Prompt Tokens: {usage.prompt_token_count}")
                    print(f"  Candidates Tokens: {usage.candidates_token_count}")
                    print(f"  Total Tokens: {usage.total_token_count}")
                else:
                    print("\nToken usage information not available in the response.")

                print("\n--- Stats ---")


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