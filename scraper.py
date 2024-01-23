from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# Configuração do objeto Options
options = Options()

# Caminho para o executável do chromedriver
chromedriver_path = "/usr/bin/google-chrome"

# Adicionando o caminho do chromedriver às opções
options.binary_location = chromedriver_path

# Configuração do driver do Chrome
driver = webdriver.Chrome(options=options)

# URL dos Exoplanetas da NASA
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Aguarde até 10 segundos para a página carregar
driver.get(START_URL)
time.sleep(10)

planets_data = []

# Defina o método de coleta de dados dos exoplanetas
def scrape():
    for i in range(0, 10):
        print(f'Coletando dados da página {i+1} ...' )

        # Objeto BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Loop para encontrar o elemento dentro das tags ul e li
        for ul_tag in soup.find_all("ul", attrs={"class": "exoplanet"}):
            li_tags = ul_tag.find_all("li")
           
            temp_list = []

            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            planets_data.append(temp_list)

        # Encontre todos os elementos na página e clique para passar para a próxima página
        driver.find_element(By.XPATH, '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Chamando o método    
scrape()

# Defina o cabeçalho
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Defina o dataframe do pandas
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Converta para CSV
planet_df_1.to_csv('scraped_data.csv', index=True, index_label="id")

# Feche o navegador quando terminar
driver.quit()
