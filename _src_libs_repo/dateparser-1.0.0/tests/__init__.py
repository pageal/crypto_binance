from unittest import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.__patches = []

        self.error = NotImplemented

    def add_patch(self, patch):
        patch.start()
        self.__patches.append(patch)

    def tearDown(self):
        super().tearDown()
        for patch in reversed(self.__patches):
            patch.stop()

    def then_error_was_raised(self, error_cls, allowed_substrings=()):
        self.assertIsInstance(self.error, error_cls)
        self.assertTrue(any(mesg in str(self.error) for mesg in allowed_substrings),
                        "Didn't found any of the expected messages (%r) -- message was: %r" % (
                            allowed_substrings, self.error))
