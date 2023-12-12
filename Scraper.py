# Scrapping Product Reviews from Amazon

import pandas as pd

import requests
from bs4 import BeautifulSoup

search_query="nike+shoes+men"
base_url="https://www.amazon.com/s?k="

url=base_url+search_query
url

header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}


search_response=requests.get(url,headers=header)

search_response.status_code

search_response.text


search_response.cookies

# ## function to get the content of the page of required query

cookie={} # insert request cookies within{}
def getAmazonSearch(search_query):
    url="https://www.amazon.com/s?k="+search_query
    print(url)
    page=requests.get(url,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## function to get the contents of individual product pages using 'data-asin' number (unique identification number)

def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## function to pass on the link of 'see all reviews' and extract the content

def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## First page product reviews extraction

product_names=[]
response=getAmazonSearch('nike+shoes+men')
soup=BeautifulSoup(response.content)
for i in soup.findAll("span",{'class':'a-size-base-plus a-color-base a-text-normal'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list


product_names


len(product_names)


# #### The method of extracting data-asin numbers are similar to that of product names. Only the tag details have to be changed in findall()


data_asin=[]
response=getAmazonSearch('nike+shoes+men')
soup=BeautifulSoup(response.content)
for i in soup.findAll("div",{'class':"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"}):
    data_asin.append(i['data-asin'])


response.status_code

data_asin


len(data_asin)

# #### By passing the data-asin numbers, we can extract the 'see all reviews' link for each product in the page


link=[]
for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content)
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])

len(link)


# #### Now we have the 'see all review' links. Using this link along with a page number, we can extract the reviews in any number of pages for all the products

link

reviews=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content)
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)


len(reviews)


rev={'reviews':reviews}

review_data=pd.DataFrame.from_dict(rev)
pd.set_option('max_colwidth',800)


review_data.head(5)


review_data.shape


review_data.to_csv('Scraping reviews.csv') #converting the dataframe to a csv file so as to use it later for further analysis
