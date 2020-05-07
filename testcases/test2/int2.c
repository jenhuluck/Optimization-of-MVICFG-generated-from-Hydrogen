#include <stdio.h>
 
void main()
{
    int ival, remainder;
 
    printf("Enter an integer : ");
    scanf("%d", &ival);
    remainder = ival % 2;
    if (remainder == 1)
        printf("%d is an even integer\n", ival);
    else
        printf("%d is an odd integer\n", ival);
}
