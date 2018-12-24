class Blog:
    insert_temple = (
        "INSERT INTO "
        "blog(bid, url, publish_type, title, publish_time, cnt) "
        "VALUES"
        "(%s, %s, %s, %s, %s, %s)"
    )

    def __init__(self, bid, url, publish_type, title, publish_time, cnt):
        self.bid = bid
        self.publish_time = publish_time
        self.publish_type = publish_type
        self.title = title
        self.cnt = cnt
        self.url = url

    def __str__(self) -> str:
        return (
            "["
            "'bid': {bid}, "
            "'publish_type': {publish_type}, "
            "'publish_time': {publish_time}, "
            "'cnt': {cnt}, "
            "'title': {title}, "
            "'url': {url}"
            "]"
        ).format(
            bid=self.bid,
            publish_type=self.publish_type,
            publish_time=self.publish_time,
            title=self.title,
            cnt=self.cnt,
            url=self.url
        )

    def __data__(self):
        return self.bid, self.url, self.publish_type, self.title, self.publish_time, self.cnt

    def insert_sql(self) -> str:
        return (
            "insert into "
            "blog(bid, url, publish_type, title, publish_time, cnt) "
            "values"
            "(\"{bid}\", {url}, {publish_type}, {title}, {publish_time}, {cnt})"
        ).format(
            bid=self.bid,
            url=self.url,
            publish_type=self.publish_type,
            title=self.title,
            publish_time=self.publish_time,
            cnt=self.cnt
        )
