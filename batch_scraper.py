from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
import yt_scrape

outputCSVFile = 'output.csv'

def get_latest_video_links(channel_url, limit, scroll_duration):
    """Extract video links from the given YouTube channel URL using Selenium."""
    video_links = []
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')  
    options.add_argument('--enable-unsafe-swiftshader') 
    service = Service('./chromedriver.exe')  

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(channel_url)
        time.sleep(5)  

        start_time = time.time()
        while time.time() - start_time < scroll_duration:
            driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 1000 pixels
            time.sleep(0.5)  # Short pause to allow content to load

        # Collect video links after scrolling
        video_elements = driver.find_elements(By.CSS_SELECTOR, 'a#video-title-link')
        for video in video_elements[:limit]:
            link = video.get_attribute('href')
            if link:
                video_links.append(link)

    except Exception as e:
        print(f"Error fetching video links: {e}")
    finally:
        driver.quit()

    return video_links

def push_to_csv(*data):
    with open(outputCSVFile, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def setup_csv():
    columns = ["title", "description", "transcript"]
    with open(outputCSVFile, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

def main(channel_url):
    setup_csv()
    video_links = get_latest_video_links(channel_url, limit=50, scroll_duration=10)
    print(f"Found {len(video_links)} videos")
    for link in video_links:
        transcript, title, description = yt_scrape.runIndividualScrape(link) 
        push_to_csv(title, description, transcript)      

if __name__ == "__main__":
    channel_url = input("Enter YouTube channel URL: ").strip()
    main(channel_url)


#https://www.youtube.com/@ozzymanreviews/videos