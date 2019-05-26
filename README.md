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
./virtualenv/bin/python manage.py test functional_tests
#   unit tests:
./virtualenv/bin/python manage.py test lists
```

### Get it running in the web

I am using an EC2 machine as my deployment server inorder to get my site published. Got a free domain registered at [freenom.com](https://my.freenom.com/). And using a **nginx + gunicorn** setup for the deployment of the staging and live server. I will be uploading the deployment settings soon.

> you can follow the guide in `deploy_tools`


#### Using fabric CLI

This will be very specific to deployment to AWS EC2 servers. We assume that you already have the `private_key` file used to log in to your remote machine. It will be used the same way you use it for logging into EC2 instances. You have to provides the username and host address of the instance.

```bash
cd /path/to/your/local/git/repo/

source virtualenv/bin/activate

cd deploy_tools/

fab -i /path/to/private_key.pem deploy:host=username@host_address
```