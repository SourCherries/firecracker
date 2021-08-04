# import setuptools
# setuptools.setup()
# from setuptools import setup
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firecracker",
    py_modules=["firecracker"],
    version="1.0",
    description="DO",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Carl Michael Gaspar",
    author_email="carl.michael.gaspar@icloud.com",
    url="https://github.com/SourCherries/firecracker",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'scipy'],
    requires_python=">=3.6",
    classifiers=[
        "Intended Audience :: Academics",
        "Intended Audience :: Scientists",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # scripts=["scripts/example_erp.py", "scripts/example_pulsar.py"]
)
