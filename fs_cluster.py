from statemachine import StateMachine, State
import uuid
import etcd3
from time import sleep
class ClusterManager(StateMachine):

    slave = State('slave', initial = True)
    candidat = State('candidat')
    master = State('master')
    fail = State('fail')


    key_not_found = slave.to(candidat)
    connection_lost = slave.to(fail)
    connection_repair = fail.to(slave)
    connection_not_found = fail.to(fail)
    key_not_my = slave.to(slave)
    key_not_set = candidat.to(slave)
    key_set = candidat.to(master)
    key_update = master.to(master)
    key_not_update = master.to(slave)


class Watcher():
    def __init__(self):
        self.c = ClusterManager()
        self.key_name = "/super/fs_cluster"
        self.my_key = uuid.uuid4().__str__()

    def etcd(self):
        with etcd3.client(host='34.69.186.246', port=2379) as cli:
            yield cli

    def watch(self):
        while True:
            cli = self.etcd().__next__()
            try:
                cli.get(key_name)
            print(cli)
            cli.close()
            sleep(5)


if __name__ == "__main__":
    w = Watcher()
    w.watch()
