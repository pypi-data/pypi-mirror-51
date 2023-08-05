from setuptools import setup, find_packages

import coriolis

setup(
    name='coriolis',
    version=coriolis.__version__,
    packages=find_packages(),
    author="Joel Thanwerdas",
    author_email="joel.thanwerdas@gmail.com",
    description="Quick visualization python software for NetCDF files",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    include_package_data=True,
    url='http://github.com/jthanwer/coriolis',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    entry_points={
        'console_scripts': [
            'coriolis = coriolis.__main__:main',
        ],
    }
)
