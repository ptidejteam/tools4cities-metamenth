from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="metamenth",
    version="1.0.6",
    packages=find_packages(include=["metamenth", "metamenth.*"]),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
        ],
    },
    author="Peter Yefi",
    author_email="peteryefi@gmail.com",
    description="Metamodel for Energy Things (MetamEnTh) is an object-oriented metamodel designed to model the "
                "operational aspects of buildings. It focuses on the relationships and interactions between "
                "mechanical, electrical, and plumbing (MEP) entities and their connections to sensors and spatial "
                "entities such as rooms and open spaces within buildings.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ptidejteam/metamenth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="Apache License 2.0",
)
