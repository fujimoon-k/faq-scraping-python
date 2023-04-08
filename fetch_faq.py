import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROMEDRIVER_PATH = "./chromedriver"
BASE_DOMAIN = "https://www.db.yugioh-card.com"
BASE_URL = "https://www.db.yugioh-card.com/yugiohdb/faq_search.action?ope=2&stype=2&keyword=&tag=-1&sort=1"
PAGE_TOTAL = 200
BATCH_SIZE = 100


def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    service.start()
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def create_json(start_page, end_page, batch_num, driver):
    faq_list = []
    path_values = []

    for page in range(start_page, end_page):
        url = f"{BASE_URL}&page={page}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "link_value")))
        link_elements = driver.find_elements(By.CLASS_NAME, "link_value")

        for element in link_elements:
            value = element.get_attribute('value')
            path_values.append(value)

        time.sleep(1)
        print(f"Processing page is {page}")

    for path in path_values:
        detail_url = f"{BASE_DOMAIN}{path}"
        driver.get(detail_url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.ID, "question_text")))
        question_element = driver.find_element(By.ID, "question_text")
        question_text = question_element.text.replace(
            '\n', '').replace('\xa0', '')
        answer_element = driver.find_element(By.ID, "answer_text")
        answer_text = answer_element.text.replace('\n', '').replace('\xa0', '')
        faq_list.append({'question': question_text, 'answer': answer_text})
        time.sleep(1)
        print(f"Processing path is {path}")

    output = {'data': faq_list}

    with open(f"faq_{batch_num}.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


driver = initialize_driver()

batch_count, last_batch_size = divmod(PAGE_TOTAL, BATCH_SIZE)

for i in range(batch_count):
    start_page = i * BATCH_SIZE + 1
    end_page = start_page + BATCH_SIZE
    create_json(start_page, end_page, i, driver)

if last_batch_size > 0:
    start_page = batch_count * BATCH_SIZE + 1
    end_page = start_page + last_batch_size
    create_json(start_page, end_page, batch_count + 1, driver)

driver.quit()
