from ckanapi import RemoteCKAN
import json
############################# Host  #############################
demo = RemoteCKAN('http://127.0.0.1:5000',apikey='73970e04-3acf-4333-acb9-b1b15b44e5c7')
data = RemoteCKAN('https://data.ccca.ac.at',apikey='431109b7-c9f9-47f1-ab3b-d42b836b6355')
sandbox = RemoteCKAN('https://sandboxdc.ccca.ac.at',apikey='431109b7-c9f9-47f1-ab3b-d42b836b6355')

######### Parameter  ##############################

update_host = sandbox
dataset = 'oks15-bias-corrected-ichec-ec-earth-rcp85-r3i1p1-dmi-hirham5'
dataset ='messnetz-wmo-essential-stations-osterreich'
#pkg = update_host.call_action('package_show', {'id':dataset})
# pkg.pop('spatial')

########################################################################

print "######## Analyzing JSON Schema files ################################"


old_f = 'ckan_ccca_formated_help_iso_inspire_tabs.json'
new_f = 'ckan_ccca_formated_help_iso_inspire_tabs_iso.json'


with open(old_f) as json_data:
    old_names = json.load(json_data)
    print(old_names)

with open(new_f) as json_data:
    new_names = json.load(json_data)
    print(new_names)



### Dataset

old_fields =  old_names['dataset_fields']
new_fields =  new_names['dataset_fields']

old_list = []
new_list = []


for i, cont in enumerate(old_fields):
    print "************"
    print old_fields[i]
    print  "----------------------"
    print cont['field_name']
    old_list.append(cont['field_name'])
    

for i, cont in enumerate(new_fields):
    print "************"
    print new_fields[i]
    print  "----------------------"
    print cont['field_name']
    new_list.append(cont['field_name'])
    

if len(old_list) != len (new_list):
    print "**************** ERROR: Number of fields changed: no automatic replacement possible!"
    exit()

else:
    print "********** Number of fields identical (" + str(len(old_list)) +")"
    
go_on = raw_input ('press enter to continue')


### Resources


old_rfields =  old_names['resource_fields']
new_rfields =  new_names['resource_fields']


old_rlist = []
new_rlist = []


for i, cont in enumerate(old_rfields):
    print "************"
    print old_rfields[i]
    print  "----------------------"
    print cont['field_name']
    old_rlist.append(cont['field_name'])
    

for i, cont in enumerate(new_rfields):
    print "************"
    print new_rfields[i]
    print  "----------------------"
    print cont['field_name']
    new_rlist.append(cont['field_name'])
    

if len(old_rlist) != len (new_rlist):
    print "**************** ERROR: Number of fields changed: no automatic replacement possible!"
    exit()

else:
    print "********** Number of fields identical (" + str(len(old_rlist)) +")"
    

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
        count_d += 1
        old_fn.append(cont)
        new_fn.append(new_list[i])
    else:
        print "NOT Changing: " + cont + " to: " + new_list[i]
        no_change += 1
        
print "************ Changing " + str(count_d) + " field_names in total; NOT changing " + str(no_change) + " field_names"

go_on = raw_input ('press enter to continue with resources')


#Resoruces
count_r = 0;
no_change =0

old_rfn = []
new_rfn = []

for i, cont in enumerate(old_rlist):
    if cont != new_rlist[i]:
        print "Changing: " + cont + " to: " + new_rlist[i]
        count_r += 1
        old_rfn.append(cont)
        new_rfn.append(new_rlist[i])
    else:
        print "NOT Changing: " + cont + " to: " + new_rlist[i]
        no_change += 1
        
print "************ Changing " + str(count_r) + " field_names (resources) in total; NOT changing " + str(no_change) + " field_names"
print "######## Finished Analyzing JSON Format files ################################"

print "######## Changing Dataset Fields ################################"

go_on = raw_input ('press enter to continue')


############################################################
################# Change Package Attributes ########################
pkg = update_host.call_action('package_show', {'id':dataset})


count_changes = 0
for x in pkg:
    print "old: " + x     
    for i, y in enumerate(old_fn):
            if x  == y:        
               count_changes += 1
               print "---x: " + x
               print "---y: " + y
               new_item = new_fn[i]
               print "Change to: " + new_item
               pkg[new_item] = pkg.pop(x)               
               break

print str(count_changes) + " field_names replaced in dataset"

repl_err = count_d - count_changes

if repl_err != 0:
    print "***************** Success  *********** But  " + str (repl_err) + " Items not found i.e. NOT replaced"

else:
    print "**************** SUCCCESS ***************"

go_on = raw_input ('press enter to continue')


############# Change Resource Attributes ############################
pkg_res = pkg['resources']
count_changes = 0


for res in pkg_res:
    for x in res:
        print "old: " + x     
        for i, y in enumerate(old_rfn):
            if x  == y:        
                count_changes += 1
                print "---x: " + x
                print "---y: " + y
                print "--new: " +   new_rfn[i]
                new_item = new_rfn[i]
                res[new_item] = res.pop(x)
                
                break
                
pkg['resources'] = pkg_res

repl_err_r  = count_r - count_changes

if repl_err_r:
    print "***************** Success  *********** BUT " + str (repl_err_r) + " Items not found i.e. replaced"

else:
    print "**************** SUCCCESS ***************"
    
print "########  Finished Changing Dataset Fields ################################"


go_on = raw_input ('press enter to continue')


############## Write to server #######################

if repl_err or repl_err_r:
    print "Missing fields in Dataset " + dataset + "; Writing package anyway ...."
else:
    print " Field names sussessfiully changed for dataset: " + dataset
    

try:
    rst_pkgdict = update_host.call_action('package_update', pkg )

except:
    print "''''''''''''''''''''Error updating dataset: " + dataset + "''''''''' Skipping '''''"
    pass

else:

    print "################# Dataset successfully updated to CKAN: " + dataset
