import os
import json

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

class Config:
    SECRET_KEY = 'd168651a2aa242e14428a991c42164ef'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:hidden_password@localhost/groundwater'
