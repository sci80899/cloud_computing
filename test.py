from scrapers import find_ID,movieinfo,review_scraper
import uuid
from moviepal import moviepal
import sys
#ID = find_ID('tom and jerry')
#print(ID)

import pymysql
def insertMovie(movie_name):
    db = pymysql.connect(host="database-1.cdnbvoqd9rxl.us-west-2.rds.amazonaws.com", 
    user="adminDanny", password="Snjnd828292929aaaaJJJJ", db="nusProject", port=3306)
    cur = db.cursor()
    movie_id = find_ID(movie_name)
    print(movie_id)
    sql="select id from movie"
    cur.execute(sql)
    result=cur.fetchall()
    id_list=[i[0] for i in result]
    review = review_scraper(movie_id)
    pal=moviepal(movie_id)
    if movie_id not in id_list:
        print('*')
        info=movieinfo(movie_id)
        sql=f"insert into movie(id,title,level,score,duration,poster,story,director,stars) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(info['ID'][0],info['title'][0],info['level'][0],info['score'][0],info['duration'][0],info['poster'][0],info['story'][0],info['director'][0],info['stars'][0])
        try:
            cur.execute(sql)
            db.commit()
            for i in range(len(review)):
                ID_UUID = uuid.uuid1()
                sql1 = f"insert into movie_review values('%s','%s','%s','%s','%s')" % (
                ID_UUID.hex, movie_id, review['user name'][i], review['score'][i],
                review['review'][i][:290].replace('"', '\\"').replace("'", "\\'"))
                try:
                    cur.execute(sql1)
                    db.commit()
                except Exception as e:
                    print(e)
            for i in range(len(pal)):
                ID_UUID2 = uuid.uuid1()
                sql2 = f"insert into movie_pal values('%s','%s','%s','%s','%s')" % (
                    ID_UUID2.hex, movie_id, pal['user name'][i], pal['score'][i],
                    pal['review'][i][:490].replace('"', '\\"').replace("'", "\\'"))
                try:
                    cur.execute(sql2)
                    db.commit()
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        finally:
            db.close()

insertMovie(sys.argv[1])

# insertMovie('Rocky')