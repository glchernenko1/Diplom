import os
from src.app import create_app

env_name = os.getenv('FLASK_ENV', 'production')
app = create_app(env_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), threaded=True)
