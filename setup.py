import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    long_description = f.read()


setuptools.setup(
    name="shellodoro",
    version="1.0.5",
    author="StepanZubkov",
    author_email="zubkovbackend@gmail.com",
    description="Pomodoro timer right in your favorite terminal!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stepan-Zubkov/shellodoro",
    keywords="pomodoro, timer, tool, cli",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["shdr=shellodoro.shellodoro:main"]},
    install_requires=["click", "plyer"],
)
