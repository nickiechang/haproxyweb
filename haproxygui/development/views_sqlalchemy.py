from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render

from sqlalchemy import * 
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.exc import OperationalError 

import os
from haproxygui import models_sqlalchemy

def hello_world(request):
    #return HttpResponse("Hello world!")
    return render(request,'hello_world.html',{'current_time': datetime.now()})

def database(request):
    #return HttpResponse("Hello world!")
    #engine = create_engine(settings.DATABASES)
    conn_str = 'mysql://root:testlab@172.16.19.2/haproxy'
    engine = create_engine(conn_str, pool_size=50, pool_recycle=3600)    
    Base = declarative_base()
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()
    if session:
        rows = session.query(models_sqlalchemy.Frontend).all()  
    return render(request,'database.html',{'rows': rows})

