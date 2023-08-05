import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ros2_llcb",
    version="0.0.1",
    author="Michael Ramos",
    author_email="mike.ramos58@gmail.com",
    description="ROS2 log level callback.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/ros2_llcb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
