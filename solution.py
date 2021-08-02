import json
import math

class ManagementSystem:
    def __init__(self):
        self.catalog={}
        self.pending_order={}
        self.fulfilled_orders=[]
    
    def print_catalog(self):
        print("{:10s}\t{:10s}".format("PRODUCT ID", "QUANTITY"))
        print("--------\t--------")
        for key in self.catalog:
            print("{0}\t\t{1}".format(key, self.catalog[key][1]))
    
    def get_pending_orders(self):
        return self.pending_order
        
    def get_fulfilled_orders(self):
        return self.fulfilled_orders
        
    def init_catalog(self, product_info):
        for key in product_info:
            self.catalog[key["product_id"]]=[key["mass_g"],0]
      
    def ship_package(self, shipment):
        print(shipment)
        
    def process_order(self,order):
        remaining_weight=1800
        order_id=order["order_id"]
        #Verify order id is unique for shipment 
        if len(self.fulfilled_orders)>0: 
              for element in self.fulfilled_orders:
                    if order_id==element["order_id"]:
                        order_id+=1
        shipment={"order_id": order_id,"shipped":[]}
        
        for key in order["requested"]:
            if key["quantity"]>0 and self.catalog[key["product_id"]][1]>0:
                items=math.floor(remaining_weight/self.catalog[key["product_id"]][0])
                remaining_weight%=self.catalog[key["product_id"]][0]
                if items>self.catalog[key["product_id"]][1]:
                    items=self.catalog[key["product_id"]][1]
                    
                self.catalog[key["product_id"]][1]-=items
                if key["quantity"]<items:
                    items=key["quantity"]

                key["quantity"]-=items
                shipment["shipped"].append({"product_id": key["product_id"], "quantity":items})
                
        if len(shipment["shipped"])>0:
            self.ship_package(shipment)
            self.fulfilled_orders.append(shipment)
        self.pending_order=order
        
    def process_restock(self,restock):
        for key in restock:
            self.catalog[key["product_id"]][1]+=key["quantity"]
        if len(self.pending_order)==0:
            return None
        #Fill any pending orders
        current_order=self.pending_order["order_id"]
        if len(self.fulfilled_orders)>0:
            current_order=self.fulfilled_orders[-1]["order_id"]+1
        while self.pending_order["requested"][len(order["requested"])-1]["quantity"]>0:
            remaining_weight=1800
            shipment={"order_id":current_order,"shipped":[]}
            for key in order["requested"]:
                if key["quantity"]>0:
                    items=math.floor(remaining_weight/self.catalog[key["product_id"]][0])
                    remaining_weight%=self.catalog[key["product_id"]][0]
                    if items>self.catalog[key["product_id"]][1]:
                        items=self.catalog[key["product_id"]][1]
                    self.catalog[key["product_id"]][1]-=items
                    print("Adding items: "+str(items)+" inventory is "+str(self.catalog[key["product_id"]][1]))
                    if key["quantity"]<items:
                        items=key["quantity"]
                        key["quantity"]=0
                    else:
                        key["quantity"]-=items
                    shipment["shipped"].append({"product_id": key["product_id"], "quantity":items})
            self.ship_package(shipment)
            self.fulfilled_orders.append(shipment)
            current_order+=1
        self.pending_order={}
    
if __name__=="__main__":
    #Initialize ManagementSystem object and get JSON payload for product info
    print("-----------------------------------------------------------")
    print("Welcome to the Inventory Management and Processing System")
    print("-----------------------------------------------------------")
    manage_orders=ManagementSystem()
    file=open("product_info.json",)
    product_info=json.load(file)
    manage_orders.init_catalog(product_info)
    file.close()
    
    print("\n\t\tMENU\n")
    print("{:30s} {:3s}".format("Restock inventory", "r/R"))
    print("{:30s} {:3s}".format("Create new order", "o/O"))
    print("{:30s} {:3s}".format("Display current inventory", "d/D"))
    print("{:30s} {:3s}".format("View pending orders", "p/P"))
    print("{:30s} {:3s}".format("View fulfilled orders", "f/f"))
    option=input("\nEnter an option from the menu or q/Q to quit:")
    while(option.lower()!="q"):
        if option.lower()=='r':
           file=open(input("Please provide restock file: "))
           restock=json.load(file)
           manage_orders.process_restock(restock)
           file.close()
        elif option.lower()=='o':
            file=open(input("Please provide order file:"))
            order=json.load(file)
            manage_orders.process_order(order)
            file.close()
        elif option.lower()=='p':
            print(manage_orders.get_pending_orders())
        elif option.lower()=='p':
            print(manage_orders.get_pending_orders())
        elif option.lower()=='f':
            print(manage_orders.get_fulfilled_orders())
        elif option.lower()=='d':
            manage_orders.print_catalog()
        else:
            print("Invalid Input!")
        option=input("Enter an option from the menu or q/Q to quit:")