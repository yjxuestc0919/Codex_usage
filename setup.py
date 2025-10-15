from setuptools import setup, find_packages

setup(
    name='codex-usage',
    version='0.1.0',
    author='Yang Junxian',
    description='CLI tool to check ChatGPT Codex usage status',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'codex-usage = codex_usage.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
