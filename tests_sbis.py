from time import sleep
from sbis_pages import SearchHelper
import os


def test1(browser):
    main_page = SearchHelper(browser)
    main_page.go_to_site()
    main_page.click_on_contacts()
    main_page.click_on_tensor()
    block_power = main_page.find_text_power()
    assert block_power is not None, "Блок не найден!"

    main_page.click_power_about(block_power)
    res = main_page.check_block_working_img_size()
    assert res and True, "Размеры картинок не соответствуют друг другу"


def test2(browser):
    main_page = SearchHelper(browser)
    main_page.go_to_site()
    main_page.click_on_contacts()
    print()
    my_region = main_page.check_region_kzn()
    assert my_region and "Казань", "Не мой регион"

    main_page.click_list_regions()
    sleep(3)
    assert my_region and "Петропавловск-Камчатский", "Несоответствие регион (контакты)"
    assert browser.title and "СБИС Контакты — Камчатский край", "Несоответствие title"
    assert browser.current_url and "https://sbis.ru/contacts/41-kamchatskij-kraj?tab=clients", "Несоответствие url"

    res = main_page.check_address()
    assert res[0] and "СБИС - Камчатка", "Несоответствие названия регион(адрес)"
    assert res[1] and "ул.Ленинская, 59, оф.202, 205", "Несоответствие адреса регион"


def test3(browser):
    main_page = SearchHelper(browser)
    main_page.go_to_site()
    main_page.click_useful()
    main_page.click_plugin()

    main_page.click_download_file()
    stats = os.stat("setup.exe")
    size = round(stats.st_size / (1024 ** 2), 2)
    assert size and 3.64
