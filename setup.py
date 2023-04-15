from setuptools import setup

setup(
    name="I2C",
    version="0.0.2",
    description="Application to enable people to communicate via eye movements using images",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/debsdebsenson/I2C",
    author="Deborah Sobiella",
    author_email="dsobiella@posteo.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["app"],
    include_package_data=True,
    install_requires=[
        "kivy"
    ],
    entry_points={"console_scripts": ["debsdebsenson=app.session.__main__:main"]},
)