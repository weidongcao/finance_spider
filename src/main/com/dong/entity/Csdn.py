import datetime


class Csdn:
    insert_temple = (
        "insert into "
        "csdn(cdate, original, fans, liked, comments, levels, visit, score, rank) "
        "values"
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

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

    def __str__(self) -> str:
        return (
            "['cid': {cid}, 'cdate': {cdate}, 'original': {original}, "
            "'fans': {fans}, 'liked': {liked}, 'comments': {comments}, 'levels': {levels}, "
            "'visit': {visit}, 'score': {score}, 'rank': {rank}] insert_sql={insert_sql}"
        ).format(
            cid=self.cid,
            cdate=self.cdate,
            original=self.original,
            fans=self.fans,
            liked=self.liked,
            comments=self.comments,
            levels=self.levels,
            visit=self.visit,
            score=self.score,
            rank=self.rank,
            insert_sql=self.insert_sql()
        )

    def __data__(self):
        return self.cdate, self.original, self.fans, self.liked, \
               self.comments, self.levels, self.visit, self.score, self.rank

    def insert_sql(self) -> str:
        return (
                "insert into "
                "csdn(cdate, original, fans, liked, comments, levels, visit, score, rank)"
                "values(\"{cdate}\", {original}, {fans}, {liked}, {comments}, {levels}, {visit}, {score}, {rank})"
            ).format(
            cdate=self.cdate,
            original=self.original,
            fans=self.fans,
            liked=self.liked,
            comments=self.comments,
            levels=self.levels,
            visit=self.visit,
            score=self.score,
            rank=self.rank
        )


if __name__ == '__main__':
    print(Csdn.insert_temple)

