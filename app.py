from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modello per il Pokémon
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    type_1 = db.Column(db.String(50), nullable=False)
    type_2 = db.Column(db.String(50))
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<Pokemon {self.name}>'

# Pagina principale che mostra tutti i Pokémon
@app.route('/')
def index():
    pokemons = Pokemon.query.all()
    return render_template('index.html', pokemons=pokemons)

# Funzione per creare il database e aggiungere alcuni Pokémon di esempio
@app.before_first_request
def create_tables():
    db.create_all()
    if Pokemon.query.count() == 0:
        # Aggiungi alcuni Pokémon di esempio se il database è vuoto
        bulbasaur = Pokemon(name="Bulbasaur", number=1, type_1="Grass", type_2="Poison", image_url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png")
        ivysaur = Pokemon(name="Ivysaur", number=2, type_1="Grass", type_2="Poison", image_url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png")
        venusaur = Pokemon(name="Venusaur", number=3, type_1="Grass", type_2="Poison", image_url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png")
        db.session.add_all([bulbasaur, ivysaur, venusaur])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
