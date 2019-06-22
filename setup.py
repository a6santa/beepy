from setuptools import setup, find_packages

setup(
    name='beepy',
    version='0.1',
    setup_requires=['easypkg'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['beepy']
)