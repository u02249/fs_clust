import uuid
import atexit
import etcd
import threading
import logging


class ClusterManager():
    def __init__(self):
        cluster_name = "SuperCluster"
        self.my_key = uuid.uuid4().__str__()
        self.con = etcd.Connection(cluster_name, self.my_key)
        self.max_wait_time = 5;

        logger = logging.getLogger("ClusterMnager")
        logger.setLevel(logging.DEBUG)
        # create the logging file handler
        fh = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s:%(name)s[%(levelname)s]\t %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)

        self.log = logger

    def check_connection(self):
        self.log.debug("checking ETCD server connection")
        res = self.con.is_connect()
        return res

    def check_key(self):
        self.log.debug("checking exists key")
        res = self.con.get_key()
        return res is not None

    def key_is_my(self):
        self.log.debug("checking key is my")
        res = self.con.get_key()
        if res == self.my_key:
            return True
        else:
            return False

    def update_key(self):
        self.log.debug("update key")
        return self.con.set_key()

    def set_key(self):
        self.log.debug("sen new key")
        res = self.con.set_key()
        return self.con.set_key()

    def stop_service(self):
        self.log.warning("service is stopped!!!")


    def start_service(self):
        self.log.warning("service is started!!!")

    def wait(self):
        timer = threading.Timer(self.max_wait_time, self.wait)
        timer.start()
        if self.check_connection():
            if self.check_key():
                if self.key_is_my():
                    if not self.update_key():
                        self.stop_service()
                    else:
                        self.log.debug("im master!!!")
                else:
                    self.log.debug('im slave!!')
                    self.stop_service()
            else:
                self.log.warning('key not found')
                if self.set_key():
                    self.start_service()
                else:
                    self.stop_service()
        else:
            self.log.warning('connection not esteblished')
            self.stop_service()





@atexit.register
def exit_func():
    print("goodbay")

if __name__ == "__main__":
    cm = ClusterManager()
    cm.wait()


