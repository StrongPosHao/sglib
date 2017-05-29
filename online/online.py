import re, bs4, requests

class SteamGameOnline(object):
    r"""Class used to represent one game on steam.

    Page will be downloaded when you alloc a SteamGame object.
    
    You can read games id, tag, name, url, img, reviews and so
    on with this class.
    """

    # ____________________ Decorated Func ____________________
    
    def __check_status(func):
        def m_check_status(self):
            if self.__status: print '<Warning> Page not found or connection failed.'
            return func(self)
        m_check_status.__doc__ = func.__doc__
        return m_check_status
    
    # ____________________ Property ____________________

    @property
    @__check_status
    def gid(self):
        r"""Get game's id
            [Return] integer"""
        return self.__id

    @gid.setter
    def gid(self, gid):
        r"""Rewrite game's id
            Page will reload"""
        self.__id = gid
        self.__init__(self.__id, self.__tag, self.__debug)
    
    @property
    @__check_status
    def gtag(self):
        r"""Get game's url tag
            [Return] string"""
        return self.__tag

    @gtag.setter
    def gtag(self, gtag):
        r"""Rewrite game's url tag
            Page will reload"""
        self.__tag = gtag
        self.__init__(self.__id, self.__tag, self.__debug)

    @property
    @__check_status
    def app_type(self):
        r"""Get game's type if gtag is app, else gtag itself
            [Return] integer"""
        return self.__get_app_type()
    
    @property
    def url(self):
        r"""Get game's url
            [Return] string"""
        return self.__url + ('  [Page not found]' if self.__status else '')

    @property
    @__check_status
    def html_text(self):
        r"""Get game's html text
            [Return] string"""
        return self.__text
    
    @property
    @__check_status
    def gname(self):
        r"""Get game's name
            [Return] string"""
        return self.__read_name() if not self.__status else ''

    @property
    def status(self):
        r"""Get the status description of loading this game's info
            [Return] string"""
        err_info = ['Loaded.','Connection Failed.',
                    'No such game id with such tag.',
                    'Tag error.', 'Unknown Error.']
        if self.__status < 10:
            return err_info[self.__status]
        else:
            return 'Error on loading page.(Errno: %d)' % self.__status

    @property
    def img(self):
        r"""Get the header image url of this game
            [Return] string"""
        return self.__soup.find(r'img', class_ = "game_header_image_full").attrs['src']
    
    @property
    def description(self):
        r"""Get the short description about this game.
            [Return] string"""
        r = self.__soup.find(r'div', class_ = "game_description_snippet")
        return r.string.strip() if r else '' 

    @property
    def recent_user_review(self):
        r"""Get the user review about this game in the last 30 days
            [Return] string"""
        r = self.user_reviews
        return '{}% of the {} user reviews in the last 30 days are positive.'.format(r[0][0], r[0][1]) if r and len(r)>1 else ''
    
    @property
    def user_reviews(self):
        r"""Get recent and overall user reviews
            [Return] list"""
        result = [i.attrs['data-store-tooltip'] for i in self.__soup.find_all('div', class_='user_reviews_summary_row')]
        if len(result) == 0:
            return None
        elif result[0] == 'Need more user reviews to generate a score':
            return None
        else:
            return [(lambda x: [int(x[0][0]),int(x[0][1])])(re.findall(re.compile(r'^(\d.+?)% of the (\d.+?) '), i.replace(',',''))) for i in result]
    
    @property
    def overall_user_review(self):
        r"""Get overall user review about this game
            [Return] string"""
        r = self.user_reviews
        return '{}% of the {} user reviews for this game are positive.'.format(r[1][0], r[1][1]) if r and len(r)==2 \
          else '{}% of the {} user reviews for this game are positive.'.format(r[0][0], r[0][1]) if r and len(r)==1 else ''

    @property
    def app_tag(self):
        r"""Get the popular user-defined tags for this product
            [Return] string"""
        return [i.string.strip().encode('utf8') \
                for i in self.__soup.find_all(r'a', class_ = "app_tag")]
       
    @property
    def developer(self):
        r"""Get the devoloper of this product
            [Return] string"""
        dev = self.__soup.find(r'a', href = re.compile(r'^http://store.steampowered.com/search/\?developer.+?'))
        return dev.string.encode('utf8') if dev else ''  
    
    @property
    def publisher(self):
        r"""Get the publisher of this product
            [Return] string"""
        pub = self.__soup.find(r'a', href = re.compile(r'^http://store.steampowered.com/search/\?publisher.+?'))
        return pub.string.encode('utf8') if pub else ''

    @property
    def languages(self):
        r"""Get the supported languages of this product
            [Return] list"""
        return [i.string.strip().encode('utf8') for i in self.__soup.find_all(r'td', class_ = 'ellipsis')]

    @property
    def original_price(self):
        r"""Get the original price of this product
            [Return] string"""
        if self.__soup.find(r'div', class_ = "discount_original_price"):
            return self.__soup.find(r'div', class_ = "discount_original_price").string.strip()
        elif self.__soup.find(r'div', class_ = "game_purchase_price price"):
            return self.__soup.find(r'div', class_ = "game_purchase_price price").string.strip()

    @property
    def discount_price(self):
        r"""Get the dicount price of this product
            [Return] string"""
        if self.__soup.find(r'div', class_ = "discount_final_price"):
            return self.__soup.find(r'div', class_ = "discount_final_price").string.strip()
        else:
            return None
        
    @property
    def min_requirements(self):
        r"""Get the minimum requirements of this game
            [Return] String"""
        if self.__soup.find(r'div', class_ = "game_area_sys_req_leftCol"):
            pass
    

    # ____________________ Override ____________________
    
    def __init__(self, gid, gtag, debug=False):
        r"""Construction function. Recieve args of game id, game tag
            and method access to this game. 'by' args should be 'net'
            or 'file'. When file specified, a data folder path should
            be given.
            """
        self.__debug = debug
        self.__id = gid
        self.__tag = 'app' if gtag==0 else 'sub' if gtag==1\
                    else 'bundle' if gtag==2 else gtag

        if self.__tag in ['app', 'sub', 'bundle']:
            self.__url = 'http://store.steampowered.com/{}/{}/'\
                     .format(self.__tag, self.__id)
            if self.__debug: print 'Loading webpage:\n ', self.__url
            self.__soup = bs4.BeautifulSoup(self.__getHtmlText(),
                                          'html.parser')
        else:
            self.__url = '<Error>'
            if self.__debug: print 'Error tag.'
            self.__status = 3     # Tag error
            self.__soup = None0

    @__check_status
    def __str__(self):
        r"""Print most properties about game in order
            [Return] string"""
        # format property to str
        fmt_property = lambda title, content: '\n%020s: %s'%(title, content)
        
        info = '[Game Info]'
        info += fmt_property('ID', str(self.__id))
        info += fmt_property('Url Tag', self.__tag)
        info += fmt_property('Url', self.__url + ('  [Page not found]' if self.__status else ''))
        info += fmt_property('Name', (self.__read_name().encode('utf-8') if not self.__status else 'None'))
        info += fmt_property('Type', self.__get_app_type())
        info += fmt_property('Developer', self.developer)
        info += fmt_property('Publisher', self.publisher)
        info += fmt_property('Original Price', (self.original_price.encode('utf-8') if not self.__status and self.original_price else 'None'))
        if self.discount_price and self.__status:
            info += fmt_property('Discount Price', (self.discount_price.encode('utf-8')))
        info += fmt_property('Languages', self.languages)
        info += fmt_property('Recent User Review', self.recent_user_review if not self.__status and self.recent_user_review else '')
        info += fmt_property('Overall User Review', self.overall_user_review if not self.__status and self.overall_user_review else '')
        info += fmt_property('Description', self.description.encode('utf-8') if not self.__status and self.description else 'None')
        tag = self.app_tag
        info += fmt_property('Game Tag', (', '.join(tag[:3] if len(tag)>3 else tag) if tag else 'None')\
                + (', ...' if len(tag)>3 else ''))
        if self.__debug:
            info += fmt_property('Status', self.status)
        return info

    def __unicode__(self):
        r"""Print most properties about game in order by unicode
            [Return] unicode string"""
        return str(self).decode('utf-8')
    
    # ____________________ Inner ____________________
    
    def __getHtmlText(self):
        r"""Return the html text of game with id=gid and tag=gtag
        """
        try:
            r = requests.get(self.__url, cookies={'birthtime':'4372812'})
            r.raise_for_status()
        except requests.ConnectionError as e:
            if self.__debug: print 'Load failed:', e.message.reason.message.split(':')[1].strip()
            self.__status = 1
            return ''
        except requests.RequestException as e:
            if self.__debug: print 'Load failed. (Errno:%d)' % e
            self.__status = r.status_code
            return ''
        r.encoding = 'utf-8'
        if self.__debug: print 'Load status:', r.status_code
        if r.status_code == 200:
            if r.text.find('<title>Welcome to Steam</title>')!=-1:
                # When page turn to Welcome, means no match game found.
                self.__status = 2     # No this page
            else:
                self.__status = 0     # Correct Loaded.
        else:
            self.__status = 1         # Connection Failed.
        self.__text = r.text
        return r.text

    def __read_name(self):
        r"""Read this game's name
            [Return] string"""
        if self.__status: return None
        return self.__soup.find('title').string[:-9]

    def __get_app_type(self):
        r"""Read this game's type if tag is "app"
            [Return] string"""
        if self.__tag !='app': return self.__tag
        return self.__soup.find(r'div', class_ = r'blockbg').find_all('a')[0].string.encode('utf8').split(' ')[-1]
    
    # ____________________ Private Variables ____________________
    # self.__[debug, url, id, tag, text, soup, status, by, path]
    
