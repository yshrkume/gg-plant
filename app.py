from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
from flask_restful import Api
import os
from models import db
from resources.plant import PlantResource, PlantListResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///plants.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
# migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(PlantListResource, "/plants")
api.add_resource(PlantResource, "/plants/<int:plant_id>")

if __name__ == "__main__":
    app.run(debug=True)
