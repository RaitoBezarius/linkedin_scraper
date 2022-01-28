import getpass
from . import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def __prompt_email_password():
  u = input("Email: ")
  p = getpass.getpass(prompt="Password: ")
  return (u, p)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def paginate_scrape(action, page_index):
    pass

def search(driver, text, timeout=10):
    driver.get("https://www.linkedin.com/search/results/all/?keywords={}&origin=GLOBAL_SEARCH_HEADER&sid=zaf".format(text))
    MORE_RESULTS = "div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a"
    PAGE_INDICATOR = ".artdeco-pagination__indicator > button > span"
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, MORE_RESULTS))).click()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "entity-result__title-line")))
    driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
    pages_indicators = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, PAGE_INDICATOR)))
    n_pages = int(pages_indicators[-1].text)
    print('n pages', n_pages)
    results = []

    for index in range(1, n_pages + 1):
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-test-pagination-page-btn=\"{}\"] > button".format(index)))
        ).click()
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/3));"
        )
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "entity-result__title-line")))
        results.extend((item.text.split('\n')[0], item.get_attribute('href')) for item in (item.find_element_by_tag_name("a") for item in driver.find_elements_by_class_name("entity-result__title-line")))
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

    return results

def login(driver, email=None, password=None, cookie = None, timeout=10):
  if cookie is not None:
    return _login_with_cookie(driver, cookie)

  if not email or not password:
    email, password = __prompt_email_password()

  driver.get("https://www.linkedin.com/login")
  element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

  email_elem = driver.find_element_by_id("username")
  email_elem.send_keys(email)

  password_elem = driver.find_element_by_id("password")
  password_elem.send_keys(password)
  password_elem.submit()

  try:
    if driver.url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
      remember = driver.find_element_by_id(c.REMEMBER_PROMPT)
      if remember:
        remember.submit()

    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, c.VERIFY_LOGIN_ID)))
  except: pass

def _login_with_cookie(driver, cookie):
  driver.get("https://www.linkedin.com/login")
  driver.add_cookie({
    "name": "li_at",
    "value": cookie
  })
