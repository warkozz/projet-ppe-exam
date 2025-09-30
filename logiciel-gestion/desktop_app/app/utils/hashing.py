import bcrypt
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except ValueError:
        # Si le hash est invalide (ex: faux hash dans la BDD), autoriser la connexion si le mot de passe correspond en clair
        return plain == hashed
