import sims4.commands
import gc
import services
import inspect
import re
from collections.abc import Iterable
from m22lib.tunings.tuning_utils import get_tuning
from m22lib.exceptions.exception_watcher import error_watcher
from m22lib.utils.files import M22LogFileManager
from _sims4_collections import frozendict
from interactions.utils.outcome import InteractionOutcomeTestBased
from sims4.collections import _ImmutableSlotsBase


@sims4.commands.Command('tuning.cls_dump', 'tuning.clear_dump', 'tuning.cls', 'tuning.clear', command_type=sims4.commands.CommandType.Live)
def dump_tuning(tuning_id: int = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    if tuning_id is None:
        output('ERROR: Missing tuning ID parameter')
        return

    log = M22LogFileManager('tuning_{}'.format(tuning_id), timestamped_filename=False)
    log.clear()
    output('Cleared log for tuning {}'.format(log.full_filename))
    del log


@error_watcher()
@sims4.commands.Command('tuning.dump', command_type=sims4.commands.CommandType.Live)
def dump_tuning(tuning_id: int = None, attribute_path: str = None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    if tuning_id is None:
        output('ERROR: Missing tuning ID parameter')
        return

    tuning = get_tuning(tuning_id, False)

    if tuning is None:
        output('ERROR: Tuning ID is invalid or does not exist')
        return

    output('Inspecting tuning {}{}\n'.format(str(tuning), '.' + attribute_path if attribute_path is not None else ''))

    log = M22LogFileManager('tuning_{}'.format(tuning_id), timestamped_filename=False)

    if attribute_path is None:
        members = inspect.getmembers(tuning)
    else:
        attribute = get_attribute(tuning, attribute_path, output, log)
        if attribute is None:
            output('ERROR: No attribute found!')
        else:
            members = inspect.getmembers(attribute)

    output('{} members logged for tuning {} ({}{})'.format(len(members), tuning_id, str(tuning), '.' + attribute_path if attribute_path is not None else ''))
    log.write('{} members logged for tuning {} ({}{})\n'.format(len(members), tuning_id, str(tuning), '.' + attribute_path if attribute_path is not None else ''))

    members[:] = [member for member in members if not '__' in str(member)]
    for member in members:
        log.write('\t{} -> {}\n'.format(member[0], type(member[1])), False)
        explore_members(log, member[1:])
        log.write('', False)

    log.write('', False)
    for i in range(0, 3):
        log.write('/' * 512, False)
    log.write('', False)


def explore_members(log, members, recursion_depth: int = 3, recursion_level: int = 1):
    if not isinstance(members, Iterable) or isinstance(members, str):
        log.write('{}\t{} -> {}'.format('\t' * recursion_level, str(type(members)), str(members)), False)
        return
    for member in members:

        if isinstance(member, (_ImmutableSlotsBase, dict)):
            log.write('{}\t{}'.format('\t' * recursion_level, type(member)), False)
            for key, value in member.items():
                log.write('{}\t\'{}\' : {}'.format('\t' * recursion_level, key, type(value) if isinstance(value, tuple) else value), False)
                if recursion_level is not recursion_depth and value is not None:
                    explore_members(log, value, recursion_depth, recursion_level + 1)
                    log.write('', False)

        elif isinstance(member, tuple):
            for element in member[0:]:
                log.write('{}\t{} -> {}'.format('\t' * recursion_level, str(type(element)), str(element)), False)
                if recursion_level is not recursion_depth:
                    explore_members(log, element, recursion_depth, recursion_level + 1)

        else:
            log.write('{}\t{} -> {}'.format('\t' * recursion_level, str(type(member)), str(member)), False)


def get_attribute(cur_attr, attributes, output, log):
    lst_attr = attributes.split('.', 1)
    re_res = re.search('\\[[0-9]+\\]', lst_attr[0])
    if re_res is not None:
        lst_attr[0] = re_res.string[0: re_res.start()]
        index = int(re_res.string[re_res.start() + 1: re_res.end() - 1])
        attr = getattr(cur_attr, lst_attr[0])

        if index >= len(attr):
            raise IndexError('{} is an invalid index for \'{}\'.'.format(index, lst_attr[0]))

        if isinstance(attr, frozendict):
            attr = list(attr.values())[index]
        else:
            attr = attr[index]
    else:
        attr = getattr(cur_attr, lst_attr[0])
        output(str(type(attr)))
        if isinstance(attr, frozendict):
            output('No index provided for \'{}\' ({} element); parsing the first index.'.format(lst_attr[0], len(attr)))
            log.write('No index provided for \'{}\' ({} element); parsing the first index.'.format(lst_attr[0], len(attr)))
            attr = list(attr.values())[0]
        elif isinstance(attr, tuple) and not isinstance(attr, _ImmutableSlotsBase):
            log.write('No index provided for \'{}\' ({} elements); parsing the first index.'.format(lst_attr[0], len(attr)))
            output('No index provided for \'{}\' ({} elements); parsing the first index.'.format(lst_attr[0], len(attr)))
            attr = attr[0]

    if len(lst_attr) > 1:
        return get_attribute(attr, lst_attr[1], output, log)
    else:
        return attr
