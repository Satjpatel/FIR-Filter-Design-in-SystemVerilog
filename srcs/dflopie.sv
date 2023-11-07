// A Custom Width D Flip Flop module for delays
`timescale 1ns / 1ps

module dflopie #(
    parameter W = 1
) (
    input               clk_i, 
    input               rst_n_i,
    input               en_i,
    input       [W-1:0] data_in, 
    output      [W-1:0] data_out 
);
    
reg [W-1:0] data_out_reg;
always @(posedge clk_i or negedge rst_n_i) begin
    if(!rst_n_i) begin 
        data_out_reg <= 0;
    end
    else if(en_i) begin 
        data_out_reg <= data_in;
    end
end

assign data_out = data_out_reg;

endmodule