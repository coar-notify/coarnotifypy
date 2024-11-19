from setuptools import setup, find_packages

setup(
    name="coarnotify",
    version="1.0.0.1",  # Version 1 of the library for the 1.0.0 spec
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    url="http://cottagelabs.com/",
    author="Cottage Labs",
    author_email="richard@cottagelabs.com",
    description="COAR Notify Common Library",
    license="Apache2",
    classifiers=[],
    extras_require={
        'docs': [
            'sphinx'
        ],
        'test': [
            "Flask>3.0.0"
        ],
    }
)
