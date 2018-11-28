from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse
import random 
import uuid
import json
from pathlib import Path
import os.path
import datetime
import hashlib


game_data_folder = Path("games")
app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, game_id, random):
        game_file_path = game_data_folder / str(game_id + ".json")
        if not os.path.isfile(game_file_path):
            return output_html("Game not found", 404)
        with open(game_file_path) as f:
            game = json.load(f)
        if not "game_id" in game or not "relations" in game:
            return output_html("Game file invalid", 400) 

        for user in game["relations"]:
            if(random == user["random"]):
                text = "<center><h3>Hallo " + str(user["name"]) + "!</h3> Du musst <b>" + str(user["gift_to"]) + "</b> etwas wichteln.</center>"
                return output_html(text, 200)
        return output_html("User not found", 404)


class Create(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        host_url = json_data["host_url"]
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
                    if not not_allowed_reciever in users:
                        return "Found user in relation thats not in names: " + not_allowed_reciever, 400
                    if not_allowed_reciever in remaining_recievers:
                        remaining_recievers.remove(not_allowed_reciever)
            if len(remaining_recievers) == 0: # möglicherweise unlösbar, oder zufällig falscher weg
                app.logger.info("no recievers remaining")
                return "Unsolved", 200
            reciever = random.choice(remaining_recievers)
            recievers.remove(reciever)
            app.logger.info(user + " ===> " + reciever)
            random_uuid = uuid.uuid4().hex
            relation = {
                "name": user,
                "random": hashlib.sha256(random_uuid.encode('utf-8')).hexdigest(),
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
        if not os.path.exists(game_data_folder):
            os.makedirs(game_data_folder)
        game_file_path = game_data_folder / str(game_id + ".json")
        with open(game_file_path, "w") as game_file:
            json.dump(game, game_file, sort_keys = True, indent = 4)

        user_request_urls = {}
        for relation in relations:
            user_request_urls[relation["name"]] = str(host_url) + str(game_id) + "/" + relation["random"]
        urls = {
            "game_id": game_id,
            "urls": user_request_urls
        }
        return urls, 201
      
class Default(Resource):
    def get(self):
        return "WichtelMat is running see documentation", 200


def output_html(text, code, headers=None):
    resp = Response(text, mimetype='text/html', headers=headers)
    resp.status_code = code
    return resp

api.add_resource(User, "/<string:game_id>/<string:random>")
api.add_resource(Create, "/create")
api.add_resource(Default, "/")

if __name__ == "__main__":
    app.run()
