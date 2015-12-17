from django.test import TestCase

# Create your tests here.
def process_cases(self, response, cases):
        for case in cases:
            self.assertContains(response, cases[case])