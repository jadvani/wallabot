import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver import Chrome, ChromeOptions
import yaml


def get_config(yaml_path):
    """
    Config file containing the identifiers for the different scrapping functionalities
    :param yaml_path: the path of the YAML file
    :return: the config dictionary to search by keys the web element identifiers
    """
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def get_driver_from_url(url):
    """
    This method creates the driver to interact with the different elements in the website. Due to the high volume of
    elements being scrapped and webs to visit, some additional options added avoid the script to be blocked.
    :param url: The url to navigate.
    :return: The driver to interact with the website.
    """
    # adding options to avoid errors during intensive search loops
    options = ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-certificate-errors')
    s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    final_driver = Chrome(executable_path=s.path, desired_capabilities=options.to_capabilities())
    final_driver.get(url)
    final_driver.implicitly_wait(1)

    return final_driver


class WallaPopSearch:
    def __init__(self, search_text):
        self.search_text = search_text.lower().replace(" ", "%20")

        pre_url = u'https://es.wallapop.com/app/search?keywords='
        post_url = u'&filters_source=search_box&latitude=37.38788&longitude=-6.00197'
        self.driver = get_driver_from_url(pre_url + self.search_text + post_url)
        self.labels = get_config('labels.yaml')
        WebDriverWait(self.driver, 20).until(
            presence_of_element_located((By.XPATH, self.labels['accept_cookies']))).click()

    def web_driver_wait(self, label):
        return WebDriverWait(self.driver, 5).until(presence_of_element_located((By.XPATH, label)))

    def set_price_range(self, min_price, max_price):
        self.web_driver_wait(self.labels['price']).click()
        self.web_driver_wait(self.labels['min_price']).send_keys(str(min_price))
        self.web_driver_wait(self.labels['max_price']).send_keys(str(max_price))
        time.sleep(0.7)
        self.web_driver_wait(self.labels['apply_price']).click()

    def set_search_order(self, order):
        """
        Set the display order.
        :param order: cheapest, most_expensive, newest, nearest
        """
        self.web_driver_wait(self.labels['order_by']).click()
        self.web_driver_wait(self.labels[order]).click()

    def retrieve_elements(self):
        counter = 1
        base = self.labels['search_item']
        price = '/div[2]/div[1]/span'
        is_booked = '/tsl-svg-icon'
        tittle = '/div[2]/div[2]/p[1]'
        while True:
            try:
                path = base + "a[" + str(counter) + "]/tsl-public-item-card/div"
                print(path)
                prod_tittle = self.web_driver_wait(path + tittle).text
                prod_price = self.web_driver_wait(path + price).text
                print(prod_tittle)
                print(prod_price)
                try:
                    if self.driver.find_element(By.XPATH, path + is_booked):
                        print("reservado")
                except:
                    pass
                counter = counter + 1
                print("\n")

            except:
                if counter > 1:
                    print("total: " + str(counter-1)+ "elementos encontrados")
                else:
                    print("no se encontraron resultados para la búsqueda.")
                break

        return counter


wallapop_elem = WallaPopSearch(u'Roberto Bolaño 2666')
wallapop_elem.set_price_range(1, 20)
wallapop_elem.set_search_order("cheapest")
time.sleep(5)
wallapop_elem.retrieve_elements()
