import etcd3
import codecs


class Connection:
    def __init__(self, cluster_name, key_val):
        self.key = cluster_name + "_master_key"
        self.key_val = key_val
        self.leaser_time = 20

    def cli(self):
        return etcd3.client(host="34.69.186.246")

    def is_connect(self):
        cli = self.cli()
        try:
            if cli.status().leader:
                return True
            else:
                return False
        except:
            if cli:
                cli.close()
            return None


    def get_key(self):
        cli = self.cli()
        encoder = codecs.getdecoder('UTF8')
        try:
            key, meta = cli.get(self.key)
            if key:
                return encoder(key)[0]
            else:
                return None
        except:
            if cli:
                cli.close()
            return None



    def set_key(self):
        cli = self.cli()
        try:
            leaser = cli.lease(ttl=self.leaser_time)
            res = cli.put(self.key, value=self.key_val, lease=leaser)
            return res
        except:
            if cli:
                cli.close()
            return None


