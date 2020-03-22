from django.core.wsgi import get_wsgi_application
import dotenv
import os

dot_env = os.path.join(os.getcwd(), '.env')
if os.path.exists(dot_env):
    dotenv.read_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nmap.settings")
application = get_wsgi_application()
