from setuptools import find_packages, setup

setup(
    name='pycipapi',
    version='0.7.0',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/genomicsengland/pycipapi',
    license='',
    author='antonior,priesgo',
    author_email='antonio.rueda-martin@genomicsengland.co.uk',
    description='',
    install_requires=[
        'requests',
        'GelReportModels>=7.3'
    ]
)
