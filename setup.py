from setuptools import setup

setup(name='tribe',
      version='0.1',
      description='Facebook group scraper',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Productivity :: Social Media',
      ],
      keywords='facebook group scraper',
      url='https://github.com/imaculate/Tribe',
      author='Imaculate Mosha',
      author_email='imaculatemosha@yahoo.com',
      license='MIT',
      packages=['tribe'],
      scripts=['tribe/Tribe.py'],
      entry_points = {
        'console_scripts': [
        'tribe=tribe.Tribe:get_posts'
        ]
    },
      zip_safe=False,
       install_requires=[
          'pandas'
      ],
      include_package_data=True)
