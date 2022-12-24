from setuptools import setup, find_packages

desc = open("README.md", "r")
desc_text = desc.read()
desc.close()

setup(
    name="django-statistics-dashboard",
    version="0.3",
    description="A stats dashboard and session tracker for Django.",
    long_description=desc_text,
    long_description_content_type="text/markdown",
    url="https://github.com/Si1veR123/django-statistics-dashboard",
    author="Connor George",
    author_email="connorgeorgeem@aol.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True
)
