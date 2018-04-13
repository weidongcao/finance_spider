import datetime
class Csdn:
    def __init__(self, cid, cdate, original, fans, liked, comments, levels, visit, score, rank):
        self.cid = cid
        self.cdate = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        self.original = original
        self.fans = fans
        self.liked = liked
        self.comments = comments
        self.levels = levels
        self.visit = visit
        self.score = score
        self.rank = rank
        self.insert_sql = """insert into csdn(cdate, original, fans, liked, comments, levels, visit, score, rank) \
                              values("{cdate}", {original}, {fans}, {liked}, {comments}, {levels}, {visit}, {score}, {rank})""".format(
            cdate=self.cdate,
            original=original,
            fans=fans,
            liked=liked,
            comments=comments,
            levels=levels,
            visit=visit,
            score=score,
            rank=rank
        )


