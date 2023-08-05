# Copyright (c) 2018-2019 Patricio Cubillos and contributors.
# bibmanager is open-source software under the MIT license (see LICENSE).

__all__ = [
  # Constants:
  'HOME', 'ROOT', 'BM_DATABASE', 'BM_BIBFILE', 'BM_TMP_BIB', 'BM_CACHE',
  'BOLD', 'END', 'BANNER',
  # Named tuples
  'Author', 'Sort_author',
  # Context managers:
  'ignored', 'cd',
  # Functions:
  'ordinal', 'count', 'nest', 'cond_split', 'cond_next',
  'parse_name', 'repr_author', 'purify', 'initials',
  'next_char', 'last_char', 'get_fields', 'req_input'
  ]

import os
import re
import numpy as np
from contextlib import contextmanager
from collections import namedtuple


# Directories/files:
HOME = os.path.expanduser("~") + "/.bibmanager/"
ROOT = os.path.realpath(os.path.dirname(__file__)) + '/'

BM_DATABASE = HOME + "bm_database.pickle"
BM_BIBFILE  = HOME + "bm_bibliography.bib"
BM_TMP_BIB  = HOME + "tmp_bibliography.bib"
BM_CACHE    = HOME + "cached_ads_querry.pickle"

# Unicode to start/end bold-face syntax:
BOLD = '\033[1m'
END  = '\033[0m'

# A delimiter:
BANNER = "\n" + ":"*70 + "\n"

# Named tuples:
Author      = namedtuple("Author",      "last first von jr")
Sort_author = namedtuple("Sort_author", "last first von jr year month")


# Context managers:
@contextmanager
def ignored(*exceptions):
  """
  Context manager to ignore exceptions. Taken from here:
  https://www.youtube.com/watch?v=anrOzOapJ2E
  """
  try:
      yield
  except exceptions:
      pass


@contextmanager
def cd(newdir):
  """
  Context manager for changing the current working directory.
  Taken from here: https://stackoverflow.com/questions/431684/
  """
  olddir = os.getcwd()
  os.chdir(os.path.expanduser(newdir))
  try:
      yield
  finally:
      os.chdir(olddir)


