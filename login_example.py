from flask import Flask, render_template, url_for,request,session,redirect
from flask_pymongo import PyMongo

#Para codificar las contraseñas
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'prueba'
app.config['MONGO_URI'] = 'mongodb+srv://jessi:123@clusterprueba.ewjtlgy.mongodb.net/prueba?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'FUISTE LOGEADO EXITOSAMENTE:'  + session['username']
    
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    users = mongo.db.users
    login_user = users.find({'name' : request.form['username']})

    if login_user:
        if login_user['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'





@app.route('/register', methods=['POST', 'GET'])
def register():
    """ Se obtiene primero la BD, donde se tendra una coleccion 
        llamada 'users' para alamcenar todos los usuarios. 
        Despues se buscara el nombre de usuario junto con la contraseña
    """
    if request.method == 'POST':    
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass })
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Este username ya existe!'

    return render_template('register.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)