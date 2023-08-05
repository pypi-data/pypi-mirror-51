import setuptools

with open("README.rst") as fp:
    long_description = fp.read()

with open("torchutils/_version.py") as fp:
    torchutils_version = fp.read().strip().split('__version__ = ')[1][1:-1]

setuptools.setup(
     name='torchutils',
     version=torchutils_version,
     author="Anjandeep Singh Sahni",
     author_email="sahni.anjandeep@gmail.com",
     description="PyTorch utility functions.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/anjandeepsahni/pytorch_utils",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     keywords='machine-learning deep-learning pytorch neuralnetwork',
     license='MIT'
 )
