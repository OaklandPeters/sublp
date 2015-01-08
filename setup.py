from setuptools import setup

setup(
    name='sublp',
    version=open('VERSION').read().strip(),
    author='Oakland John Peters',
    author_email='oakland.peters@gmail.com',
    description=(
        'Convenience Linux/Mac command-line function for opening '
        'SublimeText projects.'
    ),
    long_description=open('README.rst').read(),
    url='https://github.com/OaklandPeters/sublp',
    license='MIT',
    packages=['sublp'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors',
        'Intended Audience :: Developers',
    ]
)
