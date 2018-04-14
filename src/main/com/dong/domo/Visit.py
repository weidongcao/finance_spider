import datetime


class Visit:

    def __init__(self, sid, bid, read_cnt):
        self.sid = sid
        self.bid = bid
        self.read_cnt = read_cnt
        self.stat_time = datetime.datetime.now()
        self.insert_sql = """insert into visit(bid, read_cnt, stat_time) \
                values({bid}, {read_cnt}, "{stat_time}")""".format(
            bid=bid,
            read_cnt=read_cnt,
            stat_time=self.stat_time
        )

    def __str__(self) -> str:
        return """['sid': {sid}, 'bid': {bid}, 'read_cnt': {read_cnt}]""".format(
            sid=self.sid,
            bid=self.bid,
            read_cnt=self.read_cnt
        )



