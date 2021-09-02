from setuptools import setup

setup(
   name='COERbuoyOne',
   version='0.2.0',
   author='Simon H. Thomas',
   author_email='simon.thomas.2021@mumail.ie',
   packages=['COERbuoyOne'],
   url='http://coerbuoy.maynoothuniversity.ie',
   license='LICENSE.txt',
   description='A realistic benchmark for Wave Enegery Converter controllers',
   long_description=open('README.txt').read(),
   install_requires=[
       "numpy",
       "scipy",
       "pandas",
       "COERbuoy",
   ],
   include_package_data=True,
)
