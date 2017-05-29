import urllib, urllib2, re, bs4, os
from bs4 import BeautifulSoup
from bs4 import element

# get the text of the html
def getHtmlText(url):
    try:
        response = urllib2.urlopen(urllib2.Request(url))
    except urllib2.HTTPError, e:
        print 'Error! ==> Code:%d ' % e.code
    else:
        return response.read()

def getReview(appid, offset, p, numperpage=10, browsefilter='toprated', language='english', searchText=''):
    url='http://steamcommunity.com/app/'+str(appid)+'/homecontent/'
    form_elem = [('userreviewsoffset', str(offset)),
                 ('p', str(p)),
                 ('workshopitemspage', str(p)),
                 ('readytouseitemspage', str(p)),
                 ('mtxitemspage', str(p)),
                 ('itemspage', str(p)),
                 ('screenshotspage', str(p)),
                 ('videospage', str(p)),
                 ('artpage', str(p)),
                 ('allguidepage', str(p)),
                 ('wenguidepage', str(p)),
                 ('integratedguidepage', str(p)),
                 ('discussionspage', str(p)),
                 ('numperpage', str(numperpage)),
                 ('browsefilter', browsefilter),
                 ('appid', str(appid)),
                 ('appHubSubSection', str(numperpage)),
                 ('l', language),
                 ('appHubSubSection', str(numperpage)),
                 ('browsefilter', browsefilter),
                 ('filterLanguage', 'default'),
                 ('searchText', searchText),
                 ('forceanon', '1')]
    m_url = url + "?" + urllib.urlencode(form_elem)
    #print m_url
    text = getHtmlText(m_url)
    return text
    
def getReviewsFromTop(appid, page, numperpage=10, browsefilter='toprated', language='english', searchText=''):    
    # To find a ResultSet that not exist to create a new empty one:
    soup = BeautifulSoup('','html.parser')
    Reviews = []
    for i in range(page):
        print "\rProgress: {}%".format(float(i+1)*100/page)
        content = getReview(appid, i*numperpage, i+1, numperpage, browsefilter, language, searchText)
        soup = BeautifulSoup(content,'html.parser')
        # get review
        revlist = soup.find_all('div', class_='apphub_Card modalContentLink interactable')
        for rev in revlist:
            revd = {}
            # print str(rev)
## TODO     helpful_d = {}
            author_d = {}
            # get "helpful" details in review, ht=help total, t=total, p=percent, f=funny
## TODO     helpful_d['ht'], helpful_d['t'], helpful_d['p'], helpful_d['f'] = map(lambda x: int(x.replace(',','')) if x != '' else 0, \
##                              rev.find('div', class_='found_helpful').text.strip().replace('person', 'people').replace(',','').replace(' of ',',')\
##                              .replace(' people (',',').replace('%) found this review helpful',',')\
##                              .replace(' people found this review funny','').split(','))
            revd['helpful'] = rev.find('div', class_='found_helpful').text.strip()
            revd['appid'] = appid
            revd['title'] = rev.find('div', class_='title').string
            revd['hours'] = float(rev.find('div', class_='hours').string[:-14].replace(',', ''))
            revd['date']  = rev.find('div', class_='date_posted').string[8:]
            products = rev.find('div', class_='apphub_CardContentMoreLink ellipsis').string[:-20].replace(',','')
            revd['products'] = int(products) if products else 0
            revd['review'] = '\n'.join(map((lambda x: x.strip() if not isinstance(x, element.Tag) else '' if x.name == 'div' else reduce(lambda x, y: x+y, [i.strip().\
                        replace('<br>', '\n').replace('</br>', '\n') for i in x.prettify().encode('ascii', 'ignore').split('\n')]).strip()), rev.find('div', class_='apphub_CardTextContent').contents)).strip()
            author_info = rev.find('div', class_=re.compile(r'^apphub_CardContentAuthorName'))
            author_d['name'] = author_info.a.string
            author_d['url'] = author_info.a.attrs['href']
            author_d['img'] =  rev.find('div', class_=re.compile(r'^appHubIconHolder')).img.attrs['src']
            revd['author'] = author_d
            Reviews.append(revd)
    # process
    # print Reviews
    # print len(Reviews)
    return Reviews

def printReview(review):
    fmt_property = lambda title, content: '\n%020s: %s'%(title, content)
    info = '[Review Detail]'
    info += fmt_property('Author', review['author']['name'])
    info += fmt_property('Author\'s URL', review['author']['url'])
    info += fmt_property('Owned Products', review['products'])
    info += fmt_property('Publish Date', review['date'])
    info += fmt_property('Play Hours', review['hours'])
    info += fmt_property('Title', review['title'])
##    info += fmt_property('Helpful', '{} of {} people ({}%) found this review helpful, {} people found this review funny.'\
##                            .format(review['helpful']['ht'], review['helpful']['t'], review['helpful']['p'], review['helpful']['f']))
    info += fmt_property('Helpful', review['helpful'])
    info += fmt_property('Review Contents', '\n'+review['review'])
    return info


def main():
    appid = 400250
    reviews = getReviewsFromTop(appid, 2)
    for i in reviews:
        print printReview(i), '\n'

             
    



if __name__ == '__main__':
    main()
                    
                    
        
    
