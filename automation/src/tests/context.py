from copy import deepcopy


class TestContext:
    _test_config = None
    _test_run_mode = "test"

    def set_config(given):
        TestContext._test_config = given

    def get_config():
        return deepcopy(TestContext._test_config)
