from starlette.config import Config

config = {}
_config = Config('.env')

config['DEBUG'] = _config('DEBUG', cast=bool, default=False)
config['DB_HOST'] = _config('DB_HOST', cast=str)
config['DB_NAME'] = _config('DB_NAME', cast=str)
config['REDIS_HOST'] = _config('REDIS_HOST', cast=str)
config['SECRET_KEY'] = _config('SECRET_KEY', cast=str)
