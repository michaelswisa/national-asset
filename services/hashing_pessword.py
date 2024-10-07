import bcrypt

def save_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def check_password_hash(input_password, hashed_password):
  return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

