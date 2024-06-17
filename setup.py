from setuptools import setup

setup(
    name="samrum",
    version="0.1",
    packages=['samrun'],
    install_requires=['pygame'],
    entry_points={
        "console_scripts":["samrun = samrun.__main__:main"]
    }
)