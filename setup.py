"""Setup script for the restaurant-finder package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="restaurant-deepresearch",
    version="0.1.0",
    author="YANG LI",
    author_email="liyangauthority@gmail.com",
    description="A multi-agent system for restaurant recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YangLi-leo/restaurant-deepresearch",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "camel-ai",
        "python-dotenv",
        "colorama",
        "numpy",  # Added missing dependency
        "Pillow", # Added missing dependency for PIL
        "PyYAML", # Added missing dependency for yaml
        "requests_oauthlib", # Added missing dependency
        "pandas", # Added missing dependency
    ],
)
