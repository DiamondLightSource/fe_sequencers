from os import getcwd

from dls_fe_sequencer.fe_sequencer import FESequencer

# Import the basic framework components.
from softioc import builder, softioc
from softioc.softioc import devIocStats

from fe_sequencers.sequences import OneAbsorber, Sequence, TwoAbsorbers


# Single absorber front ends
def fe03i(args=None):
    sequencer("FE03I", OneAbsorber())


def fe04i(args=None):
    sequencer("FE04I", OneAbsorber())


def fe06i(args=None):
    sequencer("FE06I", OneAbsorber())


def fe07i(args=None):
    sequencer("FE07I", OneAbsorber())


def fe09i(args=None):
    sequencer("FE09I", OneAbsorber())


def fe11k(args=None):
    sequencer("FE11K", OneAbsorber())


def fe13i(args=None):
    sequencer("FE13I", OneAbsorber())


def fe16i(args=None):
    sequencer("FE16I", OneAbsorber())


def fe15i(args=None):
    sequencer("FE15I", OneAbsorber())


def fe18i(args=None):
    sequencer("FE18I", OneAbsorber())


def fe99i(args=None):
    sequencer("FE99I", OneAbsorber())


def fe21i(args=None):
    sequencer("FE21I", OneAbsorber())


# Double absorber front ends


def fe16b(args=None):
    sequencer("FE16B", TwoAbsorbers())


def fe99b(args=None):
    sequencer("FE99B", TwoAbsorbers())


def sequencer(front_end: str, sequence: Sequence):
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
    fe99b()
