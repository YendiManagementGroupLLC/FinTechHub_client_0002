db.getCollection('AAPL').find({"open" : 189.75})
db.getCollection('DPW').find({"date" : 1531849287})
db.getCollection('posts').find({})
db.printCollectionStats()




// ##### this is dangerous territory #####
db.getCollection('AAPL').drop()
db.getCollection('ABIL').drop()
db.getCollection('AVXL').drop()
db.getCollection('BLNK').drop()
db.getCollection('CRON').drop()
db.getCollection('DEST').drop()
db.getCollection('DPW').drop()
db.getCollection('EGY').drop()
db.getCollection('GEVO').drop()
db.getCollection('JVA').drop()
db.getCollection('KBLB').drop()
db.getCollection('NAKD').drop()
db.getCollection('POTN').drop()
db.getCollection('RKDA').drop()
db.getCollection('SNES').drop()
// ##### this is dangerous territory #####