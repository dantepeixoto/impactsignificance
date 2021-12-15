from pathlib import Path
import requests
from bs4 import BeautifulSoup

url = input('Digite a URL do site em que deseja buscar documentos: ')

baixados = set()

pasta = Path('download')
pasta.parent.mkdir(exist_ok=True)

def salva_pdf(url):
	print('salvando PDF: ',url)
	pdf = pasta/url.replace('https://', '/').replace('http://', '/')
	pdf.write_bytes(requests.get(url).content)

def baixador(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	for a in soup.find_all('a'):
		link = requests.compat.urljoin(url, a.get('href'))
		if link in baixados:
			continue
		baixados.add(link)
		print(link)

		if link.endswith('.pdf'):
			salva_pdf(link)
		elif link.endswith('/'):
			baixador(link)

baixador(url)
