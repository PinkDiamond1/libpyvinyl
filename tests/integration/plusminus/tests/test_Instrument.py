import pytest
from libpyvinyl.Instrument import Instrument
from plusminus.ArrayCalculators import ArrayCalculator
from plusminus.NumberCalculators import PlusCalculator, MinusCalculator
from plusminus.NumberData import NumberData
import plusminus.ArrayData as AD
from plusminus import DataCollection


def test_CalculationInstrument(tmpdir):
    """PlusCalculator test function, the native output of MinusCalculator is a python dictionary"""

    input1 = NumberData.from_dict({"number": 1}, "input1")
    input2 = NumberData.from_dict({"number": 2}, "input2")
    input_collection = [input1, input2]  # This could also be allowed.
    input_collection = DataCollection(input1, input2)
    calculator1 = PlusCalculator("plus", input_collection, output_keys=["plus_result"])
    calculator2 = MinusCalculator(
        "minus", input_collection, output_keys=["minus_result"]
    )

    input_collection = DataCollection(
        calculator1.output["plus_result"], calculator2.output["minus_result"]
    )
    calculator3 = ArrayCalculator(
        "array", input_collection, output_keys=["array_result"]
    )

    calculation_instrument = Instrument("calculation_instrument")
    instrument_path = tmpdir / "calculation_instrument"
    calculation_instrument.add_calculator(calculator1)
    calculation_instrument.add_calculator(calculator2)
    calculation_instrument.add_calculator(calculator3)
    calculation_instrument.set_instrument_base_dir(str(instrument_path))
    calculation_instrument.run()
    print(calculator3.output.get_data())
    calculator3.output.write(str(tmpdir / "final_result.txt"), AD.TXTFormat)
    calculator3.output.write(str(tmpdir / "final_result.h5"), AD.H5Format)
