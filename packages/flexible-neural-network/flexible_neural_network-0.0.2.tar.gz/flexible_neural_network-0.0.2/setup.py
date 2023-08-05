import setuptools

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

setuptools.setup(
    name="flexible_neural_network",
    version="0.0.2",
    author="Mohamed Abdou",
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    author_email="matex512@gmail.com",
    description="A simple and flexible python library that allows you to build custom Neural Networks where you can easily tweak parameters to change how your network behaves",
    url="https://github.com/Mohamed-512/Flexible_Neural_Net",
    packages=['flexible_neural_network'],
    require=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)