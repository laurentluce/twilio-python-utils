from distutils.core import setup
setup(
    name = "twilio-python-utils",
    packages = ["twilioresourcesdb"],
    version = "0.1",
    description = "Twilio resources DB sync library",
    author = "Laurent Luce",
    author_email = "laurentluce49@yahoo.com",
    url = "http://github.com/laurentluce/twilio-resources-db/",
    download_url = "",
    keywords = ["twilio","resources","database"],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony"
        ],
    long_description = """\
    Twilio Python Utils modules

    This library allows you to download your resources (calls, sms, notifications...) 
    to your database. It also keeps processing new ones so you don't have to be worried 
    to be out of sync.

    Dependencies:
    Twilio Python Library helper: git clone https://github.com/twilio/twilio-python.git
    SQLAchemy: easy_install SQLAlchemy
    simplejson: easy_install simplejson

    Install library:
    git clone https://github.com/laurentluce/twilio-python-utils.git
    cd twilio-python-utils
    python setup.py install
    
     LICENSE The Twilio resources DB Library is distributed under the MIT
    License """ )
