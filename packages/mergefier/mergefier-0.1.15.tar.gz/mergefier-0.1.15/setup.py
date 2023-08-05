from setuptools import setup

setup(name='mergefier',
      version='0.1.15',
      description='You use this to merge your pull requests.',
      url='http://github.com/enkelbr/mergefier',
      author='Gustavo Maia',
      author_email='gurumaia@gmail.com',
      license='GPL',
      packages=['mergefier'],
      zip_safe=False,
      install_requires=['gitator==0.1.36', 'slackclient==1.0.5']
      )
