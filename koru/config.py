

class Config:
    # Configure secret key and Database uri
    SECRET_KEY = '1b13c35d94c96ea3dffe982f0000d7d4'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///koru.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'korukorukorudance'
    MAIL_PASSWORD = 'korukoru'