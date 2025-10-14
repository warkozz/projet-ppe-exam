import bcrypt
import pymysql

# Connexion à la base MySQL
conn = pymysql.connect(host='localhost', user='root', password='root', database='foot5')
cursor = conn.cursor()

# Générer les nouveaux hash
admin_hash = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
rayane_hash = bcrypt.hashpw('rayane'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Mettre à jour admin
cursor.execute("UPDATE users SET password_hash=%s, email='admin@local', is_admin=1 WHERE username='admin'", (admin_hash,))

# Remplacer alice par rayane
cursor.execute("UPDATE users SET username='rayane', password_hash=%s, email='rayane@local', is_admin=0 WHERE username='alice'", (rayane_hash,))

conn.commit()
cursor.close()
conn.close()
print('Utilisateurs mis à jour : admin/admin et rayane/rayane')
