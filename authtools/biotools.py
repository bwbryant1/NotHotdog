import os
import authtools.settings

def get_fprint(path,fprint_name):
    #print(authtools.settings.fprint_exec_path + " " + path + fprint_name + " >> /dev/null")
    os.system(authtools.settings.fprint_exec_path + " " + path + fprint_name + " >> /dev/null")
    os.system("convert " + path+fprint_name + " " + path + fprint_name + ".png")

    print(authtools.settings.mindtct_exec + " " + path+fprint_name+".png" + " -o"+authtools.settings.decrypt_dir+fprint_name+"_temp")

def compare_fprints():
    pass
