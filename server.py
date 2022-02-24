#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return flask.Response(status=301, headers={"Location" : "http://localhost:5000/static/index.html", "Access-Control-Allow-Origin" : "*"})

@app.route("/entity/<entity>", methods=['POST','PUT','OPTIONS'])
def update(entity):
    # handle pre-flight request
    if request.method == 'OPTIONS':
        response = flask.Response()
        response.access_control_allow_headers = ["content-type"]
        response.access_control_allow_origin = "*"
        return response
    
    '''update the entities via this interface'''
    # Get the json body
    data = flask_post_json()

    # Update the entity
    myWorld.set(entity, data)
    
    return flask.Response(status=200, headers={"Access-Control-Allow-Origin" : "*"}, content_type="application/json", response=json.dumps(myWorld.get(entity)))

@app.route("/world", methods=['POST','GET','OPTIONS'])    
def world():
    # handle pre-flight request
    if request.method == 'OPTIONS':
        response = flask.Response()
        response.access_control_allow_headers = ["content-type"]
        response.access_control_allow_origin = "*"
        return response

    '''you should probably return the world here'''
    response = flask.Response(status=200, content_type="application/json", response=json.dumps(myWorld.world()))
    response.access_control_allow_origin = "*"
    print(response.headers)
    return response

@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    response = flask.Response(status=200, headers={"Access-Control-Allow-Origin" : "*"}, content_type="application/json", response=json.dumps(myWorld.get(entity)))
    return response

@app.route("/clear", methods=['POST','GET','OPTIONS'])
def clear():
    # handle pre-flight request
    if request.method == 'OPTIONS':
        print("MADE IT TO OPTIONS")
        response = flask.Response()
        response.access_control_allow_headers = ["content-type"]
        response.access_control_allow_origin = "*"
        return response

    '''Clear the world out!'''
    myWorld.clear()
    return flask.Response(status=200, headers={"Access-Control-Allow-Origin" : "*"})

if __name__ == "__main__":
    app.run()
