import pandas as pd
import jinja2
# import pdfkit #not used yet
import requests 
import tqdm
import configparser
import argparse

def get_from_api(company, api_key, product,status_to_ignore):
    api_url = f'https://{company}.aha.io/api/v1/products/{product}/features'
    response = requests.get(f'{api_url}', headers={'Authorization': f'Bearer {api_key}'})
    pages = response.json()['pagination']['total_pages']
    features = response.json()['features']
    for page in tqdm.tqdm(range(2,pages+1)):  
        response = requests.get(f'{api_url}?page={page}', headers={'Authorization': f'Bearer {api_key}'})
        features.extend(response.json()['features'])
    
    feature_list = []
    for f_id in tqdm.tqdm(features):
        response = requests.get(f'{api_url}/{f_id["id"]}', headers={'Authorization': f'Bearer {api_key}'})      
        feature = response.json()['feature']
        if feature['workflow_status']['name'].upper() not in status_to_ignore: # this is fugly; aha! doesn't support an option to call features by status
            feature_list.append(feature)  
    
    template_vars = {'cards' : feature_list}
    outtext = prepare_template(template_vars, 'cards_api')   
    write_to_html(outtext, 'cards_api')     



def read_dataset():
    df = pd.read_csv('features.csv')
    dfi = pd.read_csv('ideas.csv')
    cards = df.append(dfi, sort=False)
    cards['Feature_description'] = cards['Feature_description'].str.slice(0,180) + '...' 
    template_vars = {'cards' : cards}
    outtext = prepare_template(template_vars, 'cards')
    write_to_html(outtext, 'cards')


def prepare_template(template_vars, template):
    templateLoader = jinja2.FileSystemLoader(searchpath="./template")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = template+".html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(template_vars)
    return outputText


def write_to_html(outputText, fileName):    
    html_file = open(f'reports/{fileName}.html', 'w', encoding='utf-8')
    html_file.write(outputText)
    html_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Report Tool to gather Information from the DCGY API.')
    parser.add_argument('-api','--api',  action='store_true')
    parser.add_argument('-f', '--inFile', action='store_true')
    args = parser.parse_args()
    if args.api:
        config = configparser.ConfigParser()
        config.read('config.ini')
        company = config['AHA.IO']['COMPANY']
        api_key = config['AHA.IO']['API_KEY']
        product = config['AHA.IO']['PRODUCT']
        status_to_ignore = config['AHA.IO']['STATUS_TO_IGNORE']
        get_from_api(company,api_key, product,status_to_ignore)
    if args.inFile:
        read_dataset()