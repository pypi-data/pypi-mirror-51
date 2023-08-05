from setuptools import setup, find_packages
import sys
import os
import time


def publish():
    """Publish to PyPi"""
    print('publishing...')
    os.system("rm -rf dist igist.egg-info build")
    os.system("python3 setup.py sdist build")
    os.system("twine upload dist/*")
    os.system("rm -rf dist igist.egg-info build")


def _auto_version(version=''):
    import time
    import json

    # read from file
    with open('igist/__version__.py', 'rb') as f:
        json_v = f.readline().decode('utf-8')
    ver = json.loads(json_v)

    if version:
        ver['version'] = list(map(int, version.split('.')))
    else:
        ver['version'][2] += 1

    ver['published time'] = time.strftime(
        '%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    with open('igist/__version__.py', 'wb') as f:
        f.write(json.dumps(ver).encode('utf-8'))

    return '.'.join(map(str, ver['version']))


if sys.argv[-1] == "-p":
    publish()
    sys.exit()

setup(
    name='igist',
    # version=_auto_version(),
    version=_auto_version('1.1.2'),
    description=('igist is a python package for Github gist'),
    long_description=open('README.rst').read(),
    author='vinct',
    author_email='vt.y@qq.com',
    maintainer='vincent',
    maintainer_email='vt.y@qq.com',
    license='MIT License',
    install_requires=[],
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vincent770/igist.git',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)

# python3 setpu.py -p
