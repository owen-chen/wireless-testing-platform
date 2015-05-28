# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


setup(
      name="wtp",
        version="1.1.0",
        packages=find_packages(),
        package_data={'':['config.xml','index.html']},
        zip_safe=False,

        description="wireless testing platform",
        long_description="wireless testing platform",
        author="owen.chen",
        author_email="chenchen9@iflytek.com",

        license="GPL",
        keywords=("wireless", "test", "platform", "cis", "egg"),
        platforms="Independent",
        url="",
      )
