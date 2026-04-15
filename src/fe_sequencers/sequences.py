from dls_fe_sequencer.fe_sequencer import Action, Condition


class Sequence:
    def __init__(self):
        self.no_of_absorbers = 1
        self.close_actions: list[Action] = []
        self.close_conditions: list[Condition] = []
        self.open_actions: list[Action] = []
        self.open_conditions: list[Condition] = []

    def define_close_sequence(self):
        return self.close_actions, self.close_conditions

    def define_open_sequence(self):
        return self.open_actions, self.open_conditions


class OneAbsorber(Sequence):
    def __init__(self):
        super().__init__()
        print(f"Creating {self.__class__} sequencer")
        self.no_of_absorbers = 1

        # Define closing actions
        self.close_actions.append(
            Action("Updating beam status", "BEAM", "STA", "Closing")
        )
        self.close_actions.append(Action("Closing absorber", "ABSB", "CON", "Close"))
        self.close_actions.append(Action("Closing SHTR 02", "SHTR", "CON", "Close"))
        self.close_actions.append(Action("Closing V2", "V2", "CON", "Close"))
        self.close_actions.append(
            Action("Updating beam status", "BEAM", "STA", "Closed")
        )

        # Define closing conditions
        self.close_conditions.append(Condition())
        self.close_conditions.append(
            Condition("Waiting for absorber to close", "ABSB", "STA", ["Closed"])
        )
        self.close_conditions.append(
            Condition("Waiting for Shutter to close", "SHTR", "STA", ["Closed"])
        )
        self.close_conditions.append(
            Condition("Waiting for V2 to close", "V2", "STA", ["Closed"])
        )
        self.close_conditions.append(Condition())

        # Define opening actions
        self.open_actions.append(
            Action("Updating beam status", "BEAM", "STA", "Opening")
        )
        self.open_actions.append(Action("Resetting FV1", "FV", "CON", "Reset"))
        self.open_actions.append(Action("Arming FV1", "FV", "CON", "Arm"))
        self.open_actions.append(Action("Resetting V2", "V2", "CON", "Reset"))
        self.open_actions.append(Action("Opening V2", "V2", "CON", "Open"))
        self.open_actions.append(Action("Resetting Shutter 2", "SHTR", "CON", "Reset"))
        self.open_actions.append(Action("Opening Shutter 2", "SHTR", "CON", "Open"))
        self.open_actions.append(Action("Resetting Absorber", "ABSB", "CON", "Reset"))
        self.open_actions.append(Action("Opening Absorber", "ABSB", "CON", "Open"))
        self.open_actions.append(Action("Updating beam status", "BEAM", "STA", "Open"))

        # Define opening conditions
        self.open_conditions.append(Condition())
        self.open_conditions.append(
            Condition("Waiting for FV1 to reset", "FV", "ILKSTA", ["OK", "Run Ilks Ok"])
        )
        self.open_conditions.append(
            Condition("Waiting for FV1 to arm", "FV", "STA", ["Open Armed"])
        )
        self.open_conditions.append(
            Condition("Waiting for V2 to reset", "V2", "ILKSTA", ["OK", "Run Ilks Ok"])
        )
        self.open_conditions.append(
            Condition("Waiting for V2 to Open", "V2", "STA", ["Open"])
        )
        self.open_conditions.append(
            Condition(
                "Waiting for Shutter 2 to reset",
                "SHTR",
                "ILKSTA",
                ["OK", "Run Ilks Ok"],
            )
        )
        self.open_conditions.append(
            Condition("Waiting for Shutter 2 to Open", "SHTR", "STA", ["Open"])
        )
        self.open_conditions.append(
            Condition(
                "Waiting for Absorber to reset", "ABSB", "ILKSTA", ["OK", "Run Ilks Ok"]
            )
        )
        self.open_conditions.append(
            Condition("Waiting for Absorber to Open", "ABSB", "STA", ["Open"])
        )
        self.open_conditions.append(Condition())


class TwoAbsorbers(OneAbsorber):
    def __init__(self):
        super().__init__()
        self.no_of_absorbers = 2


