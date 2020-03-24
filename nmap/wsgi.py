from django.core.wsgi import get_wsgi_application
import dotenv
import os
from pathlib2 import Path

d = Path(__file__).resolve().parents[1]
dot_env = os.path.join(str(d), '.env')
if os.path.exists(dot_env):
    dotenv.read_dotenv(dot_env)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nmap.settings")
application = get_wsgi_application()
