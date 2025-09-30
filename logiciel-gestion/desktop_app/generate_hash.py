import bcrypt

print('admin:', bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
print('rayane:', bcrypt.hashpw('rayane'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
