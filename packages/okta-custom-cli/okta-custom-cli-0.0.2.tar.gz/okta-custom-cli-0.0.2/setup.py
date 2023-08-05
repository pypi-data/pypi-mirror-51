from setuptools import setup, find_packages


setup(name='okta-custom-cli',
      version='0.0.2',
      description='Sample Okta CLI tool in python',
      license='MIT',
      author='Atulya Kumar Pandey',
      author_email='atul3015@gmail.com',
      packages=find_packages(),
      install_requires=[
          'Click',
          'pyfiglet',
          'requests'
      ],
      entry_points='''
            [console_scripts]
            okta-custom-cli=okta_custom_cli.okta:okta
        ''',
      zip_safe=True,
      include_package_data=True
      )
