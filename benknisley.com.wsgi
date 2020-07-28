import sys

sys.path.append('/var/www/benknisley.com/')
activate_this = '/var/www/benknisley.com/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from controller import app as application
