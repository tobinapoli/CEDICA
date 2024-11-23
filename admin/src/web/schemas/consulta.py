from marshmallow import Schema, fields

class ConsultaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombrecompleto = fields.Str(required=True)
    correo = fields.Str(required=True)
    mensaje = fields.Str(required=True)
    estado = fields.Str(dump_only=True)
    comentario_interno = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    closed_at = fields.DateTime(dump_only=True)
    recaptchaToken = fields.String(required=True)

consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)