from distutils.core import setup
setup(
  name = 'megadictionary',         # How you named your package folder (MyLib)
  packages = [''],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='cc-by-sa-4.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "A fully formatted dictionary for everything you'll ever need.",   # Give a short description about your library
  author = 'Veritius',                   # Type in your name
  author_email = 'veritius@mail.com',      # Type in your E-Mail
  url = 'https://github.com/veritius/megadictionary',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Veritius/megadictionary/archive/v0.6.tar.gz',    # I explain this later on
  keywords = ['ENGLISH','DICTIONARY','DEFINITIONS','FORMATTED'],   # Keywords that define your package best
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
	'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
	'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
  ],
)