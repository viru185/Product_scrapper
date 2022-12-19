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

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('product_template.yml')

def finish_notification():
    # text2speech = gTTS("Hell yeah, fuck, it is finally finished.")
    # text2speech.save("finish_notification.mp3")
    playsound("finish_notification.mp3")

def save_progress():
    with open('progress.txt', 'w') as progress_in:
        progress_in.write(progress_counter.split('-')[-1])

def get_product_data(url):
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
    print(f"\nDownloading {url}\n")
    r = requests.get(url, headers=headers)
    
    # Simple check to check if page was blocked (Usually 503)
    if "To discuss automated access to Amazon data please contact" in r.text:
        print(f"STATUS CODE - {r.status_code}.\nPage was blocked by Amazon. Please try using better proxies\n")
        return None
    # if r.status_code > 500:
    #     print(f"Page must have been blocked by Amazon as the status code was {r.status_code}")
    #     return None
    
    # Pass the HTML of the page and create
    return e.extract(r.text)

def main():
    
    # TODO try to use advance google for product search on iherb
    
    # * read file line by line and convert list of dict
    with open('product_data.jsonl', 'r') as product_data_file_in:
        products_dict_list = []
        for line in progressbar.progressbar(product_data_file_in, prefix='Loading data...'):
            products_dict_list.append(json5.loads(line))
    
    # * get progress data
    try:
        with open('progress.txt') as progress_out:
            _start = int(progress_out.read())
            
            usr_ans = input(f'{_start} - Enter if you want to continue. or Enter number manually. : ')
            if usr_ans:
                _start = int(usr_ans)
            
    except FileNotFoundError:
        _start = input('File not found. Please Enter counter manually : ')
    
    # * getting data for each product
    for product in products_dict_list[_start:]:
        product_url = product['url']
        
        # * to save progress to file
        global progress_counter
        progress_counter = product_url[:]
        
        product_data_dict = get_product_data(product_url)
        #sleep(1)
        
        second = 5
        while product_data_dict is None or product_data_dict['product_name'] is None:
            if product_data_dict is None:
                print(f'{second} seconds')
                for _ in range(second,0,-1):
                    print(f'\rSite is BLOCKED. Trying again after {_} seconds.',end='')
                    sleep(1)
                else:
                    print()
                product_data_dict = get_product_data(product_url)
            else:
                print(f'{second} seconds')
                for _ in range(second,0,-1):
                    sleep(1)
                    print(f'\rUnable to get full data. Trying again after {_} seconds.',end='')
                else:
                    print()
                product_data_dict = get_product_data(product_url)
            second += second
        
        # * writing product data back to dict in list
        product['product_data'] = product_data_dict
        
        # * writting product data back to file
        with open('product_data.jsonl', 'w') as product_data_file_out:
            for product_dict in products_dict_list:
                json5.dump(product_dict, product_data_file_out)
                product_data_file_out.write('\n')

    finish_notification()

if __name__ == '__main__':
    main()

atexit.register(save_progress)