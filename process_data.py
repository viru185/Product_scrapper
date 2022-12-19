import json5
from pprint import pprint

myprint = lambda x:pprint(x, sort_dicts=False)


def data_to_dict(unprocess_dict):
    processed_dict = {}
    
    #get each dick in give dict
    for i in unprocess_dict:
        #storing keys and value for each dict
        key = i['key'][0]
        value = i['value']
        
        if key in ["Customer Reviews", "Best Sellers Rank", "Date First Available"]:
            continue
        #removing unvanted characters
        for n,v in enumerate(value):
            value[n] = v.replace("\u200e","")
        if len(value) == 1:
            value = value[0].split(',')
        #processing one item list 
        if len(value) == 1:
            value = value[0]
        
        # * finally creating new processed dict
        processed_dict[key] = value
    
    return processed_dict

def process_product_data(file_path_in,file_path_out):
    with open(file_path_in, 'r') as file_in, open(file_path_out,'w') as file_out:
        total_lines = 2592
        n = 1
        for product_data in file_in.readlines():
            print(f'\rdata process - {n}/{total_lines}({round(((n)/total_lines)*100)}%)',end='')
            n += 1
            data_dict = json5.loads(product_data)
            # myprint(data_dict)
            
            if data_dict['product_data']:
                if data_dict['product_data']['item_price']:
                    data_dict['product_data']['item_price'] = data_dict['product_data']['item_price'].replace("\u00a3","")
                if data_dict['product_data']['item_price_one_time_purchase']:
                    data_dict['product_data']['item_price_one_time_purchase'] = data_dict['product_data']['item_price_one_time_purchase'].replace("\u00a3","")
                
                data_to_process = ['item_specifications', 'technical_details', 'additional_information']
                for dtp in data_to_process:
                    if data_dict['product_data'][dtp]:
                        data_dict['product_data'][dtp] = data_to_dict(data_dict['product_data'][dtp])
            
            json5.dump(data_dict, file_out)
            file_out.write('\n')
            
process_product_data('product_data.jsonl', 'product_data_processed.jsonl')