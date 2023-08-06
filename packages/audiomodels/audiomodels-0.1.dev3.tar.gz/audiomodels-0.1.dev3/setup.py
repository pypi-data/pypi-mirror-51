from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

     name='audiomodels',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version='0.1.dev0',
    # according to https://semver.org/
    version='0.1.dev3',
    
    description=' audio models package with semantic features identification',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://bitbucket.org/dpenalva/stattus4-audio-models/src/master/',

    # Author details
    author='Daniel Penalva',
    author_email='dkajah@gmail.com',

    # Choose your license
    license='',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Education',
        'Intended Audience :: Religion',
        'Intended Audience :: Other Audience',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'Topic :: Multimedia :: Sound/Audio :: Mixers',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Artistic Software',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        # Pick your license as you wish (should match "license" above)

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
    ],

    # What does your project relate to?
    keywords=['physics', 'music', 'synthesis', 'psychophysics',
            'symmetry', 'change ringing', 'campanology', 'group theory', 'toolbox',
            'musical composition', 'art', 'artistic creation',
            'experimental music', 'contemporary music', 'synthesizer', 'PCM', 'audio', 'sound',
            'acoustics', 'signal processing', 'multimedia', 'psychoactive',
            'rotation', 'permutation', 'mirror', 'speech', 'singing',
            'speech synthesis', 'numpy', 'sonic art', 'hifi', 'hi-fi',
            'noise', 'high fidelity', 'hyper-fidelity', 'LUT', 'vibrato',
            'tremolo', 'AM', 'FM', 'ADSR', 'HRTF', 'spatialization',
            'spatial location'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=["music"],
    packages=find_packages(),
    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # TODO: test with virtualenv to know the dependencies

    install_requires=['numpy', 'scipy', 'matplotlib','pandas','librosa','tensorflow'],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    #extras_require = {
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
    #    'sample': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
    project_urls={
                 'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
                 #'Funding': 'https://donate.pypi.org',
                 #'Say Thanks!': 'http://saythanks.io/to/example',
                 'Source': 'https://bitbucket.org/dpenalva/stattus4-audio-models/src/master/',
                 'Tracker': 'https://github.com/pypa/sampleproject/issues',}
)
