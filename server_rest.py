from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import random 
import uuid
import json
from pathlib import Path
import os.path
import datetime


game_data_folder = Path("games")
app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, game_id, name):
        game_file_path = game_data_folder / str(game_id + ".json")
        if not os.path.isfile(game_file_path):
            return "Game not found", 404
        with open(game_file_path) as f:
            game = json.load(f)
        if not "game_id" in game or not "relations" in game:
            return "Game file invalid", 400            

        for user in game["relations"]:
            if(name == user["name"]):
                return "Hallo " + name + "! Du musst " + user["gift_to"] + " etwas wichteln.", 200
        return "User not found", 404


class Create(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        users = json_data["names"]
        not_allowed = json_data["not_allowed"]
        sender = users.copy()
        recievers = users.copy()
        relations = []
        for user in sender:
            remaining_recievers = recievers.copy() # alle die noch nicht gezogen wurden
            if user in remaining_recievers: # nicht selbst ziehen
                remaining_recievers.remove(user)
            if user in not_allowed: # regeln für nutzer prüfen
                app.logger.info(user + ' can\'t be with ' + ', '.join(not_allowed[user]))
                for not_allowed_reciever in not_allowed[user]: # alle die nichts von diesem nutzer bekommen sollen werden gelöscht
                    if not_allowed_reciever in remaining_recievers:
                        remaining_recievers.remove(not_allowed_reciever)
            if len(remaining_recievers) == 0: # möglicherweise unlösbar, oder zufällig falscher weg
                app.logger.info("no recievers remaining")
                return "Unsolved", 200
            reciever = random.choice(remaining_recievers)
            recievers.remove(reciever)
            app.logger.info(user + " ===> " + reciever)
            relation = {
                "name": user,
                "gift_to": reciever
            }
            relations.append(relation)

        game_id = str(uuid.uuid4().hex)
        game = {
            "game_id": game_id,
            "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relations": relations
        }    

        app.logger.info("GameID: " + game_id)
        game_file_path = game_data_folder / str(game_id + ".json")
        with open(game_file_path, "w") as game_file:
            json.dump(game, game_file, sort_keys = True, indent = 4)

        return game, 201
      
api.add_resource(User, "/<string:game_id>/<string:name>")
api.add_resource(Create, "/create")


app.run(debug=True)
