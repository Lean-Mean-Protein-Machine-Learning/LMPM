import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lmpm", # name available on pypi.org
    version="0.0.1",
    author="Marc Exposit, Andrew Favor, Gizem Gokce, Joe Henthorn, Melissa Ling",
    author_email="author@example.com",
    license="MIT License",
    description="Protein secretion prediction using ML",
    long_description=long_description, # this goes directly from the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/tree/main/lmpm",
    project_urls={
        "Code": "https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/tree/main/lmpm",
        "Webapp": "https://lmpm.herokuapp.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    package_dir={"": "lmpm"}, # root package on lmpm folder
    packages=setuptools.find_packages(where="lmpm"), #discover subpackages in lmpm folder
    python_requires=">=3.8", # pickle version used requires >3.8
    install_requires=['pandas','numpy'] # you can also specify version numbers here
)