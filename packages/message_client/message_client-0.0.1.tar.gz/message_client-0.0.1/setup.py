from setuptools import setup, find_packages

setup(name="message_client",
      version="0.0.1",
      description="message_client",
      author="Oleg",
      author_email="test.test@test.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy']
      )
