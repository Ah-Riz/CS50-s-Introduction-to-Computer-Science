#include <stdio.h>
#include <cs50.h>

long get_number(void);
int length_count(long number);
string check_sum(long number, int length);
string get_card(int length, int two_digit);


int main(void){
    long number = get_number();
    int length = length_count(number);
    string sum = check_sum(number, length);
    printf("%s\n", sum);
}

string get_card(int length, int two_digit){
    if((length == 16) && (51<=two_digit && 55>=two_digit)){
        return "MASTERCARD";
    }else if((length == 15) && (34==two_digit || 37==two_digit)){
        return "AMEX";
    }else if((length == 13 || length == 16) && (40<=two_digit && 49>=two_digit)){
        return "VISA";
    }else{
        return "INVALID";
    }
}

string check_sum(long number, int length){
    int sum = 0;
    int i = 0;
    int sum2 = 0;
    int first_two_digit = 0;

    while (number > 0)
    {
        int digit = number % 10;
        if (i == length - 2){
            first_two_digit = number;
        }
        if (i % 2 == 1)
        {
            int product = digit * 2;
            if (product > 9){
                int temp = 0;
                while(product > 0){
                    temp = product % 10;
                    product = product / 10;
                    sum += temp;
                }
            }else{
                sum += (product / 10) + (product % 10);
            }
        }
        else
        {
            sum2 += (digit / 10) + (digit % 10);
        }

        number = number / 10;
        i++;
    }
    int total = sum + sum2;
    if (total % 10 != 0){
        return "INVALID";
    }else{
        return get_card(length, first_two_digit);
    }

}

long get_number(void){
    long number;
    
    do{
        number = get_long("Number: ");
    }
    while (number<0);
    
    return number;
}

int length_count(long number){
    int length = 0;

    while (number > 0)
    {
        number = number / 10;
        length += 1;
    }
    

    return length;
}