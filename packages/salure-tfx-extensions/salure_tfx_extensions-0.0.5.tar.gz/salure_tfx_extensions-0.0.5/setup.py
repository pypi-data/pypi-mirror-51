from setuptools import setup, find_packages

setup(
    name='salure_tfx_extensions',
    version='0.0.5',
    description='TFX components, helper functions and pipeline definition, developed by Salure',
    author='Salure',
    author_email='bi@saslure.nl',
    license='Salure License',
    packages=find_packages(),
    package_data={'salure_tfx_extensions': ['proto/*.proto']},
    install_requires=[
        'tfx>=0.13.0',
        'tensorflow==1.14.0',
        'PyMySQL>=0.9.3,<10'
    ],
    zip_safe=False
)
