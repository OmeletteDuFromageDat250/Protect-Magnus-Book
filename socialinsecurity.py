# configured as the entry point of the app, simply imports app to start application, just run 'flask run' to start
from app import app

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024