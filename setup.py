from setuptools import setup, find_packages

setup(
    name="coarnotifypy",
    version="1.0.0.1",  # Version 1 of the library for the 1.0.0 spec
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    urls=["https://coar-notify.net/", "http://cottagelabs.com/"],
    author="Cottage Labs",
    author_email="richard@cottagelabs.com",
    description="COAR Notify Common Library",
    license="Apache2",
    classifiers=[],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-autoapi'
        ],
        'test': [
            "Flask>3.0.0"
        ],
    }
)
