import bcrypt
salt = bcrypt.gensalt()
print(salt.decode("ascii"))  # Save this to your .env file
