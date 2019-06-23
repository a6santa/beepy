from setuptools import setup, find_packages

setup(
    name='beepy',
    version='0.1.1',
    url='https://github.com/dicoinfo26/beepy',
    author='dicoinfo26',
    author_email='a6santa@outlook.com',
    setup_requires=['easypkg'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['etl']
)