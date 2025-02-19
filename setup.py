from setuptools import find_packages, setup

setup(
    name="virginia_elections_pipeline",
    packages=find_packages(exclude=["virginia_elections_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "clickhouse-driver",
        "clickhouse-sqlalchemy",
        "sqlalchemy",
        "selenium",
        "bs4",
        "pandas"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
