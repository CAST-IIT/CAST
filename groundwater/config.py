import os
import json
# Put your password in place of 'your_password'
# Create a config.json file in your environment in order to safely store your keys - for professional/live
# server development

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:hidden_password@localhost/groundwater'
