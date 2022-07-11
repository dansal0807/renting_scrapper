import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.page_load_strategy = 'none'
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver = webdriver.Chrome(options=options)
imoveis = []

parte2 = '#onde=BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Gloria,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Botafogo,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Catete,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Laranjeiras,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Central-Centro,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Copacabana&quartos=1'
url_template = 'https://www.vivareal.com.br/aluguel/rj/rio-de-janeiro/apartamento_residencial/?pagina='

for page_number in range(1, 20):
    try:
        url = url_template + str(page_number) + parte2
        page = driver.get(url)

        sleep(10)
        print('-'*40)
        print(page_number)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #soup = BeautifulSoup(page, 'html.parser')
        todos_elementos = soup.find_all(
            class_='property-card__container js-property-card')
        
        for elemento in todos_elementos:
            imovel = {}

            # endereco
            imovel['endereco'] = elemento.find(
                class_='property-card__address').getText()

            # valor do imovel
            try:
                valor_imovel = float(elemento.find(
                    class_='property-card__price js-property-card-prices js-property-card__price-small').getText().split()[1].replace('.', ''))
            except:
                valor_imovel = 0.0

            imovel['valor'] = valor_imovel

            area_imovel = elemento.find(class_='property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area').getText(
            ).replace('--', '0').replace('-', ' ').split()[0]
            imovel['area'] = area_imovel

            # Numero de quartos
            imovel['quartos'] = elemento.find(class_='property-card__detail-item property-card__detail-room js-property-detail-rooms').find(
                class_='property-card__detail-value js-property-card-value').getText().replace('--', '0').replace('-', ' ').split()[0]

            # Numero de vagas
            imovel['vagas'] = elemento.find(class_='property-card__detail-item property-card__detail-garage js-property-detail-garages').find(
                class_='property-card__detail-value js-property-card-value').getText().replace('--', '0').replace('-', ' ').split()[0]

            # numero de banheiros
            imovel['banheiros'] = elemento.find(class_='property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom').find(
                class_='property-card__detail-value js-property-card-value').getText().replace('--', '0').replace('-', ' ').split()[0]

            imovel['pagina'] = page_number
            imoveis.append(imovel)
    except:
        pass


dataset = pd.DataFrame(imoveis)
print(dataset)
dataset.to_csv('imoveis_dataset.csv', sep=';', index=False)
driver.close()