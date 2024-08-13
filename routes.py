from flask import request, jsonify
from . import app, db
from .models import Plant
from datetime import datetime


@app.route("/plants", methods=["POST"])
def add_plant():
    data = request.get_json()
    purchase_date = datetime.strptime(data["purchase_date"], "%Y-%m-%d").date()
    new_plant = Plant(
        name=data["name"],
        purchase_date=purchase_date,
        light_conditions=data["light_conditions"],
        watering_frequency=data["watering_frequency"],
        fertilizing_frequency=data["fertilizing_frequency"],
        notes=data["notes"],
        user_id=data["user_id"],
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify({"message": "Plant added successfully!"}), 201


@app.route("/plants", methods=["GET"])
def get_plants():
    user_id = request.args.get("user_id")
    plants = Plant.query.filter_by(user_id=user_id).all()
    return jsonify([plant.to_dict() for plant in plants]), 200


@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200


@app.route("/plants/<int:id>", methods=["PUT"])
def update_plant(id):
    data = request.get_json()
    plant = Plant.query.get_or_404(id)
    if plant.user_id != data["user_id"]:
        return jsonify({"message": "Unauthorized"}), 403
    plant.name = data.get("name", plant.name)
    plant.purchase_date = data.get("purchase_date", plant.purchase_date)
    plant.light_conditions = data.get("light_conditions", plant.light_conditions)
    plant.watering_frequency = data.get("watering_frequency", plant.watering_frequency)
    plant.fertilizing_frequency = data.get(
        "fertilizing_frequency", plant.fertilizing_frequency
    )
    plant.notes = data.get("notes", plant.notes)
    db.session.commit()
    return jsonify({"message": "Plant updated successfully!"}), 200


@app.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()
    return jsonify({"message": "Plant deleted successfully!"}), 200
