// Main module for filter implementation 
`timescale 1ns / 1ps
module fir_filter #(
    parameter  INPUT_SIGNAL = 8, 
    parameter  CO_EFF_WIDTH = 8,
    parameter  OUTPUT_SIGNAL = 16,
    parameter  TAPS          = 7
) (
    input clk_i,
    input rst_n_i,
    input en_i,
    input signed [INPUT_SIGNAL-1:0] noisy_sig_i,
    output reg signed [OUTPUT_SIGNAL-1:0] filtered_res_o
);


// Wires for these co-efficient registers
wire signed [CO_EFF_WIDTH-1:0] co_eff [0:TAPS-1];
// Products
wire signed [OUTPUT_SIGNAL-1:0] pdt [0:TAPS-1];
// Tap Delays
wire signed [OUTPUT_SIGNAL-1:0] delay [1:TAPS-1];
// Adders
wire signed [OUTPUT_SIGNAL-1:0] sum [1:TAPS-1];

// Co-effs generated from Python file --> TODO: Automate this with a file
assign co_eff[0] = -1;
assign co_eff[1] = 23;
assign co_eff[2] = 33;
assign co_eff[3] = 38;
assign co_eff[4] = 33;
assign co_eff[5] = 23;
assign co_eff[6] = -1;

// // Multiply operation
genvar jj;
generate
    for (jj=0 ; jj<TAPS; jj++) begin 
        assign pdt[jj] = co_eff[jj] * noisy_sig_i;
    end
endgenerate

// Addition
genvar kk;
generate
    for (kk = 1; kk < TAPS ; kk++) begin 
        assign sum[kk] = delay[kk] + pdt[TAPS-(kk+1)];
    end
endgenerate

// Delay Line
genvar ll;
generate
    for (ll = 1; ll < TAPS-1 ; ll++) begin 
        dflopie #(.W(OUTPUT_SIGNAL)) delay_ll 
        (
            .data_in(sum[ll]),
            .data_out(delay[ll+1]),
            .clk_i(clk_i),
            .rst_n_i(rst_n_i),
            .en_i(en_i)
        );
    end
endgenerate

// Final delay element
dflopie #(.W(OUTPUT_SIGNAL)) delay_ll_d 
(
    .data_in(pdt[TAPS-1]),
    .data_out(delay[1]),
    .clk_i(clk_i),
    .rst_n_i(rst_n_i),
    .en_i(en_i)        
);

// Filtered Output = noisy_signal * filter_response
always @ (posedge clk_i or negedge rst_n_i) begin 
    if(!rst_n_i) 
        filtered_res_o <= 'b0;
    else
        filtered_res_o <= sum[6]; 
end

// Remove this part when synthesizing
initial begin
    $dumpfile("dump_fir.vcd");
    $dumpvars(0, fir_filter);
  end
endmodule