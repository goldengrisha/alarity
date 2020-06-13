import os

DB_HOST = os.getenv(
    'DB_HOST', '127.0.0.1:3307')
DB_USERNAME = os.getenv(
    'DB_USERNAME', 'user')
DB_PASSWORD = os.getenv(
    'DB_PASSWORD', 'passw0rd')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/db'



