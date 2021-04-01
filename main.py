import os
import sys
import logging

try:
    if not os.path.isfile('./config/default_data.py'):
        os.system('cp ./config/factory_data.py ./config/default_data.py')
except Exception as e:
    print 'Error ' + str(e)

from operate import main_thread

def main():
    # Set logger
    root = logging.getLogger('App')
    root.setLevel(logging.DEBUG)
    handler = logging.FileHandler('./app.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    # run
    main_thread.call()

if __name__ == "__main__":
    main()