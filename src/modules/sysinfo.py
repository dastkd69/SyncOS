import os
import psutil


def getInfoFallback():
    uname_fields = ('sysname', 'nodename', 'release', 'version', 'machine')
    return 

def getInfo(diskpath):
    FIELDS = []
    FINALFIELDS = []
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(diskpath)
    uname_fields = ("Server Name", "Server OS", "Kernel Version", "System Architecture")
    display_names = ("Core Count ", " RAM Usage ", " Disk Usage ")
    for stat in list(zip(uname_fields, os.uname())):
        FINALFIELDS.append(stat)
    # FIELDS.append(list(zip(uname_fields, os.uname())))
    FIELDS.append(str(psutil.cpu_count()))
    FIELDS.append(str(round(mem.used/(1024**3),2)) + " / " + str(round(mem.total/(1024**3),2)) + " GiB " + "\t\t" + str(mem.percent) + "%")
    FIELDS.append(str(disk.percent))

    for stat in list(zip(display_names, FIELDS)):
        FINALFIELDS.append(stat)    

    print(FINALFIELDS[2][1])
    return FINALFIELDS

getInfo('/Storage/')