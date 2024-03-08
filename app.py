from flask import Flask,request,jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS,cross_origin
from control import train,hash_board_r
from game import board
import pymongo
import json
from decouple import Config, RepositoryEnv

import json


env=Config(RepositoryEnv('.env'))
app = Flask(__name__)

# api = Api(app)
# CORS(app,origins=["http://localhost:5173"])
# cors = CORS(app, resources={r"/http://localhost:5173/*": {"origins": "*"}})

db_url = env.get('SECRET_URL')
client = pymongo.MongoClient(db_url)

# Access the database
db = client["test"]

# Access the collection
collection = db["bots"]


@app.route('/', methods =['POST'])
@cross_origin()
def post():
        request_data = request.get_json()

        bot_info = request_data['data']
        print(request_data)
        user = request_data['username']     
        print(bot_info)
        X_alpha= 0.1 if not bot_info['alpha_x'] else bot_info['alpha_x']
        X_epsilon = 0.15 if not bot_info['epsilon_x'] else bot_info['epsilon_x']
        O_alpha = 0.1 if not bot_info['alpha_o'] else bot_info['alpha_o']
        O_epsilon = 0.05 if not bot_info['epsilon_o'] else bot_info['epsilon_o']
        X_gamma = 0.9   if not bot_info['gamma_x'] else bot_info['gamma_x']
        O_gamma= 0.9 if not bot_info['gamma_o'] else bot_info['gamma_o']
        
        b = board(3)
        player1, player2 = train(X_alpha,X_epsilon,O_alpha,O_epsilon,X_gamma,O_gamma,b)
        
        response= jsonify({'player_x_q':player1.Q,'player_o_q':player2.Q})

        # Create a document to insert
        document = {"player_x_q": player1.Q, "player_o_q": player2.Q,"bot_creater":user,"botName":bot_info['botName']}

        # Insert the document into the collection
        collection.insert_one(document)
        return response

# api.add_resource(trainBot, '/')

if __name__ == '__main__':
    app.run(debug='true')




