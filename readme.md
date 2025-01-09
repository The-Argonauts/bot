
# Install requirements
```bash
pip install -r requirements.txt
```

# How to update the database
```bash
cd configs
alembic upgrade head
```

# How to generate a new migration
```bash
cd configs
alembic revision --autogenerate -m "migration message"
```

# SetUp redis server
```bash
docker run --name redis -p 6379:6379 -d redis
```