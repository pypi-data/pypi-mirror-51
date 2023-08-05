import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mk_tf_img_mod",
    version="0.0.0.3",
    author="Mark Cartagena",
    author_email="mark@mknxgn.com",
    description="Easy to use Image Learning Module for Tensorflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mknxgn.com/",
    install_requires=['tensorflow', 'mknxgn_essentials', 'requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
