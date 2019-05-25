# py-tdd

A very minimal application made on Django, in order to deliver a heavily tested and automatically deployed To-Do lists webapp.  

> "Always follow the Testing Goat."

### Get it running locally
```bash
git clone https://github.com/adityaprakash-bobby/py-tdd
cd py-tdd/

# setup a virtual environment
python3 -m venv virtualenv

# prep the dev server
./virtualenv/bin/pip install -r requirements.txt

# start the dev server
./virtualenv/bin/python manage.py runserver

# run tests
#   e2e test:
./virtualenv/bin/python manage.py test funtional_tests
#   unit tests:
./virtualenv/bin/python manage.py test lists
```

### Get it running in the web

I am using an EC2 machine as my deployment server inorder to get my site published. Got a free domain registered at [freenom.com](https://my.freenom.com/). And using a **nginx + gunicorn** setup for the deployment of the staging and live server. I will be uploading the deployment settings soon.

> to be completed as the project is nearing completion.