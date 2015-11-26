# Natural Language Toolkit: PanLex Corpus Reader
#
# Copyright (C) 2001-2015 NLTK Project
# Author: David Kamholz <kamholz@panlex.org>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Module docstring from readme
"""

import os
import sqlite3

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

class PanLexCorpusReader(CorpusReader):
    MEANING_Q = """
        SELECT dnx2.mn, dnx2.uq, dnx2.ap, dnx2.ui, ex2.tt, ex2.lv
        FROM dnx
        JOIN ex ON (ex.ex = dnx.ex)
        JOIN dnx dnx2 ON (dnx2.mn = dnx.mn)
        JOIN ex ex2 ON (ex2.ex = dnx2.ex)
        WHERE dnx.ex != dnx2.ex AND ex.tt = ? AND ex.lv = ?
        ORDER BY dnx2.uq DESC
    """

    TRANSLATION_Q = """
        SELECT s.tt, sum(s.uq) AS trq FROM (
            SELECT ex2.tt, max(dnx.uq) AS uq
            FROM dnx
            JOIN ex ON (ex.ex = dnx.ex)
            JOIN dnx dnx2 ON (dnx2.mn = dnx.mn)
            JOIN ex ex2 ON (ex2.ex = dnx2.ex)
            WHERE dnx.ex != dnx2.ex AND ex.lv = ? AND ex.tt = ? AND ex2.lv = ?
            GROUP BY ex2.tt, dnx.ui
        ) s
        GROUP BY s.tt
        ORDER BY trq DESC, s.tt
    """

    def __init__(self):
        self._c = sqlite3.connect(os.environ['PANLEX_LITE']).cursor()

        self._uid_lv = {}
        self._lv_uid = {}

        for row in self._c.execute('SELECT uid, lv, lc FROM lv'):
            self._uid_lv[row[0]] = row[1]
            self._lv_uid[row[1]] = row[0]

    def language_varieties(self, lc=None):
        """given "eng" returns ["eng-001", ...]
        """

        if lc == None:
            return [ i[0] for i in self._c.execute('SELECT uid FROM lv ORDER BY uid').fetchall() ]
        else:
            return [ i[0] for i in self._c.execute('SELECT uid FROM lv WHERE lc = ? ORDER BY uid', (lc,)).fetchall() ]

    def meanings(self, expr_uid, expr_tt):
        """
        >>> panlex.meanings("eng-000", "book")

        """

        expr_lv = self._uid_lv[expr_uid]

        mn_info = {}

        for i in self._c.execute(self.MEANING_Q, (expr_tt, expr_lv)):
            mn = i[0]
            uid = self._lv_uid[i[5]]

            if not mn in mn_info:
                mn_info[mn] = { 'uq': i[1], 'ap': i[2], 'ui': i[3], 'ex': {} }

            if not uid in mn_info[mn]['ex']:
                mn_info[mn]['ex'][uid] = []

            mn_info[mn]['ex'][uid].append(i[4])

        mns = []

        for mn in mn_info:
            mns.append(Meaning(mn, mn_info[mn]))

        return mns

    def translations(self, from_uid, from_tt, to_uid):
        from_lv = self._uid_lv[from_uid]
        to_lv = self._uid_lv[to_uid]

        return self._c.execute(self.TRANSLATION_Q, (from_lv, from_tt, to_lv)).fetchall()

class Meaning(object):
    def __init__(self, mn, attr):
        self = {
            'mn': mn,
            'uq': attr['uq'],
            'ap': attr['ap'],
            'ui': attr['ui'],
            'ex': attr['ex']
        }

    def id(self):
        return self['mn']

    def quality(self):
        return self['uq']

    def source(self):
        return self['ap']

    def source_group(self):
        return self['ui']

    def expressions(self):
        return self['ex']