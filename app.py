from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class WifiSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    qualidade = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(250), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    wifi_spots = WifiSpot.query.all()
    return render_template('index.html', wifi_spots=wifi_spots)

@app.route('/get_wifi')
def get_wifi():
    wifi_spots = WifiSpot.query.all()
    result = [
        [spot.latitude, spot.longitude, spot.senha, spot.qualidade, spot.image_url]
        for spot in wifi_spots
    ]
    return jsonify(result)

@app.route('/contact_admin')
def contact_admin():
    whatsapp_url = "https://api.whatsapp.com/send?phone=5581983170988&text=Quero%20adicionar%20mais%20redes"
    return redirect(whatsapp_url)

def init_db():
    db.create_all()
    if WifiSpot.query.count() == 0:
        wifi_points = [
            # Recife
            ("Praça do Derby", "GratisWiFi", "Alta", "https://example.com/image1.jpg", -8.048, -34.877),
            ("Parque Dona Lindu", "LinduPark123", "Média", "https://example.com/image2.jpg", -8.037, -34.904),
            ("Shopping Recife", "ShoppingWiFi", "Alta", "https://example.com/image3.jpg", -8.065, -34.918),
            ("Biblioteca Pública do Estado", "Biblioteca123", "Alta", "https://example.com/image4.jpg", -8.049, -34.877),
            ("Praça do Arsenal", "ArsenalWiFi", "Alta", "https://example.com/image5.jpg", -8.053, -34.867),
            ("Centro Cultural J. B. Scalzo", "CCJS123", "Boa", "https://example.com/image11.jpg", -8.061, -34.881),
            ("Hospital das Clínicas", "HospClinicas", "Alta", "https://example.com/image12.jpg", -8.046, -34.873),
            # Jaboatão dos Guararapes (com os pontos problemáticos removidos)
            ("Universidade Federal de Pernambuco (UFPE)", "UFPEWiFi", "Alta", "https://example.com/image9.jpg", -8.120, -34.894),
            ("Teatro Guararapes", "Teatro123", "Média", "https://example.com/image13.jpg", -8.129, -34.903),
            ("Catedral de Jaboatão", "CatedralJaboatao", "Alta", "https://example.com/image14.jpg", -8.130, -34.901),
            ("-8.112305", "-34.944244", "senha789", "Boa", "https://example.com/jaboatao1.jpg"),
            ("-8.123455", "-34.920912", "senha101", "Excelente", "https://example.com/jaboatao2.jpg"),
            ("-8.145678", "-34.912345", "senha202", "Boa", "https://example.com/jaboatao3.jpg"),
            ("-8.135325", "-34.945231", "wifi777", "Média", "https://example.com/jaboatao4.jpg"),
            ("-8.125932", "-34.953478", "wifi888", "Boa", "https://example.com/jaboatao5.jpg"),
            ("-8.113893", "-34.935628", "wifi999", "Excelente", "https://example.com/jaboatao6.jpg"),
        ]
        db.session.bulk_insert_mappings(WifiSpot, [
            {"localizacao": loc, "senha": senha, "qualidade": qual, "image_url": img, "latitude": lat, "longitude": lng}
            for loc, senha, qual, img, lat, lng in wifi_points
        ])
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
