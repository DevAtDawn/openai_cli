from setuptools import setup
setup(
    name='openai_cli',
    version='0.0.1',
    packages=['openai_cli'],
    entry_points={
        'console_scripts': [
            'openai_cli=openai_cli.openai_cli:cli'
        ]
    }
)
