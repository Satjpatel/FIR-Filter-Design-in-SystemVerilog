from cocotb_test.simulator import run
def test_fir_filter():
    run(
        verilog_sources=["fir_filter.sv", "dflopie.sv"], # sources
        toplevel="fir_filter",            # top level HDL
        module="tb_fir_filter"        # name of cocotb test module
    )