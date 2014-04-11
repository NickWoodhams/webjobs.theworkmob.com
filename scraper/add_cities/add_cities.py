import sys
sys.path.append('/Users/nick/Sites/apix/webjobs/')
from modules.database import engine, db_session, Base, City, Post, Update

with open('craigs_city_list.txt') as f:
    cities = f.readlines()

for city in cities:
    db_session.add(City(name=city.strip()))
    db_session.commit()
