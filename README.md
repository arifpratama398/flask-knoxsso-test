# Running APP Development

1. Setup environment

```bash
# create virtualenv
python3.9 -m venv venv

# activate virtualenv
source venv/bin/activate

# install package
pip install -r requirements.txt
```

2. Generate Self-Signed cert

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# then fill the form
```

3. Copy Knox Gateway Certificate to this root folder with name `gateway.crt`

> Note : this is important for application jwt verification
> for this task, maybe you should contact administartor

4. Run application

```bash
./run.sh
```

