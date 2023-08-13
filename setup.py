import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="troyalab",
    version="0.1.5",
    author="Fatih Furkan",
    author_email="furkan.troyalab@outlook.com",
    description="A library to use for Troyalab development boards for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/troyalab-fatih/BG96_RASPBERY_PI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.2',
    install_requires=["pyserial>=3.5b0", "RPi.GPIO>=0.7.0"]
)
