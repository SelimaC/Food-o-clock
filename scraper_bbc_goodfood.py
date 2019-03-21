import re
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen,Request
import ssl
from requests import get
import csv
import pandas as pd
from pandas import ExcelWriter
from openpyxl import load_workbook
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#The main url to crawl
url = "https://www.bbcgoodfood.com"

cuisines = ['caribbean','british','american','chinese','french','greek','indian','italian','japanese','mediterranean',
            'mexican','moroccan','spanish','thai','turkish','vietnamese']

def get_cuisines(url_par):
    sub_url = url + url_par
    req = Request(url=sub_url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    recipes = soup.find_all("article",attrs={'class':"node-recipe"})
    links = [recipe.find('a')['href'] for recipe in recipes]
    others = soup.find_all('li',class_='pager-item')
    if others != None:
        for i in others:
            new_link = i.a['href']
            sub_url = url + new_link
            req = Request(url=sub_url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            recipes = soup.find_all("article",attrs={'class':"node-recipe"})
            new_links = [recipe.find('a')['href'] for recipe in recipes]
            links = links + new_links
    return links

def get_recipe(link,main_cat,sub_cat):
    sub_url = url + link
    req = Request(url=sub_url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    infos = {}
    
    infos['link'] = sub_url
    
    #ingredients
    ingredient = []
    for ings in soup.find_all('li',class_='ingredients-list__item'):
        ingredient.append(ings['content'])
    infos['ingredients'] = ingredient
    
    directions = "\n".join([dirs.p.text for dirs in soup.find_all('li',attrs={'itemprop':'recipeInstructions'})])
    infos['directions'] = directions
    try:
        infos['prep-time'] = soup.find('span',class_='recipe-details__cooking-time-prep').span.text
    except:
        infos['prep-time'] = 'none'
    
    try:
        infos['cook-time'] = soup.find('span',class_='recipe-details__cooking-time-cook').span.text
    except:
        infos['cook-time'] = 'none'
    
    try:
        rating = len(list(soup.find_all('span',class_='rate-fivestar-btn-filled')))
        infos['rating'] = rating
    except:
        infos["rating"] = "no rating"
        
    try:
        meta = soup.find('meta',attrs={'property':'og:description'})['content']
        infos['meta'] = meta
    except:
        infos["meta"] = "No meta "
    
    try:
        img = soup.find('img',attrs={'itemprop':'image'})['src']
        infos['picture'] = img
    except:
        infos['picture'] = "no pics"
        
    try:
        diff = soup.find('section',class_='recipe-details__item recipe-details__item--skill-level')
        infos['difficulty'] = diff.span.text
    except:
        infos['difficulty'] = 'none'
    
    try:
        diet = soup.find('div',class_='recipe-header__additional').ul.find_all('li')
        infos['diet'] = [i.text for i in diet]
    except:
        infos['diet'] = 'no info'
    
    infos['dish-name'] = soup.find('h1',class_='recipe-header__title').text
    
    if main_cat != None:
        infos[main_cat] = sub_cat
        
    return infos
    
def get_from_cuisines():
    total = []
    for cuisine in cuisines:
        for link in get_cuisines(cuisine):
            total.append(get_recipe(link,'cuisine',cuisine))
        print('{} finished'.format(cuisine))
        df = pd.DataFrame(total)
        with open('bbc_cuis.csv', 'a',encoding="utf-8") as f:
            df.to_csv(f,header=False)
        total=[]
        
def get_sub_categories(url):
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    links = soup.find_all('h3',class_='category-item--title')
    #print('Subcategories found')
    subcat = [(i.a['href'], i.a.text) for i in links]
    #print(subcat)
    return subcat

def get_from_categories(url):
    print('Started')
    total = []
    for item in get_sub_categories(url):
        for link in get_cuisines(item[0]):
            total.append(get_recipe(link,'dish-type','dinner'))
        print('{} finished'.format(item[1]))
        df = pd.DataFrame(total)
        with open('bbc_dinner.csv', 'a',encoding="utf-8") as f:
            df.to_csv(f,header=False)
        total=[]

#get_from_categories('https://www.bbcgoodfood.com/recipes/category/dinner-ideas-0')
#print(get_recipe('/recipes/3926/goats-cheese-and-red-pepper-tart','cuisine','turkish'))
        
def concat_dfs():
    df1 = pd.read_csv('bbc_cuis.csv')
    df2 = pd.read_csv('bbc_dinner.csv')
    df3 = pd.read_csv('bbc_veg.csv')

    un_links = {x:True for x in set(list(df1['link'])+list(df2['link'])+list(df3['link']))}

    dfs = [df1,df2,df3]

    total_df = []

    for df in dfs:
        for index,row in df.iterrows():
            if un_links[row['link']]:
                total_df.append(row)
                un_links[row['link']] = False
    last_df = pd.DataFrame(total_df)
    last_df.to_csv('final_recipes.csv','w',encoding='utf-8')
    return last_df

def export_to_sql(df):
    filename="recipes-gokhan"
    con=sqlite3.connect(filename+".db")
    df.to_sql('recipes',con, index=False)
    con.commit()

#export_to_sql(concat_dfs())