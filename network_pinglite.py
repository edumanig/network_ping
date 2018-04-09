import requests
import json
import os
import sys

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: transit_diag3 <controller> <gw_name> <destination_ip>\n')
        exit(1)

    gateway_name = sys.argv[2]
    target_host = sys.argv[3]

    # Script Config 
    controller_ip = sys.argv[1]
    url = "https://" + controller_ip + "/v1/api"

    #f = open("/home/ubuntu/.aviatrix/credentials", encoding="latin-1")

    # get controller credentials
    #with open(os.path.expanduser('~/.aviatrix/credentials'), 'r') as f:
    with open(os.path.expanduser('/home/ubuntu/.aviatrix/credentials'), 'r') as f:
        read_data = f.readlines()

    list=read_data[1].split("=")
    admin_password = list[1].rstrip()
    f.closed

    # Login and Get CID
    print("\nLogin and Get CID...")
    data = {
	"action": "login",
	"username": "admin",
	"password": admin_password
    }

    response = requests.post(url=url, data=data, verify=False)
    pydict = response.json()
    print(json.dumps(pydict, indent=4))

    # Get CID if login successfully
    CID = ""
    if pydict["return"] == True:
    	CID = pydict["CID"]
    # END IF

    # Call REST API "run_gateway_ping_diagnostic" 
    print("\nCall REST API \"run_gateway_ping_diagnostic\" ")
    data = {
	"action": "run_gateway_ping_diagnostic",
	"CID": CID,
	"gateway_name": gateway_name,
	"target_host": target_host
    }

    response = requests.post(url=url, data=data, verify=False)
    pydict = response.json()
    print(json.dumps(pydict, indent=4))
  
 
    if pydict["return"] == True:
        print('-------------------')
        res_data=pydict["results"]
        print(res_data)
        find_this = "100%"
        if find_this in res_data:
            print("Connectivity test - FAILED")
        else:
            print("Connectivity test - PASSED")
    print()

