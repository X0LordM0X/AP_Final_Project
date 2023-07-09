import time, requests, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread, Lock

from ProductClass import Product


class DigiKalaScrape:
    path = '/Users/LordM/Downloads/chromedriver'

    def __init__(self):
        self.mutex = Lock()

    def scrape_category(self, key_word: str, app_products: dict, product_count: int = None):
        self.results = {}

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('window-size=1920x1080')

        search_input = key_word
        search_input = '%20'.join(search_input.split())
        web = f'https://www.digikala.com/search/?q={search_input}'

        service = Service(executable_path = self.path)
        driver = webdriver.Chrome(service = service, options = options)
        driver.get(web)

        driver.maximize_window()

        time.sleep(2) # ------------------------- wait

        try:
            product_links = driver.find_elements(by = 'xpath', value = '//section/div[2]/div[@data-product-index]/a')
        except:
            product_links = []

        if not product_count: product_count = 5
        result_count = min(product_count, len(product_links))
        links = [link.get_attribute('href') for link in product_links[:result_count]]
        threads = [
            Thread(target = self.scraping_product_data, args = (link, self.path))\
            for link in links if link not in app_products
        ]

        # starting threads
        for t in threads:
            t.start()
            time.sleep(1) # ------------------- request limit

        # waiting for threads to finish
        for t in threads:
            t.join()

        driver.quit()

        self.results.update({link: app_products[link] for link in links if link in app_products})
        return self.results

    def scraping_product_data(self, url: str, path: str):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('window-size=1920x1080')
        service = Service(executable_path = path)
        driver = webdriver.Chrome(service = service, options = options)
        driver.get(url)

        try:
            # wait
            condition = EC.presence_of_element_located((By.XPATH, '//h1[@data-testid]'))
            product_title = WebDriverWait(driver, 10).until(condition).text
            product_title = product_title.replace('/', '')

            try:
                price_xpath = "//div[contains(@class, 'Marketable')]//span[contains(@class, 'text-h4')]"
                price = driver.find_element(by = 'xpath', value = price_xpath).text
            except:
                price = 'Unavailable'

            image_xpath = f"//img[contains(@alt, '{' '.join(product_title.split()[:3])}')]"
            image = driver.find_element(by = 'xpath', value = image_xpath)
            image_saving_path = f'./Files/Images/{product_title}.png'
            # with open(image_saving_path, 'wb') as file:
            #     file.write(requests.get(image.get_attribute('src')).content)
            Thread(target = self.download_image, args = (image, image_saving_path)).start()

            box = driver.find_element(by = 'id', value = "specification")

            # scrolling to box
            driver.execute_script(f'window.scrollTo(0, {box.rect["y"]});')

            # click on show more button
            try:
                button = box.find_element(by='xpath', value='./span/div')
                button.click()
            except:
                print('There is not show more button!')

            # exporting data
            titles_xpath = "./div[2]/div//div[contains(@class, 'valuesBox')]/p"
            infos_xpath = "./div[2]/div//div[contains(@class, 'valuesBox')]/div"
            titles = [title.text for title in box.find_elements(by = 'xpath', value = titles_xpath)]
            infos = [info.text for info in box.find_elements(by = 'xpath', value = infos_xpath)]

            # importing data to file
            # df = pd.DataFrame({"title": titles, "info": infos})
            # df_saving_path = f'./WebScrapingTest/{product_title}.csv'
            # df.to_csv(df_saving_path)

            result_product = Product(
                url, {"DigiKala": url}, product_title, {"DigiKala": price}, image_saving_path,
                {'title': titles, "info": infos}
            )
            self.mutex.acquire()
            self.results[url] = result_product
            self.mutex.release()

            ################################
            print('Done!')              #log
            ################################
        except:
            ################################
            print('Error!')             #log
            ################################
        driver.quit()

    @staticmethod
    def scraping_product_price(url: str, path: str):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('window-size=1920x1080')
        service = Service(executable_path = path)
        driver = webdriver.Chrome(service = service, options = options)
        driver.get(url)

        price = None

        try:
            # wait
            condition = EC.presence_of_element_located((By.XPATH, '//h1[@data-testid]'))
            product_title = WebDriverWait(driver, 10).until(condition).text

            try:
                price_xpath = "//div[contains(@class, 'Marketable')]//span[contains(@class, 'text-h4')]"
                price = driver.find_element(by = 'xpath', value = price_xpath).text
            except:
                price = 'Unavailable'

            ################################
            print('Done!')              #log
            ################################
        except:
            ################################
            print('Error!')             #log
            ################################
        driver.quit()

        return price

    @staticmethod
    def download_image(image, image_saving_path: str):
        with open(image_saving_path, 'wb') as file:
            file.write(requests.get(image.get_attribute('src')).content)