import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_restful import Api
from src.container import Container
from src.config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    
    container = Container()
    
    api.add_resource(
        container.get('auth_controller'),
        '/auth',
        resource_class_args=container.get('auth_controller_args')
    )
    
    api.add_resource(
        container.get('product_controller'),
        '/products',
        '/products/<int:product_id>',
        resource_class_args=container.get('product_controller_args')
    )
    
    api.add_resource(
        container.get('category_controller'),
        '/categories',
        '/categories/<int:category_id>',
        resource_class_args=container.get('category_controller_args')
    )
    
    api.add_resource(
        container.get('favorite_controller'),
        '/favorites',
        resource_class_args=container.get('favorite_controller_args')
    )
    
    api.add_resource(
        container.get('cart_controller'),
        '/cart',
        '/cart/items',
        '/cart/items/<int:product_id>',
        '/cart/summary',
        resource_class_args=container.get('cart_controller_args')
    )
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG)