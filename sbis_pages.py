from selenium.webdriver.common.keys import Keys
from base_app import BasePage
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request


class SearchLocators:
    # for test1
    LOCATOR_SEARCH_TENSOR = (By.CLASS_NAME, "sbisru-Contacts__logo-tensor")
    LOCATOR_SEARCH_CONTACTS = (By.LINK_TEXT, "Контакты")
    LOCATOR_SEARCH_TEXT_POWER = (By.XPATH, "./p[contains(text(), 'Сила в людях')]")
    LOCATOR_SEARCH_POWER_ABOUT = (By.LINK_TEXT, "Подробнее")
    LOCATOR_SEARCH_BLOCKS = (By.XPATH, '//div[contains(@class, "tensor_ru-Index__card")]')
    LOCATOR_SEARCH_BLOCKS_WORKING = (By.CLASS_NAME, "tensor_ru-About__block3--col-sm12")
    LOCATOR_SEARCH_IMG = (By.TAG_NAME, 'img')
    # for test2
    LOCATOR_SEARCH_MY_REGION = (By.ID, "city-id-2")
    LOCATOR_SEARCH_REGION_NAME_KZN = (By.XPATH, '//div[text()="Казань"]')
    LOCATOR_SEARCH_RT = (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    LOCATOR_SEARCH_REGIONS = (By.XPATH, "//ul[@class='sbis_ru-Region-Panel__list']")
    LOCATOR_SEARCH_REGION_KAMCHA = (By.XPATH, "//span[@title='Камчатский край']")
    LOCATOR_SEARCH_REGION_NAME2 = (By.CLASS_NAME, "sbisru-Contacts-List--ellipsis")
    LOCATOR_SEARCH_REGION_ADRS = (By.CLASS_NAME, "sbisru-Contacts-List__address")
    # for test3
    LOCATOR_SEARCH_DOWNLOAD = (By.LINK_TEXT, "Скачать СБИС")
    LOCATOR_SEARCH_PLUGIN = (By.CLASS_NAME, "controls-tabButton__overlay")
    LOCATOR_SEARCH_DOWNLOAD_FILE = (By.CLASS_NAME, "sbis_ru-DownloadNew-loadLink__link")


class SearchHelper(BasePage):
    def click_on_contacts(self):
        return self.find_element(SearchLocators.LOCATOR_SEARCH_CONTACTS, time=2).click()

    def click_on_tensor(self):
        wait = WebDriverWait(self.driver, 10)
        self.find_element(SearchLocators.LOCATOR_SEARCH_TENSOR, time=2).click()
        original_window = self.driver.current_window_handle

        wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    def find_blocks(self):
        return self.find_elements(SearchLocators.LOCATOR_SEARCH_BLOCKS, time=2)

    def find_text_power(self):
        bl = None
        for block in self.find_blocks():
            try:
                # print(block.get_attribute('outerHTML'))
                block.find_element(*SearchLocators.LOCATOR_SEARCH_TEXT_POWER)
                bl = block
                break
            except:
                continue
        return bl

    def click_power_about(self, block):
        link = block.find_element(*SearchLocators.LOCATOR_SEARCH_POWER_ABOUT)
        link.send_keys(Keys.ENTER)

    def check_block_working_img_size(self):
        height = width = 0
        res = True
        blocks = self.find_elements(SearchLocators.LOCATOR_SEARCH_BLOCKS_WORKING, time=2)
        for block in blocks:
            img_size = block.find_element(*SearchLocators.LOCATOR_SEARCH_IMG).rect
            if height == 0 and width == 0:
                height = img_size["height"]
                width = img_size["width"]
            else:
                if height != img_size["height"] or width != img_size["width"]:
                    res = False
                    break
        return res

    def check_region_kzn(self):
        region = self.find_element(SearchLocators.LOCATOR_SEARCH_MY_REGION, time=2)
        my_region = region.find_element(*SearchLocators.LOCATOR_SEARCH_REGION_NAME_KZN)
        return my_region.text

    def click_list_regions(self):
        self.find_element(SearchLocators.LOCATOR_SEARCH_RT, time=2).click()
        regions = self.find_element(SearchLocators.LOCATOR_SEARCH_REGIONS, time=2)
        regions.find_element(*SearchLocators.LOCATOR_SEARCH_REGION_KAMCHA).click()

    def check_address(self):
        adrs = self.find_element(SearchLocators.LOCATOR_SEARCH_REGION_ADRS, time=2)
        name = self.find_element(SearchLocators.LOCATOR_SEARCH_REGION_NAME2, time=2)
        return name.text, adrs.text

    def click_useful(self):
        link = self.find_element(SearchLocators.LOCATOR_SEARCH_DOWNLOAD, time=2)
        link.send_keys(Keys.ENTER)

    def click_plugin(self):
        loads = self.find_elements(SearchLocators.LOCATOR_SEARCH_PLUGIN, time=2)
        n = 0
        for load in loads:
            n += 1
            if n == 2:
                load.click()

    def click_download_file(self):
        a = self.find_elements(SearchLocators.LOCATOR_SEARCH_DOWNLOAD_FILE, time=2)
        for elem in a:
            url_text = elem.get_attribute('text')
            if url_text == "Скачать (Exe 3.64 МБ) ":
                url = elem.get_attribute('href')
                urllib.request.urlretrieve(url, "setup.exe")
                break
