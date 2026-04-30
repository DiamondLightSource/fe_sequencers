from argparse import ArgumentParser
from os import getcwd

from dls_fe_sequencer.fe_sequencer import FESequencer

# Import the basic framework components.
from softioc import builder, softioc
from softioc.softioc import devIocStats

from fe_sequencers.sequences import (
    OneAbsorber,
    Sequence,
    TwoAbsorbers,
    TwoAbsorbersFull,
)


def _run(absorber_cls, args=None):
    """
    Shared CLI implementation for all absorber entry points.

    This parses the front-end identifier from the command line and
    invokes the sequencer with the selected absorber topology.

    Args:
        absorber_cls:
            Absorber class to instantiate (e.g. OneAbsorber, TwoAbsorbers).
        args:
            Optional argument list for testing. If None, arguments are
            taken from sys.argv.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "fe",
        help="Front-end identifier (e.g. FE15I, FE16B)",
    )
    ns = parser.parse_args(args)

    sequencer(ns.fe, absorber_cls())


def one_absorber(args=None):
    """
    Entry point for single-absorber front-end sequencers.

    Example:
        one-absorber FE15I
    """
    _run(OneAbsorber, args)


def two_absorbers(args=None):
    """
    Entry point for double-absorber front-end sequencers.

    Example:
        two-absorbers FE16B
    """
    _run(TwoAbsorbers, args)


def two_absorbers_full(args=None):
    """
    Entry point for full-config double-absorber front-end sequencers.

    Example:
        two-absorbers-full FE99B
    """
    _run(TwoAbsorbersFull, args)


def sequencer(front_end: str, sequence: Sequence):
    """
    Configure and run a softIOC-based FE sequencer.

    This function performs all IOC setup, sequence configuration,
    database loading, and enters interactive IOC mode.

    Args:
        front_end:
            Front-end identifier (e.g. 'FE99B').
        sequence:
            Sequence definition object providing absorber configuration
            and open/close sequencing behaviour.
    """
    devIocStats(f"{front_end}-PY-IOC-01")

    # Set current working directory
    builder.SetDeviceName(f"{front_end}-PY-IOC-01")
    app_dir = builder.Waveform("APP_DIR", NELM=255, FTVL="CHAR")
    app_dir.set([ord(c) for c in getcwd()])

    # Create sequencer object
    sequencer = FESequencer(front_end, sequence.no_of_absorbers)
    # Configure open sequence
    open_actions, open_conditions = sequence.define_open_sequence()
    sequencer.configure_open_sequence(open_actions, open_conditions)

    # Configure close sequence
    close_actions, close_conditions = sequence.define_close_sequence()
    sequencer.configure_close_sequence(close_actions, close_conditions)

    sequencer.run()

    # Boilerplate get the IOC started
    builder.LoadDatabase()
    softioc.iocInit()

    # Finally leave the IOC running with an interactive shell.
    softioc.interactive_ioc(globals())


if __name__ == "__main__":
    two_absorbers("FE99B")
