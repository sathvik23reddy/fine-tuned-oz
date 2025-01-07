from time import sleep
import re
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_url_in_chrome(url, mode='headed'):
    if mode == 'headed':
        driver = webdriver.Chrome()
    elif mode == 'headless':   
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        service = webdriver.chrome.service.Service(executable_path='./chromedriver.exe')
        driver = webdriver.chrome.webdriver.WebDriver(options=options, service=service)
    
    driver.get(url)
    return driver

def accept_T_and_C(driver):
    driver.find_elements(By.XPATH, "//paper-button[@aria-label='No thanks']").click()
    driver.switch_to.frame(driver.find_elements(By.XPATH, "//iframe[contains(@src, 'consent.google.com')]"))
    sleep(1)
    driver.find_elements(By.XPATH, '//*[@id="introAgreeButton"]/span/span').click()
    sleep(3)
    driver.refresh()
    
def get_video_data(driver, mode):
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)

    if mode=='headed':
        try:
            print('Accepting Terms and Conditions')
            accept_T_and_C(driver)
        except:
            print("No T&Cs to accept.")
        
        print("Opening transcript")
        sleep(3)
        # Click 'More actions'
        driver.find_elements(By.XPATH, "//tp-yt-paper-button[@id='expand' and @role='button']")[0].click()
        

        # Click 'Open transcript'
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show transcript']")))
        button.click()
    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_elements(By.XPATH, "//tp-yt-paper-button[@id='expand' and @role='button']")[0].click()
        except:
            sleep(3)
            driver.refresh()
            get_video_data(driver, mode)
        
        # Click 'open transcript'
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show transcript']")))
            button.click()        
        except:
            sleep(3)
            driver.refresh()
            get_video_data(driver, mode)
    
    print("Copying transcript ")
    transcript_element = driver.find_element(By.XPATH, "//*[@id='body']/ytd-transcript-segment-list-renderer")
    transcript = transcript_element.text
    title = driver.find_element(By.CSS_SELECTOR, 'h1.style-scope.ytd-watch-metadata yt-formatted-string').text
    description = driver.find_element(By.CSS_SELECTOR, '#description-inline-expander > yt-attributed-string > span').text

    return transcript, title, description

def processTranscript(transcript):
    # Helps remove timestamps
    pattern = r'^(\d:\d{2}|\d{2}:\d{2}|\d{2})$'

    transcript = transcript.split('\n')
    transcript_text = list()
    for i in transcript:
        if re.match(pattern, i.strip()):
            continue
        else:
            transcript_text.append(i)

    return transcript_text
    

def runIndividualScrape(url, mode='headless'):
    # Supports 'headed' & 'headless' modes
    driver = open_url_in_chrome(url, mode)
    
    transcript, title, description = get_video_data(driver, mode)
    
    driver.close()
    	
    transcript = processTranscript(transcript)

    print('Saving video data')
    
    return " ".join(transcript), title, description
    

