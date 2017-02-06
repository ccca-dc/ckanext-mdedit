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
######### Check for changes ##############################

#Change hostname for renameing fields here
update_host = demo

print "######## Analyzing JSON Schema files ################################"


old_f = 'ckan_ccca_formated_help_iso_inspire_tabs.json'
new_f = 'ckan_ccca_formated_help_iso_inspire_tabs_iso.json'

log_file = 'ckan_ccca_formated_help_iso_inspire_tabs_iso.log'

log_f = open (log_file, 'w')

log_f.write("######## Analyzing JSON Schema files ################################")
log_f.write("\n")

with open(old_f) as json_data:
    old_names = json.load(json_data)
    #print(old_names)

with open(new_f) as json_data:
    new_names = json.load(json_data)
    #print(new_names)

### Dataset

old_fields =  old_names['dataset_fields']
new_fields =  new_names['dataset_fields']

old_list = []
new_list = []


for i, cont in enumerate(old_fields):
    """
    print "************"
    log_f.write("************")
    log_f.write("\n")
    print old_fields[i]
    log_f.write(str( old_fields[i]))
    log_f.write("\n")
    print  "----------------------"
    log_f.write(  "----------------------")
    log_f.write("\n")
    print cont['field_name']
    log_f.write(str( cont['field_name']))
    log_f.write("\n")
    """
    old_list.append(cont['field_name'])


for i, cont in enumerate(new_fields):
    """
    print "************"
    log_f.write("************")
    log_f.write("\n")
    print new_fields[i]
    log_f.write( str(new_fields[i] ))
    log_f.write("\n")
    print  "----------------------"
    log_f.write(  "----------------------")
    log_f.write("\n")
    print cont['field_name']
    log_f.write(str( cont['field_name']))
    log_f.write("\n")
    """
    new_list.append(cont['field_name'])


if len(old_list) != len (new_list):
    print "**************** ERROR: Number of fields changed: no automatic replacement possible!"
    log_f.write("**************** ERROR: Number of fields changed: no automatic replacement possible!")
    log_f.write("\n")
    exit()

else:
    print "********** Number of fields identical (" + str(len(old_list)) +")"
    log_f.write("********** Number of fields identical (" + str(len(old_list)) +")")
    log_f.write("\n")

go_on = raw_input ('press enter to continue')


### Resources


old_rfields =  old_names['resource_fields']
new_rfields =  new_names['resource_fields']


old_rlist = []
new_rlist = []


for i, cont in enumerate(old_rfields):
    """
    print "************"
    log_f.write("************")
    log_f.write("\n")
    print old_rfields[i]
    log_f.write (str(old_rfields[i]))
    log_f.write("\n")
    print "----------------------"
    log_f.write( "----------------------")
    log_f.write("\n")
    print cont['field_name']
    log_f.write(str( cont['field_name']))
    log_f.write("\n")
    """
    old_rlist.append(cont['field_name'])


for i, cont in enumerate(new_rfields):
    """
    print "************"
    log_f.write("************")
    log_f.write("\n")
    print new_rfields[i]
    log_f.write(str(new_rfields[i]))
    log_f.write("\n")
    print "----------------------"
    log_f.write("----------------------")
    log_f.write("\n")
    print cont['field_name']
    log_f.write (str(cont['field_name']))
    log_f.write("\n")
    """
    new_rlist.append(cont['field_name'])


if len(old_rlist) != len (new_rlist):
    print "**************** ERROR: Number of fields changed: no automatic replacement possible!"
    log_f.write("**************** ERROR: Number of fields changed: no automatic replacement possible!")
    log_f.write("\n")
    exit()

else:
    print "********** Number of fields identical (" + str(len(old_rlist)) +")"
    log_f.write("********** Number of fields identical (" + str(len(old_rlist)) +")")
    log_f.write("\n")



go_on = raw_input ('press enter to continue')


##### replace only changed fields ####
#Dataset
count_d = 0;
no_change =0

old_fn = []
new_fn = []

for i, cont in enumerate(old_list):
    if cont != new_list[i]:
        print "Changing: " + cont + " to: " + new_list[i]
        log_f.write("Changing: " + cont + " to: " + new_list[i])
        log_f.write("\n")

        count_d += 1
        old_fn.append(cont)
        new_fn.append(new_list[i])
    else:
        print "NOT Changing: " + cont + " to: " + new_list[i]
        log_f.write("NOT Changing: " + cont + " to: " + new_list[i])
        log_f.write("\n")
        no_change += 1

print "************ Changing " + str(count_d) + " field_names in total; NOT changing " + str(no_change) + " field_names"
log_f.write("************ Changing " + str(count_d) + " field_names in total; NOT changing " + str(no_change) + " field_names")
log_f.write("\n")

go_on = raw_input ('press enter to continue with resources')


#Resoruces
count_r = 0;
no_change =0

old_rfn = []
new_rfn = []

