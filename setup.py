from setuptools import setup, find_packages

setup(
    name="coarnotify",
    version="1.0.1.3",  # Version 3 of the library for the 1.0.1 spec
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    urls=["https://coar-notify.net/", "http://cottagelabs.com/"],
    author="Cottage Labs",
    author_email="richard@cottagelabs.com",
    description="COAR Notify Common Library",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
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
