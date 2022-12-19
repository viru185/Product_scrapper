import json5
import numpy
import pandas as pd
import fake_useragent
from gtts import gTTS
from time import sleep
from pprint import pprint
from playsound import playsound

myprint = lambda x:pprint(x, sort_dicts=False)

# with open('search_data.jsonl') as srch_data_file, open('search_data_processed.jsonl', 'w') as srch_data_file_processed:
#     for _ in srch_data_file.readlines():
#         srch_data_dict = json5.loads(_)
#         # print(type(srch_data_dict))
#         srch_data_dict['url'] = 'https://www.amazon.co.uk' + srch_data_dict['url']
#         srch_data_dict['price'] = srch_data_dict['price'].replace("\u00a3","")
#         myprint(srch_data_dict)
        
#         json5.dump(srch_data_dict, srch_data_file_processed)
#         srch_data_file_processed.write('\n')

    
    # db = pd.read_json(srch_data_file,lines=True)
    # print(db.head())

# with open('product_data.jsonl') as product_data_file:
#     for _ in product_data_file.readlines():
#         product_data_dict = json5.loads(_)
#         myprint(product_data_dict)

#         db = pd.read_json(product_data_dict)
#         print(db.head())

# text2speech = gTTS("Hell yeah, fuck, it is finally finished.")
# text2speech.save("finish_notification.mp3")
# playsound("finish_notification.mp3")

# with open('product_data.jsonl', 'r') as product_data_file_in:
#     products_dict_list = []

#     for line in progressbar.progressbar(product_data_file_in, prefix='Data loading...'):
#         products_dict_list.append(json5.loads(line))

ua = fake_useragent.UserAgent()
