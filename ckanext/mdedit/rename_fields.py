from ckanapi import RemoteCKAN
demo = RemoteCKAN('http://127.0.0.1:5000',apikey='73970e04-3acf-4333-acb9-b1b15b44e5c7')
pkg_list = demo.call_action('package_list')
pkg = demo.call_action('package_show', {'id':'g1111'})



mydict[new_key] = mydict.pop(old_key)

f = open('pure_names.txt', 'r')

items = []
f = open('pure_names.txt', 'r')
for line in f:
    string = str(line.strip())
    if string != '':
        items.append(string)

for x in pkg:
    print "old: " + x     
    for  index in  range(0,len(items), 2):
            y = items[index]
            if x  == y:        
               print "---x: " + x
               print "---y: " + y
               print "--new: " +  items[index+1]
               new_item = items[index+1]
               pkg[new_item] = pkg.pop(x)
               items.pop(index)
               items.pop(index)
               break
