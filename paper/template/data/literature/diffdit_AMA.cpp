#include "ap_int.h"


ap_int<58> pack2_corr_bb(ap_int<16> A, ap_int<16> B) {
    ap_int<58> corr = (A.range(8-1, 0)==0 || B.range(8-1, 0)==0) ? (ap_int<58>)0 : (ap_int<58>)(A.range(8-1, 8-1) ^ B.range(8-1, 8-1)) << 18;
    return corr;
}


ap_int<58> pack6_corr_bb(ap_int<16> A, ap_int<16> B) {
    ap_uint<1> corr_carry_5 = (A.range(3*2-1, 3*1)==0 || B.range(4*2-1, 4*1)==0) ? 0 : A[3*2-1] & ~B[4*2-1];
    ap_uint<1> corr_carry_4 = (A.range(3*2-1, 3*1)==0 || B.range(4*1-1, 4*0)==0) ? 0 : A[3*2-1] & ~B[4*1-1];
    ap_uint<1> corr_carry_3 = (A.range(3*1-1, 3*0)==0 || B.range(4*3-1, 4*2)==0) ? 0 : A[3*1-1] ^  B[4*3-1];
    ap_uint<1> corr_carry_2 = (A.range(3*1-1, 3*0)==0 || B.range(4*2-1, 4*1)==0) ? 0 : A[3*1-1] & ~B[4*2-1];
    ap_uint<1> corr_carry_1 = (A.range(3*1-1, 3*0)==0 || B.range(4*1-1, 4*0)==0) ? 0 : A[3*1-1] & ~B[4*1-1];
    ap_uint<1> corr_carry_0 = 0;
    ap_int<3> corr_neg_4 = -(A.range(3*2-1, 3*1));
    ap_int<3> corr_neg_3 = -(A.range(3*2-1, 3*1));
    ap_int<3> corr_neg_1 = -(A.range(3*1-1,   0));
    ap_int<3> corr_neg_0 = -(A.range(3*1-1,   0));
    ap_int<3> corr_unsigned_4 = B[4*2-1] ? corr_neg_4 : ap_int<3>(0);
    ap_int<3> corr_unsigned_3 = B[4*1-1] ? corr_neg_3 : ap_int<3>(0);
    ap_int<3> corr_unsigned_2 =                                   0 ;
    ap_int<3> corr_unsigned_1 = B[4*2-1] ? corr_neg_1 : ap_int<3>(0);
    ap_int<3> corr_unsigned_0 = B[4*1-1] ? corr_neg_0 : ap_int<3>(0);
    ap_int<58> corr = (                                                            corr_carry_5,
                        ap_uint<1>(0), corr_unsigned_4.range(2, 0), ap_uint<3>(0), corr_carry_4,
                        ap_uint<1>(0), corr_unsigned_3.range(2, 0), ap_uint<3>(0), corr_carry_3,
                        ap_uint<1>(0), corr_unsigned_2.range(2, 0), ap_uint<3>(0), corr_carry_2,
                        ap_uint<1>(0), corr_unsigned_1.range(2, 0), ap_uint<3>(0), corr_carry_1,
                        ap_uint<1>(0), corr_unsigned_0.range(2, 0), ap_uint<3>(0), corr_carry_0);
    return corr;
}


ap_int<58> AMA_rtl(ap_int<16> A, ap_int<16> B, bool is_diff) {
    ap_int<27> dsp_port_A;
    ap_int<24> dsp_port_B;
    ap_int<58> dsp_port_C;
    ap_int<27> dsp_port_D;
    if (!is_diff) {
        dsp_port_A = (ap_int<8>)(A.range(8-1, 0));
        dsp_port_B = (ap_int<8>)(B.range(8-1, 0));
        dsp_port_C = pack2_corr_bb(A, B);
        dsp_port_D = ((ap_int<27>)((ap_int<8>)(A.range(2*8-1, 8)))) << 18;
    }
    else {
        dsp_port_A = (ap_int<3>)(A.range(3-1,0));
        dsp_port_B = (ap_int<4*5>)(B.range(4*3-1, 4*2), ap_uint<3+1>(0), 
                                B.range(4*2-1, 4*1), ap_uint<3+1>(0), 
                                B.range(4*1-1, 4*0));
        dsp_port_C = pack6_corr_bb(A, B);
        dsp_port_D = ((ap_int<27>)((ap_int<3>)(A.range(3*2-1,3)))) << 24;
    }

    ap_int<58> dsp_port_P = (dsp_port_A + dsp_port_D) * dsp_port_B + dsp_port_C;

    return dsp_port_P;
}
