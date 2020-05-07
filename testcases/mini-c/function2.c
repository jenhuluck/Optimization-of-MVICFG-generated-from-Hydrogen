void function (char* ident) {
    //Body
    
    int body = new_label();
    fprintf(output, "_%08d:\n", body);
    return_to = new_label();
    line();

    //Epilogue

    fprintf(output, "\t_%08d:\n", return_to);
    fputs("mov esp, ebp\n"
          "pop ebp\n"
          "ret\n", output);
    
    //Prologue
    //Only after passing the body do we know how much space to allocate for the
    //local variables, so we write the prologue here at the end.
    fprintf(output, ".globl %s\n"
                    "%s:\n", ident, ident);
    fprintf(output, "push ebp\n"
                    "mov ebp, esp\n"
                    "sub esp, %d\n"
                    "jmp _%08d\n", local_no*word_size, body);
}
