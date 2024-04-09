# IRIS

### The following is a simple demo of MQTT communication: an online broker (HiveMQ client) receives messages from a publisher created with Paho MQTT and Python. 
### The publisher loops through the records of a dataset and publishes one every 2 seconds.
### A subscriber reads data from the broker and posts it to a deque that it shares with a Dash app, which visualizes the last 25 records on a table.



