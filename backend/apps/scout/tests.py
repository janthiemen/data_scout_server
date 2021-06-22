from django.test import TestCase
from data_sources import CSV
# Create your tests here.

csv = CSV({"filename": "test.csv", "delimiter": ",", "has_header": True, "encoding": "utf-8"})
df = csv(True, "random")
breakpoint()
