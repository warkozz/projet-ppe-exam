import bcrypt
import pymysql

# Connexion à la base MySQL
conn = pymysql.connect(host='localhost', user='root', password='root', database='foot5')
cursor = conn.cursor()

# Générer le hash pour admin123
superadmin_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Créer l'utilisateur superadmin
cursor.execute("""
INSERT INTO users (username, password_hash, email, role)
VALUES (%s, %s, %s, %s)
""", ('Administrateur', superadmin_hash, 'administateur@local', 'superadmin'))

conn.commit()
cursor.close()
conn.close()
print('Utilisateur superadmin Administrateur/admin123 créé !')