for i, cont in enumerate(old_rlist):
    if cont != new_rlist[i]:
        print "Changing: " + cont + " to: " + new_rlist[i]
        log_f.write("Changing: " + cont + " to: " + new_rlist[i])
        log_f.write("\n")
        count_r += 1
        old_rfn.append(cont)
        new_rfn.append(new_rlist[i])
    else:
        print "NOT Changing: " + cont + " to: " + new_rlist[i]
        log_f.write( "NOT Changing: " + cont + " to: " + new_rlist[i])
        log_f.write("\n")
        no_change += 1

print "************ Changing " + str(count_r) + " field_names (resources) in total; NOT changing " + str(no_change) + " field_names"
log_f.write("************ Changing " + str(count_r) + " field_names (resources) in total; NOT changing " + str(no_change) + " field_names")
log_f.write("\n")
print "######## Finished Analyzing JSON Format files ################################"
log_f.write("######## Finished Analyzing JSON Format files ################################")
log_f.write("\n")

print "######## Changing Dataset Fields ################################"
log_f.write("######## Changing Dataset Fields ################################")
log_f.write("\n")

go_on = raw_input ('press enter to continue')


dataset = 'test-rename-fields'
dataset = 'g2222'
dataset = 'g1111'

pkg_list = update_host.call_action('package_list')

print pkg_list
go_on = raw_input ('press enter to continue')

for dataset in pkg_list:

    ############################################################

    print "Dataset: " + dataset
    log_f.write("Dataset: " + dataset)
    log_f.write("\n")

    ################# Change Package Attributes ########################
    pkg = update_host.call_action('package_show', {'id':dataset})


    count_changes = 0
    for x in pkg:
        print "old: " + x
        log_f.write("old: " + x)
        for i, y in enumerate(old_fn):
                if x  == y:
                    count_changes += 1
                    print "---x: " + x
                    print "---y: " + y
                    log_f.write("---y: " + y)
                    new_item = new_fn[i]
                    print "Change to: " + new_item
                    log_f.write("Change to: " + new_item)
                    pkg[new_item] = pkg.pop(x)
                    break

    print str(count_changes) + " field_names replaced in dataset"
    log_f.write(str(count_changes) + " field_names replaced in dataset")
    log_f.write("\n")

    repl_err = count_d - count_changes

    if repl_err != 0:
        print "***************** Success  *********** But  " + str (repl_err) + " Items not found i.e. NOT replaced"
        log_f.write("***************** Success  *********** But  " + str (repl_err) + " Items not found i.e. NOT replaced")
        log_f.write("\n")

    else:
        print "**************** SUCCCESS ***************"
        log_f.write("**************** SUCCCESS ***************")
        log_f.write("\n")

    #go_on = raw_input ('press enter to continue')


    ############# Change Resource Attributes ############################
    pkg_res = pkg['resources']
    count_changes = 0


    for res in pkg_res:
        for x in res:
            print "old: " + x
            log_f.write("old: " + x)
            log_f.write("\n")
            for i, y in enumerate(old_rfn):
                if x  == y:
                    count_changes += 1
                    print "---x: " + x
                    print "---y: " + y
                    log_f.write("---y: " + y)
                    log_f.write("\n")
                    print "--new: " +   new_rfn[i]
                    log_f.write("--new: " +   new_rfn[i])
                    log_f.write("\n")
                    new_item = new_rfn[i]
                    res[new_item] = res.pop(x)

                    break

    pkg['resources'] = pkg_res

    repl_err_r  = count_r - count_changes

    if repl_err_r != 0:
        print "***************** Success  *********** BUT " + str (repl_err_r) + " Items not found i.e. replaced"
        log_f.write("***************** Success  *********** BUT " + str (repl_err_r) + " Items not found i.e. replaced")
        log_f.write("\n")

    else:
        print "**************** SUCCCESS ***************"
        log_f.write("**************** SUCCCESS ***************")
        log_f.write("\n")

    print "########  Finished Changing Dataset Fields ################################"
    log_f.write("########  Finished Changing Dataset Fields ################################")
    log_f.write("\n")


    #go_on = raw_input ('press enter to continue')


    ############## Write to server #######################

    if repl_err or repl_err_r:
        print "Missing fields in Dataset " + dataset + "; Writing package anyway ...."
        log_f.write("Missing fields in Dataset " + dataset + "; Writing package anyway ....")
        log_f.write("\n")

    else:
        print " Field names sussessfiully changed for dataset: " + dataset
        log_f.write(" Field names sussessfiully changed for dataset: " + dataset)
        log_f.write("\n")


    try:
       rst_pkgdict = update_host.call_action('package_update', pkg )

    except:
        print "''''''''''''''''''''Error updating dataset: " + dataset + "''''''''' Skipping '''''"
        log_f.write("''''''''''''''''''''Error updating dataset: " + dataset + "''''''''' Skipping '''''")
        log_f.write("\n")
        pass
        continue

    print "################# Dataset successfully updated to CKAN"
    log_f.write("################# Dataset successfully updated to CKAN")
    log_f.write("\n")


log_f.close()
