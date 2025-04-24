# Mobile.de Search Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/) ![GitHub last commit](https://img.shields.io/github/last-commit/igorccouto/mobile-de-cars-search-engine)

A Python Selenium-based web scraper for mobile.de car listings. This project automates browser interactions to search for cars, select make/model, and set filters such as registration year on [mobile.de](https://www.mobile.de/).

## Features
- Uses Firefox and geckodriver for browser automation
- Navigates to the mobile.de advanced search page
- Handles consent dialogs automatically
- Selects car make and model from dropdowns
- Fills registration year fields
- Easily extensible for further scraping or automation

## Requirements
- Python 3.7+
- [geckodriver](https://github.com/mozilla/geckodriver/releases) (place it in the project root)
- Firefox browser
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
1. Place `geckodriver` in the project root directory (same folder as `main.py`).
2. Run the example script:

```bash
python main.py
```

This will open Firefox, navigate to mobile.de, accept the consent dialog, select a make/model, and fill in the registration year fields.

## Example Code
```python
from mobile_de_browser import MobileDeBrowser

browser = MobileDeBrowser(headless=False)
try:
    browser.go_to_search()
    browser.select_make('Renault')
    browser.select_model('Zoe')
    browser.fill_first_registration_min('2021')
    browser.fill_first_registration_max('2021')
finally:
    browser.close()
```

## Notes
- The code uses Selenium's WebDriverWait and robust element interaction logic to handle dynamic content.
- If you encounter issues with elements not being interactable, check that geckodriver and Firefox are up to date.
- For headless operation, set `headless=True` in `MobileDeBrowser`.

## License
MIT
