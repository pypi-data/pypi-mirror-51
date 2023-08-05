import setuptools

with open('README.md') as fp:
    readme = fp.read()

setuptools.setup(
    name='vup',
    version='1.0.1',
    entry_points={
        'console_scripts': [
            'vup = vup.main:main'
        ],
    },
    packages=setuptools.find_packages(),

    description='VUP: Version UPdater: Version management system',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='SiLeader',
    url='https://github.com/SiLeader/vup',

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
    ],

    license='GPLv3.0'
)
