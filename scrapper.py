#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:15:11 2019

@author: berkisler
"""

import re
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
from requests import get
import csv
import pandas as pd
from pandas import ExcelWriter
from openpyxl import load_workbook

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def CategoryExtract(url):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    categories = []
    sub_cat =[]
    
    for i,cat in enumerate(soup.find_all("li", attrs={'class': "browse-hubs__categories"})):
        temp= []
        #print(i+1)
        #print((cat.find("h3").text))
        categories.append(cat.find("h3").text.strip())
        for j in cat.find_all("a"):
            #print(j.get("href"), j.get("title"))
            temp.append((j.get("href"), j.get("title")))
        #print("-------------------------------------------------------------")
        sub_cat.append(temp)
      
    pages = dict((cats, subs) for cats,subs in zip(categories, sub_cat))
    
    return pages

def RecipeInfoExt(url, name, cat, sub_cat):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    infos = {}
    recip = {}
    
    #link
    infos["link"] = url
    
    #ingredients
    ingredient = []
    for ings in soup.find_all("span", class_="recipe-ingred_txt added"):
        ingredient.append(ings.text)
    infos["ingredients"] = ingredient
    
    #prep-time and directions
    directions=""
    preps = soup.find("div", class_= "directions--section")
    try:
        for i in preps.find_all("li", class_="prepTime__item")[:3]:
            if "aria-label" in i.attrs and ":" in i.get("aria-label"):
                infos[i.get("aria-label").split(":")[0]] = i.get("aria-label").split(":")[1].strip()
                #print(i.get("aria-label").split(":")[1])
                #print("--------------------")
        for j in preps.find_all("span", class_="recipe-directions__list--item"):
            directions += j.text.strip()
    except:
        print(name)
    infos["directions"] = directions
    
    
    #Rating
    try:
        for k in soup.find_all("span", class_="stars stars-4-5")[:1]:
            infos["rating"] = "%.2f" %float(k["data-ratingstars"])
    except:
        infos["rating"] = "no rating"
    
    
    #Meta description
    try:
        infos["meta"] = soup.find("meta", attrs={"id":"metaDescription"})["content"]
    except:
        infos["meta"] = "No meta "
    
    #picture
    try:
    
        infos["picture"] = soup.find("img", class_="rec-photo")["src"]
    except:
        infos["picture"] = "no pics"
    #category
    infos[cat]=sub_cat
    
    recip[name] = infos
    

    return recip

#first pages contains 29 recipes the rest does 20
def ReciepExtract(categ, pagenum):
    print("MAIN CATEGORY--------------------------------------------------------->", categ)
    total = {}
    for sub_cat in pages[categ]:
        print("SUB-CATEGORY ------------------------------------------->", sub_cat[1])
        for i in range(pagenum):
            print("PAGE NUMBER----------------------------------->", i+1)
            ext = "?page={}".format(i+1)
            url = sub_cat[0] + ext
            html = urllib.request.urlopen(url, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')
            for i,recps in enumerate(soup.find_all("article", class_="fixed-recipe-card")):
                #print("Recipe number {} is being read".format(i+1))
                link = recps.find("a").get("href")
                d_name = recps.find("span", class_="fixed-recipe-card__title-link").text
                total.update(RecipeInfoExt(link, d_name, categ, sub_cat[1]))
    if categ == "Diet & Health":
        for sub_cat in pages["Cooking Style"]:
            if sub_cat[1] == "Vegan Recipes" or sub_cat[1] =="Vegetarian Recipes":
                print("SUB-CATEGORY ------------------------------------------->", sub_cat[1])
                for i in range(pagenum):
                    print("PAGE NUMBER----------------------------------->", i+1)
                    ext = "?page={}".format(i+1)
                    url = sub_cat[0] + ext
                    html = urllib.request.urlopen(url, context=ctx).read()
                    soup = BeautifulSoup(html, 'html.parser')
                    for i,recps in enumerate(soup.find_all("article", class_="fixed-recipe-card")):
                        #print("Recipe number {} is being read".format(i+1))
                        link = recps.find("a").get("href")
                        d_name = recps.find("span", class_="fixed-recipe-card__title-link").text
                        if d_name not in list(total.keys()):
                            total.update(RecipeInfoExt(link, d_name, categ, sub_cat[1]))
                

    #COLUMNS OF THE DATAFRAME
    #['dish_name', 'Cook time', 'Prep time', categ,'directions', 'ingredients', 'meta', 'picture', 'rating']    
    data = pd.DataFrame(total).transpose()
    data.reset_index(level=0, inplace=True)
    data = data.rename(columns = {"index":"dish_name"})
    
    return data


def IntersecOfSets(arr1, arr2, arr3): 
    # Converting the arrays into sets 
    s1 = set(arr1) 
    s2 = set(arr2) 
    s3 = set(arr3) 

    # Calculates intersection of  
    # sets on s1 and s2 
    set1 = s1.intersection(s2)         #[80, 20, 100] 

    # Calculates intersection of sets 
    # on set1 and s3 
    result_set = set1.intersection(s3) 

    # Converts resulting set to list 
    final_list = list(result_set) 
    return final_list


url = "https://www.allrecipes.com/recipes/"
pages = CategoryExtract(url)

#CATEGORY NAMES TO FEED IN "ReciepExtract" FUNCTION: 
#['Meal Type', 'Ingredient', 'Diet & Health', 'Seasonal', 'Dish Type', 'Cooking Style', 'World Cuisine', 'Special Collections']
meal = ReciepExtract("Meal Type",5)
diet = ReciepExtract("Diet & Health",5)
cuisine = ReciepExtract("World Cuisine",5)

with pd.ExcelWriter('Recipes.xlsx') as writer:
    meal.to_excel(writer, sheet_name='Meal')
    diet.to_excel(writer, sheet_name='Diet')
    cuisine.to_excel(writer, sheet_name='Cusine')

common_recip_all = IntersecOfSets([i for i in diet["dish_name"]], [i for i in meal["dish_name"]], [i for i in cuisine["dish_name"]])
common_recip_mecu = IntersecOfSets([i for i in meal["dish_name"]], [i for i in meal["dish_name"]], [i for i in cuisine["dish_name"]])






