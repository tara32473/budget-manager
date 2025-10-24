import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="budget-manager",
    version="1.0.0",
    description="A comprehensive command-line personal finance management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tara32473/budget-manager",
    author="tara32473",
    author_email="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Utilities",
    ],
    keywords="finance, budget, personal-finance, cli, money-management",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "enhanced": [
            "colorama>=0.4.4",
            "tabulate>=0.9.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "budget=budget_manager.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/budget-manager/issues",
        "Source": "https://github.com/your-username/budget-manager",
        "Documentation": "https://github.com/your-username/budget-manager#readme",
    },
)
