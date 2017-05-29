from review import getReview, reviewString

appid = 292030
reviews = getReview(appid, 2)

for rev in reviews:
    print reviewString(rev)
print len(reviews)
