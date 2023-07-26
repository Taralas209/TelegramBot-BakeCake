import os
import django
from bake_cake_bot.dispatcher import run_pooling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bake_cake.settings')
django.setup()


if __name__ == "__main__":
    run_pooling()
