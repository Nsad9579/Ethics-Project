#import our packages
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
#creat our lists for first loop (scraping from the website)
Num=[]
Approval_Code=[]
Committee=[]
Title=[]
Principal_Investigator=[]
Approval_Date=[]
Type=[]
#creat our lists for second loop (cleaning and extracting the data using Regex)
TITLE=[]
DATE=[]
TYPE=[]
PERIOD=[]
COMITE=[]
NUM=[]  
COMITE=[]

#my first loop : Scraping the row number, title, Approval Date ,Committee and type of each study from ethics.research.ac.ir which is an iranian website
number_of_page=10
for v in range (0,number_of_page):
    url=f"https://ethics.research.ac.ir/PortalProposalListEn.php?page={v}&order=&lastorder=&perPage=20&#search-result-table"
    res= requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    #for Number of each study 
    Numbers=soup.select(".text td:nth-child(1)")
    for x in Numbers:
        Num.append(str(x))
    #for Committee of each study 
    Committees=soup.select(".gray")
    for x in Committees:
        Committee.append(str(x))
    #for Title of each study 
    Titles=soup.select(".zarEn.normal")
    for x in Titles:
        Title.append(str(x))
    #for Approval_Date of each study 
    Approval_Dates=soup.select("td:nth-child(5)")
    for x in Approval_Dates:
        Approval_Date.append(str(x))

#my second loop:cleaning and extracting the data using Regex       
for x in Title:
    mod_string = re.sub('<td class="zarEn normal">', '', x )
    y = re.sub('</td>', '', mod_string )
    TITLE.append(y)
#for type and date
for x in Approval_Date:
    mod_string = re.sub('<td align="center" width="100">\n\t\t\t\t\t', '', x )
    y = re.sub('\t\t\t\t\t<br/>\n\t\t\t\t\t', '', mod_string )
    y = re.sub('\t\t\t\t</td>', '', y )
    DATE.append(y)

for x in DATE:
    mod_string =re.findall('[A-Z][a-z]+',x)
    TYPE.append(mod_string[0])

for x in DATE:
    mod_string =re.sub('[A-Z][a-z]+','',x)
    PERIOD.append(mod_string) 
#for committee
for x in Committee:
    mod_string =re.findall('IR.([A-Z]+.*[A-Z]+).REC',x)
    #y = re.sub('\n\t\t\t\t\t\n\t\t\t\t</td>', '', mod_string )
    COMITE.append(mod_string[0])
for x in Num:
    mod_string = re.sub('<td align="center" width="45">\n\t\t\t\t\t', '', x )
    y = re.sub('\n\t\t\t\t\t\n\t\t\t\t</td>', '', mod_string )
    NUM.append(y)

    
dict = {'Num': NUM, 'DATE': PERIOD,'Title':TITLE ,'TYPE': TYPE, 'Committee': COMITE}  
       
df = pd.DataFrame(dict)    
# saving the dataframe 
df.to_csv("PATH")
