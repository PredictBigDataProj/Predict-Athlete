# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .league import league_views
from .drills import drills_views
from .favourites import favourites_views
from .camera import camera_views


views = [user_views, index_views, auth_views, league_views, drills_views, favourites_views, camera_views] 
# blueprints must be added to this list