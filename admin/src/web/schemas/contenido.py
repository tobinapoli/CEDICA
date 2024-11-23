from marshmallow import Schema, fields

class ContenidoSchema(Schema):
    include_fk = True
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    contenido = fields.Str(required=True)
    autor_id = fields.Int(required=True)
    autor_email = fields.Method("get_autor_email")
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    fecha_publicacion = fields.Date(dump_only=True)
    estado = fields.Str(dump_only=True)
    
    def get_autor_email(self, obj):
        return obj.autor.email if obj.autor else None 
    
contenido_schema = ContenidoSchema()
contenidos_schema = ContenidoSchema(many=True)