from bs4 import BeautifulSoup
import requests 
from app import db, WorldInsurance

# set up your scraping below
def website():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_health_insurance_coverage'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    table = soup.find("table",{"class":"wikitable sortable"})
    rows = table.findAll("tr")
    data = []
    
# in order to get within the rows and columns we me understand
# headers are under th 
    # columns = [i.text.replace('\n','') for i in rows[0].findAll('th')]
    # data.append(columns)
    
    for i in range(1,len(rows)):
        tds = rows[i].findAll('td')
#         create an empty list to add all of your td texts
        tds_text = []
    
        for td in tds:
#             for each td in the row, append the stripped text to to the tds_text list (strip just removes white spaces at the beginning and end of your string)
            tds_text.append(td.text.strip())
        
#         for each row, append the tds_text list with all of your appended text items
        data.append(tds_text)

#     see what your output looks like
    #print(data)
    return data
    
    #function for website to database
def website_db(info):
    #bring in data 
    # print("Website db" ,info)
    for infos in info:
        #print(infos)
        new_row = WorldInsurance(rank = infos[0], country = infos[1],total = infos[2], government = infos[3], primary_private = infos[4])
        #print("This is a new row", new_row)
        db.session.add(new_row)
        db.session.commit()



# this `main` function should run your scraping when 
# this script is ran.
def main():
    db.drop_all()
    db.create_all()
    # call your website function
    ws = website()
    website_db(ws)
   


if __name__ == '__main__':
    main()