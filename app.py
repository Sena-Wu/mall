from flask_script import Manager
from app.utils.create_accounts import create_synthetic_data
from app import create_app

if __name__ == '__main__':
    app = create_app()

    app.app_context().push()
    manager = Manager(app=app)
    manager.add_command('create_synthetic_data', create_synthetic_data())

    manager.run()
