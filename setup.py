from setuptools import setup, find_packages

def get_requires():
    reqs = []
    for line in open('./requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

setup(
	name="FindDouble",
	version="0.1",
	description="Find doubles in Gaia by cross-matching with WDS catalog",
	license="MIT",
	packages=find_packages(),
	authors='Gonzalez-Tora, G., Kueny, J., Li, J.',
    install_requires=get_requires()
)
	
