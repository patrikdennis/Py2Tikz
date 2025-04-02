import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Py2Tikz",
    version="0.0.2",
    author="Patrik Franzén",
    author_email="patrik.franzen.dennis@gmail.com",
    description="A Python library for generating LaTeX pgfplots/tikz code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrikdennis/Py2Tikz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
         "numpy",
         "pandas",
    ],
)

