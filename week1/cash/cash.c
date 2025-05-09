#include <stdio.h>
#include <cs50.h>

int get_cents(void);

int main(void){
    int cents = get_cents();
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    int pennies = 0;
    int change = cents;
    while (change > 0)
    {
        if (change >= 25)
        {
            quarters += 1;
            change -= 25;
        }
        else if (change >= 10)
        {
            dimes += 1;
            change -= 10;
        }
        else if (change >= 5)
        {
            nickels += 1;
            change -= 5;
        }
        else if (change >= 1)
        {
            pennies += 1;
            change -= 1;
        }
    }
    printf("%i\n", quarters + dimes + nickels + pennies);
}

int get_cents(void)
{
    int cents;
    do{
        cents = get_int("Change owed: ");
    }
    while (cents<0);
    return cents;
}