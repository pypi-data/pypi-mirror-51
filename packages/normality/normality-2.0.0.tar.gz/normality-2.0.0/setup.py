from setuptools import setup, find_packages


setup(
    name='normality',
    version='2.0.0',
    description="Micro-library to normalize text strings",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='text unicode normalization slugs',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/normality',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'six >= 1.11.0',
        'banal >= 0.4.1',
        'text-unidecode',
        'chardet'
    ],
    extras_require={
        'icu': [
            'pyicu >= 1.9.3',
        ],
    },
    test_suite='test',
    entry_points={
    }
)
