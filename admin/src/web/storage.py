from minio import Minio

class Storage:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)
    

    def init_app(self, app):
        # Inicializa el cliente de Minio y lo ajusta a la app
        minio_server = app.config["MINIO_SERVER"]  
        acces_key = app.config["MINIO_ACCESS_KEY"]  
        secret_key = app.config["MINIO_SECRET_KEY"]  
        secure = app.config.get("MINIO_SECURE", False)  

        self._client = Minio(
            minio_server, access_key=acces_key, secret_key=secret_key, secure=secure
        )


        app.storage = self

        return app
    

    @property
    def client(self):
        # Getter del cliente de Minio
        return self._client
    

    @client.setter
    def client(self, value):
        # Setter del cliente de Minio
        self._client = value

storage = Storage()