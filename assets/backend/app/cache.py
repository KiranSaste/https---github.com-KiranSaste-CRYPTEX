from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import os

# Check if we're in development mode
is_development = os.environ.get('FLASK_ENV', 'development') == 'development'

# Redis client - only try to connect if not in development mode
try:
    # Redis configuration
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    ) if not is_development else None

    # Test connection
    if not is_development:
        redis_client.ping()
    
    # Cache configuration with Redis
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes default cache timeout
    }
    
    # Rate limiter configuration with Redis
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="redis://localhost:6379"
    )
    
except (redis.exceptions.ConnectionError, redis.exceptions.RedisError):
    # Fallback to simple cache for development
    print("Redis connection failed. Using simple cache for development.")
    
    # Simple cache configuration
    cache_config = {
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    }
    
    # In-memory limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

# Initialize cache with the appropriate config
cache = Cache(config=cache_config) 