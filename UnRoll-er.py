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

code ="""assign  wr_ptr_array[(i+1)*Bw- 1        :   i*Bw]   =       wr_ptr[i];
        assign  rd_ptr_array[(i+1)*Bw- 1        :   i*Bw]   =       rd_ptr[i];
        //assign    vc_nearly_full[i] = (depth[i] >= B-1);
        assign  vc_not_empty    [i] =   (depth[i] > 0);
    
    
        always @(posedge clk or posedge reset) begin
            if (reset) begin
                rd_ptr  [i] <= {Bw{1'b0}};
                wr_ptr  [i] <= {Bw{1'b0}};
                depth   [i] <= {DEPTHw{1'b0}};
            end
            else begin
                if (wr[i] && depth[i] != B) wr_ptr[i] <= wr_ptr [i]+ 1'h1;
                if (rd[i] && (depth[i] != {DEPTHw{1'b0}})) rd_ptr [i]<= rd_ptr [i]+ 1'h1;
                if (wr[i] & ~rd[i]) depth [i]<=
                //synthesis translate_off
                //synopsys  translate_off
                   #1
                //synopsys  translate_on
                //synthesis translate_on
                   depth[i] + 1'h1;
                else if (~wr[i] & rd[i]) depth [i]<=
                //synthesis translate_off
                //synopsys  translate_off
                   #1
                //synopsys  translate_on
                //synthesis translate_on
                   depth[i] - 1'h1;
            end//else
        end//always

        //synthesis translate_off
        //synopsys  translate_off
    
        always @(posedge clk) begin
            if(~reset)begin
                if (wr[i] && (depth[i] == B) && !rd[i])
                    $display("%t: ERROR: Attempt to write to full FIFO:FIFO size is %d. %m",$time,B);
                /* verilator lint_off WIDTH */
                if (rd[i] && (depth[i] == {DEPTHw{1'b0}} &&  SSA_EN !="YES"  ))
                    $display("%t: ERROR: Attempt to read an empty FIFO: %m",$time);
                if (rd[i] && !wr[i] && (depth[i] == {DEPTHw{1'b0}} &&  SSA_EN =="YES" ))
                    $display("%t: ERROR: Attempt to read an empty FIFO: %m",$time);
                /* verilator lint_on WIDTH */
          
            end//~reset      
        end//always

     
            // Asserting the Property b1 : Read and write pointers are incremented when r_en/w_en are set
            // Asserting the property b3 : Read and Write pointers are not incremented when the buffer is empty and full
            // Asserting the property b4 : Buffer can not be both full and empty at the same time
                            
        // Branch statements
        always@(posedge clk) begin
            //b1.1
            if (wr[i] && depth[i] != B && !reset) begin
                wr_ptr_check[i] <= wr_ptr[i];
            end  
            //b1.2
            if (rd[i] && (depth[i] != {DEPTHw{1'b0}}) && !reset) begin
                rd_ptr_check[i] <= rd_ptr[i];
            end
            //b3.1 trying to write to full buffer
            if (wr[i] & ~rd[i] && (depth[i] == B) && !reset) begin
                wr_ptr_check[i] <= wr_ptr[i];
            end
            //b3.2 trying to read from empty buffer
            if (rd[i] && !wr[i] && (depth[i] == {DEPTHw{1'b0}}) && !reset) begin
                rd_ptr_check[i] <= rd_ptr[i];
            end
        end            
            
    end//for"""

find_this ="[i]"
replace_this = ""

replaced=code.replace(find_this, replace_this)
print (replaced)
