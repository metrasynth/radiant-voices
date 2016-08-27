"""
Radiant Voices aims to give you a full set of tools to
create, manipulate, and write SunVox song and synth files.
"""
from setuptools import find_packages, setup

dependencies = ['attrs', 'logutils', 'hexdump', 'pyyaml']
test_dependencies = ['py', 'pytest', 'pytest-watch']

setup(
    name='radiant-voices',
    version='0.1.0',
    url='https://github.com/metrasynth/radiant-voices',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description='Create, read, modify, and write SunVox files',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    tests_require=test_dependencies,
    entry_points={},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
