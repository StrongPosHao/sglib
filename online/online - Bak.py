import re, bs4, requests

class SteamGameOnline():
    r"""Class used to represent one game on steam.

    Page will be downloaded when you alloc a SteamGame object.
    
    You can read games id, tag, name, url, img, reviews and so
    on with this class.
    """
    
    # ____________________ Property ____________________
    
    @property
    def gid(self):
        r"""Return this game's id.
        """
        if self.__status: print '<Warning> Page not found or connection failed.'
        return self.__id

    @property
    def app_type(self):
        r"""Return this game's id.
        """
        if self.__status: print '<Warning> Page not found or connection failed.'
        return self.__get_app_type()
    
    @property
    def gtag(self):
        r"""Return this game's tag.
        """
        if self.__status: print '<Warning> Page not found or connection failed.'
        return self.__tag

    @property
    def url(self):
        r"""Return this game's url.
        """
        if self.__status: print '<Warning> Page not found or connection failed.'
        return self.__url

    @property
    def html_text(self):
        r"""Return this game's text.
        """
        if self.__status: print '<Warning> Page not found or connection failed.'
        return self.__text
    
    @property
    def gname(self):
        r"""Return this game's name.
        """
        if self.__status:
            print '<Warning> Page not found or connection failed.'
            return ''
        return self.__read_name()

    @property
    def status(self):
        r"""Return the status of loading this game's info.
        """
        err_info = ['Loaded.','Connection Failed.',
                    'No such game id with such tag.',
                    'Paras error.', 'Unknown Error.']
        if self.__status < 10:
            return err_info[self.__status]
        else:
            return 'Error on loading page.(Erron:%d)' % self.__status

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

        self.__url = 'http://store.steampowered.com/{}/{}/'\
                     .format(self.__tag, self.__id)
        if self.__debug: print 'Loading webpage:\n ', self.__url
        
        if self.__tag in ['app', 'sub', 'bundle']:
            self.__soup = bs4.BeautifulSoup(self.__getHtmlText(),
                                          'html.parser')
        else:
            if self.__debug: print 'Error tag.'
            self.__status = 3     # Tag error
            self.__soup = None

    # ____________________ Inner ____________________
    
    def __getHtmlText(self):
        r"""Return the html text of game with id=gid and tag=gtag.
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
        self.__text = r.text.encode('utf8')
        return r.text

    def __read_name(self):
        r"""Read this game's name.
        """
        if self.__status: return None
        return self.__soup.find('title').string[:-9]

    def __get_app_type(self):
        r"""Read this game's type if tag is "app".
        """
        if self.__tag !='app': return self.__tag
        return self.__soup.find(r'div', class_ = r'blockbg').find_all('a')[0].string.encode('utf8').split(' ')[-1]
    
    # ____________________ Private Variables ____________________
    # self.__[debug, url, id, tag, text, soup, status, by, path]
    
