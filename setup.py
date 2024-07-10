from setuptools import setup, find_packages

setup(
    name="coarnotify",
    version="0.0.1",
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
        'docs': [],
        'test': [
            "Flask>3.0.0"
        ],
    },
    entry_points={
        "coarnotify": [
            "announce_endorsement = coarnotify.models.announce_endorsement:AnnounceEndorsement",
        ]
    }
)
