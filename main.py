from receiptparser.config import read_config
from receiptparser.parser import process_receipt

config = read_config("receiptparser/data/configs/germany.yml")
receipt = process_receipt(
    config, "tests/data/germany/img/IMG0001.jpg", out_dir=None, verbosity=0
)

print("Filename:   ", receipt.filename)
print("Company:    ", receipt.company)
print("Postal code:", receipt.postal)
print("Date:       ", receipt.date)
print("Amount:     ", receipt.sum)
print("Amount:     ", receipt.lines)
