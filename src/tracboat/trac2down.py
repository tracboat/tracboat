# -*- coding: utf-8 -*-
# Linting disabled, pulled in original file without modifying
# pylint: skip-file
# flake8: noqa

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python fileencoding=utf-8
'''
Copyright © 2013
    Eric van der Vlist <vdv@dyomedea.com>
    Shigeru KANEMOTO <support@switch-science.com>
Copyright © 2017-2018
    Elan Ruusamäe <glen@pld-linux.org>

See license information at the bottom of this file
'''

from __future__ import division
import datetime
import re
import os
import codecs
from pprint import pprint
from sys import exit

import six

def convert(text, base_path, multilines=True, note_map={}, attachments_path=None, svn2git_revisions={}):
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

    # https://stackoverflow.com/a/16891418/2314626
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    attachment_re = re.compile(r"""
        \[\[attachment:
            (?P<filename>.+?        # match filename
                (:(?P<type>.+?)     # match optional type
                    (:(?P<id>.+?))? # match optional id (optional with type)
                )?
            )
        \]\] |
        # alternative without brackets
        attachment:(?P<filename2>\S+)
    """, re.X)
    def attachment_replace(m):
        """
        @link https://trac.edgewall.org/wiki/TracLinks#attachment:links

        The link syntax for attachments is as follows:

            attachment:the_file.txt creates a link to the attachment the_file.txt of the current object
            attachment:the_file.txt:wiki:MyPage creates a link to the attachment the_file.txt of the MyPage wiki page
            attachment:the_file.txt:ticket:753 creates a link to the attachment the_file.txt of the ticket 753

        see attachments: [[attachment:x.req]] and [[attachment:req.log]])
        -> [req.log](/uploads/issue_142/req.log)

        """
        d = m.groupdict()
        d['attachments_path'] = attachments_path
        if d['filename2']:
            d['filename'] = d['filename2']
        return "[%(filename)s](%(attachments_path)s/%(filename)s)" % d

    source_re = re.compile(r"""
        # default one with brackets
        \[source:
            (?P<path>[^]]+)
        \] |

        # alternative without brackets
        source:(?P<path2>\S+)

    """, re.X)
    def source_replace(m):
        """
        @link https://trac.edgewall.org/wiki/TracLinks#source:links

         - `source:` and `browser:`
             * simple paths (/dir/file)
             * paths at a given revision (/dir/file@234)
             * paths with line number marks (/dir/file@234:10,20-30)
             * paths with line number anchor (/dir/file@234#L100)
            Marks and anchor can be combined.
            The revision must be present when specifying line numbers.
            In the few cases where it would be redundant (e.g. for tags), the
            revision number itself can be omitted: /tags/v10/file@100-110#L99

        """
        d = m.groupdict()
        path = str(d.get('path', d.get('path2')))
        path = remove_prefix(path, '/trunk/') # remove branch name, assume default branch
        path = remove_prefix(path, '/') # remove leading slash, it would not point to source otherwise
        d.update({
            'git_path' : path,
        })
        return "[%(git_path)s](%(git_path)s)" % d

    reply_re = re.compile(r'Replying to \[(?P<type>comment|ticket):(?P<id>\d+)\s+(?P<username>[^]]+)\]:')
    def reply_replace(m):
        """
        Replying to [comment:4 glen]:
        Replying to [ticket:41 katlyn]:
        """

        d = m.groupdict()
        link_id = int(d['id'])
        if d['type'] == 'comment':
            # fallback to original id, can be fixed manually after import
            note_id = note_map.get(link_id, link_id)
            d['link'] = '#note_%d' % note_id
            return "Replying to [%(username)s](%(link)s):" % d
        elif d['type'] == 'ticket':
            d['link'] = '#%d' % link_id
        else:
            raise Exception("Unsupported type: %s" % d['type'])

        return "Replying to [%(username)s](%(link)s):" % d

    commit_re = re.compile(r"""
        \[(?P<revision>\d+)\] | # revision in brackets
        r(?P<revision2>\d+) |   # revision with r-prefix
        \[(?P<rev1>\d+)-(?P<rev2>\d+)\] # revision range
    """, re.X)
    def commit_replace(m):
        """
        (In [35214])
        [36859], [36860]
        Changesets [36872-36874]
        """
        d = m.groupdict()
        d[0] = str(m.group(0))
        if d['rev1'] and d['rev2']:
            d['rev1'] = svn2git_revisions.get(d['rev1'])
            d['rev2'] = svn2git_revisions.get(d['rev2'])

            return "[%(rev1)s..%(rev2)s](../compare/%(rev1)s...%(rev2)s)" % d
        else:
            revision = str(d.get('revision', d.get('revision2')))
            d['git_hash'] = svn2git_revisions.get(revision, d[0])

            return "%(git_hash)s" % d

    image_re = re.compile(r'\[\[Image\((?:(?P<module>(?:source|wiki)):)?(?P<path>[^)]+)\)\]\]')
    def image_replace(m):
        """
        https://trac.edgewall.org/wiki/WikiFormatting#Images

        [[Image(picture.gif)]] Current page (Ticket, Wiki, Comment)

        [[Image(wiki:WikiFormatting:picture.gif)]] (referring to attachment on another page)
        [[Image(ticket:1:picture.gif)]] (file attached to a ticket)
        [[Image(htdocs:picture.gif)]] (referring to a file inside the environment htdocs directory)
        [[Image(source:/trunk/trac/htdocs/trac_logo_mini.png)]] (a file in repository)
        """

        module = m.group('module')
        path = m.group('path')

        d = m.groupdict()
        d.update({
            'base_path': os.path.relpath('/tree/master/', base_path),
            'upload_path' : '/uploads/migrated/%s' % path,
        })

        if module == 'source':
            return '![](%(base_path)s/%(path)s)' % d
        elif module == 'wiki':
            id, file = path.split(':', 2)
            d['upload_path'] = '/uploads/migrated/%s' % file
            d['file'] = file
            return '![%(file)s](%(upload_path)s)' % d
        else:
            if path.startswith('http'):
                # [[Image(http://example.org/s.jpg)]]
                return '![%(path)s](%(path)s)' % d
            else:
                return '![%(path)s](%(upload_path)s)' % d

    a = []
    is_table = False
    for line in text.split('\n'):
        # not blockquote?
        if not line.startswith('    '):
            line = re.sub(r'\[(https?://[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](\1)', line)
            line = re.sub(r'\[wiki:([^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](%s/\1)' % os.path.relpath('/wikis/', base_path), line)
            line = re.sub(r'\[wiki:([^\s\[\]]+)\]', r'[\1](\1)', line)
            line = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'\1', line)

            line = source_re.sub(source_replace, line)
            line = image_re.sub(image_replace, line)
            line = reply_re.sub(reply_replace, line)
            line = attachment_re.sub(attachment_replace, line)
            line = commit_re.sub(commit_replace, line)

            # bold
            line = re.sub(r"'''(.*?)'''", r'**\1**', line)
            # italic
            line = re.sub(r"''(.*?)''", r'_\1_', line)
            # tables?
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

def save_file(text, name, version, date, author, path):
    # We need to create a directory structure matching the hierarchical
    # page title, e.g.:
    # name == 'Chapter1/Main'
    # the output file will be:
    # Chapter1/Main.md
    components = name.split("/")
    name = components[-1]
    levels = components[:-1]
    if levels:
        path = os.path.join(path, *levels)
        if not os.path.exists(path):
            os.makedirs(path)
    filename = os.path.join(path, name + '.md')
    with codecs.open(filename, 'w', encoding='utf-8') as fp:
        # print >>fp, '<!-- Name: %s -->' % name
        # print >>fp, '<!-- Version: %d -->' % version
        # print >>fp, '<!-- Last-Modified: %s -->' % date
        # print >>fp, '<!-- Author: %s -->' % author
        fp.write(text)

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
