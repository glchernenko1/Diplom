class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    UPLOAD_FOLDER = 'images'
    COMPRESS_ALGORITHM = 'gzip'


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'images'
    COMPRESS_ALGORITHM = 'gzip'


class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    UPLOAD_FOLDER = 'images'
    COMPRESS_ALGORITHM = 'gzip'


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
