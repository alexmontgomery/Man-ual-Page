from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from waitress import serve

import pandas as pd
import os
from sqlalchemy import create_engine, text, inspect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'car_data', 'parsed_data.csv')

app = Flask(__name__)
api = Api(app)
CORS(app)

# sqlalchemy engine obj
engine = create_engine('sqlite:///manualpage.db', echo=True)

# check if data table alread exists
inspector = inspect(engine)
if 'Manuals_Data' not in inspector.get_table_names():
    # read .csv file into pandas df
    df = pd.read_csv(csv_path)
    # create Manuals_Data sql table from pandas df
    df.to_sql('Manuals_Data', engine, index=False)

# Get all makes/models from a year
class YearToSearch(Resource):

    # GET request
    def get(self, year):
        # sql query to select all rows with specified year
        sql = text('SELECT * FROM Manuals_Data WHERE year = :y')    
        params = {'y': year}
        # returns a connection obj; with/as is context manager
        with engine.connect() as conn:
            result = conn.execute(sql, params)
            # mappings() converts CursorResult into mapping-like obj --> then convert those rows to Python dicts
            cars = [dict(row) for row in result.mappings()]     
        return jsonify(cars)



api.add_resource(YearToSearch, '/api/search/<int:year>')

if __name__ == '__main__':
    # app.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000)