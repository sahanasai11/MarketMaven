# Market Maven
Investing can be overwhelming, especially when you’re new to the stock market. This interactive tool aims to simplify the investment process by generating personalized portfolios through network-based strategies.

![GIF of a demo of MarketMaven](marketmaven_gif.gif)

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

- To update schemas:
    - Ensure you're in virtual environment
    - Go to MarketMaven directory
    - `flask db migrate -m <message>`
    - `flask db upgrade`

- The adjacency list CSV should be uploaded already, but if not, run the load_adj_matrix file. 
    Note, the db needs to be loaded in order to populate the list csv. 
