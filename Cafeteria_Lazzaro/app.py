from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/lazzaro.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MODELO DE USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    rol = db.Column(db.String(10))  # 'admin' o 'usuario'
    puntos = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# RUTAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nuevo = User(
            nombre=request.form['nombre'],
            email=request.form['email'],
            password=request.form['password'],
            rol='usuario'
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.rol != 'admin':
        return redirect(url_for('menu'))
    return render_template('admin_panel.html')

@app.route('/fidelizacion')
@login_required
def fidelizacion():
    return render_template('fidelizacion.html', puntos=current_user.puntos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
