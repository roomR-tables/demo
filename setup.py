from setuptools import setup

setup(
    name='demo',
    version='1.0.0',
    install_requires=[
        'paho-mqtt',
        'RPi.GPIO'
    ],
    entry_points="""
         [paste.app_factory]
         """,
    url='',
    license='',
    author='Stephen Goedhart',
    author_email='sdg25@hotmail.com',
    description=''
)
