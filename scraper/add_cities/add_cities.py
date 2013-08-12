import sys
sys.path.append('/Users/admin/Sites/webjobs/')
from modules.database import *

with open('craigs_city_list.txt') as f:
    cities = f.readlines()

for city in cities:
    db_session.add(City(name=city.strip()))
    db_session.commit()
