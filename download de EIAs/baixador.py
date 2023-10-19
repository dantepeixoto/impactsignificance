from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

url = input('Digite a URL do site em que deseja buscar documentos: ')
urlprincipal = urlparse(url)
print(urlprincipal.netloc)

baixados = set()

pasta = Path('download')
pasta.mkdir(exist_ok=True)

def salva_pdf(url):
    print('salvando PDF: ', url)
    pdf = pasta / url.replace('https://', '').replace('http://', '')
    pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf.write_bytes(requests.get(url).content)

def baixador(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        link = urljoin(url, a.get('href'))
        if link in baixados:
            continue
        link_netloc = urlparse(link).netloc
        if urlprincipal.netloc not in link_netloc:
            continue
        baixados.add(link)
        # log #
        print(link)

        if urlprincipal.netloc in link_netloc:
            if link.endswith('.pdf'):
                salva_pdf(link)
            elif link.endswith('/'):
                baixador(link)

baixador(url)
