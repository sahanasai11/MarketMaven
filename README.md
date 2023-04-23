# CS-145
Caltech CS 145

Setup:
- Create virtual environment (only need to do this step once): `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- To run application:
    - `cd MarketMaven`
    - `export FLASK_APP=webapp `
    - `flask run`
    
- To update dependencies (make sure you're not in MarketMaven directory): `pip freeze > requirements.txt`
- If you need to change port: `export FLASK_RUN_PORT=8000`
