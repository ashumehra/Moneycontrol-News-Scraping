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
                        time = timeanddate[0].strip()
                        date = timeanddate[1].strip()
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
        data['content'] = ""
        for i in range(len(data['url'])):
            news_url = data['url'][i]
            # print(data['url'][i])
            news_content = requests.get(news_url)
            page = BeautifulSoup(news_content.content,'html.parser')
            pro_memebership_count=0
            try:
                article = page.find(class_='content_wrapper arti-flow')
                # if article is None:
                #     article = page.find(id='article-main')
                cont = article.find_all('p')
                content = []
                for para in cont:
                    # print(para.text, sep="\n\n\n")
                    content.append(para.text)
                content = "".join(content)
                data['content'][i]=content
                # print(content)
                print("Extracting...",news_url)
            except Exception as e:
                print("PRO MEMBERSHIP", e)
                pro_memebership_count+=1
                pass
        data.to_csv(self.comp_id+'-MoneyControl-data.csv',index=True,header=True)

    def economic(self,setpageno=10,file_name='Economic-MoneyControl.csv'):
        page_no = 1
        while(page_no<=setPageNo):
            url = "https://www.moneycontrol.com/news/business/economy/page-"+str(page_no)+"/"
            req = requests.get(url)
            soup = BeautifulSoup(req.content,'html.parser')
            all_FL = soup.find('div', id="left")
            lists = all_FL.find_all('li',class_="clearfix")
            with open(file_name,mode='a',newline='') as f:
                writer = csv.writer(f)
                for ele in lists:
                    title = ele.find('h2')
                    time  = ele.find('span').text.strip()
                    dateobj = datetime.datetime.strptime(time, '%B %d, %Y %I:%M %p IST')
                    link = title.find('a')['href']
                    writer.writerow([title.text,link,dateobj.date(),dateobj.time()])
                    # print(link)
            page_no+=1


