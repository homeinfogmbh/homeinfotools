"""Transfer files."""

from argparse import Namespace
from pathlib import Path

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger
from homeinfotools.functions import completed_process_to_json, execute
from homeinfotools.ssh import rsync


__all__ = ['filetransfer']


def send(system: int, src: Path, dst: Path) -> list[str]:
    """Sends a file to the system."""

    return rsync(src, (system, dst))


def retrieve(system: int, src: Path, dst: Path) -> list[str]:
    """Retrieves a file from the system."""

    dst = dst.parent / (dst.stem + f'.{system}' + dst.suffix)
    return rsync((system, src), dst)


def filetransfer(system: int, args: Namespace) -> dict:
    """Runs commands on a remote system."""

    if args.retrieve:
        command = retrieve(system, args.src, args.dst)
    elif args.send:
        command = send(system, args.src, args.dst)
    else:
        raise ValueError('No direction selected.')

    syslogger(system).debug('Sending "%s" to system.', args.src)
    completed_process = execute(command)

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    syslogger(system).debug('Returncode: %i', completed_process.returncode)

    if stdout := completed_process.stdout:
        syslogger(system).info(stdout.strip())

    if stderr := completed_process.stderr:
        syslogger(system).warning(stderr.strip())

    if not completed_process.returncode == 0:
        syslogger(system).error('File transfer failed.')

    return completed_process_to_json(completed_process)
