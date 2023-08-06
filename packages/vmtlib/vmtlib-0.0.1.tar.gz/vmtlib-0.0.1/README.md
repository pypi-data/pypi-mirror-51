# VMTlib

#### Description:

VMTlib is a simple parser for Valve Material Type (.vmt) files.

#### Note:
> 1. At the moment this package doesn't support attribute key-value pairs
> separated by tabs.
> 2. The formatting of the write function is very basic.

#### Basic Usage:
###### Import
```python
from vmtlib.vmt_file import VmtFile
```

###### Reading
```python
vmtf = VmtFile("example.vmt")
vmtf.read()
```
###### Writing
```python
vmtf.write("path/to/target.vmt")
```

###### Accessing Objects and Attributes
```python
# Attributes
basetexture = vmtf.shader.get("$baseTexture")
# or
basetexture = vmtf.shader.attributes["$baseTexture"]

# Objects
proxy_obj = vmtf.shader.get("Proxies")
#or
proxy_obj = vmtf.shader.childs["Proxies"]
```
###### Setting Attributes
```python
vmtf.shader.set("$basetexture", "new_texture")
```
###### Getting the structure as dictionary:
```python
d = vmtf.shader.dict
```
###### Creating a VMT file from a dictionary:
```python
d = {"shader": {"$basetexture": "brick", "Proxies": {"key": "val"}}}
vmtf = VmtFile()

vmtf.from_dict(d)
```
###### Getting the filename and directory:
```python
filename = vmtf.filename
dir = vmtf.directory
```
