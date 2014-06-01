from setuptools import setup


entry_points = {
    'console_scripts': [
        'airead_manager = aireadManager.main:main',
    ],
}


setup(
    name='aireadManager',
    version='0.0.1',
    description='airead manager',
    author='Airead Fan',
    author_email='fgh1987168@gmail.com',
    url='none',
    packages=['aireadManager'],
    entry_points=entry_points,
    install_requires=[
        'flask',
        'mysql-python',
        'flask-sqlalchemy',
    ],
)
