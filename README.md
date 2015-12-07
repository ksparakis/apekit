![apekit logo](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/apekitLogoDes2.png)


![banana bullet](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/smallbanana.png) Description
--------
Android app vulnerability analysis toolkit  
EC521 Cyber Security Final Project  
December 2015  

![banana bullet](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/smallbanana.png) Modules
--------
| Module | Description |
| ------ | ----------- |
| **backend** | [peewee](http://docs.peewee-orm.com/en/latest/) ORM interface to a sqlite database that holds metadata and vulnerability results. |
| **crawler** | Randomly samples Android apps from the 10-31-2014 snapshot of the Android marketplace on Archive.org. Archive.org deployed [PlayDrone](https://github.com/nviennot/playdrone) in October 2014 to capture 1.4M free apps. |
| **andgroguard** | **(not in repository)** We use the [Androguard](https://github.com/androguard/androguard) disassembler for recovering the source code from each of the apks we sample. |
| **vulns** | Modules for testing each of the vulnerabilities listed below. |

![banana bullet](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/smallbanana.png) Vulnerabilities Tested
--------

TBA

![banana bullet](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/smallbanana.png) Authors
--------
| Name | Email |
| ---- | ----- |
| Igor DePaula | igorp@bu.edu |
| Carlton Duffett | cduffett@bu.edu |
| Zach Lister | zlister@bu.edu |
| Petar Ojdrovic | pojdrov@bu.edu |
| Luke Sorenson | lasoren@bu.edu |
| Konstantino Sparakis | sparakis@bu.edu |

![bu logo](http://www.bu.edu/brand/files/2012/10/BU-Master-Logo.gif)

![banana bullet](https://raw.githubusercontent.com/ksparakis/apekit/master/imgs/smallbanana.png) Copyright and License
--------
Copyright 2015. Code released under the [Apache 2.0](./LICENSE) license.
