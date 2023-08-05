import picoweb
from . import models


class DBApp(picoweb.WebApp):

    def init(self):
        models.db.connect()
        models.Note.create_table(True)
        super().init()

app = DBApp(__name__)
