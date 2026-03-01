from setuptools import setup, find_packages

setup(
    name="algo_generators",
    version="0.1.0",
    author="Yassine Elgoumri",
    author_email="proowork15@email.com",
    description="A collection of maze generation algorithms in Python (DFS, Prim, BFS, etc.)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/maze-algorithms",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)