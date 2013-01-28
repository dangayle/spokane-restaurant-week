from setuptools import setup

setup(name='Spokane Restaurant Week',
      version='1.0',
      description='OpenShift Twilio restaurant checkin svc using MongoDB',
      author='Dan Gayle',
      author_email='dangayle@gmail.com',
      url='https://github.com/dangayle/spokane-restaurant-week/',
      install_requires=['pymongo','twilio', 'bottle'],
     )
