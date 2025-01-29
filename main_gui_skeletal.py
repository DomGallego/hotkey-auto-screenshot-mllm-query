import tkinter as tk
from tkinter import scrolledtext, Entry, Button
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

# --- GUI Setup ---
root = tk.Tk()
root.title("Screenshot Chat with Gemini")

chat_display = scrolledtext.ScrolledText(root, height=15, width=60, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10)

input_field = Entry(root, width=60)
input_field.pack(padx=10, pady=5)
input_field.bind("<Return>", lambda event=None: send_question()) # Bind Enter key to send_question

send_button = Button(root, text="Send", command=lambda: send_question())
send_button.pack(pady=5)

# --- Global variables to store screenshot path ---
current_screenshot_path = None

def append_message(sender, message):
    """Appends a message to the chat display."""
    chat_display.config(state=tk.NORMAL) # Enable editing
    chat_display.insert(tk.END, f"{sender}: {message}\n", sender) # Add sender tag
    chat_display.tag_config("user", foreground="blue") # Example styling for user messages
    chat_display.tag_config("gemini", foreground="green") # Example styling for gemini messages
    chat_display.config(state=tk.DISABLED) # Disable editing
    chat_display.yview(tk.END) # Scroll to the end

def take_screenshot():
    """Takes a screenshot of the entire screen and returns the image."""
    screenshot = pg.screenshot()
    return screenshot

def process_image_and_send_to_gemini(question):
    """Processes the screenshot, sends question to Gemini, and displays response in chat."""
    global current_screenshot_path # Use the global variable

    if current_screenshot_path is None:
        append_message("System", "Error: No screenshot taken. Please press Ctrl+Alt+1 to take a screenshot first.")
        return

    screenshot_path = current_screenshot_path # Use the stored path

    try:
        # Load image using PIL and process within 'with' block
        with Image.open(screenshot_path) as pil_image: # Use 'with' to open image
            # 5. Prepare content for Gemini API (now just a list of PIL Image and text)
            contents = [pil_image, question]  # Directly pass PIL Image and text

            # 6. Send to Gemini and get response
            start_time = time.time()  # Record start time
            response = chat_session.send_message(contents) # Send the list directly
            end_time = time.time()    # Record end time
            response_time = end_time - start_time # Calculate response time

            gemini_response_text = response.text

            # Check for token usage information (if available in the response object)
            if hasattr(response, 'usage_metadata'): # Check if usage_metadata exists
                usage = response.usage_metadata
                stats_text = (
                    f"\n--- Stats ---\n"
                    f"Response Time: {response_time:.2f} seconds\n"
                    f"Prompt Tokens: {usage.prompt_token_count}\n"
                    f"Candidates Tokens: {usage.candidates_token_count}\n"
                    f"Total Tokens: {usage.total_token_count}\n"
                    f"--- Stats ---\n"
                )
            else:
                stats_text = "\nToken usage information not available in the response.\n--- Stats ---\n"

            full_response = gemini_response_text + stats_text
            append_message("Gemini", full_response)


    except Exception as e:
        error_message = f"Error communicating with Gemini API: {e}"
        append_message("System", error_message)


def send_question():
    """Gets the question from the input field and sends it for processing."""
    question = input_field.get()
    if question:
        append_message("You", question)
        input_field.delete(0, tk.END) # Clear input field
        process_image_and_send_to_gemini(question)
    else:
        append_message("System", "Please enter a question.")


def process_screenshot_and_question():
    """Handles the screenshot hotkey press."""
    global current_screenshot_path # To store the screenshot path globally
    print("Screenshot hotkey pressed!")

    # 1. Take Screenshot
    screenshot_image = take_screenshot()

    # 2. Save screenshot to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        screenshot_path = tmp_file.name
        screenshot_image.save(screenshot_path)
        current_screenshot_path = screenshot_path # Store the path globally
        screenshot_size_bytes = os.path.getsize(screenshot_path) # Get file size in bytes
        screenshot_size_kb = screenshot_size_bytes / 1024 # Convert to KB
        append_message("System", f"Screenshot taken and saved. Size: {screenshot_size_kb:.2f} KB")

    root.deiconify() # Show the window if it was minimized
    root.attributes('-topmost', 1) # Bring to front
    root.attributes('-topmost', 0) # Release topmost so it doesn't stay always on top
    input_field.focus_set() # Focus on the input field


# Register the hotkey
keyboard.add_hotkey('ctrl+alt+1', process_screenshot_and_question)

# Hide the main window initially (optional, if you want it to appear only on hotkey press)
root.withdraw()

# Keep the script running to listen for hotkeys and GUI events
print("Script is running. Press Ctrl+Alt+1 to take a screenshot and ask a question.")
print("Press ESC to stop the script.")

def on_esc_pressed():
    print("Script stopped.")
    root.destroy() # Close the tkinter window
    return False # Stop further event processing by keyboard

keyboard.hook_key('esc', on_esc_pressed) # Hook ESC key to close window and exit

root.mainloop()