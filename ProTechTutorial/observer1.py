import uuid
import datetime

class MsgLoad(object):
    def __init__(self, load):
        self.data = load
        self.timeStamp = datetime.datetime.now()


class PubSubMsg(object):
    def __init__(self, name):
        self.sender = name

    def loadMsg(self, data):
        self.data = MsgLoad(data)
    
    def unloadMsg(self):
        return self.data.data
    


class BasePubSubTop(object):
    def __init__(self, type, id=None):
        self.setID(id)
        self.setType(type)
    
    def setID(self, topic = None):
        if topic:
            self.id = topic
        else:
            self.id = uuid.uuid4()

    def getID(self):
        return self.id

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type


class PubSubObj(BasePubSubTop):
    def availableTopics(self):
        pass

    def registerForTopic(self, topic):
        topic.addRegisters(self)
        
    def unregisterFromTopic(self, topic):
        topic.removeRegisters(self)

class Subscriber(PubSubObj):
    """docstring for ClassName"""
    def __init__(self):
        super(PubSubObj, self).__init__('Sub')
    
    def update(self, message):

        print('{} got message "{}" from "{}" sent at "{}"'.format(self.id, message.data.data, message.sender, message.data.timeStamp))

class Publisher(PubSubObj):
    """docstring for ClassName"""
    def __init__(self):
        super(PubSubObj, self).__init__('Pub')
        self.message = PubSubMsg(self.id)

    def publishToTopic(self, topic, data):
        self.message.loadMsg(data)
        topic.setMessage(self.message)


class Topic(BasePubSubTop):
    def __init__(self, name):
        self.registers = set()
        self.messages = set()
        super(Topic, self).__init__('Topic', name)

    def addRegisters(self, who):
        self.registers.add(who)

    def removeRegisters(self, who):
        self.registers.discard(who)

    def logMessage(self, message):
        self.message = message
        self.messages.add(message)


    def printRegisters(self):
        for each in self.registers:
            print(each.type, each.id)
    
    def publishToSubs(self):
        subscribers = (x for x in self.registers if x.type == 'Sub')
        for subscriber in subscribers:
            subscriber.update(self.message)

    def setMessage(self, message):
        self.logMessage(message)        
        self.publishToSubs()


if __name__ == '__main__':
    topic = Topic('test')
    print(topic.getID())

    pub = Publisher()
    print(pub.getID())

    sub = Subscriber()
    print(sub.getID())
    
    
    sub.registerForTopic(topic)
    pub.registerForTopic(topic)
    topic.printRegisters()

    # topic.publishToSubs('This is a Test')
    pub.publishToTopic(topic, 'This is a test')

    sub.unregisterFromTopic(topic)
    pub.unregisterFromTopic(topic)
    topic.printRegisters()



