#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

string string2lower(string s);
int counter_letter(string text);
int counter_word(string text);
int counter_sentence(string text);
float coleman_liau_index(int letter_count, int word_count, int sentence_count);

int main(void){
    string text = string2lower(get_string("Text: "));

    int letter_count = counter_letter(text);
    int word_count = counter_word(text);
    int sentence_count = counter_sentence(text);
    
    int index = round(coleman_liau_index(letter_count, word_count, sentence_count));

    if (index <= 0){
        printf("Before Grade 1\n");
    }else if (index >= 16){
        printf("Grade 16+\n");
    }else{
        printf("Grade %i\n", index);
    }
}

float coleman_liau_index(int letter_count, int word_count, int sentence_count){
    float L = letter_count / (float) word_count * 100;
    float S = sentence_count / (float) word_count * 100;
    return 0.0588 * L - 0.296 * S - 15.8;
}

int counter_sentence(string text){
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++){
        if (text[i] == '.' || text[i] == '!' || text[i] == '?'){
            count++;
        }
    }
    return count;
}

int counter_word(string text){
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++){
        if (text[i] == ' '){
            count++;
        }
    }
    return count + 1;
}

int counter_letter(string text){
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++){
        if (text[i] >= 'a' && text[i] <= 'z'){
            count++;
        }
    }
    return count;
}

string string2lower(string s){
    for (int i = 0; s[i] != '\0'; i++){
        s[i] = tolower(s[i]);
    }
    return s;
}