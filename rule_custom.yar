rule malware_stop_av {
    meta:
        description = "phat hien ma doc dung cac tien trinh AV"
 
    strings:
        $stop_av_process1 = { 73 63 2E 65 78 65 }    
        $stop_av_process2 = { 4E 54 41 55 54 49 4C 55 53 20 53 65 63 75 72 69 74 79 20 43 65 6E 74 65 72 } 
 
    condition:
        $stop_av_process1 or $stop_av_process2
}


rule detect_av_infection {
    meta:
        description = "phat hien ma doc lay nhiem vao cac tep tin, thu muc, tien trinh AV"
 
    strings:
        $av_infected_exe = { 2A 61 76 2E 65 78 65 }     // *.av.exe
        $av_infected_dir = { 2A 61 76 2A }              // *av*
        $av_infected_svc = { 2A 61 76 73 76 63 2E 65 78 65 }    // *avsvc.exe
        $av_infected_config = { 2A 61 76 63 6F 6E 66 69 67 2E 65 78 65 }   // *avconfig.exe
        $av_infected_process = { 2A 61 76 70 72 6F 63 65 73 73 2A }     // *avprocess*
 
    condition:
        $av_infected_exe or $av_infected_dir or $av_infected_svc or $av_infected_config or $av_infected_process
}

rule detect_anti_virus_modification {
    meta:
        description = "phat hien ma doc làm sua doi registry keys, services , drivers của AV"
 
    strings:
        $av_modify_registry_key = { 2A 61 76 2E 72 65 67 }
        $av_modify_registry_key2 = { 6D 6F 64 69 66 79 2D 61 76 }
        $av_modify_service = { 61 76 73 76 63 2E 65 78 65 }  
        $av_modify_driver = { 61 76 73 76 69 64 2E 73 79 73 }
    condition:
        $av_modify_registry_key or $av_modify_registry_key2 or $av_modify_service or $av_modify_driver
}

rule detect_virus_deletefile {
    meta:
        description = "nghi ngo ma doc xoa file"
 
    strings:
        $string1 = { 64 65 6C 65 74 65 }
        $string2 = { 01 44 65 6C 65 74 65 46 69 6C 65 }
        $pattern = { 73 79 73 74 65 6D 33 32 }
    condition:
        any of ($string*) and $pattern 
}

rule detect_virus_stop_process{
meta:
        description = "nghi ngo ma doc dung tien trinh"
 
    strings:
        $string1 = { 73 75 62 70 72 6F 63 65 73 73 }
        $string2 = { 70 61 74 74 65 72 6E 20 }
        $pattern = { 20 70 6C 61 74 66 6F 72 6D 2E 73 79 73 74 65 6D 28 29 }
    condition:
        any of ($string*) and $pattern
}

rule detect_virus_infection{
meta:
        description = "nghi ngo ma doc tiem nhiem"
 
    strings:
        $string1 = { 63 61 63 68 65 64 5F 70 72 6F 70 65 72 74 79 }
        $pattern1 = { 77 69 6E 33 32 61 70 69 }
        $pattern2 = { 70 6C 61 74 66 6F 72 6D }
        
        
    condition:
        any of ($string*) and any of ($pattern*)
}

rule detect_virus_modify{
meta:
        description = "nghi ngo ma doc sua doi"
 
    strings:
        $string1 = { 73 75 62 }
        
        $pattern1 = { 74 61 72 67 65 74 }
        $pattern2 = { 73 65 61 72 63 68 }
        $pattern3 = { 66 69 6C }
        
    condition:
        any of ($string*) and any of ($pattern*)
}




