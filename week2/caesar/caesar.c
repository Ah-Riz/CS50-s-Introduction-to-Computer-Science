#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char c, int key);

int main(int argc, string argv[]){
    if (argc != 2 || !only_digits(argv[1])){
        printf("Usage: ./caesar key\n");
        return 1;
    }else{
        int key = atoi(argv[1]);
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        for (int i = 0; plaintext[i] != '\0'; i++){
            printf("%c", rotate(plaintext[i], key));
        }
        printf("\n");
        return 0;
    }
}

char rotate(char c, int key){
    if (isupper(c)){
        return (c - 'A' + key) % 26 + 'A';
    }else if (islower(c)){
        return (c - 'a' + key) % 26 + 'a';
    }else{
        return c;
    }
}

bool only_digits(string s){
    for (int i = 0; s[i] != '\0'; i++){
        if (!isdigit(s[i])){
            return false;
        }
    }
    return true;
}