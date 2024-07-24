from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'KinyaTTS Inference'
LONG_DESCRIPTION = 'An inference API for Kinyarwanda text-to-speech.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="kinyatts",
    version=VERSION,
    author="Antoine Nzeyimana",
    author_email="<nzeyi@kinlp.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchaudio",
        "Flask",
        "scipy",
        "numpy",
        "librosa",
    ],
    keywords=['python', 'pytorch', 'vits2', 'kinlp', 'kinyarwanda', 'tts', 'deep learning'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Research and Development",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux :: Linux OS",
    ]
)
