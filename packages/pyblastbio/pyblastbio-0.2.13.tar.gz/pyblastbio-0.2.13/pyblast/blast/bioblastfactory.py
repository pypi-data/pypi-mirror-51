from pyblast.blast import BioBlast
from pyblast.blast.seqdb import SeqRecordDB
from pyblast.utils import clean_records
from uuid import uuid4
from copy import deepcopy
from pyblast.blast.blast import C
from typing import List
from Bio.SeqRecord import SeqRecord


class BioBlastFactory(object):
    """
    Instance factory for :class:`BioBlast` instance that share the same :class:`SeqRecordDB`.

    Usage:

    ::

        factory = BioBlastFactory()
        factory["plasmid_templates"] = records1
        factory["primers"] = records2
        factory["queries"] = records3

        blast1 = factory("plasmid_templates", "queries")
        blast2 = factory("primers", "queries")
    """

    def __init__(self, seq_db=None, span_origin=True):
        """
        Initialize a new BioBlastFactory.

        :param seq_db: the optional SeqRecordDB. If not provided, a new one will be created.
        :type seq_db: SeqRecordDB
        """
        if seq_db is None:
            self.db = SeqRecordDB()
        else:
            self.db = seq_db
        self.span_origin = span_origin
        self.record_groups = {}

    def __setitem__(self, record_group_name: str, records: List[SeqRecordDB]):
        """
        See add_records.
        """
        self.add_records(records, record_group_name)

    def __getitem__(self, record_group_name):
        return self.record_groups[record_group_name]

    def add_records(
        self, records: List[SeqRecordDB], record_group_name: str
    ) -> List[SeqRecord]:
        """
        Add records to the SeqRecordDB by keyword.

        :param records:
        :type records:
        :param record_group_name:
        :type record_group_name:
        :return:
        :rtype:
        """
        clean_records(records)
        keys, records = BioBlast.add_records(
            records, self.db, span_origin=self.span_origin
        )
        if record_group_name:
            self.record_groups[record_group_name] = records
        return records

    def __call__(self, subject_key, query_key, **config):
        """
        Create a new BioBlast instance with the factory's SeqRecordDB.
        
        :param subject_key: the subject key
        :type subject_key: str
        :param query_key: the query key
        :type query_key: str
        :param config: BioBlast config
        :type config: dict
        :return:
        :rtype:
        """
        if isinstance(subject_key, str):
            subjects = self.record_groups[subject_key]
        if isinstance(query_key, str):
            queries = self.record_groups[query_key]
        return BioBlast(
            subjects=subjects,
            queries=queries,
            seq_db=self.db,
            span_origin=self.span_origin,
            **config
        )
