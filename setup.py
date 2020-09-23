import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f]

setuptools.setup(
    name="flowkey_dl",
    version="0.0.1",
    author="Matthias Lienhard",
    author_email="mali270484@gmail.com",
    description="A python app to download sheet music from flowkey and save it as pdf.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'flowkey_dl':['raw/*png']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':['flowkey-dl = flowkey_dl.flowkey_dl_gui:main']},
    install_requires=requirements
)