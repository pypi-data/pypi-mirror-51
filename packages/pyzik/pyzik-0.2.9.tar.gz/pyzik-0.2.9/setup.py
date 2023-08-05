import setuptools
f = open('version.txt')
versions = f.read().split('.')
f.close()
v = int(versions[0])*100+int(versions[1])*10+int(versions[2])
v += 1
v = str(v)
v = v.zfill(3)
version = ".".join(v)
f = open('version.txt','w')
f.write(version)
f.close()
print(version)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyzik",
    version=version,
    author="FJ",
    author_email="fredericboltzmann@gmail.com",
    description="functions packages for my physic's students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['colorama','prettytable','uncertainties',
                      'astroquery','ezsheets','Pillow','mendeleev',
                     'wget','requests','chempy','pyserial','scikit-image',
                     'sti-LabJackPython','text2art','cirpy','jcamp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)