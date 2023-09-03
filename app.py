# Importing the necessary modules and libraries
import sys
import logging
from flask import Flask
from flask_cors import CORS
from src.routes.reorderRoutes import reorderBlueprint


def create_app():
    # Allow CORS for all origins
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Set up logging
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    # Registering the blueprint
    app.register_blueprint(reorderBlueprint, url_prefix='/reorder')
    return app


# Creating the app
app = create_app()


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=3000, debug=True)
