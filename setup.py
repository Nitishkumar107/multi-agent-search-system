from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="multi_agent_project",
    version="1.0.0",
    author="Nitish Kumar",
    author_email="kumar.n.gg365@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
)