# Functions:
def ordinal(number):
  """
  Get ordinal string representation for input number(s).

  Parameters
  ----------
  number: Integer or 1D integer ndarray
     An integer or array of integers.

  Returns
  -------
  ord: String or List of strings
     Ordinal representation of input number(s).  Return a string if
     input is int; else, return a list of strings.

  Examples
  --------
  >>> from utils import ordinal
  >>> print(ordinal(1))
  1st
  >>> print(ordinal(2))
  2nd
  >>> print(ordinal(11))
  11th
  >>> print(ordinal(111))
  111th
  >>> print(ordinal(121))
  121st
  >>> print(ordinal(np.arange(1,6)))
  ['1st', '2nd', '3rd', '4th', '5th']
  """
  ending = ["th", "st", "nd", "rd"]
  unit = number % 10
  teen = (number//10) % 10 != 1
  idx = unit * (unit<4) * teen
  if type(number) is int:
      return f"{number}{ending[idx]}"
  return [f"{n}{ending[i]}" for n,i in zip(number,idx)]


def count(text):
  """
  Count net number of braces in text (add 1 for each opening brace,
  subtract one for each closing brace).

  Parameters
  ----------
  text: String
     A string.

  Returns
  -------
  counts: Integer
     Net number of braces.

  Examples
  --------
  >>> from utils import count
  >>> count('{Hello} world')
  0
  """
  return text.count("{") - text.count("}")


def nest(text):
  r"""
  Get braces nesting level for each character in text.

  Parameters
  ----------
  text: String
     String to inspect.

  Returns
  -------
  counts: 1D integer list
     Braces nesting level for each character.

  Examples
  --------
  >>> from utils import nest
  >>> s = "{{P\\'erez}, F. and {Granger}, B.~E.},"
  >>> n = nest(s)
  >>> print(f"{s}\n{''.join([str(v) for v in n])}")
  {{P\'erez}, F. and {Granger}, B.~E.},
  0122222222111111111122222222111111110
  """
  counts = np.zeros(len(text), int)
  for i,s in enumerate(text[:-1]):
      if s == "{":
          counts[i+1] = counts[i] + 1
      elif s == "}":
          counts[i+1] = counts[i] - 1
      else:
          counts[i+1] = counts[i]
  return counts


def cond_split(text, pattern, nested=None, nlev=-1, ret_nests=False):
  r"""
  Conditional find and split strings in a text delimited by all
  occurrences of pattern where the brace-nested level is nlev.

  Parameters
  ----------
  text: String
     String where to search for pattern.
  pattern: String
     A regex pattern to search.
  nested: 1D integer iterable
     Braces nesting level of characters in text.
  nlev: Integer
     Required nested level to accept pattern match.
  ret_nests: Bool
     If True, return a list with the arrays of nested level for each
     of the returned substrings.

  Returns
  -------
  substrings: List of strings
     List of strings delimited by the accepted pattern matches.
  nests: List of integer ndarrays [optional]
     nested level for substrings.

  Examples
  --------
  >>> from utils import cond_split
  >>> # Split an author list string delimited by ' and ' pattern:
  >>> cond_split("{P\\'erez}, F. and {Granger}, B.~E.", " and ")
  ["{P\\'erez}, F.", '{Granger}, B.~E.']
  >>> # Protected instances (within braces) won't count:
  >>> cond_split("{AAS and Astropy Teams} and {Hendrickson}, A.", " and ")
  ['{AAS and Astropy Teams}', '{Hendrickson}, A.']
  >>> # Matches at the beginning or end do not count for split:
  >>> cond_split(",Jones, Oliphant, Peterson,", ",")
  ['Jones', ' Oliphant', ' Peterson']
  >>> # But two consecutive matches do return an empty string:
  >>> cond_split("Jones,, Peterson", ",")
  ['Jones', '', ' Peterson']
  """
  if nested is None:
      nested = nest(text)

  if nlev == -1 and len(nested) > 0:
      nlev = nested[0]

  # First and last indices of each pattern match:
  bounds = [(m.start(0), m.end(0))
            for m in re.finditer(pattern, text)
            if nested[m.start(0)] == nlev]

  flat_bounds = [item for sublist in bounds for item in sublist]

  # No matches:
  if len(flat_bounds) == 0:
      if ret_nests:
          return [text], [nested]
      return [text]

  # Matches, parse substrings:
  if flat_bounds[0] != 0:
      flat_bounds.insert(0, 0)
  else:
      flat_bounds.pop(0)
  if flat_bounds[-1] != len(text):
      flat_bounds.append(len(text))
  pairs = zip(*([iter(flat_bounds)]*2))
  substrings = [text[start:end] for (start,end) in pairs]
  if ret_nests:
      pairs = zip(*([iter(flat_bounds)]*2))
      nests = [nested[start:end] for (start,end) in pairs]
      return substrings, nests
  return substrings


def cond_next(text, pattern, nested, nlev=1):
  """
  Find next instance of pattern in text where nested is nlev.

  Parameters
  ----------
  text: String
     Text where to search for regex.
  pattern: String
     Regular expression to search for.
  nested: 1D integer iterable
     Braces-nesting level of characters in text.
  nlev: Integer
     Requested nested level.

  Returns
  -------
     Index integer of pattern in text.  If not found, return the
     index of the last character in text.

  Examples
  --------
  >>> from utils import nest, cond_next
  >>> text = '"{{HITEMP}, the high-temperature molecular database}",'
  >>> nested = nest(text)
  >>> # Ignore comma within braces:
  >>> cond_next(text, ",", nested, nlev=0)
  53
  """
  for m in re.finditer(pattern, text):
      if nested[m.start(0)] == nlev:
          return m.start(0)
  # If not found, return last index in text:
  return len(text) - 1


#@functools.lru_cache(maxsize=1024, typed=False)
def parse_name(name, nested=None):
  r"""
  Parse first, last, von, and jr parts from a name, following these rules:
  http://mirror.easyname.at/ctan/info/bibtex/tamethebeast/ttb_en.pdf
  Page 23.

  Parameters
  ----------
  name: String
     A name following the BibTeX format.
  nested: 1D integer ndarray
     Nested level of characters in name.

  Returns
  -------
  author: Author namedtuple
     Four element tuple with the parsed name.

  Examples
  --------
  >>> from utils import parse_name
  >>> names = ['{Hendrickson}, A.',
  >>>          'Eric Jones',
  >>>          '{AAS Journals Team}',
  >>>          "St{\\'{e}}fan van der Walt"]
  >>> for name in names:
  >>>     print(f'{repr(name)}:\n{parse_name(name)}\n')
  '{Hendrickson}, A.':
  Author(last='{Hendrickson}', first='A.', von='', jr='')
  
  'Eric Jones':
  Author(last='Jones', first='Eric', von='', jr='')
  
  '{AAS Journals Team}':
  Author(last='{AAS Journals Team}', first='', von='', jr='')
  
  "St{\\'{e}}fan van der Walt":
  Author(last='Walt', first="St{\\'{e}}fan", von='van der', jr='')
  """
  if nested is None:
      nested = nest(name)
  name = " ".join(cond_split(name, "~", nested=nested))
  fields, nests = cond_split(name, ",", nested=nested, ret_nests=True)
  if len(fields) > 3:
      raise ValueError("Invalid BibTeX format for author '{name}'.")

  # 'First von Last' format:
  if len(fields) == 1:
      jr = ""
      words = cond_split(name, " ", nested=nested)
      lowers = [s[0].islower() for s in words[:-1]]
      if np.any(lowers):
          ifirst = np.min(np.where(lowers))
          ilast  = np.max(np.where(lowers)) + 1
      else:
          ifirst = ilast = len(words) - 1
      first = " ".join(words[0:ifirst])
      von   = " ".join(words[ifirst:ilast])
      last  = " ".join(words[ilast:])

  else:
      istart = next_char(fields[0])
      iend   = last_char(fields[0])
      vonlast = fields[0][istart:iend]
      nested  = nests [0][istart:iend]
      if vonlast.strip() == "":
          raise ValueError(f"Invalid BibTeX format for author '{name}', it "
                           "does not have a last name.")

      # 'von Last, First' format:
      if len(fields) == 2:
          jr = ""
          first = fields[1].strip()

      # 'von Last, Jr, First' format:
      elif len(fields) == 3:
          jr    = fields[1].strip()
          first = fields[2].strip()

      words = cond_split(vonlast, " ", nested=nested)
      lowers = [s[0].islower() for s in words[:-1]]

      if np.any(lowers):
          ilast = np.max(np.where(lowers)) + 1
          von = " ".join(words[:ilast])
      else:
          von = ""
          ilast = 0
      last = " ".join(words[ilast:])

  return Author(last=last, first=first, von=von, jr=jr)


def repr_author(Author):
  """
  Get string representation an Author namedtuple in the format:
  von Last, jr., First.

  Parameters
  ----------
  Author: An Author() namedtuple
     An author name.

  Examples
  --------
  >>> from utils import repr_author, parse_name
  >>> names = ['Last', 'First Last', 'First von Last', 'von Last, First',
  >>>          'von Last, sr., First']
  >>> for name in names:
  >>>     print(f"{name!r:22}: {repr_author(parse_name(name))}")
  'Last'                : Last
  'First Last'          : Last, First
  'First von Last'      : von Last, First
  'von Last, First'     : von Last, First
  'von Last, sr., First': von Last, sr., First
  """
  name = Author.last
  if Author.von != "":
      name = " ".join([Author.von, name])
  if Author.jr != "":
      name += f", {Author.jr}"
  if Author.first != "":
      name += f", {Author.first}"
  return name


#@functools.lru_cache(maxsize=1024, typed=False)
def purify(name, german=False):
  r"""
  Replace accented characters closely following these rules:
  https://tex.stackexchange.com/questions/57743/
  For a more complete list of special characters, see Table 2.2 of
  'The Not so Short Introduction to LaTeX2e' by Oetiker et al. (2008).

  Parameters
  ----------
  name: String
     Name to be 'purified'.
  german: Bool
     Replace umlaut with german style (append 'e' after).

  Returns
  -------
  Lower-cased name without accent characters.

  Examples
  --------
  >>> from utils import purify
  >>> names = ["St{\\'{e}}fan",
               "{{\\v S}ime{\\v c}kov{\\'a}}",
               "{AAS Journals Team}",
               "Kov{\\'a}{\\v r}{\\'i}k",
               "Jarom{\\'i}r Kov{\\'a\\v r\\'i}k",
               "{\\.I}volgin",
               "Gon{\\c c}alez Nu{\~n}ez",
               "Knausg{\\aa}rd Sm{\\o}rrebr{\\o}d",
               'Schr{\\"o}dinger Be{\\ss}er']

  >>> for name in names:
  >>>     print(f"{name!r:35}: {purify(name)}")
  "St{\\'{e}}fan"                     : stefan
  "{{\\v S}ime{\\v c}kov{\\'a}}"      : simeckova
  '{AAS Journals Team}'               : aas journals team
  "Kov{\\'a}{\\v r}{\\'i}k"           : kovarik
  "Jarom{\\'i}r Kov{\\'a\\v r\\'i}k"  : jaromir kovarik
  '{\\.I}volgin'                      : ivolgin
  'Gon{\\c c}alez Nu{\\~n}ez'         : goncalez nunez
  'Knausg{\\aa}rd Sm{\\o}rrebr{\\o}d' : knausgaard smorrebrod
  'Schr{\\"o}dinger Be{\\ss}er'       : schrodinger besser
  """
  # German umlaut replace:
  if german:
      for pattern in ["a", "o", "u"]:
          name = re.sub(fr'\\"{pattern}', pattern+"e", name)
  # Remove special:
  name = re.sub(r"\\(\"|\^|`|\.|'|~)", "", name)
  # Remove special + white space:
  name = re.sub(r"\\(c |u |H |v |d |b |t )", "", name)
  # Replace pattern:
  for pattern in ["o", "O", "l", "L", "i", "j",
                  "aa", "AA", "AE", "oe", "OE", "ss"]:
      name = re.sub(fr"\\{pattern}", pattern, name)
  # Remove braces, clean up, and return:
  return re.sub("({|})", "", name).strip().lower()


def initials(name):
  r"""
  Get initials from a name.

  Parameters
  ----------
  name: String
     A name.

  Returns
  -------
  initials: String
     Name initials (lower cased).

  Examples
  --------
  >>> from utils import initials
  >>> names = ["", "D.", "D. W.", "G.O.", '{\\"O}. H.', "J. Y.-K.",
  >>>          "Phil", "Phill Henry Scott"]
  >>> for name in names:
  >>>     print(f"{name!r:20}: {initials(name)!r}")
  ''                  : ''
  'D.'                : 'd'
  'D. W.'             : 'dw'
  'G.O.'              : 'g'
  '{\\"O}. H.'        : 'oh'
  'J. Y.-K.'          : 'jyk'
  'Phil'              : 'p'
  'Phill Henry Scott' : 'phs'
  >>> # 'G.O.' is a typo by the user, should have had a blank in between.
  """
  name = purify(name)
  split_names = name.replace("-", " ").split()
  # Somehow string[0:1] does not break when string = "", unlike string[0].
  return "".join([name[0:1] for name in split_names])


def get_authors(authors, short=True):
  """
  Get string representation for the author list.

  Parameters
  ----------
  authors: List of Author() nametuple
  short: Bool
     If True, use 'short' format displaying at most the first two
     authors followed by 'et al.' if corresponds.
     If False, display the full list of authors.

  Examples
  --------
  >>> from utils import get_authors, parse_name
  >>> author_lists = [
  >>>     [parse_name('{Hunter}, J. D.')],
  >>>     [parse_name('{AAS Journals Team}'), parse_name('{Hendrickson}, A.')],
  >>>     [parse_name('Eric Jones'), parse_name('Travis Oliphant'),
  >>>      parse_name('Pearu Peterson'), parse_name('others')]
  >>>    ]
  >>> # Short format:
  >>> for i,authors in enumerate(author_lists):
  >>>     print(f"{i+1} author(s): {get_authors(authors)}")
  1 author(s): {Hunter}, J. D.
  2 author(s): {AAS Journals Team} and {Hendrickson}, A.
  3 author(s): Jones, Eric; et al.
  >>> # Long format:
  >>> for i,authors in enumerate(author_lists):
  >>>     print(f"{i+1} author(s): {get_authors(authors, short=False)}")
  1 author(s): {Hunter}, J. D.
  2 author(s): {AAS Journals Team} and {Hendrickson}, A.
  3 author(s): Jones, Eric; Oliphant, Travis; Peterson, Pearu; and others
  """
  if len(authors) <= 2:
      return " and ".join([repr_author(author) for author in authors])

  if not short:
      author_list = [repr_author(author) for author in authors]
      authors = "; ".join(author_list[:-1])
      return authors + "; and " + author_list[-1]
  else:
      return repr_author(authors[0]) + "; et al."


def next_char(text):
  r"""
  Get index of next non-blank character in string text.
  Return zero if all characters are blanks.

  Parameters
  ----------
  text: String
     A string, duh!.

  Examples
  --------
  >>> from utils import next_char
  >>> texts = ["Hello", "  Hello", "  Hello ", "", "\n Hello", "  "]
  >>> for text in texts:
  >>>     print(f"{text!r:11}: {next_char(text)}")
  'Hello'    : 0
  '  Hello'  : 2
  '  Hello ' : 2
  ''         : 0
  '\n Hello' : 2
  '  '       : 0
  """
  nchars = len(text)
  # Empty string:
  if nchars == 0:
      return 0
  i = 0
  while text[i].isspace():
      i += 1
      # Reach end of string, all characters blanks:
      if i == nchars:
          return 0
  return i


def last_char(text):
  r"""
  Get index of last non-blank character in string text.

  Parameters
  ----------
  text: String
     A string, duh!.

  Examples
  --------
  >>> from utils import last_char
  >>> texts = ["Hello", "  Hello", "  Hello  ", "", "\n Hello", "  "]
  >>> for text in texts:
  >>>     print(f"{text!r:12}: {last_char(text)}")
  'Hello'     : 5
  '  Hello'   : 7
  '  Hello  ' : 7
  ''          : 0
  '\n Hello'  : 7
  '  '        : 0
  """
  i = len(text)
  if i == 0:
      return 0
  while text[i-1].isspace() and i>0:
      i -= 1
  return i


def get_fields(entry):
  r"""
  Generator to parse entries of a bibbliographic entry.

  Parameters
  ----------
  entry: String
     A bibliographic entry text.

  Yields
  ------
  The first yield is the entry's key.  All following yields are
  three-element tuples containing a field name, field value, and
  nested level of the field value.

  Notes
  -----
  Global quotations or braces on a value are removed before yielding.

  Example
  -------
  >>> from utils import get_fields
  >>> entry = '''
  @Article{Hunter2007ieeeMatplotlib,
    Author    = {{Hunter}, J. D.},
    Title     = {Matplotlib: A 2D graphics environment},
    Journal   = {Computing In Science \& Engineering},
    Volume    = {9},
    Number    = {3},
    Pages     = {90--95},
    publisher = {IEEE COMPUTER SOC},
    doi       = {10.1109/MCSE.2007.55},
    year      = 2007
  }'''
  >>> fields = get_fields(entry)
  >>> # Get the entry's key:
  >>> print(next(fields))
  Hunter2007ieeeMatplotlib
  >>> # Now get the fields, values, and nested level:
  >>> for key, value, nested in fields:
  >>>   print(f"{key:9}: {value}\n{'':11}{''.join([str(v) for v in nested])}")
  author   : {Hunter}, J. D.
             233333332222222
  title    : Matplotlib: A 2D graphics environment
             2222222222222222222222222222222222222
  journal  : Computing In Science \& Engineering
             22222222222222222222222222222222222
  volume   : 9
             2
  number   : 3
             2
  pages    : 90--95
             222222
  publisher: IEEE COMPUTER SOC
             22222222222222222
  doi      : 10.1109/MCSE.2007.55
             22222222222222222222
  year     : 2007
             1111
  """
  # First yield is the key:
  nested = list(nest(entry))
  start = nested.index(1)
  loc   = entry.index(",")
  yield entry[start:loc]
  loc += 1

  # Next equal sign delimits key:
  while entry[loc:].find("=") >= 0:
      eq  = entry[loc:].find("=")
      key = entry[loc:loc+eq].strip().lower()
      # next non-blank character:
      start = loc + eq + 1 + next_char(entry[loc+eq+1:])

      if entry[start] == "{":
          end = start + nested[start+1:].index(1)
          start += 1
      elif entry[start] == '"':
          start += 1
          end = start + cond_next(entry[start:], '"', nested[start:], nlev=1)
      else:
          end = start + cond_next(entry[start:], ",", nested[start:], nlev=1)
      start += next_char(entry[start:end])
      end = start + last_char(entry[start:end])
      loc = end + np.clip(entry[end:].find(","), 0, len(entry)) + 1
      yield key, entry[start:end], nested[start:end]


def req_input(prompt, options):
  """
  Query for an aswer to prompt message until the user provides a
  valid input (i.e., answer is in options).

  Parameters
  ----------
  prompt: String
     Prompt text for input()'s argument.
  options: List
     List of options to accept.  Elements in list are casted into strings.

  Returns
  -------
  answer: String
     The user's input.

  Examples
  --------
  >>> from utils import req_input
  >>> req_input('Enter number between 0 and 9: ', options=np.arange(10))
  >>> # Enter the number 10:
  Enter number between 0 and 9: 10
  >>> # Now enter the number 5:
  Not a valid input.  Try again: 5
  '5'
  """
  # Cast options as str:
  options = [str(option) for option in options]

  answer = input(prompt)
  while answer not in options:
      answer = input("Not a valid input.  Try again: ")
  return answer
