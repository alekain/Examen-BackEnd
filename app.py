from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://FamiliaSuperman:aletron@localhost:4000/api_users'  # Actualiza credenciales
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula_identidad = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    primer_apellido = db.Column(db.String(100), nullable=False)
    segundo_apellido = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date, nullable=False)

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(**data)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado correctamente'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{'id': usuario.id, 'cedula_identidad': usuario.cedula_identidad, 'nombre': usuario.nombre, 'primer_apellido': usuario.primer_apellido, 'segundo_apellido': usuario.segundo_apellido, 'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%Y-%m-%d')} for usuario in usuarios]
    return jsonify(usuarios_json)

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    usuario_json = {'id': usuario.id, 'cedula_identidad': usuario.cedula_identidad, 'nombre': usuario.nombre, 'primer_apellido': usuario.primer_apellido, 'segundo_apellido': usuario.segundo_apellido, 'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%Y-%m-%d')}
    return jsonify(usuario_json)

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    data = request.json
    for key, value in data.items():
        setattr(usuario, key, value)
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado correctamente'})

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado correctamente'})

@app.route('/usuarios/promedio-edad', methods=['GET'])
def promedio_edad_usuarios():
    query = text('SELECT AVG(EXTRACT(YEAR FROM AGE(fecha_nacimiento))) AS promedio_edad FROM usuarios')
    result = db.session.execute(query).fetchone()
    promedio_edad = result['promedio_edad'] if result else 0
    return jsonify({'promedioEdad': promedio_edad})

@app.route('/estado', methods=['GET'])
def estado_api():
    return jsonify({
        'nameSystem': 'api-users',
        'version': '0.0.1',
        'developer': 'Alejandro Heredia Gonzales',
        'email': 'aleherediag@hotmail.com'
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
