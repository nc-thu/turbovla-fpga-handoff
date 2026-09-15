#include "Vtb_pack2_mult_padd.h"
#include "verilated.h"

int main(int argc, char** argv) {
    VerilatedContext context;
    context.commandArgs(argc, argv);
    auto* top = new Vtb_pack2_mult_padd{&context};
    while (!context.gotFinish()) {
        top->eval();
        context.timeInc(1);
    }
    top->final();
    delete top;
    return 0;
}
