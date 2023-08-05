from Producer_Consumer.QueueTool import QueueProducer
from Producer_Consumer.QueueTool import QueueConsumer
from Producer_Consumer.QueueTool import QueueConsumerProcess
import multiprocessing
import json

def test_func(data):
    """test function"""
    return json.dumps({"result": data})

def test():
    """test"""
    process_list = []
    producer = QueueProducer()
    lock = multiprocessing.Lock()
    for i in range(4):
        p = QueueConsumerProcess(target=test_func, input_queue=producer.queue, filename="123.json",
                                 name="process%d" % i, lock=lock)
        p.start()
        process_list.append(p)

    for i in range(1000000):
        producer.produce(str(i))

    print "produce done"
    for p in process_list:
        p.stop()
        p.join()


if __name__ == '__main__':
    test()
