from setuptools import setup

setup(name='gitator',
      version='0.1.36',
      description='Basic git functionality',
      url='http://github.com/enkelbr/gitator',
      author='Gustavo Maia',
      author_email='gurumaia@gmail.com',
      license='GPL',
      packages=['.'],
      zip_safe=False,
      install_requires=['PyGithub==1.36']
      )
