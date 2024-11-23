from flask import Blueprint
from src.core import board
from src.web.schemas.contenido import contenidos_schema, contenido_schema
from flask import request

bp = Blueprint('contenido_api', __name__, url_prefix='/api/contenido')

@bp.get('/')
def index():
    """
    Recupera una lista paginada de contenidos publicados.

    Este endpoint obtiene los contenidos publicados, con paginación y filtrados por estado 'publicado'.
    Los parámetros de la consulta `page` y `per_page` controlan la paginación de los resultados.

    - `page`: Número de página (por defecto es 1).
    - `per_page`: Número de elementos por página (por defecto es 8).

    El método devuelve los contenidos serializados en formato JSON, junto con la información de la paginación.

    Respuesta:
    - `data`: Lista de contenidos serializados.
    - `totalPages`: Número total de páginas disponibles.
    - `page`: Página actual.
    - `per_page`: Número de elementos por página.

    Ejemplo de respuesta:
    {
        "data": [...],
        "totalPages": 5,
        "page": 1,
        "per_page": 8
    }
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    filters = {
        "estado": "publicado"
    }
    
    # Llamar al método de listado con filtros y parámetros
    contenido_paginated = board.Contenido.list_contenido(page, per_page, filters)
    
    # Serializar datos
    data = contenidos_schema.dump(contenido_paginated.items)
    response = {
        "data": data,
        "totalPages": contenido_paginated.pages,
        "page": contenido_paginated.page,
        "per_page": contenido_paginated.per_page
    }, 200
    return response
    
    
