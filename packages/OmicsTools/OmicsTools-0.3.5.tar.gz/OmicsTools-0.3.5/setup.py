from setuptools import setup

setup(
    name='OmicsTools',
    packages=['OmicsTools'],
    package_dir={'OmicsTools': 'OmicsTools'},
    include_package_data=True,
    version='0.3.5',
    url='https://github.com/fraenkel-lab/OmicsTools',
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'],
    license='MIT',
    author='iamjli',
    author_email='iamjli@mit.edu',
    description='',
    install_requires=[
        "pandas>=0.20.1", 
        "numpy>=1.12.0",
        "networkx>=2.0",
        "mygene==3.1.0", 
        "goenrich==1.11"
    ]
)