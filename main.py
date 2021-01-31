class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self, result):
        result.test_started()
        self.set_up()
        try:
            exec("self." + self.name + "()")
        except:
            result.test_failed()
        self.tear_down()
        return result

    def set_up(self):
        pass

    def tear_down(self):
        pass


class TestCaseTest(TestCase):
    def set_up(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert (test.log == "set_up test_method tear_down ")

    def test_result(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert (self.result.summary() == "1 run, 0 failed")

    def test_failed_result(self):
        test = WasRun("test_broken_method")
        test.run(self.result)
        assert (self.result.summary() == "1 run, 1 failed")

    def test_failed_result_formatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert (result.summary() == "1 run, 1 failed")

    def test_suite(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.result)
        assert (self.result.summary() == "2 run, 1 failed")


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.error_count = 0

    def test_started(self):
        self.run_count += 1

    def test_failed(self):
        self.error_count += 1

    def summary(self):
        return f"{self.run_count} run, {self.error_count} failed"


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class WasRun(TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.log = None

    def test_method(self):
        self.log += "test_method "

    def set_up(self):
        self.log = "set_up "

    def tear_down(self):
        self.log += "tear_down "

    def test_broken_method(self):
        raise Exception


if __name__ == '__main__':
    suite = TestSuite()
    suite.add(TestCaseTest("test_template_method"))
    suite.add(TestCaseTest("test_result"))
    suite.add(TestCaseTest("test_failed_result"))
    suite.add(TestCaseTest("test_failed_result_formatting"))
    suite.add(TestCaseTest("test_suite"))

    result = TestResult()
    suite.run(result)
    print(result.summary())
