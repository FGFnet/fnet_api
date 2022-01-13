from django.test import TestCase

# Create your tests here.
class LCTestCase(TestCase):
    def setUp(self):
        LC.objects.create(fg_n="1", fg_s="2", name="LC01", schedule="2022/01/01")
    
    def test_lc(self):
        lc = LC.objects.get(name="LC01")