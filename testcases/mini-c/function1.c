void function (char* ident) {
    //Prologue

    fprintf(output, ".globl %s\n", ident);
    fprintf(output, "%s:\n", ident);

    fputs("push ebp\n"
          "mov ebp, esp\n", output);

    //Body

    return_to = new_label();

    line();

    //Epilogue

    fprintf(output, "\t_%08d:\n", return_to);
    fputs("mov esp, ebp\n"
          "pop ebp\n"
          "ret\n", output);
}
