import cloudinary
from app.core.config import settings

def init_cloudinary():
    cloudinary.config(**settings.cloudinary_config)
