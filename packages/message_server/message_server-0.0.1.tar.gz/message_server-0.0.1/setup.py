from setuptools import setup, find_packages

setup(name="message_server",
      version="0.0.1",
      description="message_server",
      author="Oleg",
      author_email="test.test@test.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy']
      )

