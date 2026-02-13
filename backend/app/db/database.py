"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import redis
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

# Base for models
Base = declarative_base()

# Lazy-loaded database connections
_engine = None
_SessionLocal = None
_mongo_client = None
_mongo_db = None
_redis_client = None


def get_engine():
    """Get or create PostgreSQL engine"""
    global _engine, _SessionLocal
    if _engine is None:
        try:
            _engine = create_engine(
                settings.postgres_url, 
                pool_pre_ping=True,
                connect_args={"connect_timeout": 10}
            )
            _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
            logger.info("PostgreSQL engine created successfully")
        except Exception as e:
            logger.warning(f"Could not connect to PostgreSQL: {e}")
            # Return None to allow app to start without DB
            return None
    return _engine


def get_db():
    """Get PostgreSQL database session"""
    engine = get_engine()
    if engine is None:
        logger.warning("PostgreSQL not available")
        return
    
    SessionLocal = _SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongo_db():
    """Get MongoDB database"""
    global _mongo_client, _mongo_db
    if _mongo_db is None:
        try:
            _mongo_client = MongoClient(
                settings.mongodb_url,
                serverSelectionTimeoutMS=10000
            )
            _mongo_db = _mongo_client[settings.MONGODB_DB]
            # Test connection
            _mongo_client.admin.command('ping')
            logger.info("MongoDB connected successfully")
        except Exception as e:
            logger.warning(f"Could not connect to MongoDB: {e}")
            return None
    return _mongo_db


def get_redis():
    """Get Redis client"""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=10,
                socket_timeout=10
            )
            # Test connection
            _redis_client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}")
            return None
    return _redis_client
