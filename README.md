# Jacaranda API Flask


### Running the application
1. Clone this repository `git clone https://github.com/sylviawanjiku/Jacaranda.git`
2. Navigate to the project directory `cd Jacaranda` 
3. Create the virtual environment `python3 -m venv venv`
4. Activate the virtual environment `source venv/bin/activate` and get the environment variables `source .env`
5. Install dependencies needed for the project to run `$ pip install -r requirements.txt`
6. Run the application `python3 main.py`
7. To run the tests `pytest`
8. To the load the data make a get request to `http://127.0.0.1:5000/load-data`

### Sample env
export DB_HOST='host'
export DB_USERNAME='username'
export DB_PASSWORD=''
export DB_NAME='database'
export FLASK_ENV='development'

### Endpoints
1. post-message `http://127.0.0.1:5000/message`
2. get-messages `http://127.0.0.1:5000/message`
3. get-single-message `http://127.0.0.1:5000/message/<int:message_id>`
4. patch-single-message `http://127.0.0.1:5000/message/<int:message_id>`
5. post-ticket `http://127.0.0.1:5000/ticket`
6. get-tickets `http://127.0.0.1:5000/ticket`
7. get-single-ticket `http://127.0.0.1:5000/ticket/<int:ticket_id>`
8. patch-single-ticket `http://127.0.0.1:5000/ticket/<int:ticket_id>`
9. load-data `http://127.0.0.1:5000/load-data`

### Sample ticket response
<img width="785" alt="Screenshot 2021-09-20 at 23 33 28" src="https://user-images.githubusercontent.com/28457081/134071927-547de402-9df0-4937-bd8e-1f5b06ec818d.png">
