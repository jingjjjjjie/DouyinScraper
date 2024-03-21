from setuptools import setup, find_packages

install_requires=[
        'selenium==4.0.0',  
        'beautifulsoup4==4.12.3',
        'requests==2.31.0',
        'pandas==2.0.3',
    ],


setup(
    name="DouyinScraper",
    author="Jason Ma",
    version="1.0",
    description="Douyin Scraper",
    keywords=["douyin", "scraper"],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
    packages=find_packages("."),
)