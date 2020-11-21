import os
import json
# Put your password in place of 'your_password'
class Config:
    SECRET_KEY = 'd168651a2aa242e14428a991c42164ef'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:your_password@localhost/groundwater'
