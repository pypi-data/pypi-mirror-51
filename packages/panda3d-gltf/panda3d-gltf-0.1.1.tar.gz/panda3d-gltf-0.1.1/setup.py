from setuptools import setup

def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

setup(
    name='panda3d-gltf',
    version='0.1.1',
    description='glTF utilities for Panda3D',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    keywords='panda3d gltf',
    packages=['gltf'],
    include_package_data=True,
    install_requires=[
        'panda3d',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-pylint',
    ],
    entry_points={
        'console_scripts': [
            'gltf2bam=gltf.cli:main'
        ],
        'gui_scripts': [
            'gltf-viewer=gltf.viewer:main'
        ],
        'panda3d.loaders': [
            'gltf=gltf.loader:GltfLoader'
        ],
    },
)
