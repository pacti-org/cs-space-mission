
from contract_utils import *
from generators import *

s=1
dsn_pwr = power_consumer(s=s, task="dsn", consumption=(2.0, 2.5))
print(f"dsn_pwr: {show_contract(dsn_pwr)}")

dsn_sci =  DSN_data(s=s, speed=(0.3, 0.7)).merge(nochange_contract(s=s, name="c"))
print(f"dsn_sci: {show_contract(dsn_sci)}")

dsn_nav = uncertainty_generating_nav(s=s, noise=(1.0, 1.5))
print(f"dsn_nav: {show_contract(dsn_nav)}")

dsn = dsn_pwr.merge(dsn_sci).merge(dsn_nav)
print(f"dsn: {show_contract(dsn)}")