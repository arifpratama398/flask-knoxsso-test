import jwt

token = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhcmlmIiwiaXNzIjoiS05PWFNTTyIsImV4cCI6MTY3NDkyNzU5Mywia25veC5pZCI6IjFiNjE4ODNmLWM1Y2UtNGMyNi1hOTU2LTU3NDk2NWYxYWZiMiJ9.U8B32q-fmdVKNcE1W4vPAZG_waEMS2RcpFP9qA5imLW6FcagXqbQK3Pe1J7oEp7SnsOPFs4Nw7ZhVe8mSml9hfgGsN6YAwyYz_8grmWQmmZWUlkWt8XDqeoynOqLtG1CaVkzgTJ9x3p7Lu7RHJg6QLCQ6ugDQ_3QHmsN1276PdGMVc_iLj52bmqKK3PMCcx1renkca3smwjUr5sJX_uNKuFVjq00ajBavRV3wYPsHl5irpVgvxaoGZu2uBfFlm3xprPsI8fvG2CUJrRMZkIPm_d3SJM8wEzTBAVXN7bCbS7NZbj3wtb1kymE2wPOkO6ayZHxktqLCFjKnljc0WbRRQ'

public_key = open('pub.key','rb').read()

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

public_key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )

payload = jwt.decode(token, public_key, algorithms=["RS256"])
print(payload)

