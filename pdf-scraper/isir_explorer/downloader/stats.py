from datetime import datetime, timedelta


class DownloadStats:

    def __init__(self):
        self.start = datetime.now()
        self.rows = 0
        self.errors = 0
        self.readable = 0
        self.documents = 0
        self.empty_documents = 0
        self.file_size = 0
        self.doc_types = {}
        self.stats_record = None

    def add(self, task):
        self.rows += 1
        self.file_size += task.file_size
        if not task.success:
            self.errors += 1
        if task.empty_document:
            self.empty_documents += 1
        if task.documents:
            self.readable += 1
            self.documents += len(task.documents)
        for doc in task.documents:
            typ = doc.Metadata.Typ
            if typ not in self.doc_types:
                self.doc_types[typ] = 1
            else:
                self.doc_types[typ] += 1

    async def save(self, db):
        if self.stats_record is None:
            self.__repr__()
        column_names = list(self.stats_record.keys())
        placeholders = map(lambda x: ":" + x, column_names)
        query = "INSERT INTO dl_stats (" + ",".join(column_names) + ") "  # nosec - konst. nazvy
        query += "VALUES (" + ",".join(placeholders) + ")"
        await db.execute(query=query, values=self.stats_record)

    def __repr__(self):
        now = datetime.now()
        delta = now - self.start
        delta_time = delta - timedelta(microseconds=delta.microseconds)
        not_empty = self.rows - self.empty_documents
        size_mib = self.file_size / (1024 * 1024)
        if size_mib > 1024:
            size_str = "{:.2f} GiB".format(size_mib / 1024)
        else:
            size_str = "{:.2f} MiB".format(size_mib)
        percent_readable = self.readable / \
            (not_empty / 100) if not_empty > 0 else 0
        res = "\n========= Výsledek importu =========\n"
        res += "Čas:                     {:>10}\n".format(str(delta_time))
        res += "PDF dokumentů:           {:>10} ({})\n".format(
            self.rows, size_str)
        res += "Neprázdných:             {:>10}\n".format(not_empty)
        res += "Čitelných:               {:>10} ({:.1f}%)\n".format(
            self.readable, percent_readable)
        res += "Importováno:             {:>10}\n".format(self.documents)
        res += "Chyb:                    {:>10}\n".format(self.errors)

        res += "\n========== Typy dokumentů =========\n"

        doc_types_sorted = {k: v for k, v in sorted(
            self.doc_types.items(), reverse=True, key=lambda item: item[1])}
        for doc in doc_types_sorted:
            num = doc_types_sorted[doc]
            res += doc.ljust(30) + "{:>5}\n".format(num)

        self.stats_record = {
            "tstart": self.start,
            "tend": now,
            "seconds": int(delta_time.total_seconds()),
            "mib": round(size_mib, 6),
            "docs": self.rows,
            "not_empty": not_empty,
            "readable": self.readable,
            "imported": self.documents,
            "errors": self.errors,
        }

        return res
