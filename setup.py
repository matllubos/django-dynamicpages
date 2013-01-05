from setuptools import setup, find_packages
from dynamic_pages import version

setup(
    name='django-dynamicpages',
    version=version,
    description="Application which allows dynamically change urls.",
    keywords='django, admin, pages',
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    url='https://github.com/matllubos/django-dynamicpages',
    license='GPL',
    package_dir={'dynamic_pages': 'dynamic_pages'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Czech',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    zip_safe=False
)