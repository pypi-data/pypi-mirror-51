# BunalabPy
## Install BunalabPy
```
 pip install BunalabPy 
```
## Exmaple BunalabPy
```
import BunalabPy.function as bunlab

# config 
bs = bunlab.Service(username,password)

# send mqtt
bs.SendMQ(message)

# send save data in db
bs.SendDB(table,tag,value)

# send plot map
bs.SendMap(table,lat,longt,tag,value)

```
* Function ```bunlab.Service(username,password)``` used to ```Login``` is Connect Bunalab. ```prameter about:```

    >```username``` is **username account** for Bunalab.

    >```password``` is **password account** for Bunalab.

* Function ```bs.SendMQ(message)``` after ```Login``` is Connect Bunalab. This is  function send message to device by Mqtt Bunalab. ```prameter about:```

    >```message``` is **value** for data send to device.

* Function ```bs.SendDB(table,tag,value)``` after ```Login``` is Connect Bunalab. This is  function send message to device by Mqtt but save data in databases for Bunalab system. ```prameter about:```

    >```table``` is **table name for database**.

    >```tag``` is **idendifind for data name** for device.

    >```value``` is **value** for sensor device at save data.

* Function ```bs.SendMap(table,lat,longt,tag,value)``` after ```Login``` is Connect Bunalab. This is  function send message to device by Mqtt but save data in databases for Bunalab system. can it data plot map in Bunalab system. ```prameter about:```

    >```table``` is **table name for database**.

    >```lat``` is **lati** at location.

    >```longt``` is **logti** at location.

    >```tag``` is **idendifind for data name** for device.

    >```value``` is **value** for sensor device at save data at location.

