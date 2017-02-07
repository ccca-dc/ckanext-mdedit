from ckanapi import RemoteCKAN
import json
############################# General Commands #############################
demo = RemoteCKAN('http://127.0.0.1:5000',apikey='73970e04-3acf-4333-acb9-b1b15b44e5c7')
data = RemoteCKAN('https://data.ccca.ac.at',apikey='431109b7-c9f9-47f1-ab3b-d42b836b6355')
sandbox = RemoteCKAN('https://sandboxdc.ccca.ac.at',apikey='431109b7-c9f9-47f1-ab3b-d42b836b6355')

############################# General Commands END #############################
## Change keywords in list/dict
#mydict[new_key] = mydict.pop(old_key)
#go_on = raw_input ('press enter to continue')
#pkg = demo.call_action('package_show', {'id':dataset})
#rst_pkgdict = demo.call_action('package_update', pkg )
################################################################################

######### Enter Host and logfile  ##############################

host = sandbox
log_file = 'sandbox_dataset_extras.log'


#####################################################
log_f = open (log_file, 'w')

print "######## Filtering for extras  ################################ Host:  " + str(host)

log_f.write("######## Filtering for extras  ################################ host: " + str(host))
log_f.write("\n")


pkg_list = host.call_action('package_list')

string_list = str(pkg_list)

print string_list
log_f.write(string_list)
               
go_on = raw_input ('press enter to continue')

count_e = 0
count_t = 0
count_c = 0
count_l = 0

for dataset in pkg_list:
        
    count_t += 1

    ############################################################
    
    print "#######################################################"
    log_f.write( "#######################################################")
    log_f.write("\n")
    print "Dataset: " + dataset
    log_f.write("Dataset: " + dataset)
    log_f.write("\n")

    ################# Change Package Attributes ########################
    pkg = host.call_action('package_show', {'id':dataset})

    ################# Check for extras ###############################
    
    try:
        extras = pkg['extras']

    except:
        count_c += 1
        print "''''''''''''''''''''''''''''''''''' Clean Dataset: " + dataset
        log_f.write("''''''''''''''''''''''''''''''''''' Clean Dataset " + dataset)
        log_f.write("\n")
        extras = None
        pass
        continue

    else:
        count_e += 1
        print "''''''''''''''' Extras found '''''''''''''''''''' Dataset: " + dataset
        log_f.write("''''''''''''''' Extras found '''''''''''''''''''' Dataset: " + dataset)
        log_f.write("\n")
        
        for x in extras:
            print str(x)
            log_f.write(str(x))
            log_f.write("\n")           

            if x['key'] == 'datasetLocator':
                print "''''''''''''''' Locator found ''''''''''''''''''''  " 
                log_f.write("''''''''''''''' Locator found '''''''''''''''''''' ")
                log_f.write("\n")
                count_l += 1
                break
            elif x['key'] == 'datasetURI':
                count_l += 1
                break
            elif x['key'] == 'datasetUri':
                count_l += 1
                break
            
        """ 
        try: 
          locator_prob = extras['datasetLocator']
        except:
            continue
        else:
            count_l += 1
            print "'''''''''''''''''''''''''''''''  Locator found '''''''''''''''''''' Dataset: " + dataset
            log_f.write("''''''''''''''''''''''''' Locator found '''''''''''''''''''' Dataset: " + dataset)
            log_f.write("\n")
            continue
        """
print "#######################################################"
log_f.write( "#######################################################")
log_f.write("\n")
print "Finished: Total sets: " + str( count_t) + " With extras: " + str(count_e) + " With Locator: " + str(count_l) +" clean: " + str(count_c)
log_f.write("Finished: Total sets: " + str( count_t) + " With extras: " + str(count_e) +  " With Locator: " + str(count_l) +" clean: " + str(count_c))
log_f.write("\n")
log_f.close()
