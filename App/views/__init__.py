# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .admin import setup_admin
from .league import league_views


views = [user_views, index_views, league_views] 
# blueprints must be added to this list