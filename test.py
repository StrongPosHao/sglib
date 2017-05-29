from __init__ import SteamGameOnline

def main():
    game = SteamGameOnline(292030, 0)
    game2 = SteamGameOnline(227300, 0)
    game3 = SteamGameOnline(402570, 0)
    game4 = SteamGameOnline(377160, 0)
    game5 = SteamGameOnline(3420, 0)
    dlc1 = SteamGameOnline(199, 1)
##    # Test print individually.
##    print game.img
##    print game.description
##    print game.user_reviews
##    print game.recent_user_review
##    print game.overall_user_review
##    print game.app_tag
##    print type(game.app_tag)
##    print game.developer
##    print game.publisher
##    print '========================\n'
##    
##    # Test gid changing and reloading
##    game.gtag = 'app'
##    game.gid = 358040
##    
##    # Test __str__ and __unicode__
##    print unicode(game)
##    print '========================\n'
##    
##    # Test documentation
##    help(SteamGameOnline)
##    print game.languages
##    print game2.original_price
##    print game3.original_price
##    print game4.discount_price
##    print game4.user_reviews
##    print game4.recent_user_review
##    print game4.overall_user_review
##    print game5.user_reviews
##    print game5.recent_user_review
##    print game5.overall_user_review
    dlc1.user_reviews
if __name__ == '__main__':
    main()
