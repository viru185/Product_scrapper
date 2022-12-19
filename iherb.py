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


class productData:
    def __init__(self,dict):
        # Create an Extractor by reading from the YAML file
        self.e_page = Extractor.from_yaml_file('')
        self.e_product = Extractor.from_yaml_file('')
    
    def save_process():
        pass
    
    def getProducturl():
        pass
    
    def getProductdata():
        pass

    