"""Systemd-related functions."""


__all__ = ['systemd_inhibit']


SYSTEMD_INHIBIT = '/usr/bin/systemd-inhibit'


def systemd_inhibit(
        *command_and_arguments: str,
        what: str | None = None,
        who: str | None = None,
        why: str | None = None,
        mode: str | None = None
) -> list[str]:
    """Wrap a command in systemd-inhibit."""

    cmd = [SYSTEMD_INHIBIT]

    if what is not None:
        cmd.extend(['--what', what])

    if who is not None:
        cmd.extend(['--who', who])

    if why is not None:
        cmd.extend(['--why', why])

    if mode is not None:
        cmd.extend(['--mode', mode])

    return [*cmd, *command_and_arguments]
