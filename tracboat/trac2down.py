# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python fileencoding=utf-8
'''
Copyright © 2013
    Eric van der Vlist <vdv@dyomedea.com>
    Shigeru KANEMOTO <support@switch-science.com>
See license information at the bottom of this file
'''

from __future__ import division
import datetime
import re
import os
import codecs


def convert(text, base_path, multilines=True):
    text = re.sub('\r\n', '\n', text)
    text = re.sub(r'{{{(.*?)}}}', r'`\1`', text)
    text = re.sub(r'(?sm){{{(\n?#![^\n]+)?\n(.*?)\n}}}', r'```\n\2\n```', text)

    text = text.replace('[[TOC]]', '')
    text = text.replace('[[BR]]', '\n')
    text = text.replace('[[br]]', '\n')

    if multilines:
        text = re.sub(r'^\S[^\n]+([^=-_|])\n([^\s`*0-9#=->-_|])', r'\1 \2', text)

    text = re.sub(r'(?m)^======\s+(.*?)\s+======$', r'###### \1', text)
    text = re.sub(r'(?m)^=====\s+(.*?)\s+=====$', r'##### \1', text)
    text = re.sub(r'(?m)^====\s+(.*?)\s+====$', r'#### \1', text)
    text = re.sub(r'(?m)^===\s+(.*?)\s+===$', r'### \1', text)
    text = re.sub(r'(?m)^==\s+(.*?)\s+==$', r'## \1', text)
    text = re.sub(r'(?m)^=\s+(.*?)\s+=$', r'# \1', text)
    text = re.sub(r'^             * ', r'****', text)
    text = re.sub(r'^         * ', r'***', text)
    text = re.sub(r'^     * ', r'**', text)
    text = re.sub(r'^ * ', r'*', text)
    text = re.sub(r'^ \d+. ', r'1.', text)

    a = []
    is_table = False
    for line in text.split('\n'):
        if not line.startswith('    '):
            line = re.sub(r'\[(https?://[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](\1)', line)
            line = re.sub(r'\[wiki:([^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](%s/\1)' % os.path.relpath('/wikis/', base_path), line)
            line = re.sub(r'\[wiki:([^\s\[\]]+)\]', r'[\1](\1)', line)
            line = re.sub(r'\[source:([^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](%s/\1)' % os.path.relpath('/tree/master/', base_path), line)
            line = re.sub(r'source:([\S]+)', r'[\1](%s/\1)' % os.path.relpath('/tree/master/', base_path), line)
            line = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'\1', line)
            line = re.sub(r'\[\[Image\(source:([^(]+)\)\]\]', r'![](%s/\1)' % os.path.relpath('/tree/master/', base_path), line)
            line = re.sub(r'\[\[Image\(wiki:([^\s\[\]]+):([^\s\[\]]+)\)\]\]', r'![\2](/uploads/migrated/\2)', line)
            line = re.sub(r'\[\[Image\(([^(]+)\)\]\]', r'![\1](/uploads/migrated/\1)', line)
            line = re.sub(r'\'\'\'(.*?)\'\'\'', r'*\1*', line)
            line = re.sub(r'\'\'(.*?)\'\'', r'_\1_', line)
            if line.startswith('||'):
                if not is_table:
                    sep = re.sub(r'[^|]', r'-', line)
                    line = line + '\n' + sep
                    is_table = True
                line = re.sub(r'\|\|', r'|', line)
            else:
                is_table = False
        else:
            is_table = False
        a.append(line)
    text = '\n'.join(a)
    return text


def save_file(text, name, version, date, author, directory):
    folders = name.rsplit("/", 1)
    if not os.path.exists("%s%s" % (directory, folders[0])):
        os.makedirs("%s%s" % (directory, folders[0]))
    fp = codecs.open('%s%s.md' % (directory, name), 'w', encoding='utf-8')
    # print >>fp, '<!-- Name: %s -->' % name
    # print >>fp, '<!-- Version: %d -->' % version
    # print >>fp, '<!-- Last-Modified: %s -->' % date
    # print >>fp, '<!-- Author: %s -->' % author
    fp.write(unicode(text))
    fp.close()


if __name__ == "__main__":
    SQL = '''
    select
            name, version, time, author, text
        from
            wiki w
        where
            version = (select max(version) from wiki where name = w.name)
'''

    import sqlite3

    conn = sqlite3.connect('../trac.db')
    result = conn.execute(SQL)
    for row in result:
        name = row[0]
        version = row[1]
        time = row[2]
        author = row[3]
        text = row[4]
        text = convert(text, '/wikis/')
        try:
            time = datetime.datetime.fromtimestamp(time).strftime('%Y/%m/%d %H:%M:%S')
        except ValueError:
            time = datetime.datetime.fromtimestamp(time / 1000000).strftime('%Y/%m/%d %H:%M:%S')
        save_file(text, name, version, time, author, 'wiki/')

'''
This file is part of <https://gitlab.dyomedea.com/vdv/trac-to-gitlab>.

This sotfware is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This sotfware is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library. If not, see <http://www.gnu.org/licenses/>.
'''
