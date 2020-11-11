from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import unicodedata
import csv
import pandas as pd

class MoneyControl:
    def __init__(self,comp_id,year):
        self.comp_id = str(comp_id)
        self.year = str(year)
        # self.url = 'https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=RI&pageno='+str(comp_id)+'&durationType=Y&Year='+str(year)
    
    def headline(self,file_name):
        id=1
        while True:
            print(id)
            try:
                url = 'https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id='+self.comp_id+'&pageno='+str(id)+'&durationType=Y&Year='+self.year
                req = requests.get(url)
                soup = BeautifulSoup(req.content, 'html.parser')
                all_FL = soup.find_all('div', class_="MT15 PT10 PB10")
                if(not len(all_FL)):
                    break
                with open(file_name,'a',newline='') as f:
                    writer = csv.writer(f)
                    for ele in all_FL:
                        title = ele.find('strong')
                        link_tag = ele.find(class_ = 'g_14bl')
                        timestamp = ele.find(class_ = 'PT3 a_10dgry')
                        text_string = timestamp.contents[0]
                        clean_text = unicodedata.normalize("NFKD",text_string)
                        timeanddate = clean_text.split('|')
                        time = timeanddate[0]
                        date = timeanddate[1]
                        news_url = 'https://www.moneycontrol.com'+link_tag['href']
                        # print(title.string,news_url, end='\n'*2, sep='\n'*2)
                        print(time,date)
                        writer.writerow([title.string,news_url,date,time])
                    id+=1
            except Exception as e:
                print(e)
                break
    
    def get_meta_data(self):
        print(self.comp_id,self.year)

    def content(self,file_name):
        data = pd.read_csv(file_name,names = ['title','url','date','time'],encoding='latin1')
        data['file-name'] = ""
        for i in range(len(data['url'])):
            news_url = data['url'][i]
            # print(data['url'][i])
            news_content = requests.get(news_url)
            page = BeautifulSoup(news_content.content,'html.parser')
            pro_memebership_count=0
            file_name = "article"+str(i)+".txt"
            with open(file_name,'a') as f:
                try:
                    article = page.find(id='article-main')
                    cont = article.find_all('p')
                    for para in cont:
                        f.write(para.text)
                        # print(para.text, sep="\n\n\n")
                    data['file-name'][i]=file_name
                    print(file_name)
                except:
                    print("PRO MEMBERSHIP")
                    pro_memebership_count+=1
                    pass
            f.close()
        data.to_csv('News-Meta-data2.csv',index=True,header=True)

    


