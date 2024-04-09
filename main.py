import IrisPublisher, IrisSubscriber
import threading


# TODO: add logging

publisher = IrisPublisher.IrisPublisher()
#subscriber = IrisSubscriber.IrisSubscriber()

publisher_thread = threading.Thread(target=publisher.start_loop)
#subscriber_thread = threading.Thread(target=subscriber.start)

publisher_thread.start()
#subscriber_thread.start()
