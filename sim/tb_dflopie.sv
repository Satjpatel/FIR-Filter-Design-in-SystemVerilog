// A quickcheck testbench to see if dlopie.sv is working on not

module tb();

parameter W = 1;

reg               clk_i = 1'b0;
reg               rst_n_i;
reg               en_i;
reg       [W-1:0] data_in;
wire      [W-1:0] data_out; 

dflopie dut (
    .clk_i(clk_i), 
    .rst_n_i(rst_n_i),
    .en_i(en_i),
    .data_in(data_in), 
    .data_out(data_out) 
);

always begin
    #10 clk_i = ~clk_i;

    // $display("clk_i = %b", clk_i);
end

initial begin
    clk_i = 1'b0;
    rst_n_i = 1'b1;
    data_in = 1'b0;
    en_i = 1'b0;

    @ (posedge clk_i);
    rst_n_i = 1'b0; 
    @ (posedge clk_i);
    @ (posedge clk_i);
    @ (posedge clk_i);
    rst_n_i = 1'b1; 
    en_i = 1'b1;
    assert (data_out == 1'b0) 
        else $error("Reset not proper");

    @ (negedge clk_i);
    data_in = 1'b1; 
    @ (posedge clk_i);
    @ (negedge clk_i);
    assert (data_out == 1'b1)
        else $error("Data transmission unsuccessful");

    @ (negedge clk_i);
    data_in = 1'b0; 
    @ (posedge clk_i);
    
    @ (negedge clk_i);
    assert (data_out == 1'b0)
        else $error("Data transmission unsuccessful");

    $dumpfile("waveform_dflop.vcd") ; 
    $dumpvars(1) ;
    $display($stime);
    #100000; 
    $display($stime);

    $finish;

end

endmodule