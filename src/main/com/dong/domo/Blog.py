
class blog:

    def __init__(self, bid, levels, publish_type, publish_time, title) -> None:
        self.bid = bid
        self.levels = levels
        self.publish_time = publish_time
        self.publish_type = publish_type
        self.title = title
        self.insert_sql = """insert into blog(bid, levels, publish_type, publish_time, title) 
                    values({bid}, {levels}, {publish_type}, {publish_time}, {title})""".format(
            bid=bid,
            levels=levels,
            publish_type=publish_type,
            publish_time=publish_time,
            title=title
        )

    def __str__(self) -> str:
        return """{'bid': {bid}, 'levels': {levels}, 'publish_time': {publish_time}, 'publish_type': {publish_type}, 'title': {title}}""".format(
            bid=self.bid,
            levels=self.levels,
            publish_time=self.publish_time,
            publish_type=self.publish_type,
            title=self.title
        )



