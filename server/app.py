#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.json.compact = False

migrate = Migrate(app, db)


db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantTable(Resource):
    def get(self):
        restaurants = [
            {
                "address":restaurant.address,
                "id":restaurant.id,
                "name":restaurant.name
            }
            for restaurant in Restaurant.query.all()]
        return make_response(restaurants,200)

class GetRestaurantById(Resource):
    def get(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            return make_response(restaurant.to_dict(),200)
        else:
            return make_response({"error":"Restaurant not found"},404)
        
    def delete(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            db.session.delete(restaurant)
            return '',204
        else:
            return make_response({"error":"Restaurant not found"},404)
    

class PizzaTable(Resource):
    def get(self):
        pizzas = [{
            "id":pizza.id,
            "ingredients":pizza.ingredients,
            "name":pizza.name
        } for pizza in Pizza.query.all()]
        return make_response(pizzas,200)
    

class CreateRestaurantPizza(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                price = data.get('price'),
                pizza_id = data.get('pizza_id'),
                restaurant_id = data.get("restaurant_id")
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return new_restaurant_pizza.to_dict(),201
        except :
            db.session.rollback()
            return { "errors": ["validation errors"]},400
        






api.add_resource(RestaurantTable,'/restaurants')
api.add_resource(GetRestaurantById,'/restaurants/<int:id>')
api.add_resource(PizzaTable,'/pizzas')
api.add_resource(CreateRestaurantPizza,'/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
