# Django settings for evolve project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

GENERATION_SIZE = 100
VOTES_NEEDED = 20

ADMINS = (
    ('Josh Lee', 'josh@tengwar'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'evolve'             # Or path to database file if using sqlite3.
DATABASE_USER = 'josh'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/josh/code/evolve/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/evolve_media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o&+ount@q(zj!t)_(8bijfit-xg=egchzwp56+*zo#362x5zj9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.core.template.loaders.filesystem.load_template_source',
    'django.core.template.loaders.app_directories.load_template_source',
#     'django.core.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.sessions.SessionMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

ROOT_URLCONF = 'evolve.urls'

TEMPLATE_DIRS = (
	"/home/josh/code/evolve/templates",
)

INSTALLED_APPS = (
	'evolve.art',
	'django.contrib.admin',
)
