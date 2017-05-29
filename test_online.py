from online import SteamGameOnline

def test():
##    data_set = [[440250, 1],    # Test app-Videos
##                [358040, 0],    # Test app-Hardwares
##                [431960, 0],    # Test app-Software
##                [292030, 0],    # Test app-Game
##                [232, 2],       # Test bundle
##                [124923, 1]]    # Test sub
    data_set = [[292030, 0],    # Test app-Game
                [232, 2],       # Test bundle
                [124923, 1]]    # Test sub
    for data in data_set:
        #game = SteamGameOnline(data[0], data[1], debug=True)
        game = SteamGameOnline(data[0], data[1])
        print unicode(game)

def test2():
    g = SteamGameOnline(6666666, 0)
    print g.status
    g.gid = 20
    print unicode(g)
    
if __name__=='__main__':
    test()
##    help(SteamGameOnline)

