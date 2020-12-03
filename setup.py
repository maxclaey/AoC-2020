import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) > 0:
            requirements.append(line)

setuptools.setup(
    name="aoc2020",
    version="0.0.1",
    author="Maxim Claeys",
    author_email="maximclaeys@gmail.com",
    description="Solutions for advent of code 2020",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxclaey/AoC-2020",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': ['aoc2020-solver=aoc2020.solve:main'],
    },
    python_requires='>=3.6',
)
