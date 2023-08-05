from setuptools import setup

# with open('requirements.txt') as fid:
#     requires = [line.strip() for line in fid]

requires = [
    'pandas',
    'request'
    ]

setup(
    name = 'owldata',
    version = "0.0.11",
    description = 'Testing version for owl',
    author = 'Owl Corp.',
    author_email = 'owldb@cmoney.com.tw',
    # install_requires = ['pandas', 'requests'],
    install_requires = requires,
    url = 'https://owl.cmoney.com.tw/Owl/',
    packages = ['owldata']
)
