# Moneycontrol-News-Scraping
This repo contain the python code for scraping news form money control website. There are two types of file generated news-meta data file and main-article file.

## Setup

To run this project, install all the dependencies in the requirments.txt:

```
$ pip install -r requirements.txt
```

## Usage
```
>> from moneycontrol import MoneyControl
```
Add company's id and year.
RI is code of Reliance Industries and 2020 is year.
```
>> obj = MoneyControl("RI",2020)
```
Get headline and url link of content
```
>> obj.headline("file-name.csv")
```
Get the content of each article and store it in separate file
```
>> obj.content("file-name.csv")
```
