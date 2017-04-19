from setuptools import setup, find_packages

setup(author="CCG, Murdoch University",
      author_email="info@ccg.murdoch.edu.au",
      description="Ingest script for BPA data to CKAN",
      license="GPL3",
      keywords="",
      url="https://github.com/muccg/bpa-md5qc",
      name="bpaingest",
      version="1.15.1",
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      entry_points={
          'console_scripts': [
              'bpa-md5qc=bpamd5qc.cli:main',
          ],
      })