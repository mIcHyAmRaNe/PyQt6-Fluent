import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyqt6-fluent",
    version="0.1.0",
    keywords="pyqt6 fluent design frameless window win11 acrylic mica theme tokens components widget",
    author="Michy Amrane",
    author_email="jgonx3osm@mozmail.com",
    description="Modern Windows frameless window for PyQt6 with advanced theming engine, acrylic/mica effects, and Win11 design language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/michyamrane/PyQt6-Fluent",
    project_urls={
        "Homepage": "https://github.com/michyamrane/PyQt6-Fluent",
        "Documentation": "https://github.com/michyamrane/PyQt6-Fluent/wiki",
        "Repository": "https://github.com/michyamrane/PyQt6-Fluent.git",
    },
    packages=setuptools.find_packages(),
    package_data={
        "pyqt_fluent._rc": ["title_bar/close.svg", "resource.qrc", "resource.py"],
    },
    include_package_data=True,
    install_requires=[
        "pywin32",
        "PyQt6>=6.3.1",
    ],
    extras_require={
        "webengine": ["PyQt6-WebEngine>=6.3.1"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Desktop Environment :: Window Managers",
        "Framework :: PyQt",
    ],
)
