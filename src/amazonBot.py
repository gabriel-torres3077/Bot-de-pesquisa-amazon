import bs4
import requests
from openpyxl import Workbook
import os

wb = Workbook()

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT":"1","Connection":"close",
    "Upgrade-Insecure-Requests":"1"
    }

url ='https://www.amazon.com.br/s?k=Iphone&i=electronics&rh=n%3A16209062011%2Cp_89%3AApple&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1616528213&rnid=18120432011&ref=sr_nr_p_89_1'
response = requests.get(url,headers=headers)

soup = bs4.BeautifulSoup(response.content, "lxml")

productPrice = []
productName = []
for products in range(0, 24): #Buscar os aparelhos e adicionar seus nomes e preços a suas respectivas listas

    productName.append(soup.find("div", attrs={"data-index": products}).find("span", attrs={"class": 'a-size-base-plus a-color-base a-text-normal'}).text.strip())

    if soup.find("div", attrs={"data-index": products}).find("span", attrs={"class": 'a-price-whole'}) == None: #definir valores para celulares sem marcação de preço
        productPrice.append('Valor indisponível')
    else:
        productPrice.append((soup.find("div", attrs={"data-index": products}).find("span", attrs={"class": 'a-price-whole'}).text.strip())+'00')
productsWorksheet = wb.worksheets[0]

productsWorksheet.title = 'Resultados da busca - Amazon'


productsWorksheet['A1'] = 'Produto'
productsWorksheet['B1'] = 'Preço'
row = 2
for count in range(0, len(productName)):
    productsWorksheet[('A'+str(row))] = productName[count]
    productsWorksheet[('B'+str(row))] = productPrice[count]
    row+=1

wb.save(os.path.expanduser("~/Desktop/Resultados.xlsx"))
print('Processo finalizado, a tabela está disponível  na sua área de trabalho!')
