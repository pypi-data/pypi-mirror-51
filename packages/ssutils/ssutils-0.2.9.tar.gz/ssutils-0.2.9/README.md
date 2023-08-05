# ssutils
collection of useful python functions


## Screenwriter

Use Screenwriter to prefix screen prints
**Examples**

### 1 - Default prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ()
sw.echo ('my output')
```
```
Output:
2019-07-26-11:16:04 my output
```

### 2 - Date Time parts in prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ('%Y-%m-%d %H:%M:%S.%f ')
sw.echo ('my output')
```
```
Output:
2019-07-26 11:16:04 my output
```
 
### 3 - Error, Warning & Info standard prefixes ###

```python
from ssutils import Screenwriter

sw = Screenwriter ()
sw.error ('an error message')
sw.warn  ('a warming message')
sw.info  ('an informational message')
```
```
Output:
2019-07-29-11:39:00 ERROR: an error message
2019-07-29-11:39:00 WARN:  a warming message
2019-07-29-11:39:00 INFO:  an informational message
```

### 4 - Trimming content length  ###
By default, log strings are trimmed to 1000 chars.
You can change this setting:
```python
from ssutils import Screenwriter
	
sw = Screenwriter ()
sw.set_maxlen (80) #Set maximum length to 80
```

For format options, see http://strftime.org/

## Sfdc

Use Sfdc to Query SFDC.
**Examples**

### 1 - List Objects ###

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token', False) # The last Param turns off verbose mode
sf.connect ()
sf.load_metadata ()
for api_name in sf.object_labels.keys():
        print (("API Name [" + api_name + "],").ljust(64) + "Label [" + sf.object_labels[api_name] + "]")
for api_name in sf.standard_object_names:
        print ("Standard Object [" + api_name + "]")
for api_name in sf.custom_object_names:
        print ("Custom Object [" + api_name + "]")
for api_name in sf.custom_setting_names:
        print ("Custom Setting [" + api_name + "]")

```
```

### 2 - Describe Objects ###

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token')
sf.connect ()
sf.load_metadata ()

def print_line (a, b, c, d, e):
        s = '{:7}'.format(a) + '{:50}'.format(b) + '{:20}'.format(c) + '{:20}'.format(d) + e
        print (s)

print_line ('Seq', 'API Name', 'Type', 'Length', 'Label')
print_line ('---', '--------', '----', '------', '-----')
fieldNumber = 1
for field in sf.describe_object ('Contact'):
        print_line ("#" + str(fieldNumber).ljust(3) + " - ", field['name'], field['type'], str(field['length']), field['label'])
        fieldNumber += 1

```
```
