from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configura l'app Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializza il database
db = SQLAlchemy(app)

# Modello del Pokémon
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

# Rotta per la homepage
@app.route('/')
def index():
    pokemons = Pokemon.query.all()
    return render_template('index.html', pokemons=pokemons)

# Rotta per aggiungere un Pokémon
@app.route('/add', methods=['GET', 'POST'])
def add_pokemon():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        
        new_pokemon = Pokemon(name=name, type=type, description=description)
        db.session.add(new_pokemon)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')

# Avvia il server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea le tabelle nel database
    app.run(debug=True)
