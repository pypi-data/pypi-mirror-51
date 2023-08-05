from setuptools import setup
import versioneer

setup(name='papers-fork',
      version=versioneer.get_version(),
      cmdclass = versioneer.get_cmdclass(),
      author='Mahe Perrette',
      author_email='mahe.perrette@gmail.com',
      description='utilities to keep your PDF library organized',
      url='https://github.com/perrette/papers',
      packages=['papers'],
      scripts=['scripts/papers'],
      license = "MIT",
      install_requires = ["bibtexparser","crossrefapi","fuzzywuzzy", "unidecode", "scholarly", "six"],
      )
