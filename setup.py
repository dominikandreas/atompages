from setuptools import setup

def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except:
        return "no readme available"

setup(name='atompages',
    version='0.1',
    description='Simple web page templating using jinja2, markdown and bootstrap supported responsiveness',
    url='http://github.com/dominikandreas/atompages',
    author='Dominik Dienlin',
    author_email='dominik@dienlin.net',
    install_requires=[
        "jinja2",
        "watchdog",
        "libsass",
        "markdown",
        "cherrypy",
        "MarkupSafe>=0.23"
    ],
    license='MIT',
    include_package_data=True,
    packages=['atompages'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['atompages=atompages.__main__:main'],
    })
