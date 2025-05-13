#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool only_alpha(string s);

int main(int argc, string argv[]){
    if (argc != 2 || strlen(argv[1]) != 26 || !only_alpha(argv[1])){
        printf("Usage: ./substitution key\n");
        return 1;
    }else{
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        for (int i=0; plaintext[i] != '\0'; i++){
            if (isupper(plaintext[i])){
                printf("%c", toupper(argv[1][plaintext[i] - 'A']));
            }else if (islower(plaintext[i])){
                printf("%c", tolower(argv[1][plaintext[i] - 'a']));
            }else{
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");
    }
}

bool only_alpha(string s){
    int a[26] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    for (int i = 0; s[i] != '\0'; i++){
        if (!isalpha(s[i])){
            return false;
        }
        int temp = tolower(s[i]) - 'a';
        a[temp]++;
        if (a[temp] > 1){
            return false;
        }
    }
    return true;
}