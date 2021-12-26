import requests
from bs4 import BeautifulSoup as BS
import csv


def get_html(url):
    responce = requests.get(url)
    return responce.text



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
            title = 'not found'
            location = 'not found'
            price_dollar = 'under contract'
            price_som = 'under contract'
            description = 'not found'
            link = 'not found'



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
    

    
if __name__ == '__main__':
    main()

