from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='textsense',
      version='0.1',
      description='TextSense.ai a Text analytics platform.',
      author='TextSense Team',
      author_email='agambhire@algoanalytics.com',
      install_requires=[
          'requests',
      ],
      packages=['textsense'],
      zip_safe=False)
