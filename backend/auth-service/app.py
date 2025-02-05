from flask import Flask
from routes import routes_bp
from models import Base, engine

app = Flask(__name__)


def init_db():
    Base.metadata.create_all(bind=engine)

init_db()


app.register_blueprint(routes_bp)


#@app.route('/')
#def hello():
#    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
