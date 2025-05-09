#include <stdio.h>
#include <cs50.h>

int get_height(void);
void print_row(int spaces, int hashes);
void printer(int count, string s);

int main(void)
{
    int height = get_height();
    
    for (int i = 0; i < height; i++)
    {
        int space = 0;
        int hash = 0;
        for (int j = 0; j < height; j++)
        {
            if (i + j >= height - 1)
            {
                hash += 1;
            }else{
                space += 1;
            }
        }
        print_row(space, hash);
    }
}

int get_height(void)
{
    int height;
    do{
        height = get_int("Height: ");
    }
    while (height<1);
    return height;
}

void print_row(int spaces, int hashes)
{
    printer(spaces, " ");
    printer(hashes, "#");
    printf("  ");
    printer(hashes, "#");
    printf("\n");
}

void printer(int count, string s)
{
    for (int i = 0; i < count; i++)
    {
        printf("%s",s);
    }
}