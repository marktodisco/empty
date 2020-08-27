from setuptools import setup


setup(
    name='empty',
    version='0.0.1',
    packages=['empty'],
    entry_points=dict(
        console_scripts=['empty=empty.empty:main']
    )
)
