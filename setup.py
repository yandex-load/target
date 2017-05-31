from setuptools import setup, find_packages

setup(
    name='target',
    version='0.0.11',
    description='a performance measurement stub',
    maintainer='Alexey Lavrenuke (load testing)',
    maintainer_email='direvius@yandex-team.ru',
    packages=find_packages(exclude=["tests", "tmp", "docs", "data"]),
    install_requires=[
        'numpy', 'watchdog',
        'tornado>=4.4.2',
    ],
    setup_requires=[
        'pytest-runner',
        'flake8',
    ],
    tests_require=['pytest', ],
    license='MPLv2',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'target = target.cmd:main',
        'tailgc = target.tail:main',
    ], }, )
