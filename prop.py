import requests
from bs4 propertyimport BeautifulSoup as BS
import csv
import time

start_time = time.time()

def get_html_third(url_osh):
    re = requests.get(url_osh)
    return re.text


def get_html_doska(url_doska):
    r = requests.get(url_doska)
    return r.text


def get_html(url):
    responce = requests.get(url)
    return responce.text


def get_third_site(osh):
    third = BS(osh, 'html5lib')
    lists = third.find('div', class_='listings-wrapper')
    aparts_osh = lists.find_all('div', class_='listing')
    for apart in aparts_osh:
        try:
           title = apart.find('p', class_='title').text.strip()
           location = apart.find('div', class_='address').text.strip()
           price_dollar = apart.find('div', class_='price').text.strip()
           price_som = apart.find('div', class_='price-addition').text.strip()
           description = apart.find('div', class_='description').text.strip()
           link = apart.find('a').get('href')
       
        except:
            title = ''
            location = ''
            price_dollar = ''
            price_som = ''
            description = ''
            link = ''

        data = {
            'title': title,
            'location': location,
            'price': f'{price_dollar},{price_som}',
            'description': description,
            'link': f'https://www.house.kg{link}'
        }   
 
        write_to_csv(data)
        

def get_second_site(doska):
    beauty = BS(doska, 'html5lib')
    listt = beauty.find('div', class_='doska_last_items_list')
    apartss = listt.find_all('div', class_='list_full dev')
    for ap in apartss:
        try:
            title = ap.find('a', class_='title_url').text.strip()
            price = ap.find('div', class_='list_full_price').text.strip()
            link = ap.find('a', class_='title_url').get('href')
           
        except:
            title = ''
            price = ''
            link = ''
           
        
        data = {
            'title': title,
            'price': price,
            'link': f'https://doska.kg{link}',
            'location' : 'Not found',
            'description': 'Not found'
        }   
 
        write_to_csv(data)

def get_data(html):
    soup = BS(html, 'html5lib')
    catalog = soup.find('div', class_='listings-wrapper')
    aparts = catalog.find_all('div', class_='listing')
  
    for apart in aparts:
      
        try:
           title = apart.find('p', class_='title').text.strip()
           location = apart.find('div', class_='address').text.strip()
           price_dollar = apart.find('div', class_='price').text.strip()
           price_som = apart.find('div', class_='price-addition').text.strip()
           description = apart.find('div', class_='description').text.strip()
           link = apart.find('a').get('href')
       
        except:
            title = ''
            location = ''
            price_dollar = ''
            price_som = ''
            description = ''
            link = ''

        data = {
            'title': title,
            'location': location,
            'price': f'{price_dollar},{price_som}',
            'description': description,
            'link': f'https://www.house.kg{link}'
        }   
 
        write_to_csv(data)
        
        
def write_headers():
      with open('apart.csv', 'a') as  file:
        fieldnames = ['Title', 'Location', 'Price', 'Description', 'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
def write_to_csv(data):
    with open('apart.csv', 'a') as  file:
        fieldnames = ['Title', 'Location', 'Price', 'Description', 'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'Title': data['title'],
                        'Location': data['location'],
                        'Price': data['price'],
                        'Description': data['description'],
                        'Link': data['link']
                        })


def run_doska():
    i = 1
    while True:
        url_doska = f'https://doska.kg/cat:117/&type=2&image=0&page={i}'
        html_second = get_html_doska(url_doska)
        if i == 10:
            break
        get_second_site(html_second)
        i += 1

def run_osh():
    i = 1
    while True:
        url_osh = 'https://www.house.kg/kupit?region=6&town=36&page={i}'
        html_third = get_html_third(url_osh)
        if i == 20:
            break
        get_third_site(html_third)
        i += 1


def main():
    with open('apart.csv', 'w') as file:pass
    write_headers()
    i = 1
    while True:
        url = f'https://www.house.kg/kupit?page={i}'
        html = get_html(url)
        if i == 25:
            break
        get_data(html=html)
        i += 1
    run_doska()
    run_osh()
    finish = time.time()- start_time
    print(f'Time of working {finish}')

   
if __name__ == '__main__':
    main()
