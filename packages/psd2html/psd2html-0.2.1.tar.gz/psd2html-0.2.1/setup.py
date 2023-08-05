from setuptools import setup

# This call to setup() does all the work
setup(
    name="psd2html",
    version="0.2.1",
    description="Convert PSD file to HTML",
    url="https://github.com/kimngei/psd2html",
    author="Andrew Ngei",
    author_email="andrew@kimngei.pro",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[
        "psd2html",
        "psd2html.converter",
        "psd2html.builder"
    ],
    include_package_data=True,
    install_requires=[
        "psd-tools",
        "lxml",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "psd2html=psd2html.__main__:main",
        ]
    },
)
