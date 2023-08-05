from setuptools import setup

setup(name='zar',
      version='0.3.31',
      description='Zeroincombenze Archive Replica',
      long_description="""
Backup and restore files and DBs
""",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 2.6',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
      ],
      keywords='backup, restore, replica',
      url='http://wiki.zeroincombenze.org/en/Python/opt/zar',
      author='Antonio M. Vigliotti',
      author_email='antoniomaria.vigliotti@gmail.com',
      license='Affero GPL',
      packages=['zar'],
      zip_safe=False)
