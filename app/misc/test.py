from py_vapid import Vapid
vapid = Vapid()
vapid.generate_keys()
print("Private:", vapid.private_pem().decode())
print("Public:", vapid.public_key)