# BIO

## Authors

 * [Peter Tisovčík](https://github.com/mienkofax)
 * [Klára Nečasová](https://github.com/Klarksonnek)
 * [Vašek Ševčík](https://github.com/VaclavSevcik)

## Libraries

### wsq

This implementation is taken from [https://github.com/pawelmoll/wsq](https://github.com/pawelmoll/wsq)

#### Build library

```bash
cd lib/wsq
mkdir build
cd build
cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3.5 -DPYTHON_VERSION_SUFFIX=-py35 ..
make
```

#### Usage
Copy python file into build folder.

#### Simple example

* build library
```
cd lib/wsq/build
python3
>>> import wsq
>>> wsq.wsq_to_png('01.wsq', 'out.png')
0
```
