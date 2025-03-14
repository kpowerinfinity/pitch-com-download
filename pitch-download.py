import os
import time
import openai
import base64
from PIL import Image
from playwright.sync_api import sync_playwright

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
PITCH_URL = "https://pitch.com/v/t123123"  # Replace with actual link
OUTPUT_DIR = "pitch_screenshots"
EMAIL_INPUT = "test@gmail.com"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def log_available_elements(page):
    """Logs all detected input fields and buttons to debug selection issues."""
    inputs = page.query_selector_all("input")
    buttons = page.query_selector_all("button")
    
    print("\n=== Available Input Fields ===")
    for i, inp in enumerate(inputs):
        print(f"{i+1}: {inp.evaluate('(el) => el.outerHTML')}")
    
    print("\n=== Available Buttons ===")
    for i, btn in enumerate(buttons):
        print(f"{i+1}: {btn.evaluate('(el) => el.outerHTML')}")

def get_gpt4_vision_response(image_path):
    """Use GPT-4o Mini to analyze the screen and determine next actions."""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a browser automation assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this screenshot. Identify the text input field (assuming it is the only one on the page) and the checkbox. Provide details on navigating to the next slide."},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(image_data).decode("utf-8")}}
            ]}
        ],
        max_tokens=100
    )
    
    return response.choices[0].message.content

def capture_slides():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for full automation
        page = browser.new_page()
        page.goto(PITCH_URL)
        page.wait_for_load_state("networkidle")

        # Step 1: Check if login is required
        screenshot_path = f"{OUTPUT_DIR}/login.png"
        page.screenshot(path=screenshot_path)

        # Log available elements
        log_available_elements(page)

        # Identify the input field dynamically
        text_input = page.query_selector("input")  # Get the first input field on the page
        remember_checkbox = page.query_selector("input[type='checkbox']")
        submit_button = page.query_selector("button")

        if text_input:
            print("✅ Found Email Input Field!")
            text_input.fill("your-email@example.com")
        else:
            print("❌ No email input field found!")

        if remember_checkbox:
            print("✅ Found 'Remember Email' Checkbox!")
            remember_checkbox.check()
        else:
            print("⚠️ No checkbox found, skipping...")

        if submit_button:
            print("✅ Found Submit Button! Clicking...")
            submit_button.click()
            time.sleep(5)  # Wait for page reload
        else:
            print("❌ No submit button found!")

        # Step 2: Navigate slides and take screenshots
        slide_number = 1
        while True:
            slide_path = f"{OUTPUT_DIR}/slide_{slide_number}.png"
            page.screenshot(path=slide_path)
            print(f"Saved: {slide_path}")

            # Ask GPT-4o Mini if there is a "next" button
            gpt_response = get_gpt4_vision_response(slide_path)
            print(f"Slide {slide_number}: {gpt_response}")

            next_button = page.query_selector("button[data-test-id='player-button-next']")
            if next_button:
                print("✅ Found 'Next' Button! Clicking...")
                next_button.click()
                time.sleep(2)
                slide_number += 1
            else:
                print("❌ No next button found, assuming end of slides.")
                break

        browser.close()
        convert_images_to_pdf()

def convert_images_to_pdf():
    images = [Image.open(f"{OUTPUT_DIR}/{img}") for img in sorted(os.listdir(OUTPUT_DIR)) if img.endswith(".png")]
    
    if images:
        pdf_path = "pitch_presentation.pdf"
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF saved as: {pdf_path}")
    else:
        print("No images found to create a PDF.")

# Run the automation
capture_slides()
