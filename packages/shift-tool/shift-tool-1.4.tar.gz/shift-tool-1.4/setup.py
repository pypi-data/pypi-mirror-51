import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='shift-tool',
    version='1.4',
    packages=setuptools.find_packages(),
    description='Keyed text encoding',
    url='https://github.com/Ewpratten/shift',
    author='Evan Pratten',
    author_email='ewpratten@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ),
    entry_points={
        'console_scripts': [
            'shift2 = shift.__main__:main'
        ]
    })
