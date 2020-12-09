from setuptools import setup

setup(
    name="flaskr",
    packages=["flaskr"],
    include_package_data=True,
    install_requires=[
        "flask",
    ],
    # set few lines to run test (can do without pytest)
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],
)
