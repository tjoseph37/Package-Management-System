The following project creates a package management system which is built to perform the following:

-manage product inventory
-keep track of stocked items
-transform incoming orders to outgoing shipments based on current inventory 
-display current inventory
-display shipped orders

The inventory restock and orders are provided via JSON files as seen in the example filed provided. Before the program begins, it initializes the managament system with product ids, product names and sets all quantities to 0. 

If orders are unable to be fulfilled upon request, the order is partially filledbased on current inventory. Upon restock, the rest of the order is fulfilled as a seperate shipment. Each shipment and order is uniquely identified with an id. 
