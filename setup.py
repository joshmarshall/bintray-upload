import setuptools


setuptools.setup(
    name="bintray-upload",
    version="0.1.0a0",
    description="Simple BinTray utility for uploading Debian packages.",
    author="Josh Marshall",
    author_email="catchjosh@gmail.com",
    url="https://github.com/joshmarshall/bintray",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    py_modules=["bintray_upload"],
    entry_points={
        "console_scripts": ["bintray-upload = bintray_upload:main"],
    })
