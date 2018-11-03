from setuptools import find_packages, setup


with open('README.md') as file:
    long_description = file.read()

setup(
    name='py2js',
    version='0.1.0',
    description="""
Experiment to see if it's possible to write a Python to JS transpiler.
    """.strip(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/thomasleese/py2js',
    author='Thomas Leese',
    author_email='thomas@leese.io',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['py2js = py2js.cli:main']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=['PyYaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
