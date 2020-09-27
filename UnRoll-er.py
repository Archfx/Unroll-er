# For 1D array

variable_name_1 = "[e]"
variable_name_2 = "(e"
variable_name_3 =  ""
start = 0
end = 4
# verilog_code = "assign vc_wr_addr[e] = | mux_out_gen_0 [e];"
verilog_code =  "assign mask_0[(e+1)*OUT_WIDTH_0-1 : (e)*OUT_WIDTH_0]  =   {OUT_WIDTH_0{vc_num_wr[e]} };"

for v in range (start,end):
    unrolled=verilog_code.replace(variable_name_1, "["+str(v)+"]")
    unrolled=unrolled.replace(variable_name_2, "("+str(v))
    # unrolled=unrolled.replace(variable_name_2, "["+str(v)+"]")
    # print (unrolled)

# For 2D array 
variable_name_1 = "[e][w]"
variable_name_2 = "[e+OUT_WIDTH_0*w]"
start_x = 0
end_x = 2
start_y = 0
end_y = 4
verilog_code = "assign mux_out_gen_0 [e][w]   =   masked_mux_in_0[e+OUT_WIDTH_0*w];"

for x in range (start_x,end_x):
    for y in range(start_y,end_y):
        unrolled=verilog_code.replace(variable_name_1, "["+str(x)+"]["+str(y)+"]")
        unrolled=unrolled.replace(variable_name_2, "["+str(x)+"+OUT_WIDTH_0*"+str(y)+"]")

        # print (unrolled)

code ="""assign mask_0[(0+1)*OUT_WIDTH_0-1 : (0)*OUT_WIDTH_0]  =   {OUT_WIDTH_0{vc_num_wr[0]} };
    assign mask_0[(1+1)*OUT_WIDTH_0-1 : (1)*OUT_WIDTH_0]  =   {OUT_WIDTH_0{vc_num_wr[1]} };
    assign mask_0[(2+1)*OUT_WIDTH_0-1 : (2)*OUT_WIDTH_0]  =   {OUT_WIDTH_0{vc_num_wr[2]} };
    assign mask_0[(3+1)*OUT_WIDTH_0-1 : (3)*OUT_WIDTH_0]  =   {OUT_WIDTH_0{vc_num_wr[3]} };

    assign masked_mux_in_0    = wr_ptr_array & mask_0;

    assign mux_out_gen_0 [0][0]   =   masked_mux_in_0[0+OUT_WIDTH_0*0];
    assign mux_out_gen_0 [0][1]   =   masked_mux_in_0[0+OUT_WIDTH_0*1];
    assign mux_out_gen_0 [0][2]   =   masked_mux_in_0[0+OUT_WIDTH_0*2];
    assign mux_out_gen_0 [0][3]   =   masked_mux_in_0[0+OUT_WIDTH_0*3];
    assign mux_out_gen_0 [1][0]   =   masked_mux_in_0[1+OUT_WIDTH_0*0];
    assign mux_out_gen_0 [1][1]   =   masked_mux_in_0[1+OUT_WIDTH_0*1];
    assign mux_out_gen_0 [1][2]   =   masked_mux_in_0[1+OUT_WIDTH_0*2];
    assign mux_out_gen_0 [1][3]   =   masked_mux_in_0[1+OUT_WIDTH_0*3];
    
    assign vc_wr_addr[0] = | mux_out_gen_0 [0];
    assign vc_wr_addr[1] = | mux_out_gen_0 [1];"""

find_this ="_0"
replace_this = "_1"

replaced=code.replace(find_this, replace_this)
print (replaced)
