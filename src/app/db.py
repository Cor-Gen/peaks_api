import databases
import ormar
import sqlalchemy

from .config import settings


# database object for ORM model.
database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    """
        Required to pass database to ormar models.
    """
    metadata = metadata
    database = database


class Peak(ormar.Model):
    """
        ORM model for peaks routines.
        Args:
            id  : primary key (int).
            name: moutain's peak name (str).
            alt : peak altitude in meters (int).
            lat : peak latitude in decimal degrees (float).
            lon : peak longitude in decimal degrees (float).
    """
    class Meta(BaseMeta):
        """
           Subclass of BaseMeta, to pass database to Peak model.
        """
        tablename = "peaks"

    id  : int = ormar.Integer(primary_key = True)
    name: str = ormar.String(max_length = 128, unique = True, nullable = False)
    alt : int = ormar.Integer(minimum = 0, nullable = True)                     # optional only for update (cf routines)
    lat : float = ormar.Float(minimum = -90, maximum = 90, nullable = True)     # optional only for update (cf routines)
    lon : float = ormar.Float(minimum = -180, maximum = 180, nullable = True)   # optional only for update (cf routines)


# sqlalchemy engine for database
engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)