import datetime


class Visit:
    insert_temple = "insert into visit(bid, read_cnt, stat_time) values(%s, %s, %s)"

    def __init__(self, sid, bid, read_cnt):
        self.sid = sid
        self.bid = bid
        self.read_cnt = read_cnt
        self.stat_time = datetime.datetime.now()

    def __str__(self) -> str:
        return """['sid': {sid}, 'bid': {bid}, 'read_cnt': {read_cnt}]  insert_sql = {insert_sql}""".format(
            sid=self.sid,
            bid=self.bid,
            read_cnt=self.read_cnt,
            insert_sql=self.insert_sql()
        )

    def __data__(self):
        return self.bid, self.read_cnt, self.stat_time

    def insert_sql(self) -> str:
        return (
                "insert into visit(bid, read_cnt, stat_time) "
                "values({bid}, {read_cnt}, \"{stat_time}\")"
            ).format(
            bid=self.bid,
            read_cnt=self.read_cnt,
            stat_time=self.stat_time
        )



