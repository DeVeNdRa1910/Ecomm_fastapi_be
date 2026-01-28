from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto', bcrypt__default_rounds=12)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)

 