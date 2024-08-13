from flask import request
from flask_restful import Resource, reqparse
from app import db
from models import Plant
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument("name", required=True, help="Name cannot be blank!")
parser.add_argument(
    "purchase_date", required=True, help="Purchase date cannot be blank!"
)
parser.add_argument("light_conditions", required=False)
parser.add_argument("watering_frequency", required=False)
parser.add_argument("fertilizing_frequency", required=False)
parser.add_argument("notes", required=False)
parser.add_argument("user_id", type=int, required=True, help="User ID cannot be blank!")


class PlantResource(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return {
            "id": plant.id,
            "name": plant.name,
            "purchase_date": plant.purchase_date.strftime("%Y-%m-%d"),
            "light_conditions": plant.light_conditions,
            "watering_frequency": plant.watering_frequency,
            "fertilizing_frequency": plant.fertilizing_frequency,
            "notes": plant.notes,
            "user_id": plant.user_id,
        }

    def put(self, plant_id):
        args = parser.parse_args()
        plant = Plant.query.get_or_404(plant_id)
        plant.name = args["name"]
        plant.purchase_date = datetime.strptime(args["purchase_date"], "%Y-%m-%d")
        plant.light_conditions = args.get("light_conditions")
        plant.watering_frequency = args.get("watering_frequency")
        plant.fertilizing_frequency = args.get("fertilizing_frequency")
        plant.notes = args.get("notes")
        plant.user_id = args["user_id"]

        db.session.commit()
        return {"message": "Plant updated successfully"}, 200

    def delete(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        db.session.delete(plant)
        db.session.commit()
        return {"message": "Plant deleted successfully"}, 200


class PlantListResource(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return {"message": "User ID is required"}, 400
        query = request.args.get("name", "")
        if query:
            plants = Plant.query.filter(
                Plant.user_id == user_id, Plant.name.ilike(f"%{query}%")
            ).all()
        else:
            plants = Plant.query.filter_by(user_id=user_id).all()
        if not plants:
            return {"message": "No plants found for this user"}, 404
        return [
            {
                "id": plant.id,
                "name": plant.name,
                "user_id": plant.user_id,
                "watering_frequency": plant.watering_frequency,
                "fertilizing_frequency": plant.fertilizing_frequency,
                "purchase_date": plant.purchase_date.strftime("%Y-%m-%d"),
            }
            for plant in plants
        ]

    def post(self):
        args = parser.parse_args()
        plant = Plant(
            name=args["name"],
            purchase_date=datetime.strptime(args["purchase_date"], "%Y-%m-%d"),
            light_conditions=args.get("light_conditions"),
            watering_frequency=args.get("watering_frequency"),
            fertilizing_frequency=args.get("fertilizing_frequency"),
            notes=args.get("notes"),
            user_id=args["user_id"],
        )
        db.session.add(plant)
        db.session.commit()
        return {"message": "Plant created successfully", "plant_id": plant.id}, 201
