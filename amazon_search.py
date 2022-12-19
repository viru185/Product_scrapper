import re
import json5
import requests
import pandas as pd
from gtts import gTTS
from time import sleep
from pprint import pprint
from playsound import playsound
from selectorlib import Extractor
from fake_useragent import UserAgent


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results_template.yml')

def finish_notification():
    # text2speech = gTTS("Hell yeah, fuck, it is finally finished.")
    # text2speech.save("finish_notification.mp3")
    playsound("finish_notification.mp3")

def process_data(src,dst):
    with open(src) as srch_data_file, open(dst, 'w') as srch_data_file_processed:
        for _ in srch_data_file.readlines():
            srch_data_dict = json5.loads(_)
            # print(type(srch_data_dict))
            srch_data_dict['url'] = 'https://www.amazon.co.uk' + srch_data_dict['url']
            srch_data_dict['price'] = srch_data_dict['price'].replace("\u00a3","")
            myprint(srch_data_dict)
            
            json5.dump(srch_data_dict, srch_data_file_processed)
            srch_data_file_processed.write('\n')

def get_search_urls(usr_search_url,start,end):
    if start == 0:
        start = 1

    for _ in range(start, end+1):
        yield usr_search_url + f"&page={_}"

def get_search_data(url):
    ua = UserAgent()

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.co.uk/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    
    # Simple check to check if page was blocked (Usually 503)
    if "To discuss automated access to Amazon data please contact" in r.text:
        print(f"STATUS CODE - {r.status_code}.\nPage was blocked by Amazon. Please try using better proxies\n")
        return None
    if r.status_code > 500:
        print(f"Page must have been blocked by Amazon as the status code was {r.status_code}")
        return None

    # Pass the HTML of the page and create
    return e.extract(r.text)

def main():
    usr_search_url = "https://www.amazon.co.uk/s?i=merchant-items&me=AEVI8T7EOF98V&page=4&marketplaceID=A1F83G8C2ARO7P&qid=1670271926&ref=sr_pg_40"
    usr_search_url = re.sub("&page=[0-9]|&ref=sr_pg_[0-9]", "", usr_search_url)
    
    with open('search_data.jsonl', 'w') as srch_data_file:
        for url in get_search_urls(usr_search_url,1,162):
            data = get_search_data(url)
            # pprint(data, sort_dicts=False)
            
            second = 2
            while data is None and data['products'][0]['url'] is None:
                for _ in range(second,0,-1):
                    sleep(1)
                    print(f'\rUnable to get full data. Trying again. after {_} seconds.',end='')
                else:
                    print()
                data = get_search_data(url)
            
            for product in data['products']:
                product['page_url'] = url
                
                # * write data to file
                json5.dump(product, srch_data_file)
                srch_data_file.write('\n')
            # sleep(2)

    process_data('search_data.jsonl', 'search_data_processed.jsonl')
    # finish_notification()
    
if __name__ == "__main__":
    main()



