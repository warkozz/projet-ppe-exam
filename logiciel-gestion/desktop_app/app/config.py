import os
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.getenv(
	'DATABASE_URL',
	# Configuration par défaut pour XAMPP (sans mot de passe)
	'mysql+pymysql://root:@localhost:3306/foot5'
)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
