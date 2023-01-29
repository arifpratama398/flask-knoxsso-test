from flask import Flask, request, redirect
from functools import wraps
from cryptography.x509 import load_pem_x509_certificate

import jwt

app = Flask(__name__)

# Common configuration needed for KNOXSSO
SSO_PROVIDER_REDIRECT_URL="https://winter-03.ylabs247.com:8443/gateway/knoxsso/api/v1/websso"
SSO_PROVIDER_COOKIE_NAME="hadoop-jwt"
SSO_PUBLIC_KEY_FILE="./gateway.crt"
ORIGINAL_URL_QUERY_PARAM="originalUrl="

# Get public key from provided public certificate.
# Public key used to verify signed JWT.
def get_public_key():
    cert_str = open(SSO_PUBLIC_KEY_FILE, 'rb').read()
    cert_obj = load_pem_x509_certificate(cert_str)
    public_key = cert_obj.public_key()
    return public_key

# Get cookie e.g 'hadoop-jwt' from request or browser session
# to process authentication
def get_cookie():
    cookie = request.cookies.get(SSO_PROVIDER_COOKIE_NAME)
    # START DEBUG
    print("Token: ", cookie)
    # END DEBUG
    return cookie

# Construct login URL string from provided SSO provider URL and
# original request URL for redirect client if not authenticated.
def construct_login_url():
    delimiter = "?"
    login_url = SSO_PROVIDER_REDIRECT_URL \
            + delimiter \
            + ORIGINAL_URL_QUERY_PARAM \
            + request.url
    # START DEBUG
    print("URL: ", login_url)
    # END DEBUG
    return login_url

# Decode JWT token to get Payload in JSON format.
# Process also validate token from expiration and signed cert.
def validate_and_get_payload(token):
    public_key = get_public_key()
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    return payload

# Decorate API endpoint with KNOXSSO authentication
# Apply SAML Flow from Docs:
# https://knox.apache.org/books/knox-1-6-0/dev-guide.html#KnoxSSO+Integration
def authenticate(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        jwt_token = get_cookie()
        login_url = construct_login_url()
        if not jwt_token:
            return redirect(login_url)

        try :
            payload = validate_and_get_payload(jwt_token)
            next = f(payload, *args, **kwargs)
        except jwt.exceptions.ExpiredSignatureError as expError:
            # START DEBUG
            print("token: expired")
            # END DEBUG
            return redirect(login_url)
        except ValueError as val_err:
            # START DEBUG
            print("cert error :", val_err)
            # END DEBUG
            return redirect(login_url)
        except Exception as err:
            print(err)
            return redirect(login_url)

        return next
    return decorator

# Public endpoint
@app.route("/")
def index():
    return "Root Application Path '/'"

# Private endpoint, need to authenticate
@app.route("/internal")
@authenticate
def internal(payload):
    return payload

if __name__ == '__main__':
    app.run()
