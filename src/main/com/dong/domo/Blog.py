
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
