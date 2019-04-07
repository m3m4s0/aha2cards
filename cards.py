import pandas as pd
import jinja2
import pdfkit #not used yet


def read_dataset():
    df = pd.read_csv('features.csv')
    dfi = pd.read_csv('ideas.csv')
    cards = df.append(dfi, sort=False)
    cards['Feature_description'] = cards['Feature_description'].str.slice(0,180) + '...' 
    template_vars = {'cards' : cards}
    prepare_template(template_vars, 'cards')

def prepare_template(template_vars, template):
    templateLoader = jinja2.FileSystemLoader(searchpath="./template")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = template+".html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(template_vars)
    write_to_html(outputText)


def write_to_html(outputText):    
    html_file = open('reports/cards.html', 'w', encoding='utf-8')
    html_file.write(outputText)
    html_file.close()
    

if __name__ == "__main__":
    read_dataset()
