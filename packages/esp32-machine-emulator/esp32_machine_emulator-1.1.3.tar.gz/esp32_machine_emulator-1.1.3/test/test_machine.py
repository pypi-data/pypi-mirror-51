from resetMachine import *


class TestPulse:

    def test_returnsExpectedPulse(self, resetMachine):
        machine.expectedPulseTimeForTesting = 123
        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 123

    def test_returnsExpectedPulseTimeError(self, resetMachine):
        machine.expectedPulseTimeErrorForTesting = OSError('error for testing')

        try:
            machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000)
            raise Exception("Expected error, none raised")
        except OSError as ex:
            assert (ex.args[0] == 'error for testing')

    def test_supportsMultipleExpectedPulseValues(self, resetMachine):
        machine.expectedPulseTimeForTesting = [123, 456, 789]
        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 123
        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 456
        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 789

    def test_handlesAskingForMoreValuesThanGiven(self, resetMachine):
        machine.expectedPulseTimeForTesting = [123, 456, 789]

        while len(machine.expectedPulseTimeForTesting) > 0:
            machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000)

        try:
            machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000)
            raise Exception("Expected error, none raised")
        except Exception as ex:
            assert ex.args[0] == "unexpected call to time_pulse_us on empty expectation list"

    def test_supportsErrorInExpectedPulseValues(self, resetMachine):
        machine.expectedPulseTimeForTesting = [123, OSError('error for testing'), 789]
        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 123

        try:
            # noinspection PyStatementEffect
            machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 456
            raise Exception("Expected error, none raised")
        except OSError as ex:
            assert (ex.args[0] == 'error for testing')

        assert machine.time_pulse_us(pin=1, pulse_level=1, timeout_us=1000) == 789

class TestReset:

    def test_supports_reset_to_reboot_the_device(self, resetMachine):
        machine.reset()
        assert machine.reset_called_for_testing

    def test_not_rebooted(self, resetMachine):
        assert not machine.reset_called_for_testing
