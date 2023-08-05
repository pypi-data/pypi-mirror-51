import setuptools
from pathlib import Path

setuptools.setup(
    name="chess-board",
    version="0.2.0",
    author="Ahira Adefokun",
    author_email="justiceahira@gmail.com",
    description="A python chessboard library for representing game positions.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/ahira-justice/chess-board",
    packages=setuptools.find_packages(),
    package_dir={'chessboard': 'chessboard'},
    package_data={'chessboard': ['images/*.png']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame',
    ],
)