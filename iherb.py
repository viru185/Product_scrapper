import json5
import atexit
import requests
import progressbar
from gtts import gTTS
from time import sleep
from pprint import pprint
from playsound import playsound
from selectorlib import Extractor
from fake_useragent import UserAgent

myprint = lambda x:pprint(x, sort_dicts=False)

def save_process():
    pass

class productData:
    def __init__(self,dict):
        # Create an Extractor by reading from the YAML file
        self.e_page = Extractor.from_yaml_file('iherb_search_template.yml')
        self.e_product = Extractor.from_yaml_file('iherb_product_template.yml')
        self.headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua.random,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://uk.iherb.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    
    def getData(self, headers, e_template, url):
        ua = UserAgent()

        # Download the page using requests
        print(f"\nDownloading {url}\n")
        r = requests.get(url, headers=self.headers)
        
        # if r.status_code > 500:
        #     print(f"Page must have been blocked by Amazon as the status code was {r.status_code}")
        #     return None
        
        # Pass the HTML of the page and create
        return e_template.extract(r.text)
        
    
    def getProducturl():
        pass
    
    def getProductdata():
        pass
    
    def finish_notification():
        # text2speech = gTTS("Hell yeah, fuck, it is finally finished.")
        # text2speech.save("finish_notification.mp3")
        playsound("finish_notification.mp3")

def main():
    pass

if __name__ == '__main__':
    main()