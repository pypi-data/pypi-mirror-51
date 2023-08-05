import os
from distutils.core import setup
from typing import List

from setuptools import find_packages


def find_stub_files(name: str) -> List[str]:
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


with open('README.rst', 'r') as f:
    readme = f.read()

dependencies = [
    'mypy>=0.720',
    'typing-extensions',
    'grpcio',
]

setup(
    name="grpc-stubs",
    version="1.22.2",
    description='Mypy stubs for gRPC',
    long_description=readme,
    long_description_content_type='text/x-rst',
    license='MIT',
    url="https://github.com/shabbyrobe/grpc-stubs",
    author="Blake Williams",
    author_email="code@shabbyrobe.org",
    py_modules=[],
    python_requires='>=3.6',
    install_requires=dependencies,
    packages=['grpc-stubs', *find_packages(exclude=['scripts'])],
    package_data={'grpc-stubs': find_stub_files('grpc-stubs')},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
