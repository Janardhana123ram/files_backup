from setuptools import setup

version = "0.1.0"
setup(
    name="backup",
    python_requires=">3.7",
    version=version,
    packages=["backup", "backup.upload"],
    package_dir={"backup": "backup"},
    data_files=[("backup", ["backup/upload/gcp_creds.json"])],
    include_package_data=True,
    description="This tool is used to upload files to AWS and Google Cloud storage",
    author="Janardhana",
    author_email="janardhan321ram@gmail.com",
    install_requires=[],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["backup = backup:main"]},
)
