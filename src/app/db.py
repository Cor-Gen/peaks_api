import databases
import ormar
import sqlalchemy

from .config import settings


database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Peak(ormar.Model):
    
    class Meta(BaseMeta):
        tablename = "peaks"

    id  : int = ormar.Integer(primary_key = True)
    name: str = ormar.String(max_length = 128, unique = True, nullable = False)
    alt : int = ormar.Integer()
    lat : float = ormar.Float(minimum = -90, maximum = 90)
    lon : float = ormar.Float(minimum = -180, maximum = 180)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)