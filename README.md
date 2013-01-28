#Spokane Restauraunt Week

Website to help keep track of Restaurant Week checkins. Uses Redhat Openshift, Bottle.py, MongoDB, and Twilio

##Temporary url:
http://twt-dangayle.rhcloud.com/restaurants/

##Useful mongo commands:

```javascript
#remove all codes
db.restaurants.update({},{$set:{"codes":[]}}, {multi: true})

#reset visits to 0
db.restaurants.update({},{$set:{"visits":0}}, {multi: true})

#get object timestampe
ObjectId("5104e13d88ce1d1f556d39f2").getTimestamp()
```
