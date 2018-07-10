import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
	r = requests.get(url)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')   # парсер какой использовать
	total_pages = soup.find_all('li', class_= 'paginator-catalog-l-i')[-1].find('span').text
	return int(total_pages)
#div class = "btn btn-def2

def write_csv(data):
	with open('rozetka.csv','a')as f:
		writer = csv.writer(f, delimiter = ';', lineterminator = '\n')
		writer.writerow( {data['title'],
						data['price'],
						data['desc'],
						data['url']} )

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='g-i-tile-l').find_all('div', class_='g-i-tile-i-box-desc')

	for ad in ads:
		name = ad.find('div', class_='g-i-tile-i-title').find('a').text.strip()
		if 'Ноутбук' in name:

			try:
				title = ad.find('div', class_='g-i-tile-i-title').find('a').text.strip()
			except:
				title = ''
			try:
				url = ad.find('div', class_='g-i-tile-i-title').find('a').get('href')
			except:
				url = ''
			try:
				price = ad.find('div', class_='g-price').find('span').text.strip()
			except:
				price = ''
			try:
				desc = ad.find('ul', class_='g-i-tile-short-detail').find('li').text.strip()
			except:
				desc = ''

			data = {'title':title,
					'price':price,
					'desc': desc,
					'url':url}

			return write_csv(data)
		else:
			continue

def main():
	url = 'https://rozetka.com.ua/ua/search/?text=asus&producer=4&p=1'
	base_url = 'https://rozetka.com.ua/ua/search/?text=asus&producer=4&p='

	total_pages = get_total_pages(get_html(url))

	for i in range(1, total_pages+1): #if all pages to parse
	#	url_gen = base_url+str(i)
	#	print(url_gen)

	#for i in range(1,5):
		url_gen = base_url+str(i)
		html = get_html(url_gen)
		get_page_data(html)


if __name__ == '__main__':
	main()









