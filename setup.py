from setuptools import setup


classifiers = '''\
Framework :: Django
Environment :: Web Environment
Intended Audience :: Developers
Topic :: Internet :: WWW/HTTP
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
'''

description = 'mongodb as Django sessions backend'

packages = ['mongo_sessions']


# no codecs\with for python 2.5
def long_description():
    f = open('README.rst')
    rst = f.read()
    f.close()
    return rst


setup(
    name='django-mongo-sessions',
    version='0.0.4',
    packages=packages,
    description=description,
    long_description=long_description(),
    author='hellysmile',
    author_email='hellysmile@gmail.com',
    url='https://github.com/hellysmile/django-mongo-sessions',
    zip_safe=False,
    install_requires=[
        'django >= 1.4',
        'pymongo >= 2.4.2'
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=filter(None, classifiers.split('\n')),
    keywords=[
        "django", "mongo", "sessions"
    ]
)
