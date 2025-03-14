# Pitch.com Screenshot Automation

This script automates taking screenshots of a Pitch.com presentation, navigates through slides, and combines them into a single PDF.

## Prerequisites

### 1. Install Dependencies
Ensure you have Python and Playwright installed.

```sh
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate    # On Windows

# Install required Python packages
pip install playwright openai pillow

# Install Playwright dependencies
playwright install
```

### 2. Set OpenAI API Key
You need an OpenAI API key to enable GPT-4o Mini for navigation support.

```sh
export OPENAI_API_KEY="your-api-key-here"
```

## Running the Script

1. **Activate the Virtual Environment**

```sh
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate    # On Windows
```

2. **Run the script**

```sh
python pitch-download.py
```

## Expected Behavior

- The script logs into Pitch.com by filling the email field and submitting the form.
- It navigates through all slides by clicking the `Next` button (using `data-test-id='player-button-next'`).
- Screenshots of each slide are saved in `pitch_screenshots/`.
- At the end, the script generates a PDF with all slides.

## If the PDF Wasn't Generated

In case the script did not finish properly, you can manually generate the PDF with:

```sh
convert pitch_screenshots/*.png output.pdf
```

(Requires ImageMagick, install with `brew install imagemagick` if missing.)

## Troubleshooting

- If Playwright fails to launch Chrome:
  ```sh
  playwright install
  ```
- If OpenAI API requests fail, check if your API key is valid and set properly.
- If `convert` is not found, install ImageMagick.

## Saving for Future Use

- Keep this `README.md` for reference.
- Save the script and its dependencies.
- Store your OpenAI API key securely.

## Future Enhancements

- Improve element selection using GPT-4o Mini.
- Add error handling for unexpected DOM changes.
- Optionally add logging for debugging issues.

---

_Last Updated: `$(date +%Y-%m-%d)`_
