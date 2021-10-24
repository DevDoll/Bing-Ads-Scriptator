import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.request import Request, urlopen

# Getting the Ad results
def adret(adnum, rawli):

    ad1 = str(rawli[adnum])

    rhdl1 = ad1.split('<span dir="ltr">')[1]
    hdl1 = rhdl1.split('</span>')[0]

    rlink1 = ad1.split('<cite>')[1]
    link1 = rlink1.split('</cite>')[0]

    rdisc1 = ad1.split('<span class="" dir="ltr">')[1]
    disc1 = rdisc1.split('</span>')[0]
    return hdl1, link1, disc1

# Keyword search & extraction function
def ksne(query):
    usera = ua.random
    bingurl = 'https://www.bing.com/search?q=%s&search=&form=QBLH'% query
    headers = {'User-Agent': '%s'%usera}
    cookies = {'MUIDB': '31A1AD521F3368F80610BD801E586942'}
    searching = requests.get(bingurl, headers=headers, cookies=cookies)
    searchresult = searching.text
    soup = BeautifulSoup(searchresult, 'html.parser')
    allcode = soup.prettify()
    rawli = soup.find_all('li', class_='b_algo')

    adnum = int(1)
    adnums = int(7)
    adFile = open('ad-sets.txt', 'a')
    adFile.write('\n\n--Keyword: %s'%keyword)

    while adnum <= adnums:
        try:
            headline, link, desc = adret(adnum, rawli)
            print('we got: \n %s \n %s \n %s \n'%(headline, link, desc))
            # writing ad-sets to a file
            adFile.write('\nAd-Set %s:\n'%adnum)
            adFile.write('\n%s'%headline)
            adFile.write('\n%s'%link)
            adFile.write('\n%s\n'%desc)
        except Exception as e: print(e)
        adnum +=1
    adFile.close()

#Getting SSL Proxies
def get_proxies(ua):
    proxies = []
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string})
    return proxies

#declaring Variables
ua = UserAgent()

#code
with open('keywords.txt', 'r') as kfile:
    keylines = kfile.readlines()
    for keyword in keylines:
        chstr = keyword.split(' ')
        queryraw = '+'.join(chstr)
        query = str(queryraw)
        print('\nSearching for the keyword: %s \n'%keyword)
        ksne(query)