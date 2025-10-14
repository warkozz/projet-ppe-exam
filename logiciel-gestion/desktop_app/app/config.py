import os
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.getenv(
	'DATABASE_URL',
	# Exemple MySQL : 'mysql+pymysql://user:password@localhost:3306/foot5'
	'mysql+pymysql://root:password@localhost:3306/foot5'
)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
