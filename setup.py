from setuptools import setup

setup(name='tribe',
      version='0.1',
      description='Facebook group scraper',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
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
