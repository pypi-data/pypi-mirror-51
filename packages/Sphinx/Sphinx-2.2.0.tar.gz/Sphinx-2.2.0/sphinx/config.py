"""
    sphinx.config
    ~~~~~~~~~~~~~

    Build configuration file handling.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
import traceback
import types
import warnings
from collections import OrderedDict
from os import path, getenv
from typing import Any, NamedTuple, Union

from sphinx.deprecation import RemovedInSphinx30Warning, RemovedInSphinx40Warning
from sphinx.errors import ConfigError, ExtensionError
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.i18n import format_date
from sphinx.util.osutil import cd
from sphinx.util.pycompat import execfile_
from sphinx.util.typing import NoneType

if False:
    # For type annotation
    from typing import Callable, Dict, Generator, Iterator, List, Set, Tuple  # NOQA
    from sphinx.application import Sphinx  # NOQA
    from sphinx.environment import BuildEnvironment  # NOQA
    from sphinx.util.tags import Tags  # NOQA

logger = logging.getLogger(__name__)

CONFIG_FILENAME = 'conf.py'
UNSERIALIZABLE_TYPES = (type, types.ModuleType, types.FunctionType)
copyright_year_re = re.compile(r'^((\d{4}-)?)(\d{4})(?=[ ,])')

ConfigValue = NamedTuple('ConfigValue', [('name', str),
                                         ('value', Any),
                                         ('rebuild', Union[bool, str])])


def is_serializable(obj):
    # type: (Any) -> bool
    """Check if object is serializable or not."""
    if isinstance(obj, UNSERIALIZABLE_TYPES):
        return False
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if not is_serializable(key) or not is_serializable(value):
                return False
    elif isinstance(obj, (list, tuple, set)):
        return all(is_serializable(i) for i in obj)

    return True


class ENUM:
    """represents the config value should be a one of candidates.

    Example:
        app.add_config_value('latex_show_urls', 'no', None, ENUM('no', 'footnote', 'inline'))
    """
    def __init__(self, *candidates):
        # type: (str) -> None
        self.candidates = candidates

    def match(self, value):
        # type: (Union[str, List, Tuple]) -> bool
        if isinstance(value, (list, tuple)):
            return all(item in self.candidates for item in value)
        else:
            return value in self.candidates


# RemovedInSphinx40Warning
string_classes = [str]  # type: List


class Config:
    """Configuration file abstraction.

    The config object makes the values of all config values available as
    attributes.

    It is exposed via the :py:attr:`sphinx.application.Application.config` and
    :py:attr:`sphinx.environment.Environment.config` attributes. For example,
    to get the value of :confval:`language`, use either ``app.config.language``
    or ``env.config.language``.
    """

    # the values are: (default, what needs to be rebuilt if changed)

    # If you add a value here, don't forget to include it in the
    # quickstart.py file template as well as in the docs!

    config_values = {
        # general options
        'project': ('Python', 'env', []),
        'author': ('unknown', 'env', []),
        'copyright': ('', 'html', []),
        'version': ('', 'env', []),
        'release': ('', 'env', []),
        'today': ('', 'env', []),
        # the real default is locale-dependent
        'today_fmt': (None, 'env', [str]),

        'language': (None, 'env', [str]),
        'locale_dirs': (['locales'], 'env', []),
        'figure_language_filename': ('{root}.{language}{ext}', 'env', [str]),

        'master_doc': ('index', 'env', []),
        'source_suffix': ({'.rst': 'restructuredtext'}, 'env', Any),
        'source_encoding': ('utf-8-sig', 'env', []),
        'source_parsers': ({}, 'env', []),
        'exclude_patterns': ([], 'env', []),
        'default_role': (None, 'env', [str]),
        'add_function_parentheses': (True, 'env', []),
        'add_module_names': (True, 'env', []),
        'trim_footnote_reference_space': (False, 'env', []),
        'show_authors': (False, 'env', []),
        'pygments_style': (None, 'html', [str]),
        'highlight_language': ('default', 'env', []),
        'highlight_options': ({}, 'env', []),
        'templates_path': ([], 'html', []),
        'template_bridge': (None, 'html', [str]),
        'keep_warnings': (False, 'env', []),
        'suppress_warnings': ([], 'env', []),
        'modindex_common_prefix': ([], 'html', []),
        'rst_epilog': (None, 'env', [str]),
        'rst_prolog': (None, 'env', [str]),
        'trim_doctest_flags': (True, 'env', []),
        'primary_domain': ('py', 'env', [NoneType]),   # type: ignore
        'needs_sphinx': (None, None, [str]),
        'needs_extensions': ({}, None, []),
        'manpages_url': (None, 'env', []),
        'nitpicky': (False, None, []),
        'nitpick_ignore': ([], None, []),
        'numfig': (False, 'env', []),
        'numfig_secnum_depth': (1, 'env', []),
        'numfig_format': ({}, 'env', []),  # will be initialized in init_numfig_format()

        'math_number_all': (False, 'env', []),
        'math_eqref_format': (None, 'env', [str]),
        'math_numfig': (True, 'env', []),
        'tls_verify': (True, 'env', []),
        'tls_cacerts': (None, 'env', []),
        'smartquotes': (True, 'env', []),
        'smartquotes_action': ('qDe', 'env', []),
        'smartquotes_excludes': ({'languages': ['ja'],
                                  'builders': ['man', 'text']},
                                 'env', []),
    }  # type: Dict[str, Tuple]

    def __init__(self, *args):
        # type: (Any) -> None
        if len(args) == 4:
            # old style arguments: (dirname, filename, overrides, tags)
            warnings.warn('The argument of Config() class has been changed. '
                          'Use Config.read() to read configuration from conf.py.',
                          RemovedInSphinx30Warning, stacklevel=2)
            dirname, filename, overrides, tags = args
            if dirname is None:
                config = {}  # type: Dict[str, Any]
            else:
                config = eval_config_file(path.join(dirname, filename), tags)
        else:
            # new style arguments: (config={}, overrides={})
            if len(args) == 0:
                config, overrides = {}, {}
            elif len(args) == 1:
                config, overrides = args[0], {}
            else:
                config, overrides = args[:2]

        self.overrides = overrides
        self.values = Config.config_values.copy()
        self._raw_config = config
        self.setup = config.get('setup', None)  # type: Callable

        if 'extensions' in overrides:
            if isinstance(overrides['extensions'], str):
                config['extensions'] = overrides.pop('extensions').split(',')
            else:
                config['extensions'] = overrides.pop('extensions')
        self.extensions = config.get('extensions', [])  # type: List[str]

    @classmethod
    def read(cls, confdir, overrides=None, tags=None):
        # type: (str, Dict, Tags) -> Config
        """Create a Config object from configuration file."""
        filename = path.join(confdir, CONFIG_FILENAME)
        namespace = eval_config_file(filename, tags)
        return cls(namespace, overrides or {})

    def check_types(self):
        # type: () -> None
        warnings.warn('Config.check_types() is deprecated. Use check_confval_types() instead.',
                      RemovedInSphinx30Warning, stacklevel=2)
        check_confval_types(None, self)

    def check_unicode(self):
        # type: () -> None
        warnings.warn('Config.check_unicode() is deprecated. Use check_unicode() instead.',
                      RemovedInSphinx30Warning, stacklevel=2)
        check_unicode(self)

    def convert_overrides(self, name, value):
        # type: (str, Any) -> Any
        if not isinstance(value, str):
            return value
        else:
            defvalue = self.values[name][0]
            if self.values[name][2] == Any:
                return value
            elif isinstance(defvalue, dict):
                raise ValueError(__('cannot override dictionary config setting %r, '
                                    'ignoring (use %r to set individual elements)') %
                                 (name, name + '.key=value'))
            elif isinstance(defvalue, list):
                return value.split(',')
            elif isinstance(defvalue, int):
                try:
                    return int(value)
                except ValueError:
                    raise ValueError(__('invalid number %r for config value %r, ignoring') %
                                     (value, name))
            elif hasattr(defvalue, '__call__'):
                return value
            elif defvalue is not None and not isinstance(defvalue, str):
                raise ValueError(__('cannot override config setting %r with unsupported '
                                    'type, ignoring') % name)
            else:
                return value

    def pre_init_values(self):
        # type: () -> None
        """
        Initialize some limited config variables before initialize i18n and loading extensions
        """
        variables = ['needs_sphinx', 'suppress_warnings', 'language', 'locale_dirs']
        for name in variables:
            try:
                if name in self.overrides:
                    self.__dict__[name] = self.convert_overrides(name, self.overrides[name])
                elif name in self._raw_config:
                    self.__dict__[name] = self._raw_config[name]
            except ValueError as exc:
                logger.warning("%s", exc)

    def init_values(self):
        # type: () -> None
        config = self._raw_config
        for valname, value in self.overrides.items():
            try:
                if '.' in valname:
                    realvalname, key = valname.split('.', 1)
                    config.setdefault(realvalname, {})[key] = value
                    continue
                elif valname not in self.values:
                    logger.warning(__('unknown config value %r in override, ignoring'),
                                   valname)
                    continue
                if isinstance(value, str):
                    config[valname] = self.convert_overrides(valname, value)
                else:
                    config[valname] = value
            except ValueError as exc:
                logger.warning("%s", exc)
        for name in config:
            if name in self.values:
                self.__dict__[name] = config[name]

    def __getattr__(self, name):
        # type: (str) -> Any
        if name.startswith('_'):
            raise AttributeError(name)
        if name not in self.values:
            raise AttributeError(__('No such config value: %s') % name)
        default = self.values[name][0]
        if hasattr(default, '__call__'):
            return default(self)
        return default

    def __getitem__(self, name):
        # type: (str) -> str
        return getattr(self, name)

    def __setitem__(self, name, value):
        # type: (str, Any) -> None
        setattr(self, name, value)

    def __delitem__(self, name):
        # type: (str) -> None
        delattr(self, name)

    def __contains__(self, name):
        # type: (str) -> bool
        return name in self.values

    def __iter__(self):
        # type: () -> Generator[ConfigValue, None, None]
        for name, value in self.values.items():
            yield ConfigValue(name, getattr(self, name), value[1])

    def add(self, name, default, rebuild, types):
        # type: (str, Any, Union[bool, str], Any) -> None
        if name in self.values:
            raise ExtensionError(__('Config value %r already present') % name)
        else:
            self.values[name] = (default, rebuild, types)

    def filter(self, rebuild):
        # type: (Union[str, List[str]]) -> Iterator[ConfigValue]
        if isinstance(rebuild, str):
            rebuild = [rebuild]
        return (value for value in self if value.rebuild in rebuild)

    def __getstate__(self):
        # type: () -> Dict
        """Obtains serializable data for pickling."""
        # remove potentially pickling-problematic values from config
        __dict__ = {}
        for key, value in self.__dict__.items():
            if key.startswith('_') or not is_serializable(value):
                pass
            else:
                __dict__[key] = value

        # create a picklable copy of values list
        __dict__['values'] = {}
        for key, value in self.values.items():
            real_value = getattr(self, key)
            if not is_serializable(real_value):
                # omit unserializable value
                real_value = None

            # types column is also omitted
            __dict__['values'][key] = (real_value, value[1], None)

        return __dict__

    def __setstate__(self, state):
        # type: (Dict) -> None
        self.__dict__.update(state)


def eval_config_file(filename, tags):
    # type: (str, Tags) -> Dict[str, Any]
    """Evaluate a config file."""
    namespace = {}  # type: Dict[str, Any]
    namespace['__file__'] = filename
    namespace['tags'] = tags

    with cd(path.dirname(filename)):
        # during executing config file, current dir is changed to ``confdir``.
        try:
            execfile_(filename, namespace)
        except SyntaxError as err:
            msg = __("There is a syntax error in your configuration file: %s\n")
            raise ConfigError(msg % err)
        except SystemExit:
            msg = __("The configuration file (or one of the modules it imports) "
                     "called sys.exit()")
            raise ConfigError(msg)
        except Exception:
            msg = __("There is a programmable error in your configuration file:\n\n%s")
            raise ConfigError(msg % traceback.format_exc())

    return namespace


def convert_source_suffix(app, config):
    # type: (Sphinx, Config) -> None
    """This converts old styled source_suffix to new styled one.

    * old style: str or list
    * new style: a dict which maps from fileext to filetype
    """
    source_suffix = config.source_suffix
    if isinstance(source_suffix, str):
        # if str, considers as default filetype (None)
        #
        # The default filetype is determined on later step.
        # By default, it is considered as restructuredtext.
        config.source_suffix = OrderedDict({source_suffix: None})  # type: ignore
    elif isinstance(source_suffix, (list, tuple)):
        # if list, considers as all of them are default filetype
        config.source_suffix = OrderedDict([(s, None) for s in source_suffix])  # type: ignore  # NOQA
    elif isinstance(source_suffix, dict):
        # if dict, convert it to OrderedDict
        config.source_suffix = OrderedDict(config.source_suffix)  # type: ignore
    else:
        logger.warning(__("The config value `source_suffix' expects "
                          "a string, list of strings, or dictionary. "
                          "But `%r' is given." % source_suffix))


def init_numfig_format(app, config):
    # type: (Sphinx, Config) -> None
    """Initialize :confval:`numfig_format`."""
    numfig_format = {'section': _('Section %s'),
                     'figure': _('Fig. %s'),
                     'table': _('Table %s'),
                     'code-block': _('Listing %s')}

    # override default labels by configuration
    numfig_format.update(config.numfig_format)
    config.numfig_format = numfig_format  # type: ignore


def correct_copyright_year(app, config):
    # type: (Sphinx, Config) -> None
    """correct values of copyright year that are not coherent with
    the SOURCE_DATE_EPOCH environment variable (if set)

    See https://reproducible-builds.org/specs/source-date-epoch/
    """
    if getenv('SOURCE_DATE_EPOCH') is not None:
        for k in ('copyright', 'epub_copyright'):
            if k in config:
                replace = r'\g<1>%s' % format_date('%Y')
                config[k] = copyright_year_re.sub(replace, config[k])


def check_confval_types(app, config):
    # type: (Sphinx, Config) -> None
    """check all values for deviation from the default value's type, since
    that can result in TypeErrors all over the place NB.
    """
    for confval in config:
        default, rebuild, annotations = config.values[confval.name]

        if hasattr(default, '__call__'):
            default = default(config)  # evaluate default value
        if default is None and not annotations:
            continue  # neither inferrable nor expliclitly annotated types

        if annotations is Any:
            # any type of value is accepted
            pass
        elif isinstance(annotations, ENUM):
            if not annotations.match(confval.value):
                msg = __("The config value `{name}` has to be a one of {candidates}, "
                         "but `{current}` is given.")
                logger.warning(msg.format(name=confval.name,
                                          current=confval.value,
                                          candidates=annotations.candidates))
        else:
            if type(confval.value) is type(default):
                continue
            if type(confval.value) in annotations:
                continue

            common_bases = (set(type(confval.value).__bases__ + (type(confval.value),)) &
                            set(type(default).__bases__))
            common_bases.discard(object)
            if common_bases:
                continue  # at least we share a non-trivial base class

            if annotations:
                msg = __("The config value `{name}' has type `{current.__name__}'; "
                         "expected {permitted}.")
                wrapped_annotations = ["`{}'".format(c.__name__) for c in annotations]
                if len(wrapped_annotations) > 2:
                    permitted = "{}, or {}".format(
                        ", ".join(wrapped_annotations[:-1]),
                        wrapped_annotations[-1])
                else:
                    permitted = " or ".join(wrapped_annotations)
                logger.warning(msg.format(name=confval.name,
                                          current=type(confval.value),
                                          permitted=permitted))
            else:
                msg = __("The config value `{name}' has type `{current.__name__}', "
                         "defaults to `{default.__name__}'.")
                logger.warning(msg.format(name=confval.name,
                                          current=type(confval.value),
                                          default=type(default)))


def check_unicode(config):
    # type: (Config) -> None
    """check all string values for non-ASCII characters in bytestrings,
    since that can result in UnicodeErrors all over the place
    """
    warnings.warn('sphinx.config.check_unicode() is deprecated.',
                  RemovedInSphinx40Warning)

    nonascii_re = re.compile(br'[\x80-\xff]')

    for name, value in config._raw_config.items():
        if isinstance(value, bytes) and nonascii_re.search(value):
            logger.warning(__('the config value %r is set to a string with non-ASCII '
                              'characters; this can lead to Unicode errors occurring. '
                              'Please use Unicode strings, e.g. %r.'), name, 'Content')


def check_primary_domain(app, config):
    # type: (Sphinx, Config) -> None
    primary_domain = config.primary_domain
    if primary_domain and not app.registry.has_domain(primary_domain):
        logger.warning(__('primary_domain %r not found, ignored.'), primary_domain)
        config.primary_domain = None  # type: ignore


def check_master_doc(app, env, added, changed, removed):
    # type: (Sphinx, BuildEnvironment, Set[str], Set[str], Set[str]) -> Set[str]
    """Adjust master_doc to 'contents' to support an old project which does not have
    no master_doc setting.
    """
    if (app.config.master_doc == 'index' and
            'index' not in app.project.docnames and
            'contents' in app.project.docnames):
        logger.warning(__('Since v2.0, Sphinx uses "index" as master_doc by default. '
                          'Please add "master_doc = \'contents\'" to your conf.py.'))
        app.config.master_doc = "contents"  # type: ignore

    return changed


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.connect('config-inited', convert_source_suffix)
    app.connect('config-inited', init_numfig_format)
    app.connect('config-inited', correct_copyright_year)
    app.connect('config-inited', check_confval_types)
    app.connect('config-inited', check_primary_domain)
    app.connect('env-get-outdated', check_master_doc)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
