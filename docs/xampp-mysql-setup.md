
# Using XAMPP MySQL with Pikestia

1. Start XAMPP Control Panel -> Start MySQL
2. Create DB: phpmyadmin -> new -> pikestia (utf8mb4_general_ci)
3. Install driver: pip install mysqlclient (or PyMySQL)
4. In pikestia/settings.py replace DATABASES with:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pikestia',
        'USER': 'root',
        'PASSWORD': '',  # default XAMPP root has no password
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

5. python manage.py migrate
6. Keep using python manage.py runserver (don't use Apache yet)
