from flask import Blueprint, request, jsonify
import requests
from src.core.board.consulta import Consulta # Asumimos que board maneja la lógica de negocios, como el acceso a la base de datos
from src.web.schemas.consulta import consultas_schema, consulta_schema  # Importamos el esquema de las consultas
from marshmallow import ValidationError

SECRET_KEY = '6Lfy-IMqAAAAAIsobrnnDnwfu4--N8HasHaFAAwC'

# Configuración del Blueprint para la API de contacto
bp = Blueprint('contacto_api', __name__, url_prefix='/api/contacto')

def verificar_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": SECRET_KEY,
        "response": token
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get('success', False)

@bp.post('/')
def crear_consulta():
    try:
        data = request.get_json()
        recaptcha_token = data.get("recaptchaToken")
        if not recaptcha_token or not verificar_recaptcha(recaptcha_token):
            return jsonify({"message": "reCAPTCHA inválido o no verificado"}), 400
        # Validar y deserializar los datos de entrada usando el esquema de Marshmallow
        consulta_data = consulta_schema.load(data)  # Validación con Marshmallow
        print(consulta_data)

        # Crear una nueva consulta usando el modelo
        nueva_consulta = Consulta.create(
            nombrecompleto=consulta_data['nombrecompleto'],
            correo=consulta_data['correo'],
            mensaje=consulta_data['mensaje']
        )

        # Devolver la respuesta de éxito
        return jsonify({
            'message': 'Consulta creada con éxito.',
            'consulta': {
                'id': nueva_consulta.id,
                'nombre': nueva_consulta.nombrecompleto,
                'correo': nueva_consulta.correo,
                'mensaje': nueva_consulta.mensaje,
                'estado': nueva_consulta.estado,
            }
        }), 201  # HTTP 201 Created

    except ValidationError as err:
        # En caso de error de validación (por ejemplo, datos incorrectos)
        return jsonify({'message': 'Error en los datos proporcionados', 'errors': err.messages}), 400

    except Exception as e:
        # Manejo de otros errores generales
        return jsonify({'message': 'Error al crear la consulta', 'error': str(e)}), 500

@bp.get('/')
def listar_consultas():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    filters = None
    
    # Llamar al método de listado con filtros y parámetros (aquí podrías aplicar filtros como estado, fecha, etc.)
    consultas_paginated = Consulta.list_consultas(page, per_page, filters)
    
    # Serializar los datos de las consultas
    data = consultas_schema.dump(consultas_paginated.items)
    
    # Devolver los datos paginados
    return {
        "data": data,
        "total": consultas_paginated.total,
        "page": consultas_paginated.page,
        "per_page": consultas_paginated.per_page
    }, 200
