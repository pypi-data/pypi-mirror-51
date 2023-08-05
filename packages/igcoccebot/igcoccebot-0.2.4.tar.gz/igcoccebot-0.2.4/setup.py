import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="igcoccebot",
    version="0.2.4",
    author="Lorenzo Coacci",
    author_email="lorenzo@coacci.com",
    description="The definitive package to interact on Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lollococce/igcoccebot",
    packages=setuptools.find_packages(),
    keywords='igcoccebot bot instagram selenium AI',
    license='MIT',
    include_package_data=True,
    install_requires=[
          'selenium',
          'pandas',
          'datetime',
          'termcolor',
          'pillow'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)