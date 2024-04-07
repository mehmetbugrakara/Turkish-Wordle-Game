import requests
from bs4 import BeautifulSoup
import pandas as pd

# Kelimetre.com'dan Türkçe kelime listesini çekme
url = 'https://www.kelimetre.com/kelime-listeleri'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Beş harfli kelimeleri içeren bir liste oluşturma
words = []
for baslayan in soup.find_all('div',class_={'column mt-2'}):
    starting_words=baslayan.find('a')['href']
    url_ = f'https://www.kelimetre.com/{starting_words}' 
    response_ = requests.get(url_)
    soup_ = BeautifulSoup(response_.content, 'html.parser')
    for n_letter_words in soup_.find_all('div',class_={'column mt-3'}):
        starting_with_n_number_url = n_letter_words.find('a')['href']
        response_2 = requests.get(starting_with_n_number_url)
        soup_2 = BeautifulSoup(response_2.content, 'html.parser')
        card = soup_2.find('div',class_={'card'})
        for get_words in card.find_all('li'):
            words.append(get_words.find('a').get_text())

words_df = pd.DataFrame(words,columns=['Words'])
words_df.to_csv('words_df.csv')