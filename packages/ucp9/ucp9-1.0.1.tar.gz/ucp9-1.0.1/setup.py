import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucp9",
    version="1.0.1",
    author="Tran Anh Nhan",
    author_email="vfa.nhanta@gmail.com",
    description="Unicode To CP932 Transcoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nhantranz/ucp9",
    packages=["ucp9"],
    package_data={'': ['cp932.conf']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