class OneAbsorberFull(OneAbsorber):
    def __init__(self):
        super().__init__()

        # Create additional steps to open other FE components not normally
        # used by the BL
        self.open_conditions_full: list[Condition] = []
        self.open_actions_full: list[Action] = []

        # Define where in the original open_conditions and open_actions we want
        # to insert these new steps. This will be at the beginning but after the
        # updating of the status PV, hence 1.
        insert_index = 1

        # Open and arm FV1
        self.open_actions_full.append(Action("Resetting FV1", "FV", "CON", "Reset"))
        self.open_conditions_full.append(
            Condition("Waiting for FV1 to reset", "FV", "ILKSTA", ["OK", "Run Ilks Ok"])
        )

        self.open_actions_full.append(Action("Opening FV1", "FV", "CON", "Open"))
        self.open_conditions_full.append(
            Condition(
                "Waiting for FV1 to open",
                "FV",
                "STA",
                ["Open Disarmed", "Open Armed"],
            )
        )

        self.open_actions_full.append(Action("Arming FV1", "FV", "CON", "Arm"))
        self.open_conditions_full.append(
            Condition("Waiting for FV1 to arm", "FV", "STA", ["Open Armed"])
        )

        # Open V1
        self.open_actions_full.append(Action("Resetting V1", "V1", "CON", "Reset"))
        self.open_conditions_full.append(
            Condition("Waiting for V1 to reset", "V1", "ILKSTA", ["OK", "Run Ilks Ok"])
        )

        self.open_actions_full.append(Action("Opening V1", "V1", "CON", "Open"))
        self.open_conditions_full.append(
            Condition("Waiting for V1 to open", "V1", "STA", ["Open"])
        )

        # Open port shutter
        self.open_actions_full.append(
            Action("Resetting PSHTR", "PSHTR", "CON", "Reset")
        )
        self.open_conditions_full.append(
            Condition(
                "Waiting for SHTR-01 to reset",
                "PSHTR",
                "ILKSTA",
                ["OK", "Run Ilks Ok"],
            )
        )

        self.open_actions_full.append(Action("Opening PSHTR", "PSHTR", "CON", "Open"))
        self.open_conditions_full.append(
            Condition("Waiting for SHTR-01 to Open", "PSHTR", "STA", ["Open"])
        )

        # Insert our new lists into the ones defined in the super class
        for i in range(len(self.open_actions_full)):
            self.open_actions.insert(insert_index + i, self.open_actions_full[i])
        for i in range(len(self.open_conditions_full)):
            self.open_conditions.insert(insert_index + i, self.open_conditions_full[i])


class TwoAbsorbersFull(TwoAbsorbers):
    def __init__(self):
        super().__init__()

        # Create additional steps to open other FE components not normally
        # used by the BL
        self.open_conditions_full: list[Condition] = []
        self.open_actions_full: list[Action] = []

        # Define where in the original open_conditions and open_actions we
        # want to insert these new steps. This will be at the beginning but
        # after the updating of the status PV, hence 1.
        insert_index = 1

        # Open and arm FV1
        self.open_actions_full.append(Action("Resetting FV1", "FV", "CON", "Reset"))
        self.open_conditions_full.append(
            Condition("Waiting for FV1 to reset", "FV", "ILKSTA", ["OK", "Run Ilks Ok"])
        )

        self.open_actions_full.append(Action("Opening FV1", "FV", "CON", "Open"))
        self.open_conditions_full.append(
            Condition(
                "Waiting for FV1 to open",
                "FV",
                "STA",
                ["Open Disarmed", "Open Armed"],
            )
        )

        self.open_actions_full.append(Action("Arming FV1", "FV", "CON", "Arm"))
        self.open_conditions_full.append(
            Condition("Waiting for FV1 to arm", "FV", "STA", ["Open Armed"])
        )

        # Open V1
        self.open_actions_full.append(Action("Resetting V1", "V1", "CON", "Reset"))
        self.open_conditions_full.append(
            Condition("Waiting for V1 to reset", "V1", "ILKSTA", ["OK", "Run Ilks Ok"])
        )

        self.open_actions_full.append(Action("Opening V1", "V1", "CON", "Open"))
        self.open_conditions_full.append(
            Condition("Waiting for V1 to open", "V1", "STA", ["Open"])
        )

        # Open ABSB-01
        self.open_actions_full.append(
            Action("Resetting ABSB-01", "ABSB1", "CON", "Reset")
        )
        self.open_conditions_full.append(
            Condition(
                "Waiting for ABSB-01 to reset",
                "ABSB1",
                "ILKSTA",
                ["OK", "Run Ilks Ok"],
            )
        )

        self.open_actions_full.append(Action("Opening ABSB-01", "ABSB1", "CON", "Open"))
        self.open_conditions_full.append(
            Condition("Waiting for ABSB-01 to open", "ABSB1", "STA", ["Open"])
        )

        # Open port shutter
        self.open_actions_full.append(
            Action("Resetting PSHTR", "PSHTR", "CON", "Reset")
        )
        self.open_conditions_full.append(
            Condition(
                "Waiting for SHTR-01 to reset",
                "PSHTR",
                "ILKSTA",
                ["OK", "Run Ilks Ok"],
            )
        )

        self.open_actions_full.append(Action("Opening PSHTR", "PSHTR", "CON", "Open"))
        self.open_conditions_full.append(
            Condition("Waiting for SHTR-01 to Open", "PSHTR", "STA", ["Open"])
        )

        # Insert our new lists into the ones defined in the super class
        for i in range(len(self.open_actions_full)):
            self.open_actions.insert(insert_index + i, self.open_actions_full[i])
        for i in range(len(self.open_conditions_full)):
            self.open_conditions.insert(insert_index + i, self.open_conditions_full[i])
