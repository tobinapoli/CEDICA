
from src.core.database import db;




class SituacionPrevisional(db.Model):
    """
    Modelo que representa la situación previsional de un alumno en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True,)
    obra_social = db.Column(db.String(50), nullable=False)  
    numero_afiliado = db.Column(db.String(50), nullable=True)  
    posee_curatela = db.Column(db.Boolean, nullable=False, default=False)  
    observaciones = db.Column(db.Text, nullable=True)  
    jinetes_amazonas = db.relationship('JineteAmazona', back_populates='situacion_previsional', lazy=True)



    def __repr__(self):
        """
        Devuelve una representación en cadena de la situación previsional.

        :return: Una cadena que representa la situación previsional, incluyendo su ID, obra social, número de afiliado y curatela.
        """
        return f'<SituacionPrevisional #{self.id} obra_social="{self.obra_social}" numero_afiliado="{self.numero_afiliado}" posee_curatela={self.posee_curatela}>'

    @classmethod
    def create_situacion_previsional(cls, obra_social, numero_afiliado, posee_curatela, observaciones):
        """
        Crea una nueva situación previsional en la base de datos.

        :args:
            obra_social (str): La obra social del alumno.
            numero_afiliado (str): El número de afiliado a la obra social.
            posee_curatela (bool): Indica si el alumno posee curatela (True/False).
            observaciones (str): Observaciones adicionales sobre la situación previsional.
        
        :return: La nueva situación previsional creada.
        
        :raises ValueError: Si ya existe un registro con la misma obra social y número de afiliado.
        """
            
        if cls.afiliado_existe(obra_social,numero_afiliado) is not None:
            raise ValueError("Ya se encuentra registrada la obra social")
        nueva_situacion = cls(
            obra_social=obra_social,
            numero_afiliado=numero_afiliado,
            posee_curatela=posee_curatela,
            observaciones=observaciones
        )

        db.session.add(nueva_situacion)
        db.session.commit()
        return nueva_situacion
        
    def update_situacion_previsional(cls, id, obra_social, numero_afiliado, posee_curatela, observaciones):
        """
        Actualiza una situación previsional existente.

        :args:
            id (int): El ID de la situación previsional a actualizar.
            obra_social (str): La nueva obra social del alumno.
            numero_afiliado (str): El nuevo número de afiliado a la obra social.
            posee_curatela (bool): Indica si el alumno posee curatela (True/False).
            observaciones (str): Nuevas observaciones adicionales sobre la situación previsional.

        :return: La situación previsional actualizada.

        :raises ValueError: Si ya existe un registro con el mismo número de afiliado para la obra social especificada,
                            o si la situación previsional con el ID especificado no se encuentra.
        """
        situacion_existente = cls.afiliado_existe(obra_social,numero_afiliado)


        if situacion_existente and situacion_existente.id != id:
            raise ValueError(f"El número de afiliado '{numero_afiliado}' ya está asociado a la obra social '{obra_social}' en otro registro.")


        situacion_previsional = cls.query.get(id)
        if not situacion_previsional:
            raise ValueError(f"Situación previsional con ID {id} no encontrada.")

        situacion_previsional.obra_social = obra_social or situacion_previsional.obra_social
        situacion_previsional.numero_afiliado = numero_afiliado or situacion_previsional.numero_afiliado
        situacion_previsional.posee_curatela = posee_curatela or situacion_previsional.posee_curatela
        situacion_previsional.observaciones = observaciones or situacion_previsional.observaciones

        # Guardar los cambios
        db.session.commit()

        return situacion_previsional
    
    @classmethod
    def afiliado_existe(cls,obra_social, numero_afiliado):
        """
        Verifica si el número de afiliado ya existe para una obra social dada.

        :args:
            obra_social (str): La obra social a verificar.
            numero_afiliado (str): El número de afiliado a verificar.

        :return: El afiliado si existe, o None si no.
        """
        afiliado_existe = SituacionPrevisional.query.filter_by(
            obra_social=obra_social,
            numero_afiliado=numero_afiliado
        ).first()
        return afiliado_existe

    @classmethod
    def get_situacion_previsional(cls, id):
        """
        Obtiene una situación previsional por su ID.

        :args:
            id (int): El ID de la situación previsional a buscar.

        :return: La situación previsional correspondiente al ID.

        :raises ValueError: Si no se encuentra la situación previsional con el ID especificado.
        """
        # Buscar situación previsional por ID
        situacion_previsional = cls.query.get(id)
        
        if not situacion_previsional:
            raise ValueError(f"Situación previsional con ID {id} no encontrada.")
        

        return situacion_previsional

    @classmethod
    def delete_situacion_previsional(cls, id):
        """
        Elimina una situación previsional existente.

        :args:
            id (int): El ID de la situación previsional a eliminar.

        :return: True si se eliminó la situación previsional, False si no se encontró.

        :raises Exception: Si ocurre un error al eliminar la situación previsional.
        """
        situacion_previsional = cls.query.get(id)
        if situacion_previsional:
            db.session.delete(situacion_previsional)
            db.session.commit()
            return True  
        return False  
