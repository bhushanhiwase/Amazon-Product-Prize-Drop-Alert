# Program checks the amazon price and if price drops it an sends email to  client and also notes the prices in csv file
# after every 12 hrs

from bs4 import BeautifulSoup
import requests
import smtplib
from datetime import datetime
import time
import csv
import os

link = 'https://www.amazon.com/Tang-Orange-Pineapple-Powdered-Container/dp/B00L0UKSOC?pf_rd_r=9FHBGK7SJD5QKK569SAS&pf' \
       '_rd_p=f6fb7221-cd0a-462c-a5cf-719d5bf05a98&pd_rd_r=fdbcf9bc-fb84-40bf-bb1a-f9793f40433d&pd_rd_w=8khDG&pd_rd_' \
       'wg=FZHrh&ref_=pd_gw_bia_d0'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ''(KHTML, like Gecko) '
                         'Chrome/83.0.4103.97 Safari/537.36'}


def price_track():
    y = requests.get(link, headers=headers)
    # header : 'User-Agent' is used to scrape the complete HTML script from amazon.com else partial script is recived
    text = y.text
    soup = BeautifulSoup(text,'lxml')

    find = soup.find("td", class_="a-span12")                          # finds the price field
    if find == None:                                                   # if price is not available
        print("Price not available")
        return
    else:
           price_ = find.span.text
           global price
           price = float(price_[1:])                                           # obtains float value for future comparisions
           global item_name
           item_name = soup.find("span", class_="a-size-large").text.strip()    # strip to delete extra spaces

           with open('price_logs.csv', "a") as file:                              # write the data to csv file
               csv_file = csv.writer(file)

               if os.stat("price_logs.csv").st_size > 0:
                   csv_file.writerow([item_name, datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S"), price])
               else:
                   csv_file.writerow(['ITEM', 'DATE', 'TIME', 'PRICE'])
                   csv_file.writerow([item_name, datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S"), price])

           # print(item_name)
           print('$', price)

           if price < 24.97:                                                   # enter the price you desire
               send_email()
           else:
               print("No price drop \nEmail not sent")


def send_email():
    '''
    Step to send an Email, turn on two step verification on Gmail.
    add apps password and generate window computer Gmail password/key
    '''

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('(enter email id here)', '(enter generated password here)')

    subject = f'Price For {item_name} has dropped by ${round((24.97-price), 2)}'
    body = f'Checkout the following link for details:\n\n{link} \n\n\n\n\n\n' \
           f'(This e-mail was sent using python script on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")})'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        "(sender's email id here)",
        "(receiver's email id here)",
        msg
    )

    print("Email sent successfully....")



while True:
    price_track()                                               # To check the price after every 12.00 hours
    time.sleep(43200)
