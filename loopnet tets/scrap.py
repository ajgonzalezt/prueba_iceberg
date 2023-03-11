

#%%
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse

from concurrent.futures import ThreadPoolExecutor
import pandas as pd



headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0 (Edition std-1)',

}
def get_main_links():
    all_sitemaps = []

    response_robots = requests.get('https://www.loopnet.com/robots.txt',  headers=headers)
    sitemaps_robots = response_robots.text.replace(".gz\n", "").split("Sitemap: ")[1:]

    for sitemap_elem in sitemaps_robots:
        response_site = requests.get(sitemap_elem, headers=headers)
        beauty_site = bs(response_site.text, 'lxml')
        iner_urls = beauty_site.find_all('loc')
        for url in iner_urls:
            all_sitemaps.append({'main_sitemap': sitemap_elem, 'url':url.text})
    return all_sitemaps

sitemaps = get_main_links()



def createCSV(all_sitemaps):
    df = pd.DataFrame(sitemaps)
    df.to_csv('./data/urls.csv')


createCSV(sitemaps)



def dicci(elem):
    url = elem['url']

    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'lxml')
    lista = soup.find_all('loc')
    links = []
    for elemento in lista:
        links.append(elemento.text.lstrip('<![CDATA[').rstrip('>]]'))
    elem['total_links'] = links

    
    return elem

#def ejecutar_threads(all_sitemaps):
#    with ThreadPoolExecutor(max_workers=100) as executor:
#       res = list(
#            executor.map(dicci, all_sitemaps)
#    )


def traer_pdf(url):


    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'lxml')
    links = soup.find_all('a')
 
    i = 0
 
   
    for link in links:
        complete_link= link.get('href', [])
        if ('.pdf' in complete_link):
            i += 1
            print("Downloading file: ", i)
            print( complete_link)
            parsed_link= urllib.parse.unquote(complete_link.split("=")[1])
            # Get response object for link
            response = requests.get(parsed_link, headers=headers)
            # Write content in pdf file
            pdf = open("./data/pdf_copy"+str(i)+".pdf", 'wb')
            #print(response.content)
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")
    print("All PDF files downloaded")


traer_pdf("https://www.loopnet.com/Listing/340-350-3rd-Ave-N-Saskatoon-SK/17857842/")
#%%
