import requests
import pandas as pd
from bs4 import BeautifulSoup
countries=[]
langs=[]

html = requests.get("https://www.cia.gov/the-world-factbook/field/languages/").text
soup = BeautifulSoup(html,"lxml")
countryHTML = soup.css.select("li h2 a") #HTML for each country
langHTML = soup.css.select("li h2 + p") #HTML for each language string, each must be processed

for country in countryHTML: #build the list of countries
    countries.append(country.string)
for lang in langHTML: #build the list of languages. Each index might have its own list of languages
    lang = str(lang) #convert from tags object to text
    lang = lang[3:lang.find("<br/>")] #remove anything after/before the list of languages
    lang = lang.split(',') #split the list of languages into a list data type
    for i in range(len(lang)): 
        # sometimes a language entry has parentheses with a ',' in it. That is treated as a false split
        # this loop rejoins those false splits so that there's only 1 language per index
        if lang[i].find("(") > -1 and lang[i].find(")") == -1:
            lang[i] = lang[i] + lang[i+1]
            del lang[i+1] # remove the index value that's been joined into the preceding value
        lang[i] = lang[i].strip() #remove trailing/leading whitespace in each item
        if i == len(lang)-1: #exit the loop when the length is shorter than the starting length
            break
    langs.append(lang)

df = pd.DataFrame(countries)
df2 = pd.DataFrame(langs)
df3 = pd.concat([df,df2],axis=1, ignore_index = True)
df4 = df3.melt(id_vars = [0], var_name = 'langLevel' , value_name = 'language')
df4.dropna(axis = 'rows', subset=('language'), inplace=True)
df4.to_csv("C:/Users/Nathan/Desktop/lang.csv")