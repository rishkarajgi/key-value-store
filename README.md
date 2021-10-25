# Key Value store
Author: Rishabh Karajgi

Quickstart
----------

Steps:
1. Set up a virtual environment
 - ```virtualenv venv```
 - ```source venv/bin/activate```
2. Install dependencies 
 - ``pip install -r requirements.txt``
3. Run app 
 - ``uvicorn main:app --reload``
4. API docs 
 - ``http://127.0.0.1:8000/docs``
5. To run tests 
 - ``pytest test_main.py``

You can add test json data in ```test_data.json```
Make sure to modify ```test variables``` in ```test_main.py```

 Postman collection link
 ```https://www.getpostman.com/collections/221e675cebcf1fc16655```