from setuptools import setup

setup(name='pullrequester',
      version='0.1.9',
      description='You use this to create pull requests. And be happier!',
      url='http://github.com/enkelbr/pullrequester',
      author='Gustavo Maia',
      author_email='gurumaia@gmail.com',
      license='GPL',
      packages=['pullrequester'],
      zip_safe=False,
      install_requires=['PyGithub', 'gitator==0.1.36']
      )
