from flask import Blueprint

profile_blu = Blueprint("profile",__name__,url_prefix="/user")

from info.modules.profile.views import *