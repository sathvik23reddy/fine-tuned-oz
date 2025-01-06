import pandas as pd
from time import sleep
import os
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint
import re



def open_url_in_chrome(url, mode='headed'):
    #print(f'Opening {url}')
    if mode == 'headed':
        driver = webdriver.Chrome()
    elif mode == 'headless':   
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = webdriver.chrome.service.Service(executable_path='./chromedriver.exe')
        driver = webdriver.chrome.webdriver.WebDriver(options=options, service=service)
    
    driver.get(url)
    return driver

def accept_T_and_C(driver):
    # Click 'No thanks'
    driver.common.by(XPATH = "//paper-button[@aria-label='No thanks']").click()
    
    # Click 'I agree' https://stackoverflow.com/questions/64846902/how-to-get-rid-of-the-google-cookie-pop-up-with-my-selenium-automation
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src, 'consent.google.com')]"))
    sleep(1)
    driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
    sleep(3)
    driver.refresh()
    
def get_transcript(driver, mode):
    
    driver.implicitly_wait(10)
    
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
        
        # sleep(3000)
        # Click 'Open transcript'
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show transcript']")))

        # Click the button
        button.click()
    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_elements(By.XPATH, "//tp-yt-paper-button[@id='expand' and @role='button']")[0].click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
        
        # Click 'open transcript'
        try:
            driver.find_element_by_xpath("//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
    
    # Get all transcript text
    print("Copying transcript ")
    transcript_element = driver.find_element(By.XPATH, "//*[@id='body']/ytd-transcript-segment-list-renderer")
    transcript = transcript_element.text

    return transcript

def processTranscript(transcript):
    # Helps remove timestamps
    pattern = r'^(0:\d{2}|00:\d{2}|00)$'

    transcript = transcript.split('\n')
    transcript_text = list()
    for i in transcript:
        if re.match(pattern, i.strip()):
            continue
        else:
            transcript_text.append(i)

    return transcript_text
    

def main(url, mode='headless'):
    driver = open_url_in_chrome(url, mode)
    
    transcript = get_transcript(driver, mode)
    
    driver.close()
    	
    transcript = processTranscript(transcript)

    print('Saving transcript ')
    
    with open("output.txt", "w") as file:
        file.write("".join(transcript))
    
    print("Transcript saved")

if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=5tvmMX8r_OM"
    mode = 'headed'
    main(url, mode)
    

    