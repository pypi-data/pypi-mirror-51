from setuptools import setup, find_packages

import version


def readme():
    with open('README.md', 'r', encoding='utf8') as f:
        return f.read()


setup(
    name='lightweight',
    version=version.__version__,
    py_modules=['lightweight'],
    packages=find_packages(exclude=("tests*",)),
    author='mdrachuk',
    author_email='misha@drach.uk',
    description="Static site generator i actually can use.",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/mdrachuk/lightweight",
    license="Unlicense",
    keywords="dataclasses json serialization",
    python_requires=">=3.7",
    project_urls={
        'Pipelines': 'https://dev.azure.com/misha-drachuk/lightweight',
        'Source': 'https://github.com/mdrachuk/lightweight/',
        'Issues': 'https://github.com/mdrachuk/lightweight/issues',
    },
    extras_require={
        "dev": ["pytest", "mypy"]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
)
