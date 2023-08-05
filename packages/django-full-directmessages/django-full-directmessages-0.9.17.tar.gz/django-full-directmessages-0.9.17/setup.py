from setuptools import setup, find_packages
import os
import directmessages

REQUIREMENTS = [
    'Django>=1.5',
]

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    author="Dominic Monn",
    author_email="yacine@grad4.com",
    name='django-full-directmessages',
    version=directmessages.__version__,
    description='Django-Directmessages is a low-level and easy-to-use Django App to manage simple directmessages.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
