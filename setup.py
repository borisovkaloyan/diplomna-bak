from setuptools import setup, find_packages

# Setup package
setup(
    name="pariking-buddy-backend",   # App name
    version="1.0.3",                 # App version
    packages=find_packages(),   # App packages
    install_requires=[          # App requirements
        "fastapi",
        "sqlalchemy",
        "psycopg2-binary"
    ],
    entry_points={          # App entry point
        'console_scripts': [
            'parking-buddy = backend.__main__:backend_entrypoint',
        ],
    },
    include_package_data=True
)
