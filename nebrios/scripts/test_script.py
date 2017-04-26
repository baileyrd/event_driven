

class test_script(NebriOS):

    listens_to = ['test_script']

    def check(self):
        # Check if listened variable is True
        return self.test_script == True

    def action(self):
        # Set listened variable to a value that will fail the check, in order to debounce execution
        self.test_script = False
        test_model = TestModel(test_b="321 cba")
        test_model.test_a = "hello world!"
        test_model.save()
