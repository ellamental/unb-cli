from setuptools import setup, find_packages


if __name__ == '__main__':
  setup(
    name='unb-cli',
    version='0.0.1',
    description='Command line utilities for UNB project development.',
    author='Nick Zarczynski',
    author_email='nick@unb.services',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'flake8',  # linting
    ],
    license='MIT',
    url='https://bitbucket.org/unbsolutions/unb-cli',
    entry_points='''
      [console_scripts]
      unb=scripts.unb:cli
    ''',
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Console',
      'Framework :: Django :: 1.8',
      'License :: OSI Approved :: MIT License',
      'Operating System :: POSIX',
      'Programming Language :: Python :: 2.7',
    ],
  )
