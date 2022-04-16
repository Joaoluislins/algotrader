#Importing modules

from selenium import webdriver
import time
import pandas as pd
import sys
import matplotlib.pyplot as plt
import datetime


###Configuring environment to use chromium webdriver in colab

!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
df_price_stock = pd.DataFrame(columns = ['Date', 'Close', 'Change', 'Change (%)', 'Open', 'High', 'Low', 'Volume'])

for i in range(14):
  wd.get('https://www.advfn.com/stock-market/bovespa/PETR4/historical/more-historical-data?current={}&Date1=01/01/19&Date2=03/20/22'.format(i))
  tabela_nova = wd.find_element_by_xpath('/html/body/div[8]/div/div[4]/div[2]/div[1]/div[2]/table')
  df_new = pd.read_html('<table>' + tabela_nova.get_attribute('innerHTML') + '</table>')[0]
  df_price_stock = pd.concat([df_price_stock,df_new])
  df_price_stock.reset_index(drop = True, inplace = True)
df_price_stock


### Updating the Date to a datetime instance
df_price_stock.Date = df_price_stock.Date.apply(lambda x: datetime.datetime.strptime(x, '%b %d %Y').date())
type(df_price_stock.Date[0])

### Making the Date column the index.
df_price_stock.index = df_price_stock.Date

### Saving to a csv file
df_price_stock.to_csv('Petr4_stock_data.csv')