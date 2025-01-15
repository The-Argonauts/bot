# Overview
This project facilitates seamless interaction between businesses and users for beta testing purposes. Users can register, log in, and view and engage in test plans. Businesses can register, login and create test plans with descriptions to attract test users. The matching process is enhanced using Gemini API which ensures the test user understand what the test plan is and if it aligns with its goal. Recieving feedback from users and giving reward based on the feedbacks, provide invaluable insights to refine products before their official release. Our platform bridges the gap between development and deployment, enhancing product quality and user satisfaction.

# Architecture 
![Architecture](https://github.com/user-attachments/assets/0009261a-9710-4f1f-a8bd-e4eff827ee83)

# How to use the bot
![IMG_7882](https://github.com/user-attachments/assets/ea1b1552-4fe6-427d-882f-bc2c07dfacaf)



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
