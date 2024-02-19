from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

base_url = 'https://nith.eu.org/results?page={}'

def scrap_page(url):
    html_text=requests.get(url).text
    soup=BeautifulSoup(html_text,'lxml')
    boxes=soup.find_all('div',class_='rounded-lg border bg-card text-card-foreground shadow-sm hover:shadow-lg animate-in popup')
    ranks=[]
    names=[]
    rollnos=[]
    cgs=[]
    for box in boxes:
        ranks.append(box.find('div',class_='flex justify-center items-center w-16 h-16 rounded-full bg-slate-100 dark:bg-gray-800 font-bold text-xl').text.replace(" ",""))
        names.append(box.find('h3',class_='text-2xl font-semibold leading-none tracking-tight').text.replace(" ",""))
        rollnos.append(box.find('p',class_='text-sm text-muted-foreground font-semibold').text.replace(" ",""))
        cgs.append(box.find('button',class_='inline-flex items-center justify-center font-semibold ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 transition-duration-300 bg-primary dark:bg-primary text-white hover:bg-primary/90 h-8 rounded-md px-3 py-2 text-sm').text)
    data=[ranks,names,rollnos,cgs]
    df=pd.DataFrame(data,index=['Rank','Name','RollNo','CG']).transpose()
    df.reset_index(drop=True)
    return df

for i in range(1,129):
    url = base_url.format(i)
    result_df = scrap_page(url)
    file_name = f'result_data_page_{i}.csv'
    file_path = os.path.join('folder', file_name)
    result_df.to_csv(file_path,index=False)