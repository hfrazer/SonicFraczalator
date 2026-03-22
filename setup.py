from setuptools import setup, find_packages

setup(
    name="sonicfraczalator",
    version="0.1.0",
    description="A modular chaotic‑chord synthesizer built in Python.",
    author="Hugh Frazer",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "sounddevice",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "sonicfraczalator=main:main"
        ]
    },
)
