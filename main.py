from mobile_de_browser import MobileDeBrowser

if __name__ == "__main__":
    browser = MobileDeBrowser(headless=False)
    try:
        make = 'Renault'
        model = 'Zoe'
        minimum_year = '2021'
        maximum_year = '2021'

        browser.go_to_search()
        browser.select_make(make)
        browser.select_model(model)
    finally:
        browser.close()
