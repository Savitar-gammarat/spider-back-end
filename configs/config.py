from flask_caching import Cache
"""
THE PATH OF THE MYSQL DATABASE
"""
DB_USER = "root"
DB_PASSWORD = "991004"
DB_HOST = "47.101.196.53"
DB_PORT = "3306"
DB_SCHEMA = "news-aggregation"

"""
SECRET_KEY, something important!
"""
SECRET_KEY = "Trump-eat-chicken"

"""
SUPER_ADMIN, something important!
"""
SUPER_ADMIN = ["bigdingding"]
"""
THE PATH OF THE REDIS DATABASE
"""
cache = Cache(config={
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '101.132.161.133',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_PASSWORD': 'weekbin971122'
})