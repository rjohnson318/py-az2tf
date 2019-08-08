# azurerm_eventhub_namespace_authorization_rule
def azurerm_eventhub_namespace_authorization_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_eventhub_namespace_authorization_rule"
    tcode="522-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST namespace for queue"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.EventHub/namespaces"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
        try:
            azr= r.json()["value"]
        except KeyError:
            if cde: print "Found no Namespaces for EventHubs"
            return

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            nname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            #print id
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
 
            url="https://management.azure.com/" + id + "/authorizationRules"
            params = {'api-version': '2017-04-01'}
            r = requests.get(url, headers=headers, params=params)
            #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print "Found no EventHub Authorizations"
                return
            
            if cde:
                print ("****")
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))
        

    ###############
    # specific code start
    ###############
        
        
      
        #azr2=az servicebus queue list -g rgsource --namespace-name nname -o json
            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
                    name= azr2[j]["name"]
                    rname= name.replace(".","-")
                    id= azr2[j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    rgs=id.split("/")[4]

                    rname=name.replace(".","-")
                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                   
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
                    fr.write('\t namespace_name = "' +  nname + '"\n')

                    rights= azr2[j]["properties"]["rights"]
   
                    if "Listen" in str(rights):
                        fr.write('\t listen = "true"\n')
                    else:
                        fr.write('\t listen = "false"\n')

                    if "Send" in str(rights):
                        fr.write('\t send = "true"\n')
                    else:
                        fr.write('\t send = "false"\n')

                    if "Manage" in str(rights):
                        fr.write('\t manage = "true"\n')
                    else:
                        fr.write('\t manage = "false"\n')

                    #fr.write('\t namespace_name = "' +  nname + '"\n')                

        # no tags block       


                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print f.read()

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub