from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import datetime

import slack_notify
import config


def reserve(driver, reserve_date, iframe_btm, iframe_main, screenshot_filepath):
    try:
        if driver.find_elements_by_id(reserve_date) and driver.find_element_by_id(reserve_date).get_attribute(
                'class') == 'Aki':
            driver.find_element_by_id(reserve_date).click()
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe_btm)
            driver.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/input[1]').click()
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe_main)
            driver.find_element_by_xpath('/html/body/div/form/input[1]').click()
            driver.find_element_by_xpath('/html/body/div/form/input[1]').click()

            # screenshot
            page_width = driver.execute_script('return document.body.scrollWidth')
            page_height = driver.execute_script('return document.body.scrollHeight')
            driver.set_window_size(page_width, page_height)
            driver.save_screenshot(screenshot_filepath)

            slack_notify.notify('"' + reserve_date + '" の予約ができました．', screenshot_filepath)
            print('"' + reserve_date + '" の予約ができました．')
        else:
            print('"' + reserve_date + '" は空いていませんでした．')
    except Exception:
        import traceback
        slack_notify.send_message('```' + traceback.format_exc() + '```')
        print(traceback.format_exc())


def cancel(driver, delete_date, iframe_btm, iframe_main, screenshot_filepath):
    try:
        driver.find_element_by_id(delete_date).click()
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe_btm)
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/input[2]').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe_main)
        driver.find_element_by_xpath('/html/body/div/form/input[1]').click()
        driver.find_element_by_xpath('/html/body/div/form/input[1]').click()

        # screenshot
        page_width = driver.execute_script('return document.body.scrollWidth')
        page_height = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(page_width, page_height)
        driver.save_screenshot(screenshot_filepath)

        slack_notify.notify('"' + delete_date + '" の予約を取り消しました．', screenshot_filepath)
        print('"' + delete_date + '" の予約を取り消しました．')
    except Exception:
        import traceback
        slack_notify.send_message('```' + traceback.format_exc() + '```')
        print(traceback.format_exc())


# reserve and cancel
def process(url, student_number, password):
    NOWTIME = datetime.datetime.now()
    SCREEN_SHOT_FILENAME = 'screenshot_{0:%Y%m%d%H%M}.png'.format(NOWTIME)
    SCREEN_SHOT_PATH = config.FILEPATH_HEAD + SCREEN_SHOT_FILENAME

    options = Options()
    # options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(2)
    # get a HTML response
    driver.get(url)

    iframe_btm = driver.find_element_by_xpath('//*[@id="id_btmf"]')

    # first page
    iframe_main = driver.find_element_by_xpath('//*[@id="id_mainf"]')
    driver.switch_to.frame(iframe_main)
    driver.find_element_by_name('SEITONO').send_keys(student_number)
    driver.find_element_by_name('ANSYONO').send_keys(password)
    driver.find_element_by_xpath('/html/body/div/form/div/input[2]').click()

    # # second page　高速
    # cbosya = driver.find_element_by_name('CBOSYA')
    # cbosya_element = Select(cbosya)
    # cbosya_element.select_by_value('09200')
    # driver.find_element_by_xpath('/html/body/div/form/input[1]').click()
    # if driver.find_elements_by_id('2018121805'):
    #     cancel(driver, '2018122005', iframe_btm, iframe_main, SCREEN_SHOT_PATH)
    #     reserve(driver, '2018121805', iframe_btm, iframe_main, SCREEN_SHOT_PATH)
    # elif driver.find_elements_by_id('2018121905'):
    #     cancel(driver, '2018122005', iframe_btm, iframe_main, SCREEN_SHOT_PATH)
    #     reserve(driver, '2018121905', iframe_btm, iframe_main, SCREEN_SHOT_PATH)
    #
    # driver.switch_to.default_content()
    # driver.switch_to.frame(iframe_btm)
    # driver.find_element_by_xpath('/html/body/form/input[1]').click()
    # driver.switch_to.default_content()
    # driver.switch_to.frame(iframe_main)

    # second page 実車
    cbosya = driver.find_element_by_name('CBOSYA')
    cbosya_element = Select(cbosya)
    cbosya_element.select_by_value('01212')
    driver.find_element_by_xpath('/html/body/div/form/input[1]').click()
    reserve(driver, '2018121904', iframe_btm, iframe_main, SCREEN_SHOT_PATH)

    if driver.find_elements_by_id('2018121903') and driver.find_element_by_id('2018121903').get_attribute('class') == 'Aki':
        if driver.find_elements_by_id('2018121904') and driver.find_element_by_id('2018121904').get_attribute('class') == 'Syo':
            cancel(driver, '2018121906', iframe_btm, iframe_main, SCREEN_SHOT_PATH)
            reserve(driver, '2018121903', iframe_btm, iframe_main, SCREEN_SHOT_PATH)

    # # send screenshot
    # if NOWTIME.time() > datetime.time(6, 55) and NOWTIME.time() < datetime.time(12, 5):
    #     if NOWTIME.minute % 10 == 0:
    #         page_width = driver.execute_script('return document.body.scrollWidth')
    #         page_height = driver.execute_script('return document.body.scrollHeight')
    #         driver.set_window_size(page_width, page_height)
    #         driver.save_screenshot(SCREEN_SHOT_PATH)
    #         slack_notify.notify('現在の空き状況', SCREEN_SHOT_PATH)

    driver.quit()
