from setuptools import setup

setup(name='authtools',
      version='1.0',
      description='Authentication toolkit for Senior Capstone',
      url='http://github.com/bwbryant1/NotHotdog',
      author='Team Not Hotdogs',
      author_email='bwb016@email.latech.edu',
      license='MIT',
      packages=['authtools'],
      install_requires=[
          'pyudev',
          'pycrypto',
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
      package_data = {'authtools':['data/*png']},
      entry_points={'console_scripts': ['authman = authtools.core:main']},
      zip_safe=False)
